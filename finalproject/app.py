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
import time
from datetime import datetime

import streamlit as st

import database


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AI Number Laboratory",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ============================================================================
# DATABASE
# ============================================================================

database.init_db()


# ============================================================================
# DIFFICULTY SETTINGS
# ============================================================================

DIFFICULTY_SETTINGS = {
    "easy": {
        "minimum": 1,
        "maximum": 50,
        "max_attempts": 10,
        "emoji": "🟢",
    },
    "medium": {
        "minimum": 1,
        "maximum": 100,
        "max_attempts": 7,
        "emoji": "🟡",
    },
    "hard": {
        "minimum": 1,
        "maximum": 500,
        "max_attempts": 10,
        "emoji": "🔴",
    },
}


# ============================================================================
# SESSION STATE
# ============================================================================

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "rounds" not in st.session_state:
    st.session_state.rounds = 0

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "robot_mood" not in st.session_state:
    st.session_state.robot_mood = "🤖"

if "robot_message" not in st.session_state:
    st.session_state.robot_message = (
        "Laboratory online. Give me a number and I will analyze it."
    )

if "hint_used" not in st.session_state:
    st.session_state.hint_used = False

if "visual_mode" not in st.session_state:
    st.session_state.visual_mode = "🌙 Dark"

if "experiment_running" not in st.session_state:
    st.session_state.experiment_running = False

if "lab_scan_running" not in st.session_state:
    st.session_state.lab_scan_running = False


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:

    st.markdown("## 🧪 AI LABORATORY")

    st.caption("ROBOT EXPERIMENT CONTROL CENTER")

    st.divider()

    st.session_state.visual_mode = st.radio(
        "Laboratory mode",
        options=[
            "🌙 Dark",
            "☀️ Light",
        ],
        horizontal=True,
        key="appearance_selector",
    )

    if st.session_state.visual_mode == "🌙 Dark":
        st.caption("🌌 Night laboratory mode selected.")
    else:
        st.caption("☀️ Day laboratory mode selected.")

    st.divider()

    st.markdown("### 🤖 ROBOT STATUS")

    sidebar_robot_col1, sidebar_robot_col2 = st.columns(2)

    sidebar_robot_col1.metric(
        "ENERGY",
        f"{random.randint(82, 99)}%",
    )

    sidebar_robot_col2.metric(
        "MEMORY",
        f"{random.randint(60, 96)}%",
    )

    sidebar_robot_col3, sidebar_robot_col4 = st.columns(2)

    sidebar_robot_col3.metric(
        "CONFIDENCE",
        f"{random.randint(75, 99)}%",
    )

    sidebar_robot_col4.metric(
        "PROCESSING",
        "ONLINE",
    )

    st.divider()

    st.markdown("### 🏆 SESSION")

    session_col1, session_col2 = st.columns(2)

    session_col1.metric(
        "🔥 Streak",
        st.session_state.streak,
    )

    session_col2.metric(
        "🔄 Rounds",
        st.session_state.rounds,
    )

    st.divider()

    st.markdown("### 📡 SIGNAL")

    signal_strength = random.randint(78, 99)

    st.progress(
        signal_strength / 100,
        text=f"Robot signal: {signal_strength}%",
    )

    st.divider()

    st.markdown("### 🧭 LAB MENU")

    st.write(
        "🧪 Experiment chamber\n\n"
        "🤖 Robot AI\n\n"
        "🧠 Neural processor\n\n"
        "📡 Radar scanner\n\n"
        "🖥️ System logs"
    )

    st.divider()

    st.caption(
        "AI Number Laboratory • Experimental Interface"
    )


# ============================================================================
# HEADER
# ============================================================================

st.title("🧪 AI Number Laboratory")

st.caption(
    "🤖 A space experiment where you try to outsmart the laboratory robot."
)


# ============================================================================
# LABORATORY HEADER
# ============================================================================

lab_header_col1, lab_header_col2, lab_header_col3 = st.columns(3)

lab_header_col1.metric(
    "🧪 EXPERIMENT",
    "ACTIVE",
)

lab_header_col2.metric(
    "🤖 ROBOT",
    "ONLINE",
)

lab_header_col3.metric(
    "📡 SIGNAL",
    f"{random.randint(85, 99)}%",
)

st.divider()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_game_label(game: dict) -> str:
    """Build a readable label for a game, used in dropdown menus."""

    return (
        f"#{game['id']} - "
        f"{game['player_name']} "
        f"({game['difficulty']}) - "
        f"{game['status']}"
    )


