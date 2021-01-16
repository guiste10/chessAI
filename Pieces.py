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

    piece_to_descriptor = {'WP': (True, 'pawn'),
                           'WR': (True, 'rook'),
                           'WN': (True, 'knight'),
                           'WB': (True, 'bishop'),
                           'WQ': (True, 'queen'),
                           'WK': (True, 'king'),
                           'BP': (False, 'pawn'),
                           'BR': (False, 'rook'),
                           'BN': (False, 'knight'),
                           'BB': (False, 'bishop'),
                           'BQ': (False, 'queen'),
                           'BK': (False, 'king')
                           }

    value_to_piece = {0: '0 ',
                   1: 'WP',
                   2: 'WR',
                   3: 'WN',
                   4: 'WB',
                   5: 'WQ',
                   6: 'WK',
                   -1: 'BP',
                   -2: 'BR',
                   -3: 'BN',
                   -4: 'BB',
                   -5: 'BQ',
                   -6: 'BK'}
