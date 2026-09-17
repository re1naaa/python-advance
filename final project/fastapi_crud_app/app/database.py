"""SQLite connection management and schema bootstrap."""
import sqlite3
from contextlib import contextmanager

from app.config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT DEFAULT '',
    price       REAL NOT NULL CHECK (price >= 0),
    quantity    INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def init_db() -> None:
    """Create the database file and tables if they do not exist."""
    with get_connection() as conn:
        conn.executescript(SCHEMA)


@contextmanager
def get_connection():
    """Yield a SQLite connection with row access by column name.

    Commits on success, rolls back on error, always closes.
    """
    conn = sqlite3.connect(settings.database_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
