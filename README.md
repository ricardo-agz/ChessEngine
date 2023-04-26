# ChessEngine

This is a ChessEngine implemented with the minimax algorithm. Black is played by the ChessEngine. 

Presentation Link
https://docs.google.com/presentation/d/1e-2kfJnDqCgey7RU_Q-FqPf-d-5Aqk26IF-XqMHE72s/edit#slide=id.p

Premise of Minimax:
- Explore all my possible moves, try to maximize my score
- For each of my moves, explore all the opponents’ possible moves (assume they play optimally)
  -  I.e. the opponent will try to minimize the score
- Return the best move leading to the leaf with the best score
The score is determined by an evaluation function that takes into account piece points, their position on the board, and whether the king is in check.
However, there are an exponential number of possible board states and searching through all possible moves would take a lot of time.

To speed up the minimax search, we implemented a variety of methods/techniques:
- Alpha-beta pruning
- Iterative deepening minimax
- Move ordering
  - Assigning Move Scores
  - Late Move Reduction
  - Static Exchange Evaluation
- Book Openings

# File Structure
- Pieces Folder contains python classes for each piece
- chess_board.py contains board and move logic
- chess_gui.py contains the GUI
- engine.py contains the minimax algorithm
- piece_square_tables.py contains the position points 

# Instructions to Run ChessEngine
- Download/clone repository
- Run command `python chess_gui.py`
- Make moves and play against the ChessEngine

