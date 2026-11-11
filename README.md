# Chess AI

Play against Stockfish from the terminal.

## Setup

1. Install Stockfish: Windows/macOS: download from https://stockfishchess.org/download/ and add it to your PATH (macOS: `brew install stockfish`; Linux: `sudo apt install stockfish`).
2. In VS Code: open this folder, then in the terminal:
   ```
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # macOS/Linux
   pip install -r requirements.txt
   ```
3. Press F5 ("Play chess") or run `python play.py`.

Raise `THINK_SECONDS` in `play.py` for stronger play.
