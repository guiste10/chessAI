from Pieces import Pieces, piece_to_descriptor, value_to_piece, black_enemy_pieces, white_enemy_pieces, value_to_piece_short, promotion_color_to_value
from PieceAlive import PieceAlive
from move.MoveUtils import uci_move_to_move
from move.Move import Move, EnPassant, Castle, Capture, Promotion



class Board:

    def __init__(self, board):
        self.board = board

        self.is_blacks_enemy = lambda piece_int: piece_int in black_enemy_pieces
        self.is_whites_enemy = lambda piece_int: piece_int in white_enemy_pieces

        # castling rights
        self.white_castled = False
        self.black_castled = False
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_king_rook_moved = False
        self.black_king_rook_moved = False
        self.white_queen_rook_moved = False
        self.black_queen_rook_moved = False

        # king position
        self.white_king_position = (9, 6)
        self.black_king_position = (2, 6)

    def __str__(self):
        board_str = ""
        for row in range(2, 10):
            for col in range(2, 10):
                board_str += value_to_piece[self.board[row][col]] + " "
            board_str += "\n"
        return board_str

    def init_pieces(self):
        white_pieces, black_pieces = [], []
        for row in range(2, 10):
            for col in range(2, 10):
                if self.board[row][col] != Pieces.OO:
                    piece_alive = PieceAlive(row, col)
                    if self.board[row][col] > Pieces.OO:
                        white_pieces.append(piece_alive)
                    else:
                        black_pieces.append(piece_alive)
        return white_pieces, black_pieces

    def get_color_moves(self, pieces, color, enemy_uci_move): # enemy_uci_move done before calling this method
        is_enemy, is_friendly = (self.is_whites_enemy, self.is_blacks_enemy) if color else (
            self.is_blacks_enemy, self.is_whites_enemy)
        alive_pieces, pseudo_moves = [], []
        for piece in pieces:
            if is_friendly(self.board[piece.row][piece.col]):  # check if was not killed during previous round
                alive_pieces.append(piece)
                self.add_piece_moves(piece, is_enemy, pseudo_moves)
        # todo check en passant possible + add en passant moves (if any) to pseudo_moves
        self.add_en_passant(enemy_uci_move, pseudo_moves)
        moves = pseudo_moves  # todo filter out moves that when applied, leave king attacked
        return moves, alive_pieces

    def add_piece_moves(self, alive_piece, is_enemy, moves):
        piece_int = self.board[alive_piece.row][alive_piece.col]
        piece = value_to_piece[piece_int]
        (is_white, piece_description) = piece_to_descriptor[piece]
        method_name = 'add_' + piece_description + '_moves'
        return getattr(self, method_name)(alive_piece, is_white, is_enemy, moves)

    def add_pawn_moves(self, pawn, is_white, is_enemy, moves):
        (row, col, is_pinned) = (pawn.row, pawn.col, pawn.is_pinned)
        # for color: next row, row after next row, start row, promoted row
        target_row = [row - 1, row - 2, 8, 2, row + 1, row + 2, 3, 9]
        idx = 0 if is_white else 4
        if row == target_row[idx + 2] and self.board[target_row[idx]][col] == Pieces.OO and \
                self.board[target_row[idx + 1]][col] == Pieces.OO:
            moves.append(Move(row, col, target_row[idx + 1], col))
        if target_row[idx] == target_row[idx + 3]:  # promotion on next row
            self.add_pawn_promotion_moves(row, col, target_row[idx], is_enemy, is_white, moves)
        else:
            if self.board[target_row[idx]][col] == Pieces.OO:
                moves.append(Move(row, col, target_row[idx], col))
            if is_enemy(self.board[target_row[idx]][col - 1]):
                to_piece = self.board[target_row[idx]][col - 1]
                moves.append(Capture(row, col, target_row[idx], col - 1, to_piece))
            if is_enemy(self.board[target_row[idx]][col + 1]):
                to_piece = self.board[target_row[idx]][col + 1]
                moves.append(Capture(row, col, target_row[idx], col + 1, to_piece))

    def add_pawn_promotion_moves(self, row, col, promotion_row, is_enemy, is_white, moves):
        piece_val_queen = promotion_color_to_value[('q', is_white)]  # only consider queen promotions for speed reasons
        if self.board[promotion_row][col] == Pieces.OO:
            moves.append(Promotion(row, col, promotion_row, col,  self.board[row][col], piece_val_queen))
        if is_enemy(self.board[promotion_row][col - 1]):
            to_piece = self.board[promotion_row][col - 1]
            moves.append(Promotion(row, col, promotion_row, col - 1, self.board[row][col], piece_val_queen, to_piece))
        if is_enemy(self.board[promotion_row][col + 1]):
            to_piece = self.board[promotion_row][col + 1]
            moves.append(Promotion(row, col, promotion_row, col + 1, self.board[row][col], piece_val_queen, to_piece))

    def add_en_passant(self, enemy_uci_move_performed, moves):
        (col_1, row_1, col_2, row_2) = uci_move_to_move(enemy_uci_move_performed)
        enemy_piece_moved = self.board[row_2][col_2]
        if abs(row_1 - row_2) == 2 and value_to_piece_short[enemy_piece_moved] == 'p':
            if self.board[row_2][col_2 - 1] == - enemy_piece_moved:
                moves.append(EnPassant(row_2, col_2 - 1, (row_1 + row_2) / 2, col_2))
            if self.board[row_2][col_2 + 1] == - enemy_piece_moved:
                moves.append(EnPassant(row_2, col_2 + 1, (row_1 + row_2) / 2, col_2))

    def add_queen_moves(self, queen, is_white, is_enemy, moves):
        self.add_rook_moves(queen, is_white, is_enemy, moves)
        self.add_bishop_moves(queen, is_white, is_enemy, moves)

    def add_rook_moves(self, rook, _is_white, is_enemy, moves):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.add_directed_moves(rook, directions, is_enemy, moves)

    def add_bishop_moves(self, bishop, _is_white, is_enemy, moves):
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        self.add_directed_moves(bishop, directions, is_enemy, moves)

    def add_directed_moves(self, piece, directions, is_enemy, moves):
        row, col = piece.row, piece.col
        for direction in directions:
            to_row, to_col = row + direction[0], col + direction[1]
            while self.board[to_row][to_col] == Pieces.OO:
                moves.append(Move(row, col, to_row, to_col))
                to_row, to_col = to_row + direction[0], to_col + direction[1]
            if is_enemy(self.board[to_row][to_col]):
                moves.append(Capture(row, col, to_row, to_col, self.board[to_row][to_col]))

    def add_knight_moves(self, knight, _is_white, _is_enemy, moves):
        row, col = knight.row, knight.col
        to_squares = [(row - 1, col + 2), (row + 1, col + 2), (row + 2, col + 1), (row + 2, col - 1),
                      (row + 1, col - 2), (row - 1, col - 2), (row - 2, col - 1), (row - 2, col + 1)]
        self.add_square_moves(_is_enemy, col, moves, row, to_squares)

    def add_king_moves(self, king, _is_white, _is_enemy, moves):
        row, col = king.row, king.col
        to_squares = [(row + 1, col - 1), (row + 1, col), (row + 1, col + 1), (row, col - 1), (row, col + 1),
                      (row - 1, col - 1), (row - 1, col), (row - 1, col + 1)]
        self.add_square_moves(_is_enemy, col, moves, row, to_squares)
        # todo: castling if white_castled == false

    def add_square_moves(self, _is_enemy, col, moves, row, to_squares):
        for to_square in to_squares:
            to_square_val = self.board[to_square[0]][to_square[1]]
            if to_square_val == Pieces.OO:
                moves.append(Move(row, col, to_square[0], to_square[1]))
            elif _is_enemy(to_square_val):
                moves.append(Capture(row, col, to_square[0], to_square[1], to_square_val))

    def is_king_attacked(self):
        return False

    def is_square_attacked(self):
        return False
