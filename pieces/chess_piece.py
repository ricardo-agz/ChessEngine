from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chess_board import ChessBoard

Position = tuple[int, int]


class PlayerColor(Enum):
    WHITE = 'white'
    BLACK = 'black'
    

class ChessPiece:
    def __init__(self, color: PlayerColor, position: Position):
        self.color: PlayerColor = color
        self.position: Position = position

    def get_possible_moves(self, board: "ChessBoard") -> list[Position]:
        pass