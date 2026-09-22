# Number Guessing Game (Streamlit Edition)

The computer picks a secret number, you try to guess it — all inside one
browser tab, started with a single terminal command. No separate API server
to run, no second terminal window.

## Project structure

```
number_guessing_game/
│
├── app.py              # Streamlit app: UI + game logic, all in one place
├── database.py         # SQLite database setup and queries
├── requirements.txt    # Python dependencies
└── README.md            # This file
```

## Installation

1. Open the project folder and create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate it.

   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS / Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the project

Just one command:

```bash
streamlit run app.py
```

Streamlit will automatically open a browser tab (usually
`http://localhost:8501`) with the game. If it doesn't open automatically,
copy that address into your browser.

The database file `game.db` is created automatically the first time you run
the app — nothing to set up manually.

## How to play

1. **New Game tab** — enter your name, pick a difficulty (easy / medium /
   hard), and click "Start Game".
2. **Play tab** — pick your game from the dropdown, enter a guess, and
   click "Submit Guess". You'll be told if it's too high, too low, or
   correct.
3. **All Games tab** — see every game ever created, and rename a player if
   needed.
4. **Statistics tab** — see win rate, total games, and average attempts.
5. **Leaderboard tab** — see the best (fewest-attempt) wins.
6. **Delete tab** — remove a game by its ID.

## Difficulty levels

| Difficulty | Range      | Max Attempts |
|------------|------------|--------------|
| easy       | 1 - 50     | 10           |
| medium     | 1 - 100    | 7            |
| hard       | 1 - 500    | 10           |

Enjoy the game!