def hide_secret_if_playing(game: dict) -> dict:
    """Return a copy of the game dict with the secret number hidden while active."""

    game_copy = dict(game)

    if game_copy["status"] == "playing":
        game_copy["secret_number"] = None

    return game_copy


def show_robot(
    mood: str,
    message: str,
) -> None:
    """Display the robot and its laboratory speech bubble."""

    robot_col, speech_col = st.columns(
        [1, 4],
        vertical_alignment="center",
    )

    with robot_col:
        st.markdown(
            f"# {mood}"
        )

    with speech_col:

        st.info(
            f"🤖 **ROBOT:** {message}"
        )


def show_robot_brain(
    guess: int = None,
    secret_number: int = None,
) -> None:
    """Display fake robot calculations."""

    st.markdown("### 🧠 ROBOT BRAIN")

    brain_col1, brain_col2 = st.columns(2)

    with brain_col1:

        st.code(
            "NEURAL CORE ONLINE\n"
            "-------------------\n"
            "Memory check: OK\n"
            "Pattern engine: OK\n"
            "Number scanner: OK\n"
            "Prediction engine: OK",
            language="text",
        )

    with brain_col2:

        if guess is None:

            st.code(
                "CALCULATING...\n"
                "-------------------\n"
                "Searching number space...\n"
                "Building probability map...\n"
                "Waiting for input...",
                language="text",
            )

        else:

            distance = (
                abs(secret_number - guess)
                if secret_number is not None
                else random.randint(1, 100)
            )

            confidence = max(
                5,
                min(
                    99,
                    100 - min(distance, 95),
                ),
            )

            st.code(
                f"INPUT: {guess}\n"
                f"DISTANCE: {distance}\n"
                f"PROBABILITY: {confidence}%\n"
                f"CONFIDENCE: {confidence}%\n"
                f"PROCESS: ANALYZING...",
                language="text",
            )


def show_terminal_logs(
    guess: int = None,
    result: str = "idle",
) -> None:
    """Display the fake robot terminal."""

    st.markdown("### 🖥️ ROBOT TERMINAL")

    if result == "thinking":

        logs = [
            "> Booting neural processor...",
            "> Reading player input...",
            "> Analyzing guess...",
            "> Probability calculated...",
            "> Comparing number patterns...",
            "> Robot confidence: 87%",
            "> Decision engine active...",
        ]

    elif result == "win":

        logs = [
            "> Analyzing guess...",
            "> Number matched...",
            "> Probability: 100%",
            "> Robot confidence: 0%",
            "> ALERT: PLAYER WON",
            "> Experiment result: FAILURE",
        ]

    elif result == "loss":

        logs = [
            "> Analyzing final guess...",
            "> Attempt limit reached...",
            "> Secret number protected...",
            "> Robot confidence: 99%",
            "> ALERT: PLAYER LOST",
            "> Experiment result: SUCCESS",
        ]

    else:

        logs = [
            "> Laboratory initialized...",
            "> Waiting for player...",
            "> Robot status: ONLINE",
            "> Number scanner: READY",
            "> Experiment chamber: READY",
        ]

    log_text = "\n".join(logs)

    if guess is not None:
        log_text += f"\n> Input received: {guess}"

    st.code(
        log_text,
        language="text",
    )


def show_radar(
    active: bool = False,
) -> None:
    """Display a Streamlit-native radar/scanner visualization."""

    st.markdown("### 📡 ROBOT RADAR")

    radar_frames = [
        [
            "        ◉",
            "     ╱     ╲",
            "   ╱    •    ╲",
            "  │           │",
            "   ╲    •    ╱",
            "     ╲     ╱",
            "        ◉",
        ],
        [
            "       ◉",
            "      ╱ ╲",
            "    ╱  •  ╲",
            "   │   •   │",
            "    ╲  •  ╱",
            "      ╲ ╱",
            "       ◉",
        ],
        [
            "      ◉",
            "     ╱╲",
            "   ╱ •  ╲",
            "  │  • •  │",
            "   ╲  •  ╱",
            "     ╲╱",
            "      ◉",
        ],
    ]

    if active:

        placeholder = st.empty()

        for frame in radar_frames:

            placeholder.code(
                "\n".join(frame),
                language="text",
            )

            time.sleep(0.12)

    else:

        st.code(
            "\n".join(radar_frames[0]),
            language="text",
        )

    st.caption(
        "📡 Scanning the experiment chamber..."
    )


