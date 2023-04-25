import tkinter as tk
import threading
from PIL import ImageTk, Image  # pip install pillow
from typing import Optional
from chess_board import ChessBoard, Position
from pieces.chess_piece import PlayerColor
from engine import minimax, get_best_move

class ChessGUI(tk.Tk):
    def __init__(self, board: ChessBoard):
        self.board = board
        self.selected_piece: Optional[Position] = None
        self.current_player = PlayerColor.WHITE

        self.window = tk.Tk()
        self.window.title("Chess")
        self.canvas = tk.Canvas(self.window, width=640, height=640)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_tile_click)

        # load piece images
        self.white_pieces = {
            "Pawn": ImageTk.PhotoImage(Image.open("images/white_pieces/pawn.png")),
            "Rook": ImageTk.PhotoImage(Image.open("images/white_pieces/rook.png")),
            "Knight": ImageTk.PhotoImage(Image.open("images/white_pieces/knight.png")),
            "Bishop": ImageTk.PhotoImage(Image.open("images/white_pieces/bishop.png")),
            "Queen": ImageTk.PhotoImage(Image.open("images/white_pieces/queen.png")),
            "King": ImageTk.PhotoImage(Image.open("images/white_pieces/king.png")),
        }
        self.black_pieces = {
            "Pawn": ImageTk.PhotoImage(Image.open("images/black_pieces/pawn.png")),
            "Rook": ImageTk.PhotoImage(Image.open("images/black_pieces/rook.png")),
            "Knight": ImageTk.PhotoImage(Image.open("images/black_pieces/knight.png")),
            "Bishop": ImageTk.PhotoImage(Image.open("images/black_pieces/bishop.png")),
            "Queen": ImageTk.PhotoImage(Image.open("images/black_pieces/queen.png")),
            "King": ImageTk.PhotoImage(Image.open("images/black_pieces/king.png")),
        }
        self.draw_board()
        self.place_pieces()

    def refresh_board(self):
        self.draw_board()
        self.place_pieces()

    def switch_player(self):
        if self.current_player == PlayerColor.WHITE:
            self.current_player = PlayerColor.BLACK
        else:
            self.current_player = PlayerColor.WHITE


    def highlight_square(self, row, col, color: str):
        x1, y1 = col * 80, row * 80
        x2, y2 = x1 + 80, y1 + 80
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="highlight", stipple="gray12")

    def remove_square_highlight(self, row, col):
        x1, y1 = col * 80, row * 80
        x2, y2 = x1 + 80, y1 + 80
        color = "white" if (row + col) % 2 == 0 else "gray"
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)


    def draw_board(self):
        self.canvas.delete("highlight")
        self.canvas.delete("piece")
        for row in range(8):
            for col in range(8):
                x1, y1 = col * 80, row * 80
                x2, y2 = x1 + 80, y1 + 80
                color = "lemon chiffon" if (row + col) % 2 == 0 else "sienna4"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def on_tile_click(self, event):
        if self.current_player == PlayerColor.WHITE:
            col, row = event.x // 80, event.y // 80
            clicked_position = (row, col)
            clicked_piece = self.board.get_piece(clicked_position)

            if not self.selected_piece:
                if clicked_piece and clicked_piece.color == self.current_player:
                    self.selected_piece = clicked_piece
                    self.highlight_square(row, col, "blue")
            else:
                if clicked_piece and clicked_piece.color == self.selected_piece.color:
                    # Deselect the previously selected piece and select the new piece
                    self.remove_square_highlight(self.selected_piece.position[0], self.selected_piece.position[1])
                    self.selected_piece = clicked_piece
                    self.highlight_square(row, col, "blue")
                else:
                    valid_move = self.board.move_piece(self.selected_piece, clicked_position)
                    if valid_move:
                        self.remove_square_highlight(self.selected_piece.position[0], self.selected_piece.position[1])
                        self.selected_piece = None
                        self.refresh_board()
                        self.switch_player()

                        if self.current_player == PlayerColor.BLACK:
                            threading.Thread(target=self.play_black_move).start()
                    else:
                        # Invalid move
                        self.highlight_square(row, col, "red")

    def play_black_move(self):
        print("getting black move...")
        best_piece, best_move = get_best_move(self.board, PlayerColor.BLACK, max_depth=5, max_time=7)
        print(f"best move: {best_piece}, {best_move}")
        if best_move:
            self.board.move_piece(best_piece, best_move)
            self.window.after(0, self.refresh_board_and_switch_player)
        print(f"board score: {self.board.evaluation_function()}")

    def refresh_board_and_switch_player(self):
        self.refresh_board()
        self.switch_player()

    def place_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece:
                    if piece.color == PlayerColor.WHITE:
                        piece_image = self.white_pieces[piece.__class__.__name__]
                    else:
                        piece_image = self.black_pieces[piece.__class__.__name__]
                    self.canvas.create_image(
                        col * 80 + 40,
                        row * 80 + 40,
                        image=piece_image,
                        tags=("piece", f"{row},{col}"),
                    )

    def run(self):
        self.window.mainloop()



if __name__ == "__main__":
    chess_board = ChessBoard()
    gui = ChessGUI(chess_board)
    gui.run()
