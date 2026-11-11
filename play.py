"""Play chess in the terminal against Stockfish (the strongest free engine)."""
import os
import shutil
import sys

import chess
import chess.engine

THINK_SECONDS = 2.0  # more time = stronger play


def find_stockfish():
    here = os.path.dirname(os.path.abspath(__file__))
    # a Stockfish file dropped into the project folder wins, then the system install
    path = shutil.which("stockfish", path=here) or shutil.which("stockfish") or shutil.which("/usr/games/stockfish")
    if path:
        return path
    if shutil.which("flatpak-spawn"):  # Flatpak VS Code can't see host programs; run the host's Stockfish
        return ["flatpak-spawn", "--host", "/usr/games/stockfish"]
    sys.exit("Stockfish not found. Install it (see README) or put it on your PATH.")


def main():
    board = chess.Board()
    human_white = input("Play as white? [Y/n] ").strip().lower() != "n"
    with chess.engine.SimpleEngine.popen_uci(find_stockfish()) as engine:
        while not board.is_game_over():
            print(f"\n{board}\n")
            if board.turn == human_white:
                text = input("Your move (e.g. e4, Nf3, e2e4, or 'quit'): ").strip()
                if text == "quit":
                    return
                try:
                    board.push_san(text)
                except ValueError:
                    try:
                        board.push_uci(text)
                    except ValueError:
                        print("Illegal or unreadable move, try again.")
            else:
                move = engine.play(board, chess.engine.Limit(time=THINK_SECONDS)).move
                print(f"AI plays: {board.san(move)}")
                board.push(move)
        print(f"\n{board}\n\nGame over: {board.result()} ({board.outcome().termination.name})")


if __name__ == "__main__":
    main()