def show_particles() -> None:
    """Display a lightweight simulated space-particle field."""

    particle_rows = []

    symbols = [
        "·",
        "✦",
        "⋆",
        "•",
        "✧",
        "°",
        "˙",
    ]

    for _ in range(7):

        row = "".join(
            random.choice(symbols)
            if random.random() > 0.45
            else " "
            for _ in range(48)
        )

        particle_rows.append(row)

    st.code(
        "\n".join(particle_rows),
        language="text",
    )


def show_status_panel() -> None:
    """Display the fake robot status panel."""

    st.markdown("### ⚙️ ROBOT SYSTEM STATUS")

    energy = random.randint(82, 99)
    memory = random.randint(55, 94)
    confidence = random.randint(78, 99)

    status_col1, status_col2 = st.columns(2)

    with status_col1:

        st.metric(
            "⚡ ENERGY",
            f"{energy}%",
        )

        st.progress(
            energy / 100,
        )

        st.metric(
            "🧠 MEMORY",
            f"{memory}%",
        )

        st.progress(
            memory / 100,
        )

    with status_col2:

        st.metric(
            "🎯 CONFIDENCE",
            f"{confidence}%",
        )

        st.progress(
            confidence / 100,
        )

        st.metric(
            "⚙️ PROCESSING",
            "ACTIVE",
        )

        st.info(
            "NEURAL ENGINE ONLINE"
        )


def run_robot_experiment(
    guess: int,
    secret_number: int,
) -> None:
    """Run a short native Streamlit robot thinking sequence."""

    st.session_state.experiment_running = True

    placeholder = st.empty()

    frames = [
        (
            "🤖🧠",
            "Reading your number...",
        ),
        (
            "🤖🔬",
            "Running probability calculations...",
        ),
        (
            "🤖📡",
            "Scanning the number field...",
        ),
        (
            "🤖⚡",
            "Comparing neural patterns...",
        ),
    ]

    for mood, message in frames:

        with placeholder.container():

            show_robot(
                mood,
                message,
            )

        time.sleep(0.15)

    st.session_state.experiment_running = False


def show_win_screen(
    attempts: int,
    secret_number: int,
) -> None:
    """Display a polished win result."""

    st.session_state.robot_mood = "🤖😵"

    st.session_state.robot_message = (
        "SYSTEM ERROR! You found my secret number!"
    )

    st.balloons()

    st.divider()

    show_robot(
        "🤖😵",
        "NOOO! My experiment has been defeated!",
    )

    show_terminal_logs(
        result="win",
    )

    st.success(
        f"🎉 **EXPERIMENT SUCCESS FOR THE PLAYER!** "
        f"The secret number was **{secret_number}**."
    )

    win_col1, win_col2, win_col3 = st.columns(3)

    win_col1.metric(
        "🎯 Attempts",
        attempts,
    )

    win_col2.metric(
        "🤖 Robot",
        "DEFEATED",
    )

    if attempts == 1:
        performance = "PERFECT"
    elif attempts <= 3:
        performance = "AMAZING"
    else:
        performance = "GREAT"

    win_col3.metric(
        "🏆 Result",
        performance,
    )

    if attempts == 1:

        st.success(
            "🔥 INCREDIBLE! You found it on your FIRST attempt!"
        )

    elif attempts <= 3:

        st.success(
            "⚡ Amazing guessing! The robot barely had time to react."
        )

    else:

        st.info(
            "👏 Great job! You successfully completed the experiment."
        )

    show_status_panel()


def show_loss_screen(
    attempts: int,
    max_attempts: int,
    secret_number: int,
) -> None:
    """Display a polished loss result."""

    st.session_state.robot_mood = "🤖😂"

    st.session_state.robot_message = (
        "HAHA! My experiment survived!"
    )

    st.snow()

    st.divider()

    show_robot(
        "🤖😂",
        "HAHA! I WIN THIS EXPERIMENT! Better luck next time!",
    )

    show_terminal_logs(
        result="loss",
    )

    st.error(
        f"💀 **EXPERIMENT FAILED!** "
        f"You used all **{max_attempts} attempts**."
    )

    st.warning(
        f"🤖 My secret number was **{secret_number}**."
    )

    loss_col1, loss_col2, loss_col3 = st.columns(3)

    loss_col1.metric(
        "🎯 Attempts",
        attempts,
    )

    loss_col2.metric(
        "🤖 Robot",
        "WINNER",
    )

    loss_col3.metric(
        "🔢 Secret",
        secret_number,
    )

    st.info(
        "💪 The laboratory is ready for another experiment."
    )

    show_status_panel()


