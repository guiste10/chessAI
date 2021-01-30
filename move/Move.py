from Pieces import Pieces, king_start_pos
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
        board.board[self.row_2][self.col_2] = board.board[self.row_1][self.col_1]
        board.board[self.row_1][self.col_1] = Pieces.OO

    def undo_move(self, board):
        board.board[self.row_1][self.col_1] = board.board[self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = Pieces.OO


class Capture(Move):
    def __init__(self, row_1, col_1, row_2, col_2, to_piece):
        super().__init__(row_1, col_1, row_2, col_2)
        self.to_piece = to_piece

    def undo_move(self, board):
        board.board[self.row_1][self.col_1] = board.board[self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = self.to_piece


class EnPassant(Move):
    def __init__(self, row_1, col_1, row_2, col_2):
        super().__init__(row_1, col_1, row_2, col_2)

    def do_move(self, board):
        board.board[self.row_2][self.col_2] = board.board[self.row_1][self.col_1]
        board.board[self.row_1][self.col_2] = Pieces.OO
        board.board[self.row_1][self.col_1] = Pieces.OO

    def undo_move(self, board):
        board.board[self.row_1][self.col_1] = board.board[self.row_2][self.col_2]
        board.board[self.row_1][self.col_2] = -board.board[self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = Pieces.OO


class Promotion(Move):
    def __init__(self, row_1, col_1, row_2, col_2, original_piece, promotion_piece, to_piece=Pieces.OO):
        super().__init__(row_1, col_1, row_2, col_2)
        self.original_piece = original_piece
        self.promotion_piece = promotion_piece
        self.to_piece = to_piece  # promotion while capturing

    def do_move(self, board):
        board.board[self.row_2][self.col_2] = self.promotion_piece
        board.board[self.row_1][self.col_1] = Pieces.OO

    def undo_move(self, board):
        board.board[self.row_1][self.col_1] = self.original_piece
        board.board[self.row_2][self.col_2] = self.to_piece


class StateChangeMove(Move):
    def __init__(self, row_1, col_1, row_2, col_2, game_state_old, game_state_new):
        super().__init__(row_1, col_1, row_2, col_2)
        self.game_state_old = game_state_old
        self.game_state_new = game_state_new

    def do_move(self, board):
        super().do_move(board)
        board.game_state = self.game_state_new

    def undo_move(self, board):
        super().undo_move(board)
        board.game_state = self.game_state_old


class StateChangeCapture(Capture):
    def __init__(self, row_1, col_1, row_2, col_2, to_piece, game_state_old, game_state_new):
        super().__init__(row_1, col_1, row_2, col_2, to_piece)
        self.game_state_old = game_state_old
        self.game_state_new = game_state_new

    def do_move(self, board):
        super().do_move(board)
        board.game_state = self.game_state_new

    def undo_move(self, board):
        super().undo_move(board)
        board.game_state = self.game_state_old


class Castle:
    def __init__(self, kingside, is_white):
        self.kingside = kingside
        self.is_white = is_white

    def do_move(self, board):
        (row, col) = king_start_pos[self.is_white]
        if self.kingside:
            castle_kingside(board, row, col)
            board.game_state.king_pos[self.is_white] = (row, col + 2)
        else:
            castle_queenside(board, row, col)
            board.game_state.king_pos[self.is_white] = (row, col - 2)
        board.game_state.castled[self.is_white] = True

    def undo_move(self, board):
        (row, col) = king_start_pos[self.is_white]
        if self.kingside:
            board.board[row][col] = board.board[row][col + 2]
            board.board[row][col + 2] = Pieces.OO
            board.board[row][col + 3] = board.board[row][col + 1]
            board.board[row][col + 1] = Pieces.OO
        else:
            board.board[row][col] = board.board[row][col - 2]
            board.board[row][col - 2] = Pieces.OO
            board.board[row][col - 4] = board.board[row][col - 1]
            board.board[row][col - 1] = Pieces.OO
        board.game_state.king_pos[self.is_white] = king_start_pos[self.is_white]
        board.game_state.castled[self.is_white] = False
