import unittest
from chess_board import ChessBoard, Position
from pieces import King, Queen, Rook, Bishop, Knight, Pawn, ChessPiece, PlayerColor

class TestChessBoard(unittest.TestCase):

    def test_board_init(self):
        board = ChessBoard()
        rook_position: Position = (0, 0)

        self.assertFalse(board.is_square_empty(rook_position))
        self.assertTrue(isinstance(board.get_piece(rook_position), Rook))
        
        self.assertTrue(isinstance(board.get_piece((0, 7)), Rook))
        self.assertTrue(board.get_piece(rook_position).color == PlayerColor.BLACK)

        self.assertEqual(len(board.get_pieces(PlayerColor.WHITE)), 16)
        self.assertEqual(len(board.get_pieces(PlayerColor.BLACK)), 16)

if __name__ == '__main__':
    unittest.main()
