from typing import TYPE_CHECKING

from pieces.chess_piece import ChessPiece, PlayerColor

if TYPE_CHECKING:
    from chess_board import ChessBoard

Position = tuple[int, int]


class King(ChessPiece):
    def __init__(self, color: PlayerColor, position: Position):
        super().__init__(color, position)
        self.value = float("infinity")

    def get_possible_moves(self, board: "ChessBoard") -> list[Position]:
        moves = []

        row, col = self.position
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.is_square_empty((new_row, new_col)) or \
                board.is_opponent_piece(self.color, (new_row, new_col)):
                        moves.append((new_row, new_col))

        return moves