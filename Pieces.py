class Pieces:
    XX = 7
    OO = 0
    WP = 1
    WR = 2
    WN = 3
    WB = 4
    WQ = 5
    WK = 6
    BP = -1
    BR = -2
    BN = -3
    BB = -4
    BQ = -5
    BK = -6


start_row_black = 2
start_row_white = 9
queen_rook_start_col = 2
king_start_col = 6
king_rook_start_col = 9
start_row = {False: start_row_black, True: start_row_white}
king_start_pos = {False: (start_row_black, king_start_col), True: (start_row_white, king_start_col)}
rook_start_pos = {False: ((start_row_black, queen_rook_start_col), (start_row_black, king_rook_start_col)), True: ((start_row_white, queen_rook_start_col), (start_row_white, king_rook_start_col))}

value_to_descriptor = {1: 'pawn', 2: 'rook', 3: 'knight', 4: 'bishop', 5: 'queen', 6: 'king',
                       -1: 'pawn', -2: 'rook', -3: 'knight', -4: 'bishop', -5: 'queen', -6: 'king'}

promotion_color_to_value = {('k', True): 6, ('q', True): 5, ('r', True): 2, ('b', True): 4, ('n', True): 3, ('p', True): 1, ('k', False): -6, ('q', False): -5, ('r', False): -2, ('b', False): -4,
                            ('n', False): -3, ('p', False): -1}

value_to_piece_short = {0: 'wtf', 1: 'p', 2: 'r', 3: 'n', 4: 'b', 5: 'q', 6: 'k', -1: 'p', -2: 'r', -3: 'n', -4: 'b', -5: 'q', -6: 'k'}

value_to_piece_img = {-1: '♟', -2: '♜', -3: '♞', -4: '♝', -5: '♛', -6: '♚', 1: '♙', 2: '♖', 3: '♘', 4: '♗', 5: '♕', 6: '♔', 0: '.'}

possible_promotions = {True: (2, 3, 4, 5), False: (-2, -3, -4, -5)}

black_walkable_squares = {1, 2, 3, 4, 5, 6, 0}
white_piece_values = {1, 2, 3, 4, 5, 6}
white_walkable_squares = {-1, -2, -3, -4, -5, -6, 0}
black_piece_values = {-1, -2, -3, -4, -5, -6}

is_enemy = {True: lambda piece_int: piece_int in black_piece_values, False: lambda piece_int: piece_int in white_piece_values}

rook_directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
bishop_directions = ((1, 1), (1, -1), (-1, -1), (-1, 1))
queen_directions = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))


def get_knight_squares(row, col):
    return (row - 1, col + 2), (row + 1, col + 2), (row + 2, col + 1), (row + 2, col - 1), (row + 1, col - 2), (row - 1, col - 2), (row - 2, col - 1), (row - 2, col + 1)


def get_king_squares(row, col):
    return (row + 1, col - 1), (row + 1, col), (row + 1, col + 1), (row, col - 1), (row, col + 1), (row - 1, col - 1), (row - 1, col), (row - 1, col + 1)


def get_attacking_enemy_pawn_squares(row, col, is_white):
    return [(row - 1, col - 1), (row - 1, col + 1)] if is_white else [(row + 1, col - 1), (row + 1, col + 1)]
