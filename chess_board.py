from copy import copy, deepcopy
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

        self.moves = []

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

    def get_moves(self) -> list[tuple[str, Position, Position]]:
        """Returns list of all moves already made"""
        return self.moves

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

        king_moves = []
        for piece in pieces:
            possible_moves = piece.get_possible_moves(self)
            valid_piece_moves = [move for move in possible_moves if self.is_move_valid(piece, move)]

            # Handle castling moves for King
            if isinstance(piece, King) and not piece.has_moved and not self.is_king_in_check(color):
                if self.can_castle_kingside(color):
                    valid_piece_moves.append((piece.position[0], 6))
                if self.can_castle_queenside(color):
                    valid_piece_moves.append((piece.position[0], 2))

            valid_moves.append((piece, valid_piece_moves))

        return valid_moves
        # for piece in pieces:
        #     possible_moves = piece.get_possible_moves(self)
        #     valid_piece_moves = [move for move in possible_moves if self.is_move_valid(piece, move)]
        #     if isinstance(piece, King):
        #         king_moves = valid_piece_moves
        #                 # Handle castling moves for King
        #     if piece.has_moved and not self.is_king_in_check(color):
        #         if self.can_castle_kingside(color):
        #             valid_piece_moves.append((piece.position[0], 6))
        #         if self.can_castle_queenside(color):
        #             valid_piece_moves.append((piece.position[0], 2))
        #         king_moves.extend(valid_piece_moves)
        #     valid_moves.append((piece, valid_piece_moves))
        

        
        # valid_moves.append((piece, valid_piece_moves))

        # return valid_moves

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

        # record move
        self.moves.append((piece.to_str(), piece.position, new_position))

        # Move the piece
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.position = new_position

        # If Castle move: Move the Rook as well
        if isinstance(piece, King) and not piece.has_moved and abs(old_col - new_col) == 2:
            # Castling kingside
            if new_col > old_col:
                rook = self.get_piece((old_row, 7))
                if rook is not None and not rook.has_moved:
                    self.board[old_row][7] = None
                    self.board[old_row][5] = rook
                    rook.position = (old_row, 5)
                    rook.has_moved = True
                else:
                    print("Illegal move:/")
                    return False
            # Castling queenside
            else:
                rook = self.get_piece((old_row, 0))
                if rook is not None and not rook.has_moved:
                    self.board[old_row][0] = None
                    self.board[old_row][3] = rook
                    rook.position = (old_row, 3)
                    rook.has_moved = True
                else:
                    print("Illegal move:/")
                    return False
        
        # Castling Purposes: If piece=King or Rook, set has_moved to True
        if isinstance(piece, King) or isinstance(piece, Rook):
            piece.has_moved = True
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
            for row in range(8):
                for col in range(8):
                    piece = self.get_piece((row, col))
                    if piece is not None:
                        row_flip = row if piece.color == PlayerColor.WHITE else 7-row

                        # calculate a multiplier based on the position of the piece
                        position_score = 0
                        if isinstance(piece, Pawn):
                            position_score += pst_pawn[row_flip][col]
                        elif isinstance(piece, Knight):
                            position_score += pst_knight[row_flip][col]
                        elif isinstance(piece, Bishop):
                            position_score += pst_bishop[row_flip][col]
                        elif isinstance(piece, Rook):
                            position_score += pst_rook[row_flip][col]
                        elif isinstance(piece, Queen):
                            position_score += pst_queen[row_flip][col]
                        elif isinstance(piece, King):
                            position_score += pst_king[row_flip][col]
                        
                        position_multiple = (position_score + 100) / 100
                        added_score = piece.value * 10 * position_multiple

                        min_max_multiplier = 1 if piece.color == PlayerColor.WHITE else -1
                        score += added_score * min_max_multiplier # multiply by -1 if player is black

                        mobility = len(piece.get_possible_moves(self)) * 0.2
                        added_score += mobility

        if self.is_king_in_check(PlayerColor.WHITE):
            score -= 10
        elif self.is_king_in_check(PlayerColor.BLACK):
            score += 10
        return score

    def __hash__(self):
        # Use a tuple of tuples containing the board state as the hash input
        return hash(tuple(tuple(self.board[row][col] for col in range(8)) for row in range(8)))

    def can_castle_kingside(self, color: PlayerColor) -> bool:
            
            row = 7 if color == PlayerColor.WHITE else 0
            king = self.get_piece((row, 4))
            rook = self.get_piece((row, 7))
            if not isinstance(king, King) or king.has_moved:
                return False
            if not isinstance(rook, Rook) or rook.has_moved:
                return False
            
            # Check if squares between king and rook are empty
            for col in range(5, 7):
                if not self.is_square_empty((row, col)):
                    return False

            # Check if squares king moves through are not attacked
            opponent_possible_moves = self.get_opponent_possible_moves_without_check(color)
            for col in range(4, 8):
                if (row, col) in opponent_possible_moves:
                    return False
            return True
    
    def can_castle_queenside(self, color: PlayerColor) -> bool:
            row = 7 if color == PlayerColor.WHITE else 0
            king = self.get_piece((row, 4))
            rook = self.get_piece((row, 0))
            if not isinstance(king, King) or king.has_moved:
                return False
            if not isinstance(rook, Rook) or rook.has_moved:
                return False
            
            # Check if squares between king and rook are empty
            for col in range(1, 3+1):
                if not self.is_square_empty((row, col)):
                    return False

            # Check if squares king moves through are not attacked
            opponent_possible_moves = self.get_opponent_possible_moves_without_check(color)
            for col in range(0, 4+1):
                if (row, col) in opponent_possible_moves:
                    return False
            return True  
    

    def __deepcopy__(self, memo):
        new_board = ChessBoard()
        new_board.board = deepcopy(self.board, memo)
        new_board.moves = copy(self.moves)
        return new_board