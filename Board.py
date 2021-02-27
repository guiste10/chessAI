from Pieces import value_to_descriptor, value_to_piece_img, value_to_piece_short, promotion_color_to_value, rook_directions, bishop_directions, queen_directions, is_enemy, \
    get_knight_squares, get_king_squares, get_attacking_enemy_pawn_squares, rook_start_pos, possible_promotions, king_rook_start_col, queen_rook_start_col, start_row
from Zobrist import init_hash
from move import Moves
from move.MoveUtils import uci_move_to_move
from move.Moves import Move, EnPassant, Castle, Promotion
import copy


def get_direction(diff, divider):
    return diff[0] // divider, diff[1] // divider


def add_to_captures(enemy_move_row, enemy_move_col, move, moves, to_row, to_col):
    if to_row == enemy_move_row and to_col == enemy_move_col:
        moves["recap"].append(move)
    else:
        moves["capture"].append(move)


class Board:

    def __init__(self, board):
        self.board = copy.deepcopy(board)
        self.king_pos = {False: (2, 6), True: (9, 6)}
        self.cannot_castle = {True: False, False: False}
        self.rook_moved = {(2, 2): False, (2, 9): False, (9, 2): False, (9, 9): False}
        self.current_hash = init_hash(self.board)

    def __str__(self):
        board_str = "\t"
        for letter in 'abcdefgh':
            board_str += letter + '\t'
        board_str += '\n'
        for row in range(2, 10):
            board_str += str(8 - (row - 2)) + '\t'
            for col in range(2, 10):
                board_str += value_to_piece_img[self.board[row][col]] + '\t'
            board_str += str(8 - (row - 2)) + '\n'
        board_str += '\t'
        for letter in 'abcdefgh':
            board_str += letter + '\t'
        return board_str + '\n'

    def get_color_moves(self, is_white, enemy_uci_move):
        enemy_move = uci_move_to_move(enemy_uci_move)
        pseudo_moves_dict = {"move": [], "move2": [], "capture": [], "recap": [], "en passant": [], "promotion": [], "castle": []}
        for row in range(2, 10):
            for col in range(2, 10):
                if is_enemy[not is_white](self.board[row][col]):
                    self.add_piece_moves(row, col, pseudo_moves_dict, enemy_move[3], enemy_move[2], is_white)
        self.add_en_passant(enemy_move, pseudo_moves_dict, is_white)
        pseudo_moves_sorted_list = [*pseudo_moves_dict["en passant"], *pseudo_moves_dict["recap"], *pseudo_moves_dict["capture"], *pseudo_moves_dict["promotion"], *pseudo_moves_dict["castle"],
                                    *pseudo_moves_dict["move"], *pseudo_moves_dict["move2"]]
        return self.filter_invalid_moves(is_white, pseudo_moves_sorted_list)

    def add_piece_moves(self, row, col, moves, enemy_move_row, enemy_move_col, is_white):
        piece_int = self.board[row][col]
        piece_description = value_to_descriptor[piece_int]
        method_name = 'add_' + piece_description + '_moves'
        return getattr(self, method_name)(row, col, is_white, moves, enemy_move_row, enemy_move_col)

    def add_pawn_moves(self, row, col, is_white, moves, enemy_move_row, enemy_move_col):
        target_row = (row - 1, row - 2, 8, 2) if is_white else (row + 1, row + 2, 3, 9)  # next row, row after next row, start row, promoted row
        if row == target_row[2] and self.board[target_row[0]][col] == 0 and self.board[target_row[1]][col] == 0:
            moves["move"].append(Move(row, col, target_row[1], col, is_white))
        if target_row[0] == target_row[3]:  # promotion on next row
            self.add_pawn_promotion_moves(row, col, target_row[0], is_white, moves)
        else:
            if self.board[target_row[0]][col] == 0:
                moves["move"].append(Move(row, col, target_row[0], col, is_white))
            for capture_col in (col - 1, col + 1):
                if is_enemy[is_white](self.board[target_row[0]][capture_col]):
                    to_piece = self.board[target_row[0]][capture_col]
                    move = Move(row, col, target_row[0], capture_col, is_white, to_piece)
                    add_to_captures(enemy_move_row, enemy_move_col, move, moves, target_row[0], capture_col)

    def add_pawn_promotion_moves(self, row, col, promotion_row, is_white, moves):
        if self.board[promotion_row][col] == 0:
            for piece_val in possible_promotions[is_white]:
                moves["promotion"].append(Promotion(row, col, promotion_row, col, piece_val, is_white))
        for promotion_col in (col - 1, col + 1):
            if is_enemy[is_white](self.board[promotion_row][promotion_col]):
                to_piece = self.board[promotion_row][promotion_col]
                for piece_val in possible_promotions[is_white]:
                    moves["promotion"].append(Promotion(row, col, promotion_row, promotion_col, piece_val, is_white, to_piece))

    def add_en_passant(self, enemy_move_performed, moves, is_white):
        (col_1, row_1, col_2, row_2) = enemy_move_performed
        enemy_piece_moved = self.board[row_2][col_2]
        if abs(row_1 - row_2) == 2 and value_to_piece_short[enemy_piece_moved] == 'p':
            for en_passant_col in (col_2 - 1, col_2 + 1):
                if self.board[row_2][en_passant_col] == - enemy_piece_moved:
                    moves["en passant"].append(EnPassant(row_2, en_passant_col, (row_1 + row_2) // 2, col_2, is_white))

    def add_queen_moves(self, row, col, is_white, moves, enemy_move_row, enemy_move_col):
        self.add_directed_moves(row, col, queen_directions, is_white, moves, enemy_move_row, enemy_move_col, getattr(Moves, 'Move'), 'move')

    def add_rook_moves(self, row, col, is_white, moves, enemy_move_row, enemy_move_col):
        move_class_name, move_storage_name = ('Move', 'move') if (self.cannot_castle[is_white] or (row, col) not in rook_start_pos[is_white] or self.rook_moved[(row, col)]) else (
            'MoveCastlingRightsChange', 'move2')
        self.add_directed_moves(row, col, rook_directions, is_white, moves, enemy_move_row, enemy_move_col, getattr(Moves, move_class_name), move_storage_name)

    def add_bishop_moves(self, row, col, is_white, moves, enemy_move_row, enemy_move_col):
        self.add_directed_moves(row, col, bishop_directions, is_white, moves, enemy_move_row, enemy_move_col, getattr(Moves, 'Move'), 'move')

    def add_directed_moves(self, row, col, directions, is_white, moves, enemy_move_row, enemy_move_col, move_class, move_storage_name):
        for direction in directions:
            to_row, to_col = row + direction[0], col + direction[1]
            while self.board[to_row][to_col] == 0:
                moves[move_storage_name].append(Move(row, col, to_row, to_col, is_white, 0))
                to_row, to_col = to_row + direction[0], to_col + direction[1]
            if is_enemy[is_white](self.board[to_row][to_col]):
                move = move_class(row, col, to_row, to_col, is_white, self.board[to_row][to_col])
                add_to_captures(enemy_move_row, enemy_move_col, move, moves, to_row, to_col)

    def add_knight_moves(self, row, col, is_white, moves, enemy_move_row, enemy_move_col):
        self.add_square_moves(row, col, get_knight_squares(row, col), is_white, moves, enemy_move_row, enemy_move_col, getattr(Moves, 'Move'), 'move')

    def add_square_moves(self, row, col, to_squares, is_white, moves, enemy_move_row, enemy_move_col, move_class, move_storage_name):
        for to_square in to_squares:
            to_square_val = self.board[to_square[0]][to_square[1]]
            if to_square_val == 0:
                moves[move_storage_name].append(move_class(row, col, to_square[0], to_square[1], is_white, to_square_val))
            elif is_enemy[is_white](to_square_val):
                move = move_class(row, col, to_square[0], to_square[1], is_white, to_square_val)
                add_to_captures(enemy_move_col, enemy_move_row, move, moves, to_square[0], to_square[1])

    def add_king_moves(self, row, col, is_white, moves, enemy_move_row, enemy_move_col):
        (move_class_name, move_storage_name) = ('KingMove', 'move2') if self.cannot_castle[is_white] or self.both_rooks_moved(is_white) else ('MoveCastlingRightsChange', 'move')
        self.add_square_moves(row, col, get_king_squares(row, col), is_white, moves, enemy_move_row, enemy_move_col, getattr(Moves, move_class_name), move_storage_name)
        if not self.cannot_castle[is_white] and not self.is_square_attacked(row, col, is_white):
            self.add_castling_moves(row, col, is_white, moves)

    def both_rooks_moved(self, is_white):
        for start_pos in rook_start_pos[is_white]:
            if not self.rook_moved[start_pos]:
                return False
        return True

    def add_castling_moves(self, row, col, is_white, moves):
        if not self.rook_moved[(start_row[is_white], king_rook_start_col)] and self.board[start_row[is_white]][king_rook_start_col] == promotion_color_to_value[('r', is_white)] and self.safe_to_castle_kingside(row, col, is_white):
            moves["castle"].append(Castle(True, is_white))
        if not self.rook_moved[(start_row[is_white], queen_rook_start_col)] and self.board[start_row[is_white]][queen_rook_start_col] == promotion_color_to_value[('r', is_white)] and self.safe_to_castle_queenside(row, col, is_white):
            moves["castle"].append(Castle(False, is_white))

    def safe_to_castle_kingside(self, row, col, is_white):
        return self.board[row][col + 1] == 0 and self.board[row][col + 2] == 0 and not self.is_square_attacked(row, col + 1, is_white) and not self.is_square_attacked(row, col + 2, is_white)

    def safe_to_castle_queenside(self, row, col, is_white):
        return self.board[row][col - 1] == 0 and self.board[row][col - 2] == 0 and self.board[row][col - 3] == 0 and \
               not self.is_square_attacked(row, col - 1, is_white) and not self.is_square_attacked(row, col - 2, is_white)

    def is_king_attacked(self, is_white):
        (king_row, king_col) = self.king_pos[is_white]
        return self.is_square_attacked(king_row, king_col, is_white)

    def filter_invalid_moves(self, is_white, pseudo_moves):
        is_king_attacked = self.is_king_attacked(is_white)
        valid_moves = []
        for move in pseudo_moves:
            if move.__class__.__name__ == 'Castle':
                valid_moves.append(move)
            elif value_to_piece_short[self.board[move.row_1][move.col_1]] == 'k':
                if not self.is_king_attacked_after_move(is_white, move):
                    valid_moves.append(move)
            elif self.non_king_move_leaves_king_safe(move, is_king_attacked, is_white, self.king_pos[is_white][0], self.king_pos[is_white][1]):
                valid_moves.append(move)
        return valid_moves

    def non_king_move_leaves_king_safe(self, move, is_king_attacked, is_white, king_row, king_col):  # for non king moves only
        return self.keep_move_king_attacked(is_white, king_col, king_row, move) if is_king_attacked else self.keep_move_king_safe(is_white, king_col, king_row, move)

    def keep_move_king_attacked(self, is_white, king_col, king_row, move):
        row_2, col_2 = move.row_2, move.col_2
        if abs(king_row - row_2) == abs(king_col - col_2):  # destination in in bishop direction of the king
            return self.protects_king_bishop_direction(move, is_white, king_row, king_col, row_2, col_2)
        elif king_row == row_2 or king_col == col_2:  # destination is in rook direction of the king
            return self.protects_king_rook_direction(move, is_white, king_row, king_col, row_2, col_2)
        elif (row_2, col_2) in get_knight_squares(king_row, king_col):  # destination is in knight direction of the king
            return self.protects_king_from_knight(move, is_white, row_2, col_2)
        return False  # move cannot protect the checked king

    def protects_king_bishop_direction(self, move, is_white, king_row, king_col, row_2, col_2):
        diff = (row_2 - king_row, col_2 - king_col)
        direction = get_direction(diff, abs(diff[0]))
        target_values = [promotion_color_to_value[(target, not is_white)] for target in ('q', 'b')]
        if not (self.protect_king_from_pawn(row_2, col_2, king_row, king_col, is_white) or self.protect_king_from_target(direction, row_2, col_2, target_values)):
            return False
        return not self.is_king_attacked_after_move(is_white, move)  # see if king still attacked after move that can protect king

    def protect_king_from_pawn(self, row_2, col_2, king_row, king_col, is_white):
        return (row_2, col_2) in get_attacking_enemy_pawn_squares(king_row, king_col, is_white) and promotion_color_to_value[('p', not is_white)] == self.board[row_2][col_2]

    def protects_king_rook_direction(self, move, is_white, king_row, king_col, row_2, col_2):
        diff = (king_row - row_2, king_col - col_2)
        direction = get_direction(diff, max(abs(diff[0]), abs(diff[1])))
        target_values = [promotion_color_to_value[(target, not is_white)] for target in ('q', 'r')]
        if not self.protect_king_from_target(direction, row_2, col_2, target_values):
            return False
        return not self.is_king_attacked_after_move(is_white, move)  # see if king still attacked after move that can protect king

    def protect_king_from_target(self, direction, row_2, col_2, target_values):
        while self.board[row_2][col_2] == 0:
            row_2, col_2 = row_2 + direction[0], col_2 + direction[1]
        return self.board[row_2][col_2] in target_values

    def protects_king_from_knight(self, move, is_white, row_2, col_2):
        if self.board[row_2][col_2] != promotion_color_to_value[('n', not is_white)]:
            return False
        return not self.is_king_attacked_after_move(is_white, move)  # see if king still attacked after move that can protect king

    def keep_move_king_safe(self, is_white, king_col, king_row, move):
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

    def is_square_attacked(self, row, col, is_white):
        for (directions, piece) in ((bishop_directions, 'b'), (rook_directions, 'r')):
            for direction in directions:
                to_col, to_row = self.advance_when_empty(row, col, direction)
                if self.board[to_row][to_col] == promotion_color_to_value[(piece, not is_white)] or self.board[to_row][to_col] == promotion_color_to_value[('q', not is_white)]:
                    return True
        for (squares, piece) in ((get_knight_squares(row, col), 'n'), (get_king_squares(row, col), 'k')):
            for square in squares:
                if self.board[square[0]][square[1]] == promotion_color_to_value[(piece, not is_white)]:
                    return True
        for square in get_attacking_enemy_pawn_squares(row, col, is_white):
            if self.board[square[0]][square[1]] == promotion_color_to_value[('p', not is_white)]:
                return True
        return False

    def advance_when_empty(self, row, col, direction):
        to_row, to_col = row + direction[0], col + direction[1]
        while self.board[to_row][to_col] == 0:
            to_row, to_col = to_row + direction[0], to_col + direction[1]
        return to_col, to_row
