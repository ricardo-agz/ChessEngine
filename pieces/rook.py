from typing import TYPE_CHECKING

from pieces.chess_piece import ChessPiece, PlayerColor

if TYPE_CHECKING:
    from chess_board import ChessBoard

Position = tuple[int, int]


class Rook(ChessPiece):
    def __init__(self, color: PlayerColor, position: Position):
        super().__init__(color, position)
        self.value = 5

    def get_possible_moves(self, board: "ChessBoard") -> list[Position]:
        moves = []

        row, col = self.position

        # Horizontal and vertical moves
        for i in range(1, 8):
            directions = [
                (row + i, col),     # Down
                (row - i, col),     # Up
                (row, col + i),     # Right
                (row, col - i)      # Left
            ]

            for new_row, new_col in directions:
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if board.is_square_empty((new_row, new_col)):
                        moves.append((new_row, new_col))
                    elif board.is_opponent_piece(self.color, (new_row, new_col)):
                        moves.append((new_row, new_col))
                        break # blocking piece
                    else:
                        break # self blocking piece

        # Remove moves that are outside the board
        valid_moves = [move for move in moves if 0 <= move[0] < 8 and 0 <= move[1] < 8]

        return valid_moves
