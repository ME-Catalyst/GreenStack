"""
Statistics API Routes
Provides codebase and project statistics
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any
import logging
import json
from pathlib import Path
from src.utils.codebase_stats import generate_stats

logger = logging.getLogger(__name__)
router = APIRouter()

# Cache for statistics (regenerated on server start)
_stats_cache = None


class CodebaseStatsResponse(BaseModel):
    """Response model for codebase statistics"""
    generated_at: str
    project_name: str
    language_stats: Dict[str, Any]
    git_stats: Dict[str, Any]
    file_counts: Dict[str, int]
    project_structure: Dict[str, int]
    package_stats: Dict[str, int]
    totals: Dict[str, int]


def load_or_generate_stats():
    """Load cached stats or generate new ones"""
    global _stats_cache

    # Try to load from file first
    stats_file = Path("codebase_stats.json")
    if stats_file.exists():
        try:
            with open(stats_file, 'r') as f:
                _stats_cache = json.load(f)
                logger.info("Loaded codebase statistics from cache file")
                return _stats_cache
        except Exception as e:
            logger.warning(f"Failed to load stats cache: {e}")

    # Generate new stats
    logger.info("Generating fresh codebase statistics...")
    _stats_cache = generate_stats()

    # Save to file
    try:
        with open(stats_file, 'w') as f:
            json.dump(_stats_cache, f, indent=2)
        logger.info("Saved statistics to cache file")
    except Exception as e:
        logger.warning(f"Failed to save stats cache: {e}")

    return _stats_cache


@router.get("/codebase", response_model=CodebaseStatsResponse)
async def get_codebase_stats():
    """
    Get comprehensive codebase statistics

    Returns detailed statistics about:
    - Lines of code by language
    - Git repository metrics
    - File and directory counts
    - Project structure breakdown
    - Package dependencies
    """
    try:
        stats = load_or_generate_stats()
        if not stats:
            raise HTTPException(status_code=500, detail="Failed to generate statistics")

        return CodebaseStatsResponse(**stats)

    except Exception as e:
        logger.error(f"Error fetching codebase stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/codebase/refresh")
async def refresh_codebase_stats():
    """
    Force refresh of codebase statistics

    This will regenerate all statistics from scratch.
    Use sparingly as it can be CPU-intensive.
    """
    try:
        global _stats_cache

        logger.info("Force refreshing codebase statistics...")
        _stats_cache = generate_stats()

        # Save to file
        stats_file = Path("codebase_stats.json")
        with open(stats_file, 'w') as f:
            json.dump(_stats_cache, f, indent=2)

        return {
            "status": "success",
            "message": "Statistics refreshed successfully",
            "generated_at": _stats_cache['generated_at']
        }

    except Exception as e:
        logger.error(f"Error refreshing stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Initialize statistics on module import (server start)
try:
    logger.info("Initializing codebase statistics...")
    load_or_generate_stats()
except Exception as e:
    logger.error(f"Failed to initialize statistics: {e}")
