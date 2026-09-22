import sqlite3

DB_NAME = "store.db"


def get_db_connection():
  """Creates and returns a connection to the SQLite database."""
  conn = sqlite3.connect(DB_NAME)
  conn.row_factory = (
      sqlite3.Row
  )  # Allows accessing columns by name instead of index
  return conn


def init_db():
  """Initializes the database and creates the items table if it doesn't exist."""
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            in_stock INTEGER NOT NULL
        )
    """)
  conn.commit()
  conn.close()