def show_guess_feedback(
    guess: int,
    secret_number: int,
    remaining: int,
) -> None:
    """Display feedback after an incorrect guess."""

    if guess < secret_number:

        st.warning(
            f"📈 **Too low!** Try a higher number. "
            f"**{remaining} attempts left.**"
        )

        st.session_state.robot_mood = "🤖🔬"

        st.session_state.robot_message = (
            "My scanner says your number is too low!"
        )

        show_robot(
            "🤖🔬",
            "The scanner detected a LOW reading. Go higher!",
        )

    else:

        st.warning(
            f"📉 **Too high!** Try a lower number. "
            f"**{remaining} attempts left.**"
        )

        st.session_state.robot_mood = "🤖😏"

        st.session_state.robot_message = (
            "Too high! My scanner detected an oversized reading."
        )

        show_robot(
            "🤖😏",
            "The scanner says TOO HIGH. Try a lower number!",
        )


def process_guess(
    game: dict,
    guess: int,
) -> None:
    """Check a guess against a game's secret number and update the database."""

    attempts = game["attempts"] + 1

    secret_number = game["secret_number"]

    max_attempts = game["max_attempts"]

    run_robot_experiment(
        guess,
        secret_number,
    )

    if guess == secret_number:

        finished_at = datetime.utcnow().isoformat()

        database.update_after_guess(
            game["id"],
            attempts,
            "won",
            finished_at,
        )

        st.session_state.streak += 1

        st.session_state.rounds += 1

        st.session_state.last_result = "won"

        show_win_screen(
            attempts=attempts,
            secret_number=secret_number,
        )

    elif attempts >= max_attempts:

        finished_at = datetime.utcnow().isoformat()

        database.update_after_guess(
            game["id"],
            attempts,
            "lost",
            finished_at,
        )

        st.session_state.streak = 0

        st.session_state.rounds += 1

        st.session_state.last_result = "lost"

        show_loss_screen(
            attempts=attempts,
            max_attempts=max_attempts,
            secret_number=secret_number,
        )

    else:

        database.update_after_guess(
            game["id"],
            attempts,
            "playing",
            None,
        )

        remaining = max_attempts - attempts

        show_guess_feedback(
            guess=guess,
            secret_number=secret_number,
            remaining=remaining,
        )


# ============================================================================
# TABS
# ============================================================================

tab_new, tab_play, tab_robot, tab_games, tab_stats, tab_leaderboard, tab_delete = st.tabs(
    [
        "🆕 New Game",
        "🎮 Play",
        "🤖 Robot Lab",
        "📋 All Games",
        "📊 Statistics",
        "🏆 Leaderboard",
        "🗑️ Delete",
    ]
)


# ============================================================================
# NEW GAME TAB
# ============================================================================

with tab_new:

    st.subheader("🚀 Start a New Experiment")

    show_robot(
        "🤖🔬",
        "Welcome to my laboratory. Pick a difficulty and enter my experiment!",
    )

    st.markdown("### ✨ Space Laboratory")

    show_particles()

    st.write(
        "Choose your player name and difficulty. "
        "The robot will secretly generate a number."
    )

    player_name = st.text_input(
        "👤 Player name",
        key="new_game_player_name",
    )

    difficulty = st.selectbox(
        "🎯 Difficulty",
        options=[
            "easy",
            "medium",
            "hard",
        ],
        key="new_game_difficulty",
    )

    settings = DIFFICULTY_SETTINGS[difficulty]

    difficulty_col1, difficulty_col2, difficulty_col3 = st.columns(3)

    difficulty_col1.metric(
        "🔢 Range",
        f"{settings['minimum']}-{settings['maximum']}",
    )

    difficulty_col2.metric(
        "🎯 Attempts",
        settings["max_attempts"],
    )

    difficulty_col3.metric(
        "🤖 Level",
        difficulty.upper(),
    )

    st.progress(
        settings["max_attempts"] / 10,
        text=f"{settings['max_attempts']} maximum attempts",
    )

    if st.button(
        "🚀 Start Experiment",
        type="primary",
        use_container_width=True,
    ):

        cleaned_name = player_name.strip()

        if not cleaned_name:

            st.error(
                "❌ Player name cannot be empty."
            )

        else:

            secret_number = random.randint(
                settings["minimum"],
                settings["maximum"],
            )

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

            st.session_state.robot_mood = "🤖😈"

            st.session_state.robot_message = (
                "Secret number locked. Begin the experiment!"
            )

            st.success(
                f"🎮 **Game #{new_game['id']} created!** "
                f"Good luck, {new_game['player_name']}!"
            )

            show_robot(
                "🤖😈",
                "I've selected my secret number. You cannot see it!",
            )

            st.info(
                f"🔢 Guess a number between "
                f"**{new_game['minimum_number']}** and "
                f"**{new_game['maximum_number']}**."
            )


