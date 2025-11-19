"""
Database Query Caching Manager
Redis-based caching layer for frequently accessed queries
"""
import json
import logging
import hashlib
from typing import Any, Optional, Callable, List
from functools import wraps
import redis
from datetime import timedelta

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Centralized cache manager for database queries using Redis

    Features:
    - Automatic cache invalidation
    - TTL-based expiration
    - Tag-based invalidation
    - Cache statistics
    """

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """
        Initialize cache manager

        Args:
            redis_url: Redis connection URL
        """
        self.redis_url = redis_url
        self.client: Optional[redis.Redis] = None
        self.enabled = True
        self._connect()

    def _connect(self):
        """Establish Redis connection"""
        try:
            self.client = redis.from_url(
                self.redis_url,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            self.client.ping()
            logger.info(f"Cache manager connected to Redis: {self.redis_url}")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis, caching disabled: {e}")
            self.client = None
            self.enabled = False

    def is_available(self) -> bool:
        """Check if cache is available"""
        if not self.client or not self.enabled:
            return False

        try:
            self.client.ping()
            return True
        except:
            return False

    def _make_key(self, namespace: str, key: str) -> str:
        """Create namespaced cache key"""
        return f"cache:{namespace}:{key}"

    def _make_tag_key(self, tag: str) -> str:
        """Create tag key for grouping"""
        return f"cache:tag:{tag}"

    def get(self, namespace: str, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            namespace: Cache namespace (e.g., 'devices', 'parameters')
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        if not self.is_available():
            return None

        try:
            cache_key = self._make_key(namespace, key)
            value = self.client.get(cache_key)

            if value:
                logger.debug(f"Cache HIT: {cache_key}")
                return json.loads(value)

            logger.debug(f"Cache MISS: {cache_key}")
            return None

        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(
        self,
        namespace: str,
        key: str,
        value: Any,
        ttl: int = 300,
        tags: Optional[List[str]] = None
    ):
        """
        Set value in cache

        Args:
            namespace: Cache namespace
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl: Time to live in seconds (default: 5 minutes)
            tags: Optional tags for grouped invalidation
        """
        if not self.is_available():
            return

        try:
            cache_key = self._make_key(namespace, key)
            serialized = json.dumps(value)

            # Set value with TTL
            self.client.setex(cache_key, ttl, serialized)

            # Add to tag sets for grouped invalidation
            if tags:
                for tag in tags:
                    tag_key = self._make_tag_key(tag)
                    self.client.sadd(tag_key, cache_key)
                    self.client.expire(tag_key, ttl + 60)  # Tag lives slightly longer

            logger.debug(f"Cache SET: {cache_key} (TTL: {ttl}s, tags: {tags})")

        except Exception as e:
            logger.error(f"Cache set error: {e}")

    def delete(self, namespace: str, key: str):
        """Delete specific cache entry"""
        if not self.is_available():
            return

        try:
            cache_key = self._make_key(namespace, key)
            self.client.delete(cache_key)
            logger.debug(f"Cache DELETE: {cache_key}")
        except Exception as e:
            logger.error(f"Cache delete error: {e}")

    def invalidate_by_tag(self, tag: str):
        """
        Invalidate all cache entries with a specific tag

        Args:
            tag: Tag to invalidate (e.g., 'device:123', 'all_devices')
        """
        if not self.is_available():
            return

        try:
            tag_key = self._make_tag_key(tag)
            cache_keys = self.client.smembers(tag_key)

            if cache_keys:
                # Delete all cached entries with this tag
                self.client.delete(*cache_keys)
                # Delete the tag set itself
                self.client.delete(tag_key)
                logger.info(f"Cache invalidated by tag '{tag}': {len(cache_keys)} entries")

        except Exception as e:
            logger.error(f"Cache invalidation error: {e}")

    def invalidate_namespace(self, namespace: str):
        """
        Invalidate all entries in a namespace

        Args:
            namespace: Namespace to clear (e.g., 'devices', 'parameters')
        """
        if not self.is_available():
            return

        try:
            pattern = self._make_key(namespace, "*")
            cursor = 0
            deleted = 0

            # Use SCAN to avoid blocking Redis
            while True:
                cursor, keys = self.client.scan(cursor, match=pattern, count=100)
                if keys:
                    self.client.delete(*keys)
                    deleted += len(keys)

                if cursor == 0:
                    break

            logger.info(f"Cache namespace '{namespace}' cleared: {deleted} entries")

        except Exception as e:
            logger.error(f"Cache namespace invalidation error: {e}")

    def clear_all(self):
        """Clear all cache entries (use with caution!)"""
        if not self.is_available():
            return

        try:
            pattern = "cache:*"
            cursor = 0
            deleted = 0

            while True:
                cursor, keys = self.client.scan(cursor, match=pattern, count=100)
                if keys:
                    self.client.delete(*keys)
                    deleted += len(keys)

                if cursor == 0:
                    break

            logger.warning(f"All cache cleared: {deleted} entries")

        except Exception as e:
            logger.error(f"Cache clear error: {e}")

    def get_stats(self) -> dict:
        """Get cache statistics"""
        if not self.is_available():
            return {"enabled": False, "connected": False}

        try:
            info = self.client.info("stats")

            return {
                "enabled": self.enabled,
                "connected": True,
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "used_memory_human": self.client.info("memory").get("used_memory_human"),
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"enabled": self.enabled, "connected": False, "error": str(e)}


def cached(
    namespace: str,
    key_func: Optional[Callable] = None,
    ttl: int = 300,
    tags_func: Optional[Callable] = None
):
    """
    Decorator for caching function results

    Args:
        namespace: Cache namespace
        key_func: Function to generate cache key from args (default: hash of args)
        ttl: Time to live in seconds
        tags_func: Function to generate tags from args

    Example:
        @cached('devices', key_func=lambda device_id: f"device:{device_id}", ttl=600)
        def get_device(device_id: int):
            return fetch_from_db(device_id)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = getattr(wrapper, '_cache_manager', None)

            # Skip cache if not available
            if not cache or not cache.is_available():
                return func(*args, **kwargs)

            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default: hash function args
                key_data = f"{func.__name__}:{args}:{kwargs}"
                cache_key = hashlib.md5(key_data.encode()).hexdigest()

            # Try to get from cache
            cached_value = cache.get(namespace, cache_key)
            if cached_value is not None:
                return cached_value

            # Execute function
            result = func(*args, **kwargs)

            # Cache result
            tags = tags_func(*args, **kwargs) if tags_func else None
            cache.set(namespace, cache_key, result, ttl=ttl, tags=tags)

            return result

        return wrapper
    return decorator


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager(redis_url: str = "redis://localhost:6379/0") -> CacheManager:
    """Get or create global cache manager instance"""
    global _cache_manager

    if _cache_manager is None:
        _cache_manager = CacheManager(redis_url)

    return _cache_manager


def setup_cache(redis_url: str = "redis://localhost:6379/0") -> CacheManager:
    """Initialize cache manager (call at application startup)"""
    return get_cache_manager(redis_url)
