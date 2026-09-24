"""
app.py

Number Guessing Game - Streamlit Edition
------------------------------------------
A single-command app: the computer picks a secret number and you try to
guess it. Everything (game creation, guessing, stats, leaderboard) happens
right here in the browser tab that Streamlit opens for you.

Run with:
    streamlit run app.py
"""

import random
from datetime import datetime

import streamlit as st

import database


# ---------------------------------------------------------------------------
# Difficulty settings
# ---------------------------------------------------------------------------

DIFFICULTY_SETTINGS = {
    "easy": {"minimum": 1, "maximum": 50, "max_attempts": 10},
    "medium": {"minimum": 1, "maximum": 100, "max_attempts": 7},
    "hard": {"minimum": 1, "maximum": 500, "max_attempts": 10},
}


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

database.init_db()

st.set_page_config(page_title="Number Guessing Game", page_icon="🎯", layout="centered")
st.title("🎯 Number Guessing Game")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def format_game_label(game: dict) -> str:
    """Build a readable label for a game, used in dropdown menus."""
    return f"#{game['id']} - {game['player_name']} ({game['difficulty']}) - {game['status']}"


def hide_secret_if_playing(game: dict) -> dict:
    """Return a copy of the game dict with the secret number hidden while active."""
    game_copy = dict(game)
    if game_copy["status"] == "playing":
        game_copy["secret_number"] = None
    return game_copy


def process_guess(game: dict, guess: int) -> None:
    """Check a guess against a game's secret number and update the database."""
    attempts = game["attempts"] + 1
    secret_number = game["secret_number"]
    max_attempts = game["max_attempts"]

    if guess == secret_number:
        finished_at = datetime.utcnow().isoformat()
        database.update_after_guess(game["id"], attempts, "won", finished_at)
        st.success(f"🎉 Correct! You found the number in {attempts} attempts.")
        st.balloons()
    elif attempts >= max_attempts:
        finished_at = datetime.utcnow().isoformat()
        database.update_after_guess(game["id"], attempts, "lost", finished_at)
        st.error(f"💀 Game over! You used all {max_attempts} attempts. The number was {secret_number}.")
    else:
        database.update_after_guess(game["id"], attempts, "playing", None)
        remaining = max_attempts - attempts
        if guess < secret_number:
            st.warning(f"📈 Too low! Try a higher number. ({remaining} attempts left)")
        else:
            st.warning(f"📉 Too high! Try a lower number. ({remaining} attempts left)")


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------

tab_new, tab_play, tab_games, tab_stats, tab_leaderboard, tab_delete = st.tabs(
    ["🆕 New Game", "🎮 Play", "📋 All Games", "📊 Statistics", "🏆 Leaderboard", "🗑️ Delete"]
)


# --- New Game tab -----------------------------------------------------------
with tab_new:
    st.subheader("Start a New Game")

    player_name = st.text_input("Player name", key="new_game_player_name")
    difficulty = st.selectbox("Difficulty", options=["easy", "medium", "hard"], key="new_game_difficulty")

    settings = DIFFICULTY_SETTINGS[difficulty]
    st.caption(
        f"Range: {settings['minimum']}-{settings['maximum']} | "
        f"Max attempts: {settings['max_attempts']}"
    )

    if st.button("Start Game", type="primary"):
        cleaned_name = player_name.strip()
        if not cleaned_name:
            st.error("Player name cannot be empty.")
        else:
            secret_number = random.randint(settings["minimum"], settings["maximum"])
            created_at = datetime.utcnow().isoformat()
            new_game = database.create_game(
                player_name=cleaned_name,
                difficulty=difficulty,
                minimum_number=settings["minimum"],
                maximum_number=settings["maximum"],
                secret_number=secret_number,
                max_attempts=settings["max_attempts"],
                created_at=created_at,
            )
            st.success(
                f"Game #{new_game['id']} created for {new_game['player_name']}! "
                f"Guess a number between {new_game['minimum_number']} and {new_game['maximum_number']}."
            )


