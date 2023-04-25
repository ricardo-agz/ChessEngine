from typing import TYPE_CHECKING

from pieces.chess_piece import ChessPiece, PlayerColor
from util import position_to_string

if TYPE_CHECKING:
    from chess_board import ChessBoard

Position = tuple[int, int]


class King(ChessPiece):
    def __init__(self, color: PlayerColor, position: Position):
        super().__init__(color, position)
        self.value = 0
        self.has_moved = False

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


        # Castling
        # if not self.has_moved and not board.is_king_in_check(self.color):
        #     row = 0 if self.color == PlayerColor.WHITE else 7
        #      # Check kingside castling
        #     if board.can_castle_kingside(self.color):
        #         moves.append((row, 6))

        #     # Check queenside castling
        #     if board.can_castle_queenside(self.color):
        #         moves.append((row, 2))
        return moves

    def has_moved(self):
        return self.has_moved

    def to_str(self):
        return "King"

    def __str__(self):
        return f"<{self.color.value.title()} King at {position_to_string(self.position)}>"