from Pieces import Pieces, piece_to_descriptor, value_to_piece, value_to_piece_short, promotion_color_to_value, rook_directions, bishop_directions, queen_directions, is_enemy, get_knight_squares, \
    get_king_squares, rook_start_pos
from move.MoveUtils import uci_move_to_move
from move.Move import Move, EnPassant, Castle, KingMove, Promotion, MoveCastlingRightsChange


def get_direction(diff, divider):
    return diff[0] // divider, diff[1] // divider


def add_to_captures(enemy_move_row, enemy_move_col, move, moves, to_row, to_col):
    if to_row == enemy_move_row and to_col == enemy_move_col:
        moves["recap"].append(move)
    else:
        moves["capture"].append(move)


class Board:

    def __init__(self, board):
        self.board = board
        self.king_pos = {False: (2, 6), True: (9, 6)}
        self.cannot_castle = {True: False, False: False}
        self.rook_moved = {(2, 2): False, (2, 9): False, (9, 2): False, (9, 9): False}

    def __str__(self):
        board_str = ""
        for row in range(2, 10):
            for col in range(2, 10):
                board_str += value_to_piece[self.board[row][col]] + " "
            board_str += "\n"
        return board_str

    def get_color_moves(self, is_white, enemy_uci_move):  # enemy_uci_move done before calling this method
        enemy_move = uci_move_to_move(enemy_uci_move)
        pseudo_moves_dict = {"move": [], "move2": [], "capture": [], "recap": [], "en passant": [], "promotion": [], "castle": []}
        for row in range(2, 10):
            for col in range(2, 10):
                if is_enemy[not is_white](self.board[row][col]):
                    self.add_piece_moves((row, col), pseudo_moves_dict, enemy_move[3], enemy_move[2])
        self.add_en_passant(enemy_move, pseudo_moves_dict)
        pseudo_moves_sorted_list = pseudo_moves_dict["en passant"] + pseudo_moves_dict["recap"] + pseudo_moves_dict["promotion"] + pseudo_moves_dict["castle"] + pseudo_moves_dict["move"] + pseudo_moves_dict["capture"] + pseudo_moves_dict["move2"]
        return self.filter_invalid_moves(is_white, pseudo_moves_sorted_list)

    def filter_invalid_moves(self, is_white, pseudo_moves):
        is_king_attacked = self.is_king_attacked(is_white)
        (king_row, king_col) = self.king_pos[is_white]
        valid_moves = []
        for move in pseudo_moves:
            if move.__class__.__name__ == 'Castle':
                valid_moves.append(move)
            elif value_to_piece_short[self.board[move.row_1][move.col_1]] == 'k':
                if not self.is_square_attacked(move.row_2, move.col_2, is_white):
                    valid_moves.append(move)
            elif self.keep_invalid_non_king_move(move, is_king_attacked, is_white, king_row, king_col):
                valid_moves.append(move)
        return valid_moves

    def keep_invalid_non_king_move(self, move, is_king_attacked, is_white, king_row, king_col):  # for non king moves only
        return self.keep_invalid_move_king_attacked(is_white, king_col, king_row, move) if is_king_attacked else self.keep_invalid_move_king_safe(is_white, king_col, king_row, move)

    def keep_invalid_move_king_attacked(self, is_white, king_col, king_row, move):
        row_2, col_2 = move.row_2, move.col_2
        if abs(king_row - row_2) == abs(king_col - col_2):  # destination in in bishop direction of the king, can it protect the king?
            diff = (king_row - row_2, king_col - col_2)
            direction = get_direction(diff, abs(diff[0]))
            if not self.can_protect(is_white, direction, row_2, col_2, 'b'):
                return False
        elif king_row == row_2 or king_col == col_2:  # destination is in rook direction of the king, can it protect the king?
            diff = (king_row - row_2, king_col - col_2)
            direction = get_direction(diff, max(abs(diff[0]), abs(diff[1])))
            if not self.can_protect(is_white, direction, row_2, col_2, 'r'):
                return False
        else:
            return False
        return not self.is_king_attacked_after_move(is_white, move)  # see if king still attacked after move that can protect king

    def can_protect(self, is_white, direction, row_2, col_2, target):
        while self.board[row_2][col_2] == Pieces.OO:
            row_2, col_2 = row_2 + direction[0], col_2 + direction[1]
        return is_enemy[is_white](self.board[row_2][col_2]) and value_to_piece_short[self.board[row_2][col_2]] in ('q', target)

    def keep_invalid_move_king_safe(self, is_white, king_col, king_row, move):
        row_1, col_1 = move.row_1, move.col_1
        if abs(king_row - row_1) != abs(king_col - col_1) and king_row != row_1 and king_col != col_1:  # if no chance to leave king exposed
            return True
        row_2, col_2 = move.row_2, move.col_2
        diff_2 = (king_row - row_2, king_col - col_2)
        if abs(king_row - row_2) == abs(king_col - col_2):  # bishop direction
            direction_2 = get_direction(diff_2, abs(diff_2[0]))
        elif king_row == row_2 or king_col == col_2:  # rook direction
            direction_2 = get_direction(diff_2, max(abs(diff_2[0]), abs(diff_2[1])))
        else:
            return not self.is_king_attacked_after_move(is_white, move)
        diff_1 = (king_row - row_1, king_col - col_1)
        if abs(king_row - row_1) == abs(king_col - col_1):  # bishop direction
            direction_1 = get_direction(diff_1, abs(diff_1[0]))
        else:  # rook direction
            direction_1 = get_direction(diff_1, max(abs(diff_1[0]), abs(diff_1[1])))
        if direction_1 == direction_2:  # if direction stays the same, king will stay unattacked (even if piece was pinned)
            return True
        return not self.is_king_attacked_after_move(is_white, move)

    def is_king_attacked_after_move(self, is_white, move):
        move.do_move(self)
        is_king_still_attacked = self.is_king_attacked(is_white)
        move.undo_move(self)
        return is_king_still_attacked

    def add_piece_moves(self, piece_val, moves, enemy_move_row, enemy_move_col):
        piece_int = self.board[piece_val[0]][piece_val[1]]
        piece = value_to_piece[piece_int]
        (is_white, piece_description) = piece_to_descriptor[piece]
        method_name = 'add_' + piece_description + '_moves'
        return getattr(self, method_name)(piece_val, is_white, moves, enemy_move_row, enemy_move_col)

    def add_pawn_moves(self, pawn, is_white, moves, _enemy_move_row, _enemy_move_col):
        (row, col) = (pawn[0], pawn[1])
        # for color: next row, row after next row, start row, promoted row
        target_row = (row - 1, row - 2, 8, 2, row + 1, row + 2, 3, 9)
        idx = 0 if is_white else 4
        if row == target_row[idx + 2] and self.board[target_row[idx]][col] == Pieces.OO and self.board[target_row[idx + 1]][col] == Pieces.OO:
            moves["move"].append(Move(row, col, target_row[idx + 1], col))
        if target_row[idx] == target_row[idx + 3]:  # promotion on next row
            self.add_pawn_promotion_moves(row, col, target_row[idx], is_white, moves)
        else:
            if self.board[target_row[idx]][col] == Pieces.OO:
                moves["move"].append(Move(row, col, target_row[idx], col))
            if is_enemy[is_white](self.board[target_row[idx]][col - 1]):
                to_piece = self.board[target_row[idx]][col - 1]
                moves["recap"].append(Move(row, col, target_row[idx], col - 1, to_piece))
            if is_enemy[is_white](self.board[target_row[idx]][col + 1]):
                to_piece = self.board[target_row[idx]][col + 1]
                moves["recap"].append(Move(row, col, target_row[idx], col + 1, to_piece))

    def add_pawn_promotion_moves(self, row, col, promotion_row, is_white, moves, _enemy_move_row, _enemy_move_col):
        piece_val_queen = promotion_color_to_value[('q', is_white)]
        piece_val_knight = promotion_color_to_value[('n', is_white)]
        piece_val_rook = promotion_color_to_value[('r', is_white)]
        piece_val_bishop = promotion_color_to_value[('b', is_white)]
        if self.board[promotion_row][col] == Pieces.OO:
            moves["promotion"].append(Promotion(row, col, promotion_row, col, self.board[row][col], piece_val_queen))
            moves["promotion"].append(Promotion(row, col, promotion_row, col, self.board[row][col], piece_val_knight))
            moves["promotion"].append(Promotion(row, col, promotion_row, col, self.board[row][col], piece_val_rook))
            moves["promotion"].append(Promotion(row, col, promotion_row, col, self.board[row][col], piece_val_bishop))

        if is_enemy[is_white](self.board[promotion_row][col - 1]):
            to_piece = self.board[promotion_row][col - 1]
            moves["promotion"].append(Promotion(row, col, promotion_row, col - 1, self.board[row][col], piece_val_queen, to_piece))
            moves["promotion"].append(Promotion(row, col, promotion_row, col - 1, self.board[row][col], piece_val_knight, to_piece))
            moves["promotion"].append(Promotion(row, col, promotion_row, col - 1, self.board[row][col], piece_val_rook, to_piece))
            moves["promotion"].append(Promotion(row, col, promotion_row, col - 1, self.board[row][col], piece_val_bishop, to_piece))

        if is_enemy[is_white](self.board[promotion_row][col + 1]):
            to_piece = self.board[promotion_row][col + 1]
            moves["promotion"].append(Promotion(row, col, promotion_row, col + 1, self.board[row][col], piece_val_queen, to_piece))
            moves["promotion"].append(Promotion(row, col, promotion_row, col + 1, self.board[row][col], piece_val_knight, to_piece))
            moves["promotion"].append(Promotion(row, col, promotion_row, col + 1, self.board[row][col], piece_val_rook, to_piece))
            moves["promotion"].append(Promotion(row, col, promotion_row, col + 1, self.board[row][col], piece_val_bishop, to_piece))

    def add_en_passant(self, enemy_move_performed, moves):
        (col_1, row_1, col_2, row_2) = enemy_move_performed
        enemy_piece_moved = self.board[row_2][col_2]
        if abs(row_1 - row_2) == 2 and value_to_piece_short[enemy_piece_moved] == 'p':
            if self.board[row_2][col_2 - 1] == - enemy_piece_moved:
                moves["en passant"].append(EnPassant(row_2, col_2 - 1, (row_1 + row_2) // 2, col_2))
            if self.board[row_2][col_2 + 1] == - enemy_piece_moved:
                moves["en passant"].append(EnPassant(row_2, col_2 + 1, (row_1 + row_2) // 2, col_2))

    def add_queen_moves(self, queen, is_white, moves, enemy_move_row, enemy_move_col):
        self.add_directed_moves(queen, queen_directions, is_white, moves, enemy_move_row, enemy_move_col)

    def add_rook_moves(self, rook, is_white, moves, enemy_move_row, enemy_move_col):
        self.add_directed_rook_moves(rook, is_white, moves, enemy_move_row, enemy_move_col)

    def add_directed_rook_moves(self, rook, is_white, moves, enemy_move_row, enemy_move_col):
        row, col = rook[0], rook[1]
        if self.cannot_castle[is_white] or (row, col) not in rook_start_pos[is_white] or self.rook_moved[(row, col)]:
            self.add_directed_moves(rook, rook_directions, is_white, moves, enemy_move_row, enemy_move_col)
        else:  # castling rights are affected
            for direction in rook_directions:
                to_row, to_col = row + direction[0], col + direction[1]
                while self.board[to_row][to_col] == Pieces.OO:
                    moves["move2"].append(MoveCastlingRightsChange(row, col, to_row, to_col, is_white))
                    to_row, to_col = to_row + direction[0], to_col + direction[1]
                if is_enemy[is_white](self.board[to_row][to_col]):
                    move = MoveCastlingRightsChange(row, col, to_row, to_col, is_white, self.board[to_row][to_col])
                    add_to_captures(enemy_move_row, enemy_move_col, move, moves, to_row, to_col)

    def add_bishop_moves(self, bishop, is_white, moves, enemy_move_row, enemy_move_col):
        self.add_directed_moves(bishop, bishop_directions, is_white, moves, enemy_move_row, enemy_move_col)

    def add_directed_moves(self, piece, directions, is_white, moves, enemy_move_row, enemy_move_col):
        row, col = piece[0], piece[1]
        for direction in directions:
            to_row, to_col = row + direction[0], col + direction[1]
            while self.board[to_row][to_col] == Pieces.OO:
                moves["move"].append(Move(row, col, to_row, to_col))
                to_row, to_col = to_row + direction[0], to_col + direction[1]
            if is_enemy[is_white](self.board[to_row][to_col]):
                move = Move(row, col, to_row, to_col, self.board[to_row][to_col])
                add_to_captures(enemy_move_row, enemy_move_col, move, moves, to_row, to_col)

    def add_knight_moves(self, knight, is_white, moves, enemy_move_row, enemy_move_col):
        self.add_square_moves(knight[0], knight[1], get_knight_squares(knight[0], knight[1]), is_white, moves, enemy_move_row, enemy_move_col)

    def add_square_moves(self, row, col, to_squares, is_white, moves, enemy_move_row, enemy_move_col):
        for to_square in to_squares:
            to_square_val = self.board[to_square[0]][to_square[1]]
            move = Move(row, col, to_square[0], to_square[1], to_square_val)
            if to_square_val == Pieces.OO:
                moves["move"].append(move)
            elif is_enemy[is_white](to_square_val):
                add_to_captures(enemy_move_col, enemy_move_row, move, moves, to_square[0], to_square[1])

    def add_king_moves(self, king, is_white, moves, enemy_move_row, enemy_move_col):
        row, col = king[0], king[1]
        self.add_king_square_moves(row, col, get_king_squares(row, col), is_white, moves, enemy_move_row, enemy_move_col)
        if not self.cannot_castle[is_white] and not self.is_square_attacked(row, col, is_white):
            self.add_castling_moves(col, is_white, moves, row)

    def add_king_square_moves(self, row, col, to_squares, is_white, moves, enemy_move_row, enemy_move_col):
        if self.cannot_castle[is_white]:
            for to_square in to_squares:
                to_square_val = self.board[to_square[0]][to_square[1]]
                if to_square_val == Pieces.OO:
                    moves["move2"].append(KingMove(row, col, to_square[0], to_square[1], is_white))
                elif is_enemy[is_white](to_square_val):
                    move = KingMove(row, col, to_square[0], to_square[1], is_white, to_square_val)
                    add_to_captures(enemy_move_col, enemy_move_row, move, moves, to_square[0], to_square[1])
        else:
            for to_square in to_squares:
                to_square_val = self.board[to_square[0]][to_square[1]]
                if to_square_val == Pieces.OO:
                    moves["move"].append(MoveCastlingRightsChange(row, col, to_square[0], to_square[1], is_white))
                elif is_enemy[is_white](to_square_val):
                    moves["capture"].append(MoveCastlingRightsChange(row, col, to_square[0], to_square[1], is_white, to_square_val))

    def add_castling_moves(self, col, is_white, moves, row):
        if not self.rook_moved[(row, col + 3)] and self.board[row][col + 3] == promotion_color_to_value[('r', is_white)] and self.safe_to_castle_kingside(row, col, is_white):
            moves["castle"].append(Castle(True, is_white))
        if not self.rook_moved[(row, col - 4)] and self.board[row][col - 4] == promotion_color_to_value[('r', is_white)] and self.safe_to_castle_queenside(row, col, is_white):
            moves["castle"].append(Castle(False, is_white))

    def safe_to_castle_kingside(self, row, col, is_white):
        return self.board[row][col + 1] == Pieces.OO and self.board[row][col + 2] == Pieces.OO and \
               not self.is_square_attacked(row, col + 1, is_white) and not self.is_square_attacked(row, col + 2, is_white)

    def safe_to_castle_queenside(self, row, col, is_white):
        return self.board[row][col - 1] == Pieces.OO and self.board[row][col - 2] == Pieces.OO and self.board[row][col - 3] == Pieces.OO and \
               not self.is_square_attacked(row, col - 1, is_white) and not self.is_square_attacked(row, col - 2, is_white)

    def is_king_attacked(self, is_white):
        (king_row, king_col) = self.king_pos[is_white]
        return self.is_square_attacked(king_row, king_col, is_white)

    def is_square_attacked(self, row, col, is_white):
        for direction in bishop_directions:
            to_col, to_row = self.advance_when_empty(row, col, direction)
            if self.board[to_row][to_col] == promotion_color_to_value[('b', not is_white)] or self.board[to_row][to_col] == promotion_color_to_value[('q', not is_white)]:
                return True

        for direction in rook_directions:
            to_col, to_row = self.advance_when_empty(row, col, direction)
            if self.board[to_row][to_col] == promotion_color_to_value[('r', not is_white)] or self.board[to_row][to_col] == promotion_color_to_value[('q', not is_white)]:
                return True

        enemy_knight_squares = get_knight_squares(row, col)
        for square in enemy_knight_squares:
            if self.board[square[0]][square[1]] == promotion_color_to_value[('n', not is_white)]:
                return True

        enemy_king_squares = get_king_squares(row, col)
        for square in enemy_king_squares:
            if self.board[square[0]][square[1]] == promotion_color_to_value[('k', not is_white)]:
                return True

        enemy_pawn_squares = [(row - 1, col - 1), (row - 1, col + 1)] if is_white else [(row + 1, col - 1), (row + 1, col + 1)]
        for square in enemy_pawn_squares:
            if self.board[square[0]][square[1]] == promotion_color_to_value[('p', not is_white)]:
                return True

        return False

    def advance_when_empty(self, row, col, direction):
        to_row, to_col = row + direction[0], col + direction[1]
        while self.board[to_row][to_col] == Pieces.OO:
            to_row, to_col = to_row + direction[0], to_col + direction[1]
        return to_col, to_row
