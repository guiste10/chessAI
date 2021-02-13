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


king_start_pos = {False: (2, 6), True: (9, 6)}
king_castled_kingside_pos = {False: (2, 8), True: (9, 8)}
king_castled_queenside_pos = {False: (2, 4), True: (9, 4)}
rook_start_pos = {False: ((2, 2), (2, 9)), True: ((9, 2), (9, 9))}

piece_to_descriptor = {'WP': (True, 'pawn'), 'WR': (True, 'rook'), 'WN': (True, 'knight'), 'WB': (True, 'bishop'),
                       'WQ': (True, 'queen'), 'WK': (True, 'king'), 'BP': (False, 'pawn'), 'BR': (False, 'rook'),
                       'BN': (False, 'knight'), 'BB': (False, 'bishop'), 'BQ': (False, 'queen'), 'BK': (False, 'king')}

value_to_piece = {0: '0 ', 1: 'WP', 2: 'WR', 3: 'WN', 4: 'WB', 5: 'WQ', 6: 'WK', -1: 'BP', -2: 'BR', -3: 'BN', -4: 'BB',
                  -5: 'BQ', -6: 'BK'}

promotion_color_to_value = {('k', True): 6, ('q', True): 5, ('r', True): 2, ('b', True): 4, ('n', True): 3, ('p', True): 1,
                            ('k', False): -6, ('q', False): -5, ('r', False): -2, ('b', False): -4, ('n', False): -3, ('p', False): -1}

value_to_piece_short = {0: 'wtf', 1: 'p', 2: 'r', 3: 'n', 4: 'b', 5: 'q', 6: 'k', -1: 'p', -2: 'r', -3: 'n', -4: 'b', -5: 'q',
                        -6: 'k'}

possible_promotions = {True: (2, 3, 4, 5), False: (-2, -3, -4, -5)}

black_walkable_squares = {1, 2, 3, 4, 5, 6, 0}
white_piece_values = {1, 2, 3, 4, 5, 6}
white_walkable_squares = {-1, -2, -3, -4, -5, -6, 0}
black_piece_values = {-1, -2, -3, -4, -5, -6}

is_enemy = {True: lambda piece_int: piece_int in black_piece_values,
            False: lambda piece_int: piece_int in white_piece_values}

rook_directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
bishop_directions = ((1, 1), (1, -1), (-1, -1), (-1, 1))
queen_directions = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))


def get_knight_squares(row, col):
    return ((row - 1, col + 2), (row + 1, col + 2), (row + 2, col + 1), (row + 2, col - 1), (row + 1, col - 2),
            (row - 1, col - 2), (row - 2, col - 1), (row - 2, col + 1))


def get_king_squares(row, col):
    return ((row + 1, col - 1), (row + 1, col), (row + 1, col + 1), (row, col - 1), (row, col + 1), (row - 1, col - 1),
            (row - 1, col), (row - 1, col + 1))
