from Pieces import Pieces
from move.MoveUtils import col_to_uci_dict, row_to_uci_dict, castle_kingside, castle_queenside


class Move:
    def __init__(self, row_1, col_1, row_2, col_2, game_state_old, game_state_new):
        self.row_1 = row_1
        self.col_1 = col_1
        self.row_2 = row_2
        self.col_2 = col_2
        self.game_state_old = game_state_old
        self.game_state_new = game_state_new

    def __str__(self):
        return col_to_uci_dict[self.col_1] + row_to_uci_dict[self.row_1] + col_to_uci_dict[self.col_2] + \
               row_to_uci_dict[self.row_2]

    def do_move(self, board):
        board.board[self.row_2][self.col_2] = board.board[self.row_1][self.col_1]
        board.board[self.row_1][self.col_1] = Pieces.OO
        board.game_state = self.game_state_new

    def undo_move(self, board):
        board.board[self.row_1][self.col_1] = board.board[self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = Pieces.OO
        board.game_state = self.game_state_old


class EnPassant(Move):
    def __init__(self, row_1, col_1, row_2, col_2, game_state_old, game_state_new):
        super().__init__(row_1, col_1, row_2, col_2, game_state_old, game_state_new)

    def do_move(self, board):
        board.board[self.row_2][self.col_2] = board.board[self.row_1][self.col_1]
        board.board[self.row_1][self.col_2] = Pieces.OO
        board.board[self.row_1][self.col_1] = Pieces.OO
        board.game_state = self.game_state_new

    def undo_move(self, board):
        board.board[self.row_1][self.col_1] = board.board[self.row_2][self.col_2]
        board.board[self.row_1][self.col_2] = -board.board[self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = Pieces.OO
        board.game_state = self.game_state_old


class Castle:
    def __init__(self, row_1, col_1, kingside, game_state_old, game_state_new):
        self.row_1 = row_1
        self.col_1 = col_1
        self.kingside = kingside
        self.game_state_old = game_state_old
        self.game_state_new = game_state_new

    def do_move(self, board):
        if self.kingside:
            castle_kingside(board, self.row_1, self.col_1)
        else:
            castle_queenside(board, self.row_1, self.col_1)
        board.game_state = self.game_state_new

    def undo_move(self, board):
        if self.kingside:
            board.board[self.row_1][self.col_1] = board.board[self.row_1][self.col_1 + 2]
            board.board[self.row_1][self.col_1 + 2] = Pieces.OO
            board.board[self.row_1][self.col_1 + 3] = board.board[self.row_1][self.col_1 + 1]
            board.board[self.row_1][self.col_1 + 1] = Pieces.OO
        else:
            board.board[self.row_1][self.col_1] = board.board[self.row_1][self.col_1 - 2]
            board.board[self.row_1][self.col_1 - 2] = Pieces.OO
            board.board[self.row_1][self.col_1 - 4] = board.board[self.row_1][self.col_1 - 1]
            board.board[self.row_1][self.col_1 - 1] = Pieces.OO
        board.game_state = self.game_state_old


class Capture(Move):
    def __init__(self, row_1, col_1, row_2, col_2, to_piece, game_state_old, game_state_new):
        super().__init__(row_1, col_1, row_2, col_2, game_state_old, game_state_new)
        self.to_piece = to_piece

    def undo_move(self, board):
        board.board[self.row_1][self.col_1] = board.board[self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = self.to_piece
        board.game_state = self.game_state_old


class Promotion(Move):
    def __init__(self, row_1, col_1, row_2, col_2, original_piece, promotion_piece, game_state_old, game_state_new, to_piece=Pieces.OO):
        super().__init__(row_1, col_1, row_2, col_2, game_state_old, game_state_new)
        self.original_piece = original_piece
        self.promotion_piece = promotion_piece
        self.to_piece = to_piece  # promotion while capturing

    def do_move(self, board):
        board.board[self.row_2][self.col_2] = self.promotion_piece
        board.board[self.row_1][self.col_1] = Pieces.OO
        board.game_state = self.game_state_new

    def undo_move(self, board):
        board.board[self.row_1][self.col_1] = self.original_piece
        board.board[self.row_2][self.col_2] = self.to_piece
        board.game_state = self.game_state_old
