from board.Pieces import Pieces, king_start_pos, value_to_piece_short, promotion_color_to_value, king_start_col, king_rook_start_col
from move.MoveUtils import castle_kingside, castle_queenside
from move import Zobrist as Zob
from ai.Evaluation import piece_value_to_placement_score, piece_value_to_piece_score


class Move:
    def __init__(self, row_1, col_1, row_2, col_2, is_white, to_piece=Pieces.OO):
        self.row_1 = row_1
        self.col_1 = col_1
        self.row_2 = row_2
        self.col_2 = col_2
        self.is_white = is_white
        self.to_piece = to_piece

    def do_move(self, board, current_eval):
        self.update_hash(board, board.board[self.row_1][self.col_1])
        piece_val = board.board[self.row_1][self.col_1]
        new_eval = current_eval - piece_value_to_placement_score[piece_val][self.row_1][self.col_1] \
                   + piece_value_to_placement_score[piece_val][self.row_2][self.col_2]
        if self.to_piece != Pieces.OO:
            enemy_piece_val = board.board[self.row_2][self.col_2]
            new_eval -= piece_value_to_piece_score[enemy_piece_val] + piece_value_to_placement_score[enemy_piece_val][self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = board.board[self.row_1][self.col_1]
        board.board[self.row_1][self.col_1] = Pieces.OO
        return new_eval

    def undo_move(self, board):
        board.board[self.row_1][self.col_1] = board.board[self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = self.to_piece

    def update_hash(self, board, piece_val):
        board.current_hash ^= Zob.side_hash[self.is_white] ^ Zob.piece_hash_for_squares[piece_val][self.row_1][self.col_1] ^ Zob.piece_hash_for_squares[piece_val][self.row_2][self.col_2]
        if self.to_piece != Pieces.OO:
            board.current_hash ^= Zob.piece_hash_for_squares[self.to_piece][self.row_2][self.col_2]
        elif value_to_piece_short[piece_val] == 'p' and abs(self.row_1 - self.row_2) == 2:
            board.current_hash ^= Zob.file_hash[self.col_1]



class KingMove(Move):  # castling rights unchanged (castling was already not possible)
    def __init__(self, row_1, col_1, row_2, col_2, is_white, to_piece=Pieces.OO):
        super().__init__(row_1, col_1, row_2, col_2, is_white, to_piece)
        self.is_white = is_white

    def do_move(self, board, current_eval):
        board.king_pos[self.is_white] = (self.row_2, self.col_2)
        return super().do_move(board, current_eval)

    def undo_move(self, board):
        board.king_pos[self.is_white] = (self.row_1, self.col_1)
        super().undo_move(board)


class MoveCastlingRightsChange(Move):  # change castling rights related to a rook or king's capture/move
    def __init__(self, row_1, col_1, row_2, col_2, is_white, to_piece=Pieces.OO):
        super().__init__(row_1, col_1, row_2, col_2, is_white, to_piece)
        self.is_white = is_white

    def do_move(self, board, current_eval):
        if value_to_piece_short[board.board[self.row_1][self.col_1]] == 'k':
            board.king_pos[self.is_white] = (self.row_2, self.col_2)
            board.cannot_castle[self.is_white] = True
        else:  # rook
            board.rook_moved[(self.row_1, self.col_1)] = True
        return super().do_move(board, current_eval)

    def undo_move(self, board):
        if value_to_piece_short[board.board[self.row_2][self.col_2]] == 'k':
            board.king_pos[self.is_white] = (self.row_1, self.col_1)
            board.cannot_castle[self.is_white] = False
        else:  # rook
            board.rook_moved[(self.row_1, self.col_1)] = False
        super().undo_move(board)

    def update_hash(self, board, piece_val):
        if self.col_1 == king_start_col:
            board.current_hash ^= Zob.castling_rights_hash[self.is_white][True]
            board.current_hash ^= Zob.castling_rights_hash[self.is_white][False]
        elif self.col_1 == king_rook_start_col:
            board.current_hash ^= Zob.castling_rights_hash[self.is_white][True]
        else:
            board.current_hash ^= Zob.castling_rights_hash[self.is_white][False]
        super().update_hash(board, piece_val)


class Castle:
    def __init__(self, kingside, is_white):
        self.kingside = kingside
        self.is_white = is_white

    def do_move(self, board, current_eval):
        self.update_hash(board, king_start_pos[self.is_white][0], king_start_pos[self.is_white][1])
        (row, col) = king_start_pos[self.is_white]
        king_val = board.board[row][col]
        if self.kingside:
            rook_val = board.board[row][col + 3]
            new_eval = current_eval - piece_value_to_placement_score[king_val][row][col] + piece_value_to_placement_score[king_val][row][col + 2] - \
                       piece_value_to_placement_score[rook_val][row][col + 3] + piece_value_to_placement_score[rook_val][row][col + 1]
            castle_kingside(board.board, row, col)
            board.king_pos[self.is_white] = (row, col + 2)
        else:
            rook_val = board.board[row][col - 4]
            new_eval = current_eval - piece_value_to_placement_score[king_val][row][col] + piece_value_to_placement_score[king_val][row][col - 2] - \
                       piece_value_to_placement_score[rook_val][row][col - 4] + piece_value_to_placement_score[rook_val][row][col - 1]
            castle_queenside(board.board, row, col)
            board.king_pos[self.is_white] = (row, col - 2)
        board.cannot_castle[self.is_white] = True
        return new_eval

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

    def update_hash(self, board, king_row, king_col):
        (king_val, rook_val) = (promotion_color_to_value[('k', self.is_white)], promotion_color_to_value[('r', self.is_white)])
        board.current_hash ^= Zob.side_hash[self.is_white] ^ Zob.piece_hash_for_squares[king_val][king_row][king_col]
        if self.kingside:
            board.current_hash ^= Zob.piece_hash_for_squares[king_val][king_row][king_col + 2] ^ Zob.piece_hash_for_squares[rook_val][king_row][king_col + 3] ^ \
                                  Zob.piece_hash_for_squares[rook_val][king_row][king_col + 1] ^ Zob.castling_rights_hash[self.is_white][True]
        else:
            board.current_hash ^= Zob.piece_hash_for_squares[king_val][king_row][king_col - 2] ^ Zob.piece_hash_for_squares[rook_val][king_row][king_col - 4] ^ \
                                  Zob.piece_hash_for_squares[rook_val][king_row][king_col - 1] ^ Zob.castling_rights_hash[self.is_white][False]


class EnPassant(Move):
    def __init__(self, row_1, col_1, row_2, col_2, is_white):
        super().__init__(row_1, col_1, row_2, col_2, is_white)

    def do_move(self, board, current_eval):
        self.update_hash(board, promotion_color_to_value[('p', self.is_white)])
        piece_val = board.board[self.row_1][self.col_1]
        new_eval = current_eval - piece_value_to_placement_score[piece_val][self.row_1][self.col_1] \
                   + piece_value_to_placement_score[piece_val][self.row_2][self.col_2] - (piece_value_to_piece_score[-piece_val] + piece_value_to_placement_score[-piece_val][self.row_1][self.col_2])
        board.board[self.row_2][self.col_2] = board.board[self.row_1][self.col_1]
        board.board[self.row_1][self.col_2] = Pieces.OO  # kill enemy pawn
        board.board[self.row_1][self.col_1] = Pieces.OO
        return new_eval

    def undo_move(self, board):
        board.board[self.row_1][self.col_1] = board.board[self.row_2][self.col_2]
        board.board[self.row_1][self.col_2] = -board.board[self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = Pieces.OO

    def update_hash(self, board, piece_val):
        board.current_hash ^= Zob.side_hash[self.is_white] ^ Zob.piece_hash_for_squares[piece_val][self.row_1][self.col_1] ^ Zob.piece_hash_for_squares[piece_val][self.row_2][self.col_2] \
                              ^ Zob.piece_hash_for_squares[-piece_val][self.row_1][self.col_2]


class Promotion(Move):
    def __init__(self, row_1, col_1, row_2, col_2, promotion_piece, is_white, to_piece=Pieces.OO):
        super().__init__(row_1, col_1, row_2, col_2, is_white)
        self.promotion_piece = promotion_piece
        self.to_piece = to_piece  # promotion while capturing

    def do_move(self, board, current_eval):
        self.update_hash(board, board.board[self.row_1][self.col_1])
        piece_val = board.board[self.row_1][self.col_1]
        new_eval = current_eval - piece_value_to_piece_score[piece_val] - piece_value_to_placement_score[piece_val][self.row_1][self.col_1] \
                   + piece_value_to_piece_score[self.promotion_piece] + piece_value_to_placement_score[self.promotion_piece][self.row_2][self.col_2]
        if self.to_piece != Pieces.OO:
            enemy_piece_val = board.board[self.row_2][self.col_2]
            new_eval -= piece_value_to_piece_score[enemy_piece_val] + piece_value_to_placement_score[enemy_piece_val][self.row_2][self.col_2]
        board.board[self.row_2][self.col_2] = self.promotion_piece
        board.board[self.row_1][self.col_1] = Pieces.OO
        return new_eval

    def undo_move(self, board):
        original_pawn_val = promotion_color_to_value[('p', self.is_white)]
        board.board[self.row_1][self.col_1] = original_pawn_val
        board.board[self.row_2][self.col_2] = self.to_piece

    def update_hash(self, board, original_pawn_val):
        board.current_hash ^= Zob.side_hash[self.is_white] ^ Zob.piece_hash_for_squares[original_pawn_val][self.row_1][self.col_1] ^ Zob.piece_hash_for_squares[self.promotion_piece][self.row_2][self.col_2]
        if self.to_piece != Pieces.OO:
            board.current_hash ^= Zob.piece_hash_for_squares[self.to_piece][self.row_2][self.col_2]
