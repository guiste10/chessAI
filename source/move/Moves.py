from board.Pieces import Pieces, king_start_pos, value_to_piece_short, promotion_color_to_value, king_start_col, king_rook_start_col
from move import Zobrist as Zob
from ai.Evaluation import piece_value_to_placement_score, piece_value_to_piece_score


def add_to_history(history, position_hash):
    if position_hash in history:
        history[position_hash] += 1
    else:
        history[position_hash] = 1


def remove_from_history(history, position_hash):
    if history[position_hash] > 1:
        history[position_hash] -= 1
    else:
        history.pop(position_hash)


class Move(object):
    def __init__(self, row_1, col_1, row_2, col_2, is_white, to_piece=Pieces.OO):
        self.row_1 = row_1
        self.col_1 = col_1
        self.row_2 = row_2
        self.col_2 = col_2
        self.is_white = is_white
        self.to_piece = to_piece

    def do_move(self, board):
        self.update_hash(board, board.board[self.row_1][self.col_1])
        add_to_history(board.history, board.current_hash)
        piece_val = board.board[self.row_1][self.col_1]
        board.current_eval += piece_value_to_placement_score[piece_val][self.row_2][self.col_2] - piece_value_to_placement_score[piece_val][self.row_1][self.col_1]
        if self.to_piece != Pieces.OO:
            enemy_piece_val = board.board[self.row_2][self.col_2]
            board.current_eval -= piece_value_to_piece_score[enemy_piece_val] + piece_value_to_placement_score[enemy_piece_val][self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = board.board[self.row_1][self.col_1]
        board.board[self.row_1][self.col_1] = Pieces.OO

    def undo_move(self, board):
        remove_from_history(board.history, board.current_hash)
        board.board[self.row_1][self.col_1] = board.board[self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = self.to_piece

    def update_hash(self, board, piece_val):
        board.current_hash ^= Zob.black_hash ^ Zob.piece_hash_for_squares[piece_val][self.row_1][self.col_1] ^ Zob.piece_hash_for_squares[piece_val][self.row_2][self.col_2]
        if self.to_piece != Pieces.OO:
            board.current_hash ^= Zob.piece_hash_for_squares[self.to_piece][self.row_2][self.col_2]
        elif value_to_piece_short[piece_val] == 'p' and abs(self.row_1 - self.row_2) == 2:
            board.current_hash ^= Zob.file_hash[self.col_1]


class KingMove(Move):  # castling rights unchanged (castling was already not possible)
    def __init__(self, row_1, col_1, row_2, col_2, is_white, to_piece=Pieces.OO):
        super(KingMove, self).__init__(row_1, col_1, row_2, col_2, is_white, to_piece)
        self.is_white = is_white

    def do_move(self, board):
        board.king_pos[self.is_white] = (self.row_2, self.col_2)
        super(KingMove, self).do_move(board)

    def undo_move(self, board):
        board.king_pos[self.is_white] = (self.row_1, self.col_1)
        super(KingMove, self).undo_move(board)


class MoveCastlingRightsChange(Move):  # change castling rights related to a rook or king's capture/move
    def __init__(self, row_1, col_1, row_2, col_2, is_white, to_piece=Pieces.OO):
        super(MoveCastlingRightsChange, self).__init__(row_1, col_1, row_2, col_2, is_white, to_piece)
        self.is_white = is_white

    def do_move(self, board):
        if value_to_piece_short[board.board[self.row_1][self.col_1]] == 'k':
            board.king_pos[self.is_white] = (self.row_2, self.col_2)
            board.cannot_castle[self.is_white] = True
        else:  # rook
            board.rook_moved[(self.row_1, self.col_1)] = True
        super(MoveCastlingRightsChange, self).do_move(board)

    def undo_move(self, board):
        if value_to_piece_short[board.board[self.row_2][self.col_2]] == 'k':
            board.king_pos[self.is_white] = (self.row_1, self.col_1)
            board.cannot_castle[self.is_white] = False
        else:  # rook
            board.rook_moved[(self.row_1, self.col_1)] = False
        super(MoveCastlingRightsChange, self).undo_move(board)

    def update_hash(self, board, piece_val):
        if self.col_1 == king_start_col:
            board.current_hash ^= Zob.castling_rights_hash[self.is_white][True]
            board.current_hash ^= Zob.castling_rights_hash[self.is_white][False]
        elif self.col_1 == king_rook_start_col:
            board.current_hash ^= Zob.castling_rights_hash[self.is_white][True]
        else:
            board.current_hash ^= Zob.castling_rights_hash[self.is_white][False]
        super(MoveCastlingRightsChange, self).update_hash(board, piece_val)


class Castle:
    def __init__(self, kingside, is_white):
        self.kingside = kingside
        self.is_white = is_white

    def do_move(self, board):
        self.update_hash(board, king_start_pos[self.is_white][0], king_start_pos[self.is_white][1])
        add_to_history(board.history, board.current_hash)
        (row, col) = king_start_pos[self.is_white]
        king_val = board.board[row][col]
        if self.kingside:
            rook_val = board.board[row][col + 3]
            board.current_eval += piece_value_to_placement_score[king_val][row][col + 2] - piece_value_to_placement_score[king_val][row][col] + piece_value_to_placement_score[rook_val][row][col + 1] - \
                                  piece_value_to_placement_score[rook_val][row][col + 3]
            board.board[row][col + 2] = board.board[row][col]
            board.board[row][col] = Pieces.OO
            board.board[row][col + 1] = board.board[row][col + 3]
            board.board[row][col + 3] = Pieces.OO
            board.king_pos[self.is_white] = (row, col + 2)
        else:
            rook_val = board.board[row][col - 4]
            board.current_eval += piece_value_to_placement_score[king_val][row][col - 2] - piece_value_to_placement_score[king_val][row][col] - + piece_value_to_placement_score[rook_val][row][
                col - 1] - piece_value_to_placement_score[rook_val][row][col - 4]
            board.board[row][col - 2] = board.board[row][col]
            board.board[row][col] = Pieces.OO
            board.board[row][col - 1] = board.board[row][col - 4]
            board.board[row][col - 4] = Pieces.OO
            board.king_pos[self.is_white] = (row, col - 2)
        board.cannot_castle[self.is_white] = True

    def undo_move(self, board):
        remove_from_history(board.history, board.current_hash)
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

    def update_hash(self, board, king_row, king_col):
        (king_val, rook_val) = (promotion_color_to_value[('k', self.is_white)], promotion_color_to_value[('r', self.is_white)])
        board.current_hash ^= Zob.black_hash ^ Zob.piece_hash_for_squares[king_val][king_row][king_col]
        if self.kingside:
            board.current_hash ^= Zob.piece_hash_for_squares[king_val][king_row][king_col + 2] ^ Zob.piece_hash_for_squares[rook_val][king_row][king_col + 3] ^ \
                                  Zob.piece_hash_for_squares[rook_val][king_row][king_col + 1] ^ Zob.castling_rights_hash[self.is_white][True]
        else:
            board.current_hash ^= Zob.piece_hash_for_squares[king_val][king_row][king_col - 2] ^ Zob.piece_hash_for_squares[rook_val][king_row][king_col - 4] ^ \
                                  Zob.piece_hash_for_squares[rook_val][king_row][king_col - 1] ^ Zob.castling_rights_hash[self.is_white][False]


class EnPassant(Move):
    def __init__(self, row_1, col_1, row_2, col_2, is_white):
        super(EnPassant, self).__init__(row_1, col_1, row_2, col_2, is_white)

    def do_move(self, board):
        self.update_hash(board, promotion_color_to_value[('p', self.is_white)])
        add_to_history(board.history, board.current_hash)
        piece_val = board.board[self.row_1][self.col_1]
        board.current_eval += piece_value_to_placement_score[piece_val][self.row_2][self.col_2] - piece_value_to_placement_score[piece_val][self.row_1][self.col_1] - piece_value_to_piece_score[
            -piece_val] - piece_value_to_placement_score[-piece_val][self.row_1][self.col_2]
        board.board[self.row_2][self.col_2] = board.board[self.row_1][self.col_1]
        board.board[self.row_1][self.col_2] = Pieces.OO  # kill enemy pawn
        board.board[self.row_1][self.col_1] = Pieces.OO

    def undo_move(self, board):
        remove_from_history(board.history, board.current_hash)
        board.board[self.row_1][self.col_1] = board.board[self.row_2][self.col_2]
        board.board[self.row_1][self.col_2] = -board.board[self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = Pieces.OO

    def update_hash(self, board, piece_val):
        board.current_hash ^= Zob.black_hash ^ Zob.piece_hash_for_squares[piece_val][self.row_1][self.col_1] ^ Zob.piece_hash_for_squares[piece_val][self.row_2][self.col_2] ^ \
                              Zob.piece_hash_for_squares[-piece_val][self.row_1][self.col_2]


class Promotion(Move):
    def __init__(self, row_1, col_1, row_2, col_2, is_white, to_piece=Pieces.OO):
        super(Promotion, self).__init__(row_1, col_1, row_2, col_2, is_white)
        self.to_piece = to_piece  # promotion while capturing
        self.promotion_piece = promotion_color_to_value[('q', self.is_white)]  # only consider queen promotions for efficiency

    def do_move(self, board):
        self.update_hash(board, board.board[self.row_1][self.col_1])
        add_to_history(board.history, board.current_hash)
        piece_val = board.board[self.row_1][self.col_1]
        board.current_eval += piece_value_to_piece_score[self.promotion_piece] + piece_value_to_placement_score[self.promotion_piece][self.row_2][self.col_2] - piece_value_to_piece_score[piece_val] - \
                              piece_value_to_placement_score[piece_val][self.row_1][self.col_1]
        if self.to_piece != Pieces.OO:
            enemy_piece_val = board.board[self.row_2][self.col_2]
            board.current_eval -= piece_value_to_piece_score[enemy_piece_val] + piece_value_to_placement_score[enemy_piece_val][self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = self.promotion_piece
        board.board[self.row_1][self.col_1] = Pieces.OO

    def undo_move(self, board):
        remove_from_history(board.history, board.current_hash)
        original_pawn_val = promotion_color_to_value[('p', self.is_white)]
        board.board[self.row_1][self.col_1] = original_pawn_val
        board.board[self.row_2][self.col_2] = self.to_piece

    def update_hash(self, board, original_pawn_val):
        board.current_hash ^= Zob.black_hash ^ Zob.piece_hash_for_squares[original_pawn_val][self.row_1][self.col_1] ^ Zob.piece_hash_for_squares[self.promotion_piece][self.row_2][
            self.col_2]
        if self.to_piece != Pieces.OO:
            board.current_hash ^= Zob.piece_hash_for_squares[self.to_piece][self.row_2][self.col_2]


class NullMove:
    def __init__(self, is_white):
        self.is_white = is_white

    def do_move(self, board):
        board.current_hash ^= Zob.black_hash

    def undo_move(self, board):
        board.current_hash ^= Zob.black_hash