# --- Play tab ----------------------------------------------------------------
with tab_play:
    st.subheader("Make a Guess")

    active_games = [g for g in database.get_all_games() if g["status"] == "playing"]

    if not active_games:
        st.info("No active games. Start one in the 'New Game' tab first.")
    else:
        game_options = {format_game_label(g): g["id"] for g in active_games}
        selected_label = st.selectbox("Choose your game", options=list(game_options.keys()))
        selected_game_id = game_options[selected_label]
        current_game = database.get_game_by_id(selected_game_id)

        st.caption(
            f"Range: {current_game['minimum_number']}-{current_game['maximum_number']} | "
            f"Attempts used: {current_game['attempts']}/{current_game['max_attempts']}"
        )

        guess = st.number_input(
            "Your guess",
            min_value=current_game["minimum_number"],
            max_value=current_game["maximum_number"],
            step=1,
            key=f"guess_input_{selected_game_id}",
        )

        if st.button("Submit Guess", type="primary"):
            process_guess(current_game, int(guess))


# --- All Games tab -------------------------------------------------------------
with tab_games:
    st.subheader("All Games")

    games = database.get_all_games()
    if not games:
        st.info("No games yet. Start one in the 'New Game' tab.")
    else:
        display_rows = []
        for game in games:
            safe_game = hide_secret_if_playing(game)
            display_rows.append(
                {
                    "ID": safe_game["id"],
                    "Player": safe_game["player_name"],
                    "Difficulty": safe_game["difficulty"],
                    "Range": f"{safe_game['minimum_number']}-{safe_game['maximum_number']}",
                    "Attempts": f"{safe_game['attempts']}/{safe_game['max_attempts']}",
                    "Status": safe_game["status"],
                    "Secret Number": safe_game["secret_number"] if safe_game["secret_number"] is not None else "hidden",
                }
            )
        st.dataframe(display_rows, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Rename a Player")
    rename_game_id = st.number_input("Game ID", min_value=1, step=1, key="rename_game_id")
    new_name = st.text_input("New player name", key="rename_new_name")
    if st.button("Update Name"):
        existing = database.get_game_by_id(int(rename_game_id))
        if existing is None:
            st.error(f"Game with ID {int(rename_game_id)} was not found.")
        elif not new_name.strip():
            st.error("Player name cannot be empty.")
        else:
            database.update_player_name(int(rename_game_id), new_name.strip())
            st.success("Player name updated.")


# --- Statistics tab -------------------------------------------------------------
with tab_stats:
    st.subheader("Statistics")

    stats = database.get_statistics()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Games", stats["total_games"])
    col2.metric("Games Won", stats["games_won"])
    col3.metric("Games Lost", stats["games_lost"])

    col4, col5, col6 = st.columns(3)
    col4.metric("Currently Playing", stats["games_playing"])
    col5.metric("Win Rate", f"{stats['win_rate']}%")
    col6.metric("Avg. Attempts (wins)", stats["average_attempts"])


# --- Leaderboard tab -------------------------------------------------------------
with tab_leaderboard:
    st.subheader("Leaderboard")

    leaderboard = database.get_leaderboard()
    if not leaderboard:
        st.info("No completed games yet.")
    else:
        display_rows = []
        for rank, entry in enumerate(leaderboard, start=1):
            display_rows.append(
                {
                    "Rank": rank,
                    "Player": entry["player_name"],
                    "Difficulty": entry["difficulty"],
                    "Attempts": entry["attempts"],
                    "Date": entry["finished_at"],
                }
            )
        st.dataframe(display_rows, use_container_width=True, hide_index=True)


# --- Delete tab -------------------------------------------------------------
with tab_delete:
    st.subheader("Delete a Game")

    delete_id = st.number_input("Game ID to delete", min_value=1, step=1, key="delete_game_id")
    if st.button("Delete Game", type="secondary"):
        existing = database.get_game_by_id(int(delete_id))
        if existing is None:
            st.error(f"Game with ID {int(delete_id)} was not found.")
        else:
            database.delete_game(int(delete_id))
            st.success(f"Game #{int(delete_id)} was deleted.")
