from typing import TYPE_CHECKING

from pieces.chess_piece import ChessPiece, PlayerColor
from util import position_to_string

if TYPE_CHECKING:
    from chess_board import ChessBoard

Position = tuple[int, int]


class Bishop(ChessPiece):
    def __init__(self, color: PlayerColor, position: Position):
        super().__init__(color, position)
        self.value = 3

    def get_possible_moves(self, board: "ChessBoard") -> list[Position]:
        moves = []

        row, col = self.position

        # Define direction vectors
        directions = [
            (1, 1), (1, -1), (-1, 1), (-1, -1)   # Diagonal
        ]

        # Iterate through directions
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if board.is_square_empty((new_row, new_col)):
                        moves.append((new_row, new_col))
                    elif board.is_opponent_piece(self.color, (new_row, new_col)):
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break

        return moves

    def __str__(self):
        return f"<{self.color.value.title()} Bishop at {position_to_string(self.position)}>"
