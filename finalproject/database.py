"""
database.py

Handles all SQLite database operations for the Number Guessing Game.
The database file (game.db) is created automatically the first time
the application starts.
"""

import sqlite3
from typing import Optional, List, Dict, Any

DB_NAME = "game.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a new database connection with row access by column name."""
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    """Create the games table if it does not already exist."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            minimum_number INTEGER NOT NULL,
            maximum_number INTEGER NOT NULL,
            secret_number INTEGER NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0,
            max_attempts INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'playing',
            created_at TEXT NOT NULL,
            finished_at TEXT
        )
        """
    )
    connection.commit()
    connection.close()


def create_game(
    player_name: str,
    difficulty: str,
    minimum_number: int,
    maximum_number: int,
    secret_number: int,
    max_attempts: int,
    created_at: str,
) -> Dict[str, Any]:
    """Insert a new game into the database and return it as a dictionary."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO games (
            player_name, difficulty, minimum_number, maximum_number,
            secret_number, attempts, max_attempts, status, created_at, finished_at
        )
        VALUES (?, ?, ?, ?, ?, 0, ?, 'playing', ?, NULL)
        """,
        (
            player_name,
            difficulty,
            minimum_number,
            maximum_number,
            secret_number,
            max_attempts,
            created_at,
        ),
    )
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return get_game_by_id(new_id)


def get_all_games() -> List[Dict[str, Any]]:
    """Return all games in the database, most recently created first."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM games ORDER BY id DESC")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def get_game_by_id(game_id: int) -> Optional[Dict[str, Any]]:
    """Return a single game by its ID, or None if it does not exist."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
    row = cursor.fetchone()
    connection.close()
    return dict(row) if row else None


def update_player_name(game_id: int, player_name: str) -> Optional[Dict[str, Any]]:
    """Update only the player name of a game and return the updated game."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE games SET player_name = ? WHERE id = ?",
        (player_name, game_id),
    )
    connection.commit()
    connection.close()
    return get_game_by_id(game_id)


def update_after_guess(
    game_id: int,
    attempts: int,
    status: str,
    finished_at: Optional[str],
) -> Optional[Dict[str, Any]]:
    """Update a game's attempts, status, and finished_at timestamp after a guess."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE games
        SET attempts = ?, status = ?, finished_at = ?
        WHERE id = ?
        """,
        (attempts, status, finished_at, game_id),
    )
    connection.commit()
    connection.close()
    return get_game_by_id(game_id)


def delete_game(game_id: int) -> bool:
    """Delete a game by ID. Return True if a row was actually deleted."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))
    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()
    return deleted


def get_statistics() -> Dict[str, Any]:
    """Calculate and return overall statistics about all games."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM games")
    total_games = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS won FROM games WHERE status = 'won'")
    games_won = cursor.fetchone()["won"]

    cursor.execute("SELECT COUNT(*) AS lost FROM games WHERE status = 'lost'")
    games_lost = cursor.fetchone()["lost"]

    cursor.execute("SELECT COUNT(*) AS playing FROM games WHERE status = 'playing'")
    games_playing = cursor.fetchone()["playing"]

    cursor.execute("SELECT AVG(attempts) AS avg_attempts FROM games WHERE status = 'won'")
    avg_row = cursor.fetchone()["avg_attempts"]
    average_attempts = round(avg_row, 2) if avg_row is not None else 0.0

    connection.close()

    finished_games = games_won + games_lost
    win_rate = round((games_won / finished_games) * 100, 2) if finished_games > 0 else 0.0

    return {
        "total_games": total_games,
        "games_won": games_won,
        "games_lost": games_lost,
        "games_playing": games_playing,
        "win_rate": win_rate,
        "average_attempts": average_attempts,
    }


def get_leaderboard(limit: int = 10) -> List[Dict[str, Any]]:
    """Return the best completed (won) games, sorted by fewest attempts first."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT player_name, difficulty, attempts, finished_at
        FROM games
        WHERE status = 'won'
        ORDER BY attempts ASC, finished_at ASC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]
