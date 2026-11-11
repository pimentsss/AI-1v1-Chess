# Chess vs Stockfish

Play chess against Stockfish, one of the strongest chess engines in the world, on a clickable board.

## 1. Get the game

Install [Python 3.10+](https://www.python.org/downloads/) (on Windows, tick "Add python.exe to PATH" in the installer).

Then download this project: click the green **Code** button on GitHub → **Download ZIP** and unzip it, or:

```
git clone https://github.com/pimentsss/chess.git
cd chess
```

## 2. Install Stockfish

| System | How |
|---|---|
| Ubuntu / Debian | `sudo apt install stockfish` |
| Fedora | `sudo dnf install stockfish` |
| macOS | `brew install stockfish` |
| Windows | Download from https://stockfishchess.org/download/, unzip, and copy the `.exe` into this project folder. Rename it to `stockfish.exe`. |

## 3. Install the Python libraries

Open a terminal **in the project folder** (the one with `gui.py`).

Windows:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS / Linux:
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

(On Ubuntu/Pop!_OS, if the first command fails, run `sudo apt install python3-venv` first.)

## 4. Play

```
python gui.py
```

Click a piece, then click where it should go. To play black: `python gui.py black`.
Prefer the terminal? `python play.py`.

Next time, you only need to activate the venv (step 3's second line) and run `python gui.py`.

Want a stronger or faster opponent? Change `THINK_SECONDS` in `play.py`.

## Troubleshooting

- **"Stockfish not found"**: redo step 2. On Windows, check the file is named `stockfish.exe` and is next to `gui.py`.
- **No window appears / `x11 not available`** on Linux: you're probably using VS Code installed as a Flatpak, which can't open game windows. Run the game from your normal system terminal instead.
- **`No module named 'chess'` or `'pygame'`**: the venv isn't active. Run the activate line from step 3 again.
