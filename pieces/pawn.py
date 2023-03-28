from typing import TYPE_CHECKING

from pieces.chess_piece import ChessPiece, PlayerColor
from util import position_to_string

if TYPE_CHECKING:
    from chess_board import ChessBoard

Position = tuple[int, int]


class Pawn(ChessPiece):
    def __init__(self, color: PlayerColor, position: Position):
        super().__init__(color, position)
        self.value = 1

    def get_possible_moves(self, board: "ChessBoard") -> list[Position]:
        moves = []

        row, col = self.position

        if self.color == PlayerColor.WHITE:
            # One square forward
            if 0 <= row - 1 < 8 and board.is_square_empty((row - 1, col)):
                moves.append((row - 1, col))

            # Two squares forward from the starting position
            if row == 6 and board.is_square_empty((row - 1, col)) and board.is_square_empty((row - 2, col)):
                moves.append((row - 2, col))

            # Capture moves
            if 0 <= row - 1 < 8:
                if 0 <= col - 1 < 8 and board.is_opponent_piece(self.color, (row - 1, col - 1)):
                    moves.append((row - 1, col - 1))
                if 0 <= col + 1 < 8 and board.is_opponent_piece(self.color, (row - 1, col + 1)):
                    moves.append((row - 1, col + 1))

        else:  # "black"
            # One square forward
            if 0 <= row + 1 < 8 and board.is_square_empty((row + 1, col)):
                moves.append((row + 1, col))

            # Two squares forward from the starting position
            if row == 1 and board.is_square_empty((row + 1, col)) and board.is_square_empty((row + 2, col)):
                moves.append((row + 2, col))

            # Capture moves
            if 0 <= row + 1 < 8:
                if 0 <= col - 1 < 8 and board.is_opponent_piece(self.color, (row + 1, col - 1)):
                    moves.append((row + 1, col - 1))
                if 0 <= col + 1 < 8 and board.is_opponent_piece(self.color, (row + 1, col + 1)):
                    moves.append((row + 1, col + 1))

        return moves

    def __str__(self):
        return f"<{self.color.value.title()} Pawn at {position_to_string(self.position)}>"
        
