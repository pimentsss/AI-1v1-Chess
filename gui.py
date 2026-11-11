"""Play Stockfish in a window: click a piece, then click where it should go.

Run `python gui.py` to play white, `python gui.py black` to play black.
"""
import io
import sys

import chess
import chess.engine
import chess.svg
import pygame

from play import THINK_SECONDS, find_stockfish

SQ = 80  # square size in pixels
LIGHT, DARK = (240, 217, 181), (181, 136, 99)
SELECTED, LAST_MOVE = (246, 246, 105), (205, 210, 106)


def load_pieces():
    # python-chess ships the classic piece drawings as SVG; render each once.
    return {
        symbol: pygame.image.load_sized_svg(
            io.BytesIO(chess.svg.piece(chess.Piece.from_symbol(symbol)).encode()), (SQ, SQ)
        )
        for symbol in "PNBRQKpnbrqk"
    }


def square_at(pos, human_white):
    col, row = pos[0] // SQ, pos[1] // SQ
    return chess.square(col, 7 - row) if human_white else chess.square(7 - col, row)


def square_xy(square, human_white):
    file, rank = chess.square_file(square), chess.square_rank(square)
    return (file * SQ, (7 - rank) * SQ) if human_white else ((7 - file) * SQ, rank * SQ)


def draw(screen, board, pieces, human_white, selected):
    last = board.peek() if board.move_stack else None
    targets = {m.to_square for m in board.legal_moves if m.from_square == selected}
    for square in chess.SQUARES:
        x, y = square_xy(square, human_white)
        color = LIGHT if (chess.square_file(square) + chess.square_rank(square)) % 2 else DARK
        if square == selected:
            color = SELECTED
        elif last and square in (last.from_square, last.to_square):
            color = LAST_MOVE
        pygame.draw.rect(screen, color, (x, y, SQ, SQ))
        piece = board.piece_at(square)
        if piece:
            screen.blit(pieces[piece.symbol()], (x, y))
        if square in targets:
            pygame.draw.circle(screen, (90, 90, 90), (x + SQ // 2, y + SQ // 2), SQ // 7)
    pygame.display.flip()


def main():
    human_white = "black" not in sys.argv[1:]
    pygame.display.init()  # display only: initializing audio can hang inside the Flatpak sandbox
    screen = pygame.display.set_mode((8 * SQ, 8 * SQ))
    pygame.display.set_caption("Chess vs Stockfish")
    pieces = load_pieces()
    board = chess.Board()
    selected = None

    with chess.engine.SimpleEngine.popen_uci(find_stockfish()) as engine:
        while True:
            draw(screen, board, pieces, human_white, selected)
            if board.is_game_over():
                pygame.display.set_caption(f"Game over: {board.result()} ({board.outcome().termination.name})")
            elif board.turn != human_white:
                pygame.display.set_caption("Stockfish is thinking...")
                pygame.event.pump()  # keep the window responsive while the engine thinks
                board.push(engine.play(board, chess.engine.Limit(time=THINK_SECONDS)).move)
                pygame.display.set_caption("Your move")
                continue

            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                return
            if event.type != pygame.MOUSEBUTTONDOWN or board.is_game_over():
                continue
            square = square_at(event.pos, human_white)
            piece = board.piece_at(square)
            if selected is None:
                if piece and piece.color == board.turn:
                    selected = square
                continue
            move = chess.Move(selected, square)
            # shortcut: pawns always promote to a queen, add a picker if you want underpromotion
            if board.piece_type_at(selected) == chess.PAWN and chess.square_rank(square) in (0, 7):
                move.promotion = chess.QUEEN
            if move in board.legal_moves:
                board.push(move)
                selected = None
            else:  # clicking another of your pieces switches the selection
                selected = square if piece and piece.color == board.turn else None


if __name__ == "__main__":
    main()
