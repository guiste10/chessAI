from Pieces import Pieces, king_start_pos, value_to_piece_short
from move.MoveUtils import castle_kingside, castle_queenside

# move = capture of a piece with value 0 = Pieces.OO


class Move:
    def __init__(self, row_1, col_1, row_2, col_2, to_piece=Pieces.OO):
        self.row_1 = row_1
        self.col_1 = col_1
        self.row_2 = row_2
        self.col_2 = col_2
        self.to_piece = to_piece

    def do_move(self, board):
        board.board[self.row_2][self.col_2] = board.board[self.row_1][self.col_1]
        board.board[self.row_1][self.col_1] = Pieces.OO

    def undo_move(self, board):
        board.board[self.row_1][self.col_1] = board.board[self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = self.to_piece


class KingMove(Move):  # castling rights unchanged (castling was already not possible)
    def __init__(self, row_1, col_1, row_2, col_2, is_white, to_piece=Pieces.OO):
        super().__init__(row_1, col_1, row_2, col_2, to_piece)
        self.is_white = is_white

    def do_move(self, board):
        board.king_pos[self.is_white] = (self.row_2, self.col_2)
        super().do_move(board)

    def undo_move(self, board):
        board.king_pos[self.is_white] = (self.row_1, self.col_1)
        super().undo_move(board)


class MoveCastlingRightsChange(Move):  # change castling rights related to a rook or king's capture/move
    def __init__(self, row_1, col_1, row_2, col_2, is_white, to_piece=Pieces.OO):
        super().__init__(row_1, col_1, row_2, col_2, to_piece)
        self.is_white = is_white

    def do_move(self, board):
        if value_to_piece_short[board.board[self.row_1][self.col_1]] == 'k':
            board.king_pos[self.is_white] = (self.row_2, self.col_2)
            board.cannot_castle[self.is_white] = True
        else:  # rook
            board.rook_moved[(self.row_1, self.col_1)] = True
        super().do_move(board)

    def undo_move(self, board):
        if value_to_piece_short[board.board[self.row_2][self.col_2]] == 'k':
            board.king_pos[self.is_white] = (self.row_2, self.col_2)
            board.cannot_castle[self.is_white] = False
        else:  # rook
            board.rook_moved[(self.row_1, self.col_1)] = False
        super().undo_move(board)


class Castle:
    def __init__(self, kingside, is_white):
        self.kingside = kingside
        self.is_white = is_white

    def do_move(self, board):
        (row, col) = king_start_pos[self.is_white]
        if self.kingside:
            castle_kingside(board.board, row, col)
            board.king_pos[self.is_white] = (row, col + 2)
        else:
            castle_queenside(board.board, row, col)
            board.king_pos[self.is_white] = (row, col - 2)
        board.cannot_castle[self.is_white] = True

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
        board.king_pos[self.is_white] = king_start_pos[self.is_white]
        board.cannot_castle[self.is_white] = False


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