# ============================================================================
# PLAY TAB
# ============================================================================
#
# IMPORTANT:
# The Play tab is intentionally kept focused on the actual guessing game.
# Robot Brain, Robot Terminal, Robot Radar, particles, and system diagnostics
# have been moved to the separate Robot Lab tab.
# ============================================================================

with tab_play:

    st.subheader("🎮 Experiment Chamber")

    active_games = [
        game
        for game in database.get_all_games()
        if game["status"] == "playing"
    ]

    if not active_games:

        show_robot(
            "🤖😴",
            "The experiment chamber is empty. Start a new experiment!",
        )

        st.info(
            "No active games. Start one in the **New Game** tab first."
        )

    else:

        game_options = {
            format_game_label(game): game["id"]
            for game in active_games
        }

        selected_label = st.selectbox(
            "🎯 Choose your experiment",
            options=list(game_options.keys()),
        )

        selected_game_id = game_options[selected_label]

        current_game = database.get_game_by_id(
            selected_game_id
        )

        if current_game is None:

            st.error(
                "❌ The selected game could not be found."
            )

        else:

            # ---------------------------------------------------------------
            # ROBOT PLAYING MESSAGE
            # ---------------------------------------------------------------

            show_robot(
                st.session_state.robot_mood,
                st.session_state.robot_message,
            )

            # ---------------------------------------------------------------
            # GAME INFORMATION
            # ---------------------------------------------------------------

            info_col1, info_col2, info_col3 = st.columns(3)

            info_col1.metric(
                "🔢 RANGE",
                f"{current_game['minimum_number']}-"
                f"{current_game['maximum_number']}",
            )

            info_col2.metric(
                "🎯 ATTEMPTS",
                f"{current_game['attempts']}/"
                f"{current_game['max_attempts']}",
            )

            remaining_attempts = (
                current_game["max_attempts"]
                - current_game["attempts"]
            )

            info_col3.metric(
                "❤️ REMAINING",
                remaining_attempts,
            )

            if current_game["max_attempts"] > 0:

                progress = (
                    current_game["attempts"]
                    / current_game["max_attempts"]
                )

                st.progress(
                    min(progress, 1.0),
                    text=(
                        f"🧪 Experiment progress: "
                        f"{current_game['attempts']} / "
                        f"{current_game['max_attempts']}"
                    ),
                )

            st.divider()

            # ---------------------------------------------------------------
            # HINT
            # ---------------------------------------------------------------

            hint_col1, hint_col2 = st.columns(
                [3, 1]
            )

            with hint_col1:

                st.caption(
                    "💡 Need laboratory assistance?"
                )

            with hint_col2:

                hint_pressed = st.button(
                    "💡 Hint",
                    use_container_width=True,
                )

            if hint_pressed:

                minimum = current_game["minimum_number"]

                maximum = current_game["maximum_number"]

                middle = (
                    minimum + maximum
                ) // 2

                if current_game["secret_number"] <= middle:

                    st.info(
                        f"💡 **Robot Hint:** "
                        f"The secret number is between "
                        f"**{minimum}** and **{middle}**."
                    )

                else:

                    st.info(
                        f"💡 **Robot Hint:** "
                        f"The secret number is between "
                        f"**{middle + 1}** and **{maximum}**."
                    )

                st.session_state.hint_used = True

            st.divider()

            # ---------------------------------------------------------------
            # GUESS
            # ---------------------------------------------------------------

            guess = st.number_input(
                "🔢 Enter your experimental guess",
                min_value=current_game["minimum_number"],
                max_value=current_game["maximum_number"],
                step=1,
                key=f"guess_input_{selected_game_id}",
            )

            if st.button(
                "🎯 Submit Guess",
                type="primary",
                use_container_width=True,
            ):

                process_guess(
                    current_game,
                    int(guess),
                )


# ============================================================================
# ROBOT LAB TAB
# ============================================================================

with tab_robot:

    st.subheader("🤖 Robot Laboratory")

    st.caption(
        "This area contains the robot's experimental systems and diagnostics."
    )

    # ------------------------------------------------------------------------
    # ROBOT
    # ------------------------------------------------------------------------

    show_robot(
        st.session_state.robot_mood,
        st.session_state.robot_message,
    )

    st.divider()

    # ------------------------------------------------------------------------
    # PARTICLES
    # ------------------------------------------------------------------------

    st.markdown("### 🌌 Laboratory Environment")

    show_particles()

    st.divider()

    # ------------------------------------------------------------------------
    # ROBOT BRAIN
    # ------------------------------------------------------------------------

    show_robot_brain()

    st.divider()

    # ------------------------------------------------------------------------
    # ROBOT TERMINAL
    # ------------------------------------------------------------------------

    show_terminal_logs()

    st.divider()

    # ------------------------------------------------------------------------
    # ROBOT RADAR
    # ------------------------------------------------------------------------

    show_radar()

    st.divider()

    # ------------------------------------------------------------------------
    # SYSTEM STATUS
    # ------------------------------------------------------------------------

    show_status_panel()


# ============================================================================
# ALL GAMES TAB
# ============================================================================

with tab_games:

    st.subheader("📋 Experiment Database")

    games = database.get_all_games()

    if not games:

        st.info(
            "No games yet. Start one in the 'New Game' tab."
        )

    else:

        display_rows = []

        for game in games:

            safe_game = hide_secret_if_playing(game)

            display_rows.append(
                {
                    "ID": safe_game["id"],
                    "Player": safe_game["player_name"],
                    "Difficulty": safe_game["difficulty"],
                    "Range": (
                        f"{safe_game['minimum_number']}-"
                        f"{safe_game['maximum_number']}"
                    ),
                    "Attempts": (
                        f"{safe_game['attempts']}/"
                        f"{safe_game['max_attempts']}"
                    ),
                    "Status": safe_game["status"],
                    "Secret Number": (
                        safe_game["secret_number"]
                        if safe_game["secret_number"] is not None
                        else "hidden"
                    ),
                }
            )

        st.dataframe(
            display_rows,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.subheader("✏️ Rename a Player")

    rename_game_id = st.number_input(
        "Game ID",
        min_value=0,
        step=1,
        key="rename_game_id",
    )

    new_name = st.text_input(
        "New player name",
        key="rename_new_name",
    )

    if st.button(
        "✏️ Update Name",
        use_container_width=True,
    ):

        existing = database.get_game_by_id(
            int(rename_game_id)
        )

        if existing is None:

            st.error(
                f"Game with ID {int(rename_game_id)} "
                f"was not found."
            )

        elif not new_name.strip():

            st.error(
                "Player name cannot be empty."
            )

        else:

            database.update_player_name(
                int(rename_game_id),
                new_name.strip(),
            )

            st.success(
                "✅ Player name updated."
            )


# ============================================================================
# STATISTICS TAB
# ============================================================================

with tab_stats:

    st.subheader("📊 Laboratory Statistics")

    stats = database.get_statistics()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🎮 Total Games",
        stats["total_games"],
    )

    col2.metric(
        "🏆 Games Won",
        stats["games_won"],
    )

    col3.metric(
        "💀 Games Lost",
        stats["games_lost"],
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "🎯 Currently Playing",
        stats["games_playing"],
    )

    col5.metric(
        "🔥 Win Rate",
        f"{stats['win_rate']}%",
    )

    col6.metric(
        "📈 Avg. Attempts",
        stats["average_attempts"],
    )

    st.divider()

    st.subheader("🤖 Current Robot Session")

    session_col1, session_col2, session_col3 = st.columns(3)

    session_col1.metric(
        "🔥 Streak",
        st.session_state.streak,
    )

    session_col2.metric(
        "🔄 Rounds",
        st.session_state.rounds,
    )

    if st.session_state.last_result == "won":

        last_result = "🏆 WIN"

    elif st.session_state.last_result == "lost":

        last_result = "💀 LOSS"

    else:

        last_result = "—"

    session_col3.metric(
        "🎯 Last Result",
        last_result,
    )

    if stats["total_games"] > 0:

        st.subheader("🎯 Win Rate")

        st.progress(
            min(stats["win_rate"] / 100, 1.0),
            text=f"{stats['win_rate']}% win rate",
        )

    else:

        st.info(
            "Play your first game to start building statistics!"
        )

    st.divider()

    show_status_panel()


# ============================================================================
# LEADERBOARD TAB
# ============================================================================

