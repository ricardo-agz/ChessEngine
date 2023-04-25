from copy import deepcopy
from typing import List, Tuple, Optional
import random
import time

from chess_board import ChessBoard, Position
from pieces.chess_piece import ChessPiece, PlayerColor


def minimax(
        board_state: ChessBoard, 
        depth: int, 
        maximizing_player: bool, 
        player_color: PlayerColor, 
        alpha: float = -float('inf'), 
        beta: float = float('inf'),
        cache: Optional[dict[str, tuple[Optional[ChessPiece], Optional[Position], int]]] = None,
        start_time: time = None,
        time_limit: time = None
    ) -> Tuple[Optional[ChessPiece], Optional[Position], int]:
    """
    Minimax algorithm with alpha-beta pruning for the chess AI
    
    Args:
        board_state (ChessBoard): Current state of the chess board.
        depth (int): Depth of the search tree.
        maximizing_player (bool): True if maximizing player, otherwise False.
        player_color (PlayerColor): Color of the current player.
        alpha (float, optional): Alpha value for alpha-beta pruning. Defaults to -float('inf').
        beta (float, optional): Beta value for alpha-beta pruning. Defaults to float('inf').
        cache (Optional[dict[str, tuple[Optional[ChessPiece], Optional[Position], int]]], optional): A dictionary to store previously computed board evaluations. Defaults to None.

    Returns:
        Tuple[Optional[ChessPiece], Optional[Position], int]: Best piece, best move, and score of the best move.
    """

    if cache is None:
        cache = {}

    board_key = hash(board_state)
    if board_key in cache and depth == cache[board_key][2]:
        return cache[board_key]

    elapsed_time = time.time() - start_time
    
    # base case: depth is 0 or game over
    if  depth == 0 or \
        board_state.is_checkmate(player_color) or \
        board_state.is_stalemate(player_color) or \
        (start_time is not None and time_limit is not None and elapsed_time >= time_limit):

        return None, None, board_state.evaluation_function()

    best_move = None
    best_piece = None
    opponent_color = PlayerColor.WHITE if player_color == PlayerColor.BLACK else PlayerColor.BLACK

    if maximizing_player:
        max_score = -float('inf')

        # Get all possible moves and their scores
        possible_moves = [(piece, move) for piece, moves in board_state.get_possible_moves(player_color) for move in moves]

        # Sort the moves based on their scores
        possible_moves.sort(key=lambda move: move_score(move, board_state), reverse=True)

        # Iterate over the ordered moves
        for piece, move in possible_moves:
            # create a new board and move the piece
            new_board = deepcopy(board_state)
            new_piece = deepcopy(piece)
            new_board.move_piece(new_piece, move)
            
            # recursive call with depth - 1 and switched player
            _, _, score = minimax(
                board_state=new_board, 
                depth=depth - 1, 
                maximizing_player=False, 
                player_color=player_color, 
                alpha=alpha, 
                beta=beta, 
                start_time=start_time, 
                time_limit=time_limit)

            # update best move if a better score is found
            if score > max_score:
                max_score = score
                best_move = move
                best_piece = piece

            # update alpha and prune if beta <= alpha
            alpha = max(alpha, max_score)
            if beta <= alpha:
                return best_piece, best_move, max_score

        cache[board_key] = best_piece, best_move, max_score
        return best_piece, best_move, max_score
    else:
        min_score = float('inf')

        # Get all possible moves and their scores
        possible_moves = [(piece, move) for piece, moves in board_state.get_possible_moves(player_color) for move in moves]

        # Sort the moves based on their scores
        possible_moves.sort(key=lambda move: move_score(move, board_state), reverse=False)

        for piece, move in possible_moves:
            # create a new board and move the piece
            new_board = deepcopy(board_state)
            new_piece = deepcopy(piece)
            new_board.move_piece(new_piece, move)

            # recursive call with depth - 1 and switched player
            _, _, score = minimax(
                board_state=new_board, 
                depth=depth - 1, 
                maximizing_player=True, 
                player_color=opponent_color, 
                alpha=alpha, 
                beta=beta, 
                start_time=start_time, 
                time_limit=time_limit)

            # update best move if a lower score is found
            if score < min_score:
                min_score = score
                best_move = move
                best_piece = piece

            # update beta and prune if beta <= alpha
            beta = min(beta, min_score)
            if beta <= alpha:
                return best_piece, best_move, min_score

        cache[board_key] = best_piece, best_move, min_score
        return best_piece, best_move, min_score


def iterative_deepening_minimax(
        board_state: ChessBoard, 
        max_depth: int, 
        maximizing_player: bool, 
        player_color: PlayerColor, 
        time_limit: int,
    ) -> Tuple[Optional[ChessPiece], Optional[Position], int]:

    start_time = time.time()
    best_piece, best_move, best_score = None, None, -float('inf') if maximizing_player else float('inf')

    for current_depth in range(1, max_depth + 1):
        piece, move, score = minimax(
            board_state=board_state, 
            depth=current_depth, 
            maximizing_player=maximizing_player, 
            player_color=player_color, 
            start_time=start_time, 
            time_limit=time_limit)

        if maximizing_player and score > best_score:
            best_piece, best_move, best_score = piece, move, score
        elif not maximizing_player and score < best_score:
            best_piece, best_move, best_score = piece, move, score

        # check if time limit has been reached and break if so
        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit:
            break

    return best_piece, best_move, best_score


def get_random_move(board_state: ChessBoard, color: PlayerColor) -> Tuple[ChessPiece, Position]:
    possible_moves = []

    for piece, moves in board_state.get_possible_moves(color):
        for move in moves:
            possible_moves.append((piece, move))

    if not possible_moves:
        return None, None

    return random.choice(possible_moves)


def move_score(move: Tuple[ChessPiece, Position], board_state: ChessBoard) -> int:
    piece, target_position = move
    target_piece = board_state.get_piece(target_position)

    score = 0

    # capture moves given priority based on relative value
    if target_piece is not None and target_piece.color != piece.color:
        score += (target_piece.value - piece.value) * 100

    new_board = deepcopy(board_state)
    new_piece = deepcopy(piece)
    new_board.move_piece(new_piece, target_position)

    # check moves also given priority
    opponent_color = PlayerColor.WHITE if piece.color == PlayerColor.BLACK else PlayerColor.BLACK
    if new_board.is_king_in_check(opponent_color):
        score += 50

    # center control bonus
    central_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    if target_position in central_squares:
        score += 10

    # moved piece mobility is rewarded
    mobility = len(new_piece.get_possible_moves(new_board))
    score += mobility

    return score


def get_best_move(board_state: ChessBoard, color: PlayerColor, max_depth: int = None, max_time: int = None) -> Tuple[ChessPiece, Position]:
    time_limit = 10  # time limit in secondsz
    max_depth = max_depth

    piece, move, _ = iterative_deepening_minimax(
        board_state=board_state,
        max_depth=max_depth,
        maximizing_player=True,
        player_color=color,
        time_limit=time_limit,
    )
    # piece, move, _ = minimax(board_state, depth, True, color)
    # piece, move = get_random_move(board_state, color)

    return piece, move

