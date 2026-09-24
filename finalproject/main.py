"""
main.py

FastAPI backend for the Number Guessing Game.

Run with:

    uvicorn main:app --reload

Then open:

    http://127.0.0.1:8000/

API documentation:

    http://127.0.0.1:8000/docs

Alternative documentation:

    http://127.0.0.1:8000/redoc

This backend uses the SAME game.db database as the Streamlit application.
"""

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import database


# ---------------------------------------------------------------------------
# Database initialization
# ---------------------------------------------------------------------------

database.init_db()


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Number Guessing Game API",
    description=(
        "Backend API for the Number Guessing Game. "
        "This API connects directly to the game's SQLite database "
        "and provides statistics, games, and database information."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class PlayerNameUpdate(BaseModel):
    """Data required to update a player's name."""

    player_name: str


# ---------------------------------------------------------------------------
# Home / Dashboard
# ---------------------------------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse,
    tags=["Dashboard"],
)
def home():
    """
    Display a simple browser dashboard.

    Open http://127.0.0.1:8000/ in Chrome.
    """

    stats = database.get_statistics()
    games = database.get_all_games()

    total_games = stats["total_games"]
    games_won = stats["games_won"]
    games_lost = stats["games_lost"]
    games_playing = stats["games_playing"]
    win_rate = stats["win_rate"]
    average_attempts = stats["average_attempts"]

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Number Guessing Game API</title>
    </head>

    <body>

        <h1>🎯 Number Guessing Game</h1>

        <p>
            <strong>FastAPI Backend Dashboard</strong>
        </p>

        <hr>

        <h2>📊 Statistics</h2>

        <h3>🎮 Total Games</h3>
        <p>{total_games}</p>

        <h3>🏆 Games Won</h3>
        <p>{games_won}</p>

        <h3>💀 Games Lost</h3>
        <p>{games_lost}</p>

        <h3>🎯 Currently Playing</h3>
        <p>{games_playing}</p>

        <h3>🔥 Win Rate</h3>
        <p>{win_rate}%</p>

        <h3>📈 Average Attempts</h3>
        <p>{average_attempts}</p>

        <hr>

        <h2>🗄️ Database</h2>

        <p>
            Total database records:
            <strong>{len(games)}</strong>
        </p>

        <hr>

        <h2>🔗 API Links</h2>

        <ul>
            <li>
                <a href="/docs">
                    📚 Swagger API Documentation
                </a>
            </li>

            <li>
                <a href="/redoc">
                    📖 ReDoc API Documentation
                </a>
            </li>

            <li>
                <a href="/stats">
                    📊 Statistics API
                </a>
            </li>

            <li>
                <a href="/games">
                    🗄️ All Games
                </a>
            </li>

            <li>
                <a href="/leaderboard">
                    🏆 Leaderboard
                </a>
            </li>

            <li>
                <a href="/health">
                    ❤️ API Health
                </a>
            </li>
        </ul>

        <hr>

        <p>
            🤖 Number Guessing Game Backend
        </p>

    </body>
    </html>
    """


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get(
    "/health",
    tags=["Dashboard"],
)
def health_check():
    """Check whether the backend is running."""

    return {
        "status": "online",
        "service": "Number Guessing Game API",
        "database": "game.db",
    }


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

@app.get(
    "/stats",
    tags=["Statistics"],
)
def get_stats():
    """
    Return all game statistics.

    Example:

        GET /stats
    """

    stats = database.get_statistics()

    return {
        "total_games": stats["total_games"],
        "games_won": stats["games_won"],
        "games_lost": stats["games_lost"],
        "games_playing": stats["games_playing"],
        "win_rate": stats["win_rate"],
        "average_attempts": stats["average_attempts"],
    }


# ---------------------------------------------------------------------------
# All games
# ---------------------------------------------------------------------------

@app.get(
    "/games",
    tags=["Games"],
)
def get_games():
    """
    Return all games from the database.

    Secret numbers are hidden while a game is still playing.
    """

    games = database.get_all_games()

    safe_games = []

    for game in games:

        game_copy = dict(game)

        if game_copy["status"] == "playing":
            game_copy["secret_number"] = None

        safe_games.append(game_copy)

    return {
        "count": len(safe_games),
        "games": safe_games,
    }


# ---------------------------------------------------------------------------
# Single game
# ---------------------------------------------------------------------------

@app.get(
    "/games/{game_id}",
    tags=["Games"],
)
def get_game(game_id: int):
    """
    Return one game by its ID.

    Example:

        GET /games/1
    """

    game = database.get_game_by_id(game_id)

    if game is None:
        raise HTTPException(
            status_code=404,
            detail=f"Game with ID {game_id} was not found.",
        )

    game_copy = dict(game)

    if game_copy["status"] == "playing":
        game_copy["secret_number"] = None

    return game_copy


# ---------------------------------------------------------------------------
# Leaderboard
# ---------------------------------------------------------------------------

@app.get(
    "/leaderboard",
    tags=["Statistics"],
)
def get_leaderboard():
    """
    Return the current leaderboard.
    """

    leaderboard = database.get_leaderboard()

    return {
        "count": len(leaderboard),
        "leaderboard": leaderboard,
    }


# ---------------------------------------------------------------------------
# Update player name
# ---------------------------------------------------------------------------

@app.put(
    "/games/{game_id}/player",
    tags=["Database CRUD"],
)
def update_player(
    game_id: int,
    data: PlayerNameUpdate,
):
    """
    Update a player's name.

    Example request:

        PUT /games/1/player

    JSON:

        {
            "player_name": "Alex"
        }
    """

    cleaned_name = data.player_name.strip()

    if not cleaned_name:
        raise HTTPException(
            status_code=400,
            detail="Player name cannot be empty.",
        )

    existing_game = database.get_game_by_id(game_id)

    if existing_game is None:
        raise HTTPException(
            status_code=404,
            detail=f"Game with ID {game_id} was not found.",
        )

    updated_game = database.update_player_name(
        game_id,
        cleaned_name,
    )

    return {
        "message": "Player name updated successfully.",
        "game": updated_game,
    }


# ---------------------------------------------------------------------------
# Delete game
# ---------------------------------------------------------------------------

@app.delete(
    "/games/{game_id}",
    tags=["Database CRUD"],
)
def delete_game(game_id: int):
    """
    Delete a game from the database.

    Example:

        DELETE /games/1
    """

    existing_game = database.get_game_by_id(game_id)

    if existing_game is None:
        raise HTTPException(
            status_code=404,
            detail=f"Game with ID {game_id} was not found.",
        )

    deleted = database.delete_game(game_id)

    if not deleted:
        raise HTTPException(
            status_code=500,
            detail="The game could not be deleted.",
        )

    return {
        "message": f"Game #{game_id} deleted successfully.",
        "game_id": game_id,
    }


# ---------------------------------------------------------------------------
# Database information
# ---------------------------------------------------------------------------

@app.get(
    "/database",
    tags=["Database CRUD"],
)
def database_info():
    """
    Return information about the current database.
    """

    games = database.get_all_games()
    stats = database.get_statistics()

    return {
        "database_file": database.DB_NAME,
        "table": "games",
        "total_records": len(games),
        "statistics": stats,
    }


# ---------------------------------------------------------------------------
# Run directly with Python
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
