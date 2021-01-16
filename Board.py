from Pieces import Pieces
from PieceAlive import PieceAlive
from Move import Move


class Board:

    def __init__(self):
        self.board = [
            [Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX,
             Pieces.XX, Pieces.XX, Pieces.XX],
            [Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX,
             Pieces.XX, Pieces.XX, Pieces.XX],
            [Pieces.XX, Pieces.XX, Pieces.BR, Pieces.BN, Pieces.BB, Pieces.BQ, Pieces.BK, Pieces.BB, Pieces.BN,
             Pieces.BR, Pieces.XX, Pieces.XX],
            [Pieces.XX, Pieces.XX, Pieces.BP, Pieces.BP, Pieces.BP, Pieces.BP, Pieces.BP, Pieces.BP, Pieces.BP,
             Pieces.BP, Pieces.XX, Pieces.XX],
            [Pieces.XX, Pieces.XX, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO,
             Pieces.OO, Pieces.XX, Pieces.XX],
            [Pieces.XX, Pieces.XX, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO,
             Pieces.OO, Pieces.XX, Pieces.XX],
            [Pieces.XX, Pieces.XX, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO,
             Pieces.OO, Pieces.XX, Pieces.XX],
            [Pieces.XX, Pieces.XX, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO, Pieces.OO,
             Pieces.OO, Pieces.XX, Pieces.XX],
            [Pieces.XX, Pieces.XX, Pieces.WP, Pieces.WP, Pieces.WP, Pieces.WP, Pieces.WP, Pieces.WP, Pieces.WP,
             Pieces.WP, Pieces.XX, Pieces.XX],
            [Pieces.XX, Pieces.XX, Pieces.WR, Pieces.WN, Pieces.WB, Pieces.WQ, Pieces.WK, Pieces.WB, Pieces.WN,
             Pieces.WR, Pieces.XX, Pieces.XX],
            [Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX,
             Pieces.XX, Pieces.XX, Pieces.XX],
            [Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX, Pieces.XX,
             Pieces.XX, Pieces.XX, Pieces.XX]]

        self.is_white_piece = lambda piece_int: piece_int > 0
        self.is_black_piece = lambda piece_int: piece_int < 0

        # castling rights
        self.white_castled = False
        self.black_castled = False
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_king_rook_moved = False
        self.black_king_rook_moved = False
        self.white_queen_rook_moved = False
        self.black_queen_rook_moved = False

    def __str__(self):
        board_str = ""
        for row in range(2, 10):
            for col in range(2, 10):
                board_str += Pieces.value_to_piece[self.board[row][col]] + " "
            board_str += "\n"
        return board_str

    def init_pieces(self):
        white_pieces = []
        black_pieces = []
        for row in range(2, 10):
            for col in range(2, 10):
                if self.board[row][col] != Pieces.OO:
                    piece_alive = PieceAlive(row, col)
                    if self.board[row][col] > Pieces.OO:
                        white_pieces.append(piece_alive)
                    else:
                        black_pieces.append(piece_alive)
        return (white_pieces, black_pieces)

    def get_color_moves(self, pieces, color):
        (is_enemy_evaluator, is_friendly_evaluator) = (self.is_black_piece, self.is_white_piece) if color \
            else (self.is_white_piece, self.is_black_piece)
        alive_pieces = []
        moves = []
        for piece in pieces:
            if is_friendly_evaluator(self.board[piece.row][piece.col]):  # check if was just killed
                alive_pieces.append(piece)
                if not piece.is_pinned:  # todo update is_pinned from other color when pinning enemy's piece
                    self.add_piece_moves(piece, moves, is_enemy_evaluator)
        return (moves, alive_pieces)

    def add_piece_moves(self, alive_piece, moves, is_enemy_evaluator):
        piece_int = self.board[alive_piece.row][alive_piece.col]
        piece = Pieces.value_to_piece[piece_int]
        (is_white, piece_description) = Pieces.piece_to_descriptor[piece]
        method_name = 'add_' + piece_description + '_moves'
        return getattr(self, method_name)(alive_piece, is_white, is_enemy_evaluator, moves)

    def add_pawn_moves(self, pawn, is_white, is_enemy_evaluator, moves):  # todo en passant
        (row, col, is_pinned) = (pawn.row, pawn.col, pawn.is_pinned)
        target_row = [row - 1, row - 2, 8, row + 1, row + 2, 3]
        idx = 0 if is_white else 3
        if row == target_row[idx + 2] and self.board[target_row[idx]][col] == Pieces.OO and self.board[target_row[idx + 1]][
            col] == Pieces.OO:
            moves.append(Move(row, col, target_row[idx + 1], col, self.board[target_row[idx + 1]][col]))
        if self.board[target_row[idx]][col] == Pieces.OO and self.board[target_row[idx]][col] == Pieces.OO:
            moves.append(Move(row, col, target_row[idx], col, self.board[target_row[idx]][col]))
        if self.is_in_bounds(target_row[idx], col - 1) and is_enemy_evaluator(self.board[target_row[idx]][col - 1]):
            moves.append(Move(row, col, target_row[idx], col - 1, self.board[target_row[idx]][col - 1]))
        if self.is_in_bounds(target_row[idx], col + 1) and is_enemy_evaluator(self.board[target_row[idx]][col + 1]):
            moves.append(Move(row, col, target_row[idx], col + 1, self.board[target_row[idx]][col + 1]))

    def add_knight_moves(self, knight, _is_white, is_enemy_evaluator, moves):
        row, col = knight.row, knight.col
        to_row = [row-1, row+1, row+2, row+2, row+1, row-1, row-2, row-2]
        to_col = [col+2, col+2, col+1, col-1, col-2, col-2, col-1, col+1]
        for i in range(0, len(to_row)):
            to_square_val = self.board[to_row[i]][to_col[i]]
            if (to_square_val == Pieces.OO or is_enemy_evaluator(to_square_val)) and to_square_val != Pieces.XX:
                moves.append(Move(row, col, to_row[i], to_col[i], to_square_val))

    def add_queen_moves(self, queen, is_white, is_enemy_evaluator, moves):
        self.add_rook_moves(queen, is_white, is_enemy_evaluator, moves)
        self.add_bishop_moves(queen, is_white, is_enemy_evaluator, moves)

    def add_rook_moves(self, rook, _is_white, is_enemy_evaluator, moves):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.add_directed_moves(rook, directions, is_enemy_evaluator, moves)

    def add_bishop_moves(self, bishop, _is_white, is_enemy_evaluator, moves):
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        self.add_directed_moves(bishop, directions, is_enemy_evaluator, moves)

    def add_directed_moves(self, piece, directions, is_enemy_evaluator, moves):
        row, col = piece.row, piece.col
        for direction in directions:
            to_row, to_col = row+direction[0], col+direction[1]
            while(self.board[to_row][to_col] == Pieces.OO):
                moves.append(Move(row, col, to_row, to_col, self.board[to_row][to_col]))
                to_row, to_col = to_row + direction[0], to_col + direction[1]
            if is_enemy_evaluator(self.board[to_row][to_col]):
                moves.append(Move(row, col, to_row, to_col, self.board[to_row][to_col]))

    def add_king_moves(self, king, is_white, is_enemy_evaluator, moves):
        row, col = king.row, king.col
        to_squares = [(row+1, col-1), (row+1, col), (row+1, col+1), (row, col-1), (row, col+1), (row-1, col-1), (row-1, col), (row-1, col+1)]
        for to_square in to_squares:
            to_square_val = self.board[to_square[0]][to_square[1]]
            if to_square_val == Pieces.OO or is_enemy_evaluator(to_square_val):
                moves.append(Move(row, col, to_square[0], to_square[1], to_square_val))
        # todo castle update castling rights + see if square attacked

    def do_move(self, move):  # todo queen pawn
        self.board[move.x2][move.y2] = self.board[move.x1][move.y1]
        self.board[move.x1][move.y1] = Pieces.OO

    def undo_move(self, move):  # todo unqueen pawn
        self.board[move.x1][move.y1] = self.board[move.x2][move.y2]
        self.board[move.x2][move.y2] = move.old_value

    def is_in_bounds(self, row, col):
        return self.board[row][col] != Pieces.XX
