from chess_board import ChessBoard, Position

class ChessPiece:
    def __init__(self, color: str, position: Position):
        self.color: str = color
        self.position: Position = position

    def get_possible_moves(self, board: ChessBoard) -> list[Position]:
        pass

class King(ChessPiece):
    def get_possible_moves(self, board: ChessBoard) -> list[Position]:
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
                moves.append((new_row, new_col))

        return moves


class Queen(ChessPiece):
    def get_possible_moves(self, board: ChessBoard) -> list[Position]:
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

        # Diagonal moves
        for i in range(1, 8):
            directions = [
                (row + i, col + i), # Down-right
                (row + i, col - i), # Down-left
                (row - i, col + i), # Up-right
                (row - i, col - i)  # Up-left
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

        return moves

class Rook(ChessPiece):
    def get_possible_moves(self, board: ChessBoard) -> list[Position]:
        moves = []

        row, col = self.position

        # Horizontal and vertical moves
        for i in range(1, 8):
            moves.append((row + i, col))  # Down
            moves.append((row - i, col))  # Up
            moves.append((row, col + i))  # Right
            moves.append((row, col - i))  # Left

        # Remove moves that are outside the board
        valid_moves = [move for move in moves if 0 <= move[0] < 8 and 0 <= move[1] < 8]

        return valid_moves


class Bishop(ChessPiece):
    def get_possible_moves(self, board: ChessBoard) -> list[Position]:
        moves = []

        row, col = self.position

        # Diagonal moves
        for i in range(1, 8):
            moves.append((row + i, col + i))  # Down-right
            moves.append((row + i, col - i))  # Down-left
            moves.append((row - i, col + i))  # Up-right
            moves.append((row - i, col - i))  # Up-left

        # Remove moves that are outside the board
        valid_moves = [move for move in moves if 0 <= move[0] < 8 and 0 <= move[1] < 8]

        return valid_moves

class Knight(ChessPiece):
    def get_possible_moves(self, board: ChessBoard) -> list[Position]:
        moves = []

        row, col = self.position
        directions = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2),  (1, 2),
            (2, -1),  (2, 1)
        ]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.is_square_empty((new_row, new_col)) or board.is_opponent_piece(self.color, (new_row, new_col)):
                    moves.append((new_row, new_col))

        return moves

class Pawn(ChessPiece):
    def get_possible_moves(self, board: ChessBoard) -> list[Position]:
        moves = []

        row, col = self.position

        if self.color == "white":
            # One square forward
            if 0 <= row - 1 < 8 and board.is_square_empty((row - 1, col)):
                moves.append((row - 1, col))

            # Two squares forward from the starting position
            if row == 6 and board.is_square_empty((row - 1, col)) and board.is_square_empty((row - 2, col)):
                moves.append((row - 2, col))

            # Capture moves
            if 0 <= row - 1 < 8:
                if 0 <= col - 1 < 8 and board.is_opponent_piece(self.color, (row - 1, col - 1)):
                    moves.append((row - 1, col - 1))
                if 0 <= col + 1 < 8 and board.is_opponent_piece(self.color, (row - 1, col + 1)):
                    moves.append((row - 1, col + 1))

        else:  # "black"
            # One square forward
            if 0 <= row + 1 < 8 and board.is_square_empty((row + 1, col)):
                moves.append((row + 1, col))

            # Two squares forward from the starting position
            if row == 1 and board.is_square_empty((row + 1, col)) and board.is_square_empty((row + 2, col)):
                moves.append((row + 2, col))

            # Capture moves
            if 0 <= row + 1 < 8:
                if 0 <= col - 1 < 8 and board.is_opponent_piece(self.color, (row + 1, col - 1)):
                    moves.append((row + 1, col - 1))
                if 0 <= col + 1 < 8 and board.is_opponent_piece(self.color, (row + 1, col + 1)):
                    moves.append((row + 1, col + 1))

        return moves


