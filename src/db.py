"""
SQLAlchemy Database Configuration with Connection Pooling
Supports both SQLite (development) and PostgreSQL (production)
"""

import logging
import os
from contextlib import contextmanager
from typing import Generator

from prometheus_client import Gauge
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool, QueuePool

from src import config

logger = logging.getLogger(__name__)

# ============================================================================
# Connection Pool Metrics
# ============================================================================

db_pool_size = Gauge(
    'db_connection_pool_size',
    'Current size of database connection pool'
)

db_pool_checked_out = Gauge(
    'db_connection_pool_checked_out',
    'Number of connections currently checked out from pool'
)

db_pool_overflow = Gauge(
    'db_connection_pool_overflow',
    'Current overflow count of database connection pool'
)

# ============================================================================
# Database Engine Configuration
# ============================================================================

def create_db_engine() -> Engine:
    """
    Create SQLAlchemy engine with optimized connection pooling settings.

    Configuration varies based on database type:
    - SQLite: Uses NullPool (no pooling needed for file-based DB)
    - PostgreSQL: Uses QueuePool with production-ready settings

    Returns:
        Configured SQLAlchemy Engine instance
    """
    database_url = config.DATABASE_URL

    # Determine if using SQLite
    is_sqlite = database_url.startswith('sqlite:///')

    if is_sqlite:
        logger.info("Configuring SQLite database (no connection pooling)")
        engine = create_engine(
            database_url,
            poolclass=NullPool,  # SQLite doesn't benefit from pooling
            echo=config.LOG_SQL_QUERIES,
            connect_args={
                "check_same_thread": False,  # Allow multi-threaded access
                "timeout": 30,  # Lock timeout in seconds
            }
        )
    else:
        logger.info("Configuring PostgreSQL database with connection pooling")

        # Connection pool configuration
        pool_size = int(os.getenv('DB_POOL_SIZE', '20'))
        max_overflow = int(os.getenv('DB_MAX_OVERFLOW', '40'))
        pool_timeout = int(os.getenv('DB_POOL_TIMEOUT', '30'))
        pool_recycle = int(os.getenv('DB_POOL_RECYCLE', '3600'))  # 1 hour

        engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=pool_size,              # Base connection pool size
            max_overflow=max_overflow,        # Additional connections under load
            pool_timeout=pool_timeout,        # Seconds to wait for connection
            pool_recycle=pool_recycle,        # Recycle connections (prevents stale connections)
            pool_pre_ping=True,               # Verify connection health before use
            echo=config.LOG_SQL_QUERIES,      # Log SQL queries (development only)
            connect_args={
                "connect_timeout": 10,         # Initial connection timeout
                "options": "-c timezone=utc",  # Force UTC timezone
            }
        )

        logger.info(
            "Database pool configured: "
            f"size={pool_size}, max_overflow={max_overflow}, "
            f"timeout={pool_timeout}s, recycle={pool_recycle}s"
        )

    # Register event listeners for pool monitoring
    register_pool_metrics(engine)

    return engine


def register_pool_metrics(engine: Engine) -> None:
    """
    Register Prometheus metrics for connection pool monitoring.

    Args:
        engine: SQLAlchemy engine to monitor
    """
    if not hasattr(engine.pool, 'size'):
        # NullPool doesn't have these attributes
        return

    @event.listens_for(engine, "connect")
    def receive_connect(dbapi_conn, connection_record):
        """Track connection pool metrics on new connections."""
        try:
            pool = engine.pool
            db_pool_size.set(pool.size())
            db_pool_checked_out.set(pool.checkedout())
            db_pool_overflow.set(pool.overflow())
        except Exception as e:
            logger.warning(f"Failed to update pool metrics: {e}")

    @event.listens_for(engine, "checkin")
    def receive_checkin(dbapi_conn, connection_record):
        """Track connection pool metrics when connections are returned."""
        try:
            pool = engine.pool
            db_pool_size.set(pool.size())
            db_pool_checked_out.set(pool.checkedout())
            db_pool_overflow.set(pool.overflow())
        except Exception as e:
            logger.warning(f"Failed to update pool metrics: {e}")


# ============================================================================
# Global Engine and Session Factory
# ============================================================================

# Create single engine instance (reused across application)
engine = create_db_engine()

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.

    Automatically handles session lifecycle:
    - Creates new session
    - Commits on success
    - Rolls back on error
    - Closes session in all cases

    Usage:
        with get_db_session() as session:
            device = session.query(Device).filter_by(id=123).first()
            device.name = "Updated Name"
            # Automatically commits here

    Yields:
        SQLAlchemy Session instance
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection function for FastAPI.

    Usage in FastAPI endpoints:
        @app.get("/devices")
        def get_devices(db: Session = Depends(get_db)):
            devices = db.query(Device).all()
            return devices

    Yields:
        SQLAlchemy Session instance
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_pool_status() -> dict:
    """
    Get current connection pool status for monitoring/debugging.

    Returns:
        Dictionary with pool statistics
    """
    pool = engine.pool

    if not hasattr(pool, 'size'):
        return {
            "pool_type": "NullPool",
            "message": "No connection pooling (SQLite mode)"
        }

    return {
        "pool_type": pool.__class__.__name__,
        "size": pool.size(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "queue_size": pool.size() + pool.overflow() - pool.checkedout(),
        "timeout": pool._timeout,
        "recycle": pool._recycle,
    }


def close_db_connections() -> None:
    """
    Close all database connections and dispose of the engine.

    Call this during application shutdown.
    """
    logger.info("Closing database connections...")
    engine.dispose()
    logger.info("Database connections closed")
