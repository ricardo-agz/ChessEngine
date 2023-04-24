from copy import deepcopy
from typing import List, Tuple, Optional
import random

from chess_board import ChessBoard, Position
from pieces.chess_piece import ChessPiece, PlayerColor


def minimax(board_state: ChessBoard, depth: int, maximizing_player: bool, player_color: PlayerColor, alpha: float = -float('inf'), beta: float = float('inf')) -> Tuple[Optional[ChessPiece], Optional[Position], int]:
    """
    Minimax algorithm with alpha-beta pruning for the chess AI
    
    Args:
        board_state (ChessBoard): Current state of the chess board.
        depth (int): Depth of the search tree.
        maximizing_player (bool): True if maximizing player, otherwise False.
        player_color (PlayerColor): Color of the current player.
        alpha (float, optional): Alpha value for alpha-beta pruning. Defaults to -float('inf').
        beta (float, optional): Beta value for alpha-beta pruning. Defaults to float('inf').

    Returns:
        Tuple[Optional[ChessPiece], Optional[Position], int]: Best piece, best move, and score of the best move.
    """
    
    # base case: depth is 0 or game over
    if depth == 0 or board_state.is_checkmate(player_color) or board_state.is_stalemate(player_color):
        return None, None, board_state.evaluation_function()

    best_move = None
    best_piece = None

    if maximizing_player:
        max_score = -float('inf')

        # iterate over all possible moves for the current player
        for piece, moves in board_state.get_possible_moves(player_color):
            for move in moves:
                # create a new board and move the piece
                new_board = deepcopy(board_state)
                new_piece = deepcopy(piece)
                new_board.move_piece(new_piece, move)
                
                # recursive call with depth - 1 and switched player
                _, _, score = minimax(new_board, depth - 1, False, player_color, alpha, beta)

                # update best move if a better score is found
                if score > max_score:
                    max_score = score
                    best_move = move
                    best_piece = piece

                # update alpha and prune if beta <= alpha
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    return best_piece, best_move, max_score

        return best_piece, best_move, max_score
    else:
        min_score = float('inf')
        opponent_color = PlayerColor.WHITE if player_color == PlayerColor.BLACK else PlayerColor.BLACK

        # iterate over all possible moves for the opponent
        for piece, moves in board_state.get_possible_moves(opponent_color):
            for move in moves:
                # create a new board and move the piece
                new_board = deepcopy(board_state)
                new_piece = deepcopy(piece)
                new_board.move_piece(new_piece, move)
                
                # recursive call with depth - 1 and switched player
                _, _, score = minimax(new_board, depth - 1, True, opponent_color, alpha, beta)

                # update best move if a lower score is found
                if score < min_score:
                    min_score = score
                    best_move = move
                    best_piece = piece

                # update beta and prune if beta <= alpha
                beta = min(beta, min_score)
                if beta <= alpha:
                    return best_piece, best_move, min_score

        # if best_move is None or best_piece is None:
        #     print("no meaningful move found... making random move lol")
        #     best_piece, best_move = get_random_move(board_state, player_color if maximizing_player else opponent_color)

        return best_piece, best_move, min_score





def get_random_move(board_state: ChessBoard, color: PlayerColor) -> Tuple[ChessPiece, Position]:
    possible_moves = []

    for piece, moves in board_state.get_possible_moves(color):
        for move in moves:
            possible_moves.append((piece, move))

    if not possible_moves:
        return None, None

    return random.choice(possible_moves)


def get_best_move(board_state: ChessBoard, depth: int, color: PlayerColor) -> Tuple[ChessPiece, Position]:
    piece, move, _ = minimax(board_state, depth, True, color)
    # piece, move = get_random_move(board_state, color)

    return piece, move

