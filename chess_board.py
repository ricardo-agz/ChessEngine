from copy import deepcopy
from enum import Enum
from typing import Optional

from pieces import ChessPiece, PlayerColor, Rook, Knight, Bishop, King, Queen, Pawn

Position = tuple[int, int]


class ChessBoard:
    def __init__(self):
        self.board = self.create_empty_board()
        self.place_pieces()

    def create_empty_board(self) -> list[list[Optional[ChessPiece]]]:
        """Create an empty 8x8 chess board"""
        return [[None] * 8 for _ in range(8)]

    def place_pieces(self):
        """Places chess pieces in starting positions of chess board"""
        pieces = [
            Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook
        ]

        for i, Piece in enumerate(pieces):
            self.board[0][i] = Piece(PlayerColor.BLACK, (0, i))
            self.board[7][i] = Piece(PlayerColor.WHITE, (7, i))
            self.board[1][i] = Pawn(PlayerColor.BLACK, (1, i))
            self.board[6][i] = Pawn(PlayerColor.WHITE, (6, i))

    def is_square_empty(self, position: Position) -> bool:
        """
        Returns True if given position does not contain a piece
        """
        return self.get_piece(position) is None

    def is_opponent_piece(self, color: PlayerColor, position: Position) -> bool:
        """
        Returns whether the given position contains an opponent piece for the given player
        """
        piece = self.get_piece(position)
        return piece is not None and piece.color != color

    def move_piece(self, piece: ChessPiece, new_position: Position):
        """
        Moves a piece on the board
        """
        color = piece.color
        valid_moves_with_pieces = self.get_possible_moves(color)

        # Get the list of valid moves for the specific piece
        valid_moves = []
        for piece_and_moves in valid_moves_with_pieces:
            current_piece, moves = piece_and_moves
            if current_piece == piece:
                valid_moves = moves
                break

        if new_position not in valid_moves:
            raise ValueError("Invalid move")

        old_row, old_col = piece.position
        new_row, new_col = new_position

        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.position = new_position

    def get_piece(self, position: Position) -> Optional[ChessPiece]:
        """
        Returns the piece at a given board position
        """
        row, col = position
        return self.board[row][col]

    def get_pieces(self, color: PlayerColor) -> list[ChessPiece]:
        """
        Returns all pieces on the board for a given player
        """
        pieces: list[ChessPiece] = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece((row, col))
                if piece and piece.color == color:
                    pieces.append(piece)

        return pieces

    def get_possible_moves(self, color: PlayerColor) -> list[tuple[ChessPiece, list[Position]]]:
        """
        Returns a list of all pieces and their possible moves on the board for a given player
        """
        valid_moves = []
        pieces = self.get_pieces(color)

        for piece in pieces:
            possible_moves = piece.get_possible_moves(self)
            valid_piece_moves = []

            for move in possible_moves:
                # Create a copy of the board and make the move
                board_copy = deepcopy(self)
                board_copy.move_piece(piece, move)

                # Check if the king is in check after the move
                if not board_copy.is_king_in_check(color):
                    valid_piece_moves.append(move)

            valid_moves.append((piece, valid_piece_moves))

        return valid_moves

    def is_king_in_check(self, color: PlayerColor) -> bool:
        """
        Returns true if the king for the given player is in check under the current board position
        """
        king_position: Optional[Position] = None
        for row in range(8):
            for col in range(8):
                piece = self.get_piece((row, col))
                if piece and piece.color == color and isinstance(piece, King):
                    king_position = (row, col)
                    break
            if king_position:
                break

        opponent_color = PlayerColor.WHITE if color == PlayerColor.BLACK else PlayerColor.BLACK
        opponent_possible_moves = self.get_possible_moves(opponent_color)
        return king_position in opponent_possible_moves

    def is_checkmate(self, color: PlayerColor) -> bool:
        """
        Returns true if the king is in check and there are no moves that would take the king out of check
        """
        if not self.is_king_in_check(color):
            return False

        possible_moves = self.get_possible_moves(color)
        for move in possible_moves:
            # Create a copy of the board and make the move
            board_copy = deepcopy(self)
            piece = board_copy.get_piece(move[0])
            board_copy.move_piece(piece, move[1])

            # Check if the king is still in check after the move
            if not board_copy.is_king_in_check(color):
                return False

        return True

    def is_stalemate(self, color: PlayerColor) -> bool:
        """
        Returns true if the king is not in check there are no valid moves that would keep the king out of check
        """
        if self.is_king_in_check(color):
            return False

        possible_moves = self.get_possible_moves(color)
        for move in possible_moves:
            # Create a copy of the board and make the move
            board_copy = deepcopy(self)
            piece = board_copy.get_piece(move[0])
            board_copy.move_piece(piece, move[1])

            # Check if the king is in check after the move
            if not board_copy.is_king_in_check(color):
                return False

        return True
