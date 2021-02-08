from Pieces import Pieces, piece_to_descriptor, value_to_piece, value_to_piece_short, promotion_color_to_value, rook_directions, bishop_directions, queen_directions, is_enemy, get_knight_squares, \
    get_king_squares, rook_start_pos
from move.MoveUtils import uci_move_to_move
from move.Move import Move, EnPassant, Castle, Capture, Promotion, MoveStateChange, CaptureStateChange
from BoardState import BoardState
import copy


class Board:

    def __init__(self, board):
        self.board = board
        self.state = BoardState()

    def __str__(self):
        board_str = ""
        for row in range(2, 10):
            for col in range(2, 10):
                board_str += value_to_piece[self.board[row][col]] + " "
            board_str += "\n"
        return board_str

    def get_color_moves(self, is_white, enemy_uci_move):  # enemy_uci_move done before calling this method
        pseudo_moves_dict = {"move": [], "capture": [], "en passant": [], "promotion": [], "castle": []}
        for row in range(2, 10):
            for col in range(2, 10):
                if is_enemy[not is_white](self.board[row][col]):
                    self.add_piece_moves((row, col), pseudo_moves_dict)
        self.add_en_passant(enemy_uci_move, pseudo_moves_dict)
        pseudo_moves_sorted_list = pseudo_moves_dict["en passant"] + pseudo_moves_dict["promotion"] + pseudo_moves_dict["capture"] + pseudo_moves_dict["castle"] + pseudo_moves_dict["move"]
        return self.filter_invalid_moves(is_white, pseudo_moves_sorted_list)

    def filter_invalid_moves(self, is_white, pseudo_moves):
        valid_moves = []
        for move in pseudo_moves:
            move.do_move(self)
            if not self.is_king_attacked(is_white):
                valid_moves.append(move)
            move.undo_move(self)
        return valid_moves

    def add_piece_moves(self, piece_val, moves):
        piece_int = self.board[piece_val[0]][piece_val[1]]
        piece = value_to_piece[piece_int]
        (is_white, piece_description) = piece_to_descriptor[piece]
        method_name = 'add_' + piece_description + '_moves'
        return getattr(self, method_name)(piece_val, is_white, moves)

    def add_pawn_moves(self, pawn, is_white, moves):
        (row, col) = (pawn[0], pawn[1])
        # for color: next row, row after next row, start row, promoted row
        target_row = [row - 1, row - 2, 8, 2, row + 1, row + 2, 3, 9]
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
                moves["capture"].append(Capture(row, col, target_row[idx], col - 1, to_piece))
            if is_enemy[is_white](self.board[target_row[idx]][col + 1]):
                to_piece = self.board[target_row[idx]][col + 1]
                moves["capture"].append(Capture(row, col, target_row[idx], col + 1, to_piece))

    def add_pawn_promotion_moves(self, row, col, promotion_row, is_white, moves):
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

    def add_en_passant(self, enemy_uci_move_performed, moves):
        (col_1, row_1, col_2, row_2) = uci_move_to_move(enemy_uci_move_performed)
        enemy_piece_moved = self.board[row_2][col_2]
        if abs(row_1 - row_2) == 2 and value_to_piece_short[enemy_piece_moved] == 'p':
            if self.board[row_2][col_2 - 1] == - enemy_piece_moved:
                moves["en passant"].append(EnPassant(row_2, col_2 - 1, (row_1 + row_2) // 2, col_2))
            if self.board[row_2][col_2 + 1] == - enemy_piece_moved:
                moves["en passant"].append(EnPassant(row_2, col_2 + 1, (row_1 + row_2) // 2, col_2))

    def add_queen_moves(self, queen, is_white, moves):
        self.add_directed_moves(queen, queen_directions, is_white, moves)

    def add_rook_moves(self, rook, is_white, moves):
        self.add_directed_rook_moves(rook, rook_directions, is_white, moves)

    def add_directed_rook_moves(self, rook, directions, is_white, moves):
        row, col = rook[0], rook[1]
        if self.state.cannot_castle[is_white] or (row, col) not in rook_start_pos[is_white]:
            self.add_directed_moves(rook, rook_directions, is_white, moves)  # castling rights unaffected
        else:
            new_game_state = copy.deepcopy(self.state)
            new_game_state.rook_moved[(row, col)] = True
            for direction in directions:
                to_row, to_col = row + direction[0], col + direction[1]
                while self.board[to_row][to_col] == Pieces.OO:
                    moves["move"].append(MoveStateChange(row, col, to_row, to_col, self.state, new_game_state))
                    to_row, to_col = to_row + direction[0], to_col + direction[1]
                if is_enemy[is_white](self.board[to_row][to_col]):
                    moves["capture"].append(CaptureStateChange(row, col, to_row, to_col, self.board[to_row][to_col], self.state, new_game_state))

    def add_bishop_moves(self, bishop, is_white, moves):
        self.add_directed_moves(bishop, bishop_directions, is_white, moves)

    def add_directed_moves(self, piece, directions, is_white, moves):
        row, col = piece[0], piece[1]
        for direction in directions:
            to_row, to_col = row + direction[0], col + direction[1]
            while self.board[to_row][to_col] == Pieces.OO:
                moves["move"].append(Move(row, col, to_row, to_col))
                to_row, to_col = to_row + direction[0], to_col + direction[1]
            if is_enemy[is_white](self.board[to_row][to_col]):
                moves["capture"].append(Capture(row, col, to_row, to_col, self.board[to_row][to_col]))

    def add_knight_moves(self, knight, is_white, moves):
        self.add_square_moves(knight[0], knight[1], get_knight_squares(knight[0], knight[1]), is_white, moves)

    def add_square_moves(self, row, col, to_squares, is_white, moves):
        for to_square in to_squares:
            to_square_val = self.board[to_square[0]][to_square[1]]
            if to_square_val == Pieces.OO:
                moves["move"].append(Move(row, col, to_square[0], to_square[1]))
            elif is_enemy[is_white](to_square_val):
                moves["capture"].append(Capture(row, col, to_square[0], to_square[1], to_square_val))

    def add_king_moves(self, king, is_white, moves):
        row, col = king[0], king[1]
        self.add_king_square_moves(row, col, get_king_squares(row, col), is_white, moves)
        if not self.state.cannot_castle[is_white] and not self.is_king_attacked(is_white):
            self.add_castling_moves(col, is_white, moves, row)

    def add_king_square_moves(self, row, col, to_squares, is_white, moves):
        for to_square in to_squares:
            new_game_state = copy.deepcopy(self.state)
            new_game_state.cannot_castle[is_white] = True
            new_game_state.king_pos[is_white] = (to_square[0], to_square[1])
            to_square_val = self.board[to_square[0]][to_square[1]]
            if to_square_val == Pieces.OO:
                moves["move"].append(MoveStateChange(row, col, to_square[0], to_square[1], self.state, new_game_state))
            elif is_enemy[is_white](to_square_val):
                moves["capture"].append(CaptureStateChange(row, col, to_square[0], to_square[1], to_square_val, self.state, new_game_state))

    def add_castling_moves(self, col, is_white, moves, row):
        if not self.state.rook_moved[(row, col + 3)] and self.board[row][col + 3] == promotion_color_to_value[('r', is_white)] and self.safe_to_castle_kingside(row, col, is_white):
            moves["castle"].append(Castle(True, is_white))
        if not self.state.rook_moved[(row, col - 4)] and self.board[row][col - 4] == promotion_color_to_value[('r', is_white)] and self.safe_to_castle_queenside(row, col, is_white):
            moves["castle"].append(Castle(False, is_white))

    def safe_to_castle_kingside(self, row, col, is_white):
        return self.board[row][col + 1] == Pieces.OO and self.board[row][col + 2] == Pieces.OO and not self.is_square_attacked(row, col + 1, is_white) and not self.is_square_attacked(row, col + 2,
                                                                                                                                                                                       is_white)

    def safe_to_castle_queenside(self, row, col, is_white):
        return self.board[row][col - 1] == Pieces.OO and self.board[row][col - 2] == Pieces.OO and self.board[row][col - 3] == Pieces.OO and not self.is_square_attacked(row, col - 1,
                                                                                                                                                                         is_white) and not self.is_square_attacked(
            row, col - 2, is_white)

    def is_king_attacked(self, is_white):
        (king_row, king_col) = self.state.king_pos[is_white]
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