with tab_leaderboard:

    st.subheader("🏆 Laboratory Leaderboard")

    st.caption(
        "The fastest successful experiments appear at the top."
    )

    leaderboard = database.get_leaderboard()

    if not leaderboard:

        st.info(
            "🏆 No completed games yet. "
            "Be the first player on the leaderboard!"
        )

    else:

        display_rows = []

        for rank, entry in enumerate(
            leaderboard,
            start=1,
        ):

            if rank == 1:

                rank_display = "🥇 1"

            elif rank == 2:

                rank_display = "🥈 2"

            elif rank == 3:

                rank_display = "🥉 3"

            else:

                rank_display = str(rank)

            display_rows.append(
                {
                    "Rank": rank_display,
                    "Player": entry["player_name"],
                    "Difficulty": entry["difficulty"],
                    "Attempts": entry["attempts"],
                    "Date": entry["finished_at"],
                }
            )

        st.dataframe(
            display_rows,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================================
# DELETE / FULL CRUD DATABASE MANAGER
# ============================================================================

with tab_delete:

    st.subheader("🗄️ Database Control Center")

    st.caption(
        "Full CRUD management for the games database."
    )

    st.warning(
        "⚠️ Database changes made here affect the actual game database."
    )

    crud_create, crud_read, crud_update, crud_delete = st.tabs(
        [
            "➕ CREATE",
            "🔍 READ",
            "✏️ UPDATE",
            "🗑️ DELETE",
        ]
    )

    # ========================================================================
    # CREATE
    # ========================================================================

    with crud_create:

        st.markdown("### ➕ Create Database Record")

        st.info(
            "This creates a new playable game directly in the database."
        )

        crud_player_name = st.text_input(
            "Player name",
            key="crud_create_player_name",
        )

        crud_difficulty = st.selectbox(
            "Difficulty",
            options=[
                "easy",
                "medium",
                "hard",
            ],
            key="crud_create_difficulty",
        )

        crud_settings = DIFFICULTY_SETTINGS[
            crud_difficulty
        ]

        st.write(
            f"Range: **{crud_settings['minimum']} - "
            f"{crud_settings['maximum']}**"
        )

        st.write(
            f"Maximum attempts: **{crud_settings['max_attempts']}**"
        )

        if st.button(
            "➕ Create Game Record",
            type="primary",
            use_container_width=True,
        ):

            cleaned_name = crud_player_name.strip()

            if not cleaned_name:

                st.error(
                    "Player name cannot be empty."
                )

            else:

                crud_secret = random.randint(
                    crud_settings["minimum"],
                    crud_settings["maximum"],
                )

                crud_created_at = datetime.utcnow().isoformat()

                created_game = database.create_game(
                    player_name=cleaned_name,
                    difficulty=crud_difficulty,
                    minimum_number=crud_settings["minimum"],
                    maximum_number=crud_settings["maximum"],
                    secret_number=crud_secret,
                    max_attempts=crud_settings["max_attempts"],
                    created_at=crud_created_at,
                )

                st.success(
                    f"✅ Database record created: "
                    f"Game #{created_game['id']}"
                )

                st.write(
                    f"Player: **{created_game['player_name']}**"
                )

                st.write(
                    f"Status: **{created_game['status']}**"
                )

    # ========================================================================
    # READ
    # ========================================================================

    with crud_read:

        st.markdown("### 🔍 Read Database Records")

        all_database_games = database.get_all_games()

        if not all_database_games:

            st.info(
                "The database is currently empty."
            )

        else:

            read_search = st.text_input(
                "🔎 Search by player name",
                key="crud_read_search",
            )

            read_status = st.selectbox(
                "Filter by status",
                options=[
                    "all",
                    "playing",
                    "won",
                    "lost",
                ],
                key="crud_read_status",
            )

            filtered_games = []

            for game in all_database_games:

                name_matches = (
                    read_search.strip().lower()
                    in game["player_name"].lower()
                )

                status_matches = (
                    read_status == "all"
                    or game["status"] == read_status
                )

                if name_matches and status_matches:

                    filtered_games.append(game)

            read_rows = []

            for game in filtered_games:

                safe_game = hide_secret_if_playing(game)

                read_rows.append(
                    {
                        "ID": safe_game["id"],
                        "Player": safe_game["player_name"],
                        "Difficulty": safe_game["difficulty"],
                        "Min": safe_game["minimum_number"],
                        "Max": safe_game["maximum_number"],
                        "Attempts": safe_game["attempts"],
                        "Max Attempts": safe_game["max_attempts"],
                        "Status": safe_game["status"],
                        "Secret": (
                            safe_game["secret_number"]
                            if safe_game["secret_number"] is not None
                            else "hidden"
                        ),
                        "Created": safe_game["created_at"],
                        "Finished": safe_game["finished_at"],
                    }
                )

            st.dataframe(
                read_rows,
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                f"{len(filtered_games)} record(s) displayed."
            )

            st.divider()

            st.markdown("### 🔎 Inspect One Record")

            inspect_id = st.number_input(
                "Game ID to inspect",
                min_value=0,
                step=1,
                key="crud_read_inspect_id",
            )

            if st.button(
                "🔍 Inspect Record",
                use_container_width=True,
            ):

                inspected_game = database.get_game_by_id(
                    int(inspect_id)
                )

                if inspected_game is None:

                    st.error(
                        "❌ Record not found."
                    )

                else:

                    safe_inspected_game = hide_secret_if_playing(
                        inspected_game
                    )

                    st.json(
                        safe_inspected_game
                    )

    # ========================================================================
    # UPDATE
    # ========================================================================

    with crud_update:

        st.markdown("### ✏️ Update Database Record")

        update_id = st.number_input(
            "Game ID to update",
            min_value=0,
            step=1,
            key="crud_update_id",
        )

        update_name = st.text_input(
            "New player name",
            key="crud_update_name",
        )

        if st.button(
            "✏️ Update Player Name",
            use_container_width=True,
        ):

            existing_update_game = database.get_game_by_id(
                int(update_id)
            )

            if existing_update_game is None:

                st.error(
                    f"Game #{int(update_id)} was not found."
                )

            elif not update_name.strip():

                st.error(
                    "Player name cannot be empty."
                )

            else:

                database.update_player_name(
                    int(update_id),
                    update_name.strip(),
                )

                st.success(
                    f"✅ Game #{int(update_id)} updated successfully."
                )

                updated_game = database.get_game_by_id(
                    int(update_id)
                )

                if updated_game is not None:

                    st.json(
                        updated_game
                    )

        st.divider()

        st.markdown("### 🔎 Current Record")

        current_update_id = st.number_input(
            "Game ID to view before updating",
            min_value=0,
            step=1,
            key="crud_update_view_id",
        )

        if st.button(
            "🔍 Load Record",
            use_container_width=True,
        ):

            current_update_game = database.get_game_by_id(
                int(current_update_id)
            )

            if current_update_game is None:

                st.error(
                    "❌ Record not found."
                )

            else:

                st.json(
                    hide_secret_if_playing(
                        current_update_game
                    )
                )

    # ========================================================================
    # DELETE
    # ========================================================================

    with crud_delete:

        st.markdown("### 🗑️ Delete Database Record")

        st.error(
            "⚠️ Delete is permanent. The selected game will be removed "
            "from the SQLite database."
        )

        delete_id = st.number_input(
            "Game ID to delete",
            min_value=0,
            step=1,
            key="crud_delete_id",
        )

        delete_confirmation = st.checkbox(
            "I understand that this permanently deletes the record.",
            key="crud_delete_confirmation",
        )

        if st.button(
            "🗑️ Delete Game",
            type="secondary",
            use_container_width=True,
        ):

            if not delete_confirmation:

                st.warning(
                    "Please confirm the deletion first."
                )

            else:

                existing_delete_game = database.get_game_by_id(
                    int(delete_id)
                )

                if existing_delete_game is None:

                    st.error(
                        f"Game #{int(delete_id)} was not found."
                    )

                else:

                    deleted = database.delete_game(
                        int(delete_id)
                    )

                    if deleted:

                        st.success(
                            f"✅ Game #{int(delete_id)} "
                            f"was permanently deleted."
                        )

                    else:

                        st.error(
                            "❌ The database did not delete the record."
                        )

        st.divider()

        st.markdown("### 📋 Existing Records")

        delete_games = database.get_all_games()

        if not delete_games:

            st.info(
                "No records currently exist."
            )

        else:

            delete_rows = []

            for game in delete_games:

                delete_rows.append(
                    {
                        "ID": game["id"],
                        "Player": game["player_name"],
                        "Difficulty": game["difficulty"],
                        "Status": game["status"],
                        "Attempts": (
                            f"{game['attempts']}/"
                            f"{game['max_attempts']}"
                        ),
                    }
                )

            st.dataframe(
                delete_rows,
                use_container_width=True,
                hide_index=True,
            )


# ============================================================================
# FOOTER
# ============================================================================

st.divider()

footer_col1, footer_col2, footer_col3 = st.columns(3)

footer_col1.caption(
    "🧪 AI LAB: ONLINE"
)

footer_col2.caption(
    "🤖 ROBOT: ACTIVE"
)

footer_col3.caption(
    "📡 SIGNAL: STABLE"
)
