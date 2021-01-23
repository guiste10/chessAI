from Pieces import Pieces
from move.MoveUtils import col_to_uci_dict, row_to_uci_dict, castle_kingside, castle_queenside


class Move:
    def __init__(self, row_1, col_1, row_2, col_2):
        self.row_1 = row_1
        self.col_1 = col_1
        self.row_2 = row_2
        self.col_2 = col_2

    def __str__(self):
        return col_to_uci_dict[self.col_1] + row_to_uci_dict[self.row_1] + col_to_uci_dict[self.col_2] + \
               row_to_uci_dict[self.row_2]

    def do_move(self, board):
        board[self.row_2][self.col_2] = board[self.row_1][self.col_1]
        board[self.row_1][self.col_1] = Pieces.OO

    def undo_move(self, board):
        board[self.row_1][self.col_1] = board[self.row_2][self.col_2]
        board[self.row_2][self.col_2] = Pieces.OO


class EnPassant(Move):
    def __init__(self, row_1, col_1, row_2, col_2):
        super().__init__(row_1, col_1, row_2, col_2)

    def do_move(self, board):
        board[self.row_2][self.col_2] = board[self.row_1][self.col_1]
        board[self.row_1][self.col_2] = Pieces.OO
        board[self.row_1][self.col_1] = Pieces.OO

    def undo_move(self, board):
        board[self.row_1][self.col_1] = board[self.row_2][self.col_2]
        board[self.row_1][self.col_2] = -board[self.row_2][self.col_2]
        board[self.row_2][self.col_2] = Pieces.OO


class Castle:
    def __init__(self, row_1, col_1, kingside):
        self.row_1 = row_1
        self.col_1 = col_1
        self.kingside = kingside

    def do_move(self, board):
        if self.kingside:
            castle_kingside(self.board, self.row_1, self.col_1)
        else:
            castle_queenside(self.board, self.row_1, self.col_1)

    def undo_move(self, board):
        if self.kingside:
            board[self.row_1][self.col_1] = board[self.row_1][self.col_1 + 2]
            board[self.row_1][self.col_1 + 2] = Pieces.OO
            board[self.row_1][self.col_1 + 3] = board[self.row_1][self.col_1 + 1]
            board[self.row_1][self.col_1 + 1] = Pieces.OO
        else:
            board[self.row_1][self.col_1] = board[self.row_1][self.col_1 - 2]
            board[self.row_1][self.col_1 - 2] = Pieces.OO
            board[self.row_1][self.col_1 - 4] = board[self.row_1][self.col_1 - 1]
            board[self.row_1][self.col_1 - 1] = Pieces.OO


class Capture(Move):
    def __init__(self, row_1, col_1, row_2, col_2, to_piece):
        super().__init__(row_1, col_1, row_2, col_2)
        self.to_piece = to_piece

    def undo_move(self, board):
        board[self.row_1][self.col_1] = board[self.row_2][self.col_2]
        board[self.row_2][self.col_2] = self.to_piece


class Promotion(Move):
    def __init__(self, row_1, col_1, row_2, col_2, original_piece, promotion_piece, to_piece=Pieces.OO):
        super().__init__(row_1, col_1, row_2, col_2)
        self.original_piece = original_piece
        self.promotion_piece = promotion_piece
        self.to_piece = to_piece  # promotion while capturing

    def do_move(self, board):
        board[self.row_2][self.col_2] = self.promotion_piece
        board[self.row_1][self.col_1] = Pieces.OO

    def undo_move(self, board):
        board[self.row_1][self.col_1] = self.original_piece
        board[self.row_2][self.col_2] = self.to_piece
