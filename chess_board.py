from copy import deepcopy
from typing import Optional

from pieces import ChessPiece, PlayerColor, Rook, Knight, Bishop, King, Queen, Pawn
from piece_square_tables import pst_pawn, pst_knight, pst_bishop, pst_king, pst_rook, pst_queen

Position = tuple[int, int]


class ChessBoard:
    def __init__(self, board_state: list[list[Optional[ChessPiece]]] = None):
        if board_state is None:
            self.board = self.create_empty_board()
            self.place_pieces()
        else:
            self.board = board_state

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

    def is_move_valid(self, piece: ChessPiece, new_position: Position) -> bool:
        """
        Checks if a move is valid by creating a copy of the board, making the move,
        and checking if the king is in check after the move.
        """
        color = piece.color

        # Create a copy of the board and make the move
        board_copy = deepcopy(self)
        old_row, old_col = piece.position
        new_row, new_col = new_position
        board_copy.board[old_row][old_col] = None
        board_copy.board[new_row][new_col] = piece

        # Check if the king is in check after the move
        return not board_copy.is_king_in_check(color)

    def get_possible_moves(self, color: PlayerColor) -> list[tuple[ChessPiece, list[Position]]]:
        """
        Returns a list of all pieces and their possible moves on the board for a given player
        """
        valid_moves = []
        pieces = self.get_pieces(color)

        for piece in pieces:
            possible_moves = piece.get_possible_moves(self)
            valid_piece_moves = [move for move in possible_moves if self.is_move_valid(piece, move)]
            valid_moves.append((piece, valid_piece_moves))

        return valid_moves

    def move_piece(self, piece: ChessPiece, new_position: Position) -> bool:
        """
        Moves a piece on the board, returns False if invalid move
        """
        color = piece.color
        valid_moves_with_pieces = self.get_possible_moves(color)

        # Get the list of valid moves for the specific piece
        valid_moves = []
        for curr_piece, possible_moves in valid_moves_with_pieces:
            if curr_piece.position == piece.position:
                valid_moves = possible_moves
                break

        if new_position not in valid_moves:
            print("Illegal move:/")
            return False

        old_row, old_col = piece.position
        new_row, new_col = new_position

        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.position = new_position

        return True

    def get_opponent_possible_moves_without_check(self, color: PlayerColor) -> list[Position]:
        """
        Returns a list of all possible moves for the opponent without checking for check.
        """
        opponent_color = PlayerColor.WHITE if color == PlayerColor.BLACK else PlayerColor.BLACK
        opponent_pieces = self.get_pieces(opponent_color)
        opponent_possible_moves = []

        for piece in opponent_pieces:
            possible_moves = piece.get_possible_moves(self)
            opponent_possible_moves.extend(possible_moves)

        return opponent_possible_moves

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

        opponent_possible_moves = self.get_opponent_possible_moves_without_check(color)
        return king_position in opponent_possible_moves

    def is_checkmate(self, color: PlayerColor) -> bool:
        """
        Returns true if the king is in check and there are no moves that would take the king out of check
        """
        if not self.is_king_in_check(color):
            return False

        possible_moves_per_piece = self.get_possible_moves(color)
        for curr_piece, possible_moves in possible_moves_per_piece:
            # Create a copy of the board and make the move
            for move in possible_moves:
                board_copy = deepcopy(self)
                piece_copy = deepcopy(curr_piece)
                
                # Try the move and continue to the next move if it is invalid
                move_result = board_copy.move_piece(piece_copy, move)
                if not move_result:
                    continue

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

        possible_moves_per_piece = self.get_possible_moves(color)
        for curr_piece, possible_moves in possible_moves_per_piece:
            # Create a copy of the board and make the move
            for move in possible_moves:
                board_copy = deepcopy(self)
                piece_copy = deepcopy(curr_piece)
                
                # Try the move and continue to the next move if it is invalid
                move_result = board_copy.move_piece(piece_copy, move)
                if not move_result:
                    continue

                # Check if the king is still in check after the move
                if not board_copy.is_king_in_check(color):
                    return False

        return True


    # Game Score Function
    def evaluation_function(self):
        '''
        This function will return a score for the current board state
        If white is winning it would return a positive number, if black is winning negative.
        If either side is in checkmate it will return inf or -inf
        '''
        if self.is_checkmate(PlayerColor.WHITE):
            print("i have been checkmated by a robot...")
            return float("infinity")
        elif self.is_checkmate(PlayerColor.BLACK):
            print("checkmate bitch")
            return -float("infinity")
        else:
            score = 0
            print(f"init score: {score}")
            for row in range(8):
                for col in range(8):
                    piece = self.get_piece((row, col))
                    if piece is not None:
                        if piece.color == PlayerColor.WHITE:
                            score += piece.value
                            print(f"added value score: {score}")
                            if isinstance(piece, Pawn):
                                score += pst_pawn[row][col]
                            elif isinstance(piece, Knight):
                                score += pst_knight[row][col]
                            elif isinstance(piece, Bishop):
                                score += pst_bishop[row][col]
                            elif isinstance(piece, Rook):
                                score += pst_rook[row][col]
                            elif isinstance(piece, Queen):
                                score += pst_queen[row][col]
                            elif isinstance(piece, King):
                                score += pst_king[row][col]
                        else:
                            score -= piece.value
                            print(f"minus value score: {score}")
                            if isinstance(piece, Pawn):
                                score -= pst_pawn[7-row][col]
                            elif isinstance(piece, Knight):
                                score -= pst_knight[7-row][col]
                            elif isinstance(piece, Bishop):
                                score -= pst_bishop[7-row][col]
                            elif isinstance(piece, Rook):
                                score -= pst_rook[7-row][col]
                            elif isinstance(piece, Queen):
                                score -= pst_queen[7-row][col]
                            elif isinstance(piece, King):
                                score -= pst_king[7-row][col]

        print(f"evaluation score: {score}")
        return score
