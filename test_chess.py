from copy import deepcopy
import unittest
from chess_board import ChessBoard, Position
from pieces import King, Queen, Rook, Bishop, Knight, Pawn, ChessPiece, PlayerColor
from util import position_to_string

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

    def test_king_in_check(self):
        black_king = King(PlayerColor.BLACK, (0, 0))
        white_queen = Queen(PlayerColor.WHITE, (7, 7))
        
        board_state = [
            [black_king, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, white_queen],
        ]

        board = ChessBoard(board_state=board_state)

        self.assertTrue(board.is_king_in_check(PlayerColor.BLACK))
        self.assertFalse(board.is_king_in_check(PlayerColor.WHITE))
        self.assertFalse(board.is_checkmate(PlayerColor.WHITE))
        self.assertFalse(board.is_checkmate(PlayerColor.BLACK))

    def test_possible_moves_king_no_check(self):
        black_king = King(PlayerColor.BLACK, (7, 7))
        white_king = King(PlayerColor.WHITE, (0, 0))
        
        board_state = [
            [white_king, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, black_king],
        ]

        board = ChessBoard(board_state=board_state)

        white_king_moves = [(0, 1), (1, 0), (1, 1)]
        black_king_moves = [(6, 6), (6, 7), (7, 6)]

        self.assertEqual(set(white_king_moves), set(white_king.get_possible_moves(board)))
        self.assertEqual(set(black_king_moves), set(black_king.get_possible_moves(board)))

    def test_king_in_stalemate(self):
        black_king = King(PlayerColor.BLACK, (0, 0))
        white_rook_1 = Rook(PlayerColor.WHITE, (1, 7))
        white_rook_2 = Rook(PlayerColor.WHITE, (7, 1))
        
        board_state = [
            [black_king, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, white_rook_1],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, white_rook_2, None, None, None, None, None, None],
        ]

        board = ChessBoard(board_state=board_state)

        self.assertFalse(board.is_king_in_check(PlayerColor.BLACK))
        self.assertFalse(board.is_checkmate(PlayerColor.BLACK))
        self.assertTrue(board.is_stalemate(PlayerColor.BLACK))

if __name__ == '__main__':
    unittest.main()
