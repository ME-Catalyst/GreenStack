"""
Database Configuration and Connection Management
Centralized database access for GreenStack application
"""

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Default database path
DEFAULT_DB_PATH = "greenstack.db"

# Global database path configuration
_db_path: Optional[str] = None


def set_db_path(path: str) -> None:
    """
    Set the global database path

    Args:
        path: Path to the SQLite database file
    """
    global _db_path
    _db_path = path
    logger.info("Database path set to: %s", path)


def get_db_path() -> str:
    """
    Get the configured database path

    Returns:
        Path to the SQLite database file
    """
    return _db_path if _db_path is not None else DEFAULT_DB_PATH


def get_connection(enable_foreign_keys: bool = True) -> sqlite3.Connection:
    """
    Get a database connection with recommended settings

    Args:
        enable_foreign_keys: Enable foreign key constraints (default: True)

    Returns:
        sqlite3.Connection object
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)

    # Enable foreign keys if requested
    if enable_foreign_keys:
        conn.execute("PRAGMA foreign_keys = ON")

    # Set row factory for dict-like access
    conn.row_factory = sqlite3.Row

    return conn


@contextmanager
def get_db_connection(enable_foreign_keys: bool = True):
    """
    Context manager for database connections

    Automatically handles connection cleanup and commit/rollback

    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices")
            ...

    Args:
        enable_foreign_keys: Enable foreign key constraints (default: True)

    Yields:
        sqlite3.Connection object
    """
    conn = get_connection(enable_foreign_keys)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize_database(db_path: Optional[str] = None) -> None:
    """
    Initialize database connection settings

    Args:
        db_path: Optional custom database path
    """
    if db_path:
        set_db_path(db_path)

    # Verify database exists or can be created
    path = Path(get_db_path())
    if not path.exists():
        logger.warning("Database file does not exist: %s", path)
        logger.info("Database will be created on first connection")
    else:
        logger.info("Using existing database: %s", path)
