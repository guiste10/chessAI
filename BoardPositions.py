from Pieces import Pieces as Pc
from Board import Board

normal_board = [[Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.BR, Pc.BN, Pc.BB, Pc.BQ, Pc.BK, Pc.BB, Pc.BN, Pc.BR, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.BP, Pc.BP, Pc.BP, Pc.BP, Pc.BP, Pc.BP, Pc.BP, Pc.BP, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.WP, Pc.WP, Pc.WP, Pc.WP, Pc.WP, Pc.WP, Pc.WP, Pc.WP, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.WR, Pc.WN, Pc.WB, Pc.WQ, Pc.WK, Pc.WB, Pc.WN, Pc.WR, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX]]

no_attack_board = [[Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                   [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                   [Pc.XX, Pc.XX, Pc.BR, Pc.BN, Pc.BB, Pc.BQ, Pc.BK, Pc.BB, Pc.OO, Pc.BR, Pc.XX, Pc.XX],
                   [Pc.XX, Pc.XX, Pc.BP, Pc.BP, Pc.BP, Pc.OO, Pc.BP, Pc.BP, Pc.BP, Pc.BP, Pc.XX, Pc.XX],
                   [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.BN, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                   [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.BP, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                   [Pc.XX, Pc.XX, Pc.WP, Pc.OO, Pc.OO, Pc.WP, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                   [Pc.XX, Pc.XX, Pc.OO, Pc.WP, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                   [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.WP, Pc.OO, Pc.WP, Pc.WP, Pc.WP, Pc.WP, Pc.XX, Pc.XX],
                   [Pc.XX, Pc.XX, Pc.WR, Pc.WN, Pc.WB, Pc.WQ, Pc.WK, Pc.WB, Pc.WN, Pc.WR, Pc.XX, Pc.XX],
                   [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                   [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX]]

attack_board = [[Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.BR, Pc.OO, Pc.OO, Pc.OO, Pc.BK, Pc.OO, Pc.OO, Pc.BR, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.BP, Pc.BP, Pc.OO, Pc.BB, Pc.BB, Pc.BP, Pc.BP, Pc.OO, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.OO, Pc.BQ, Pc.BN, Pc.OO, Pc.BP, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.BP, Pc.WP, Pc.WB, Pc.OO, Pc.BP, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.WP, Pc.OO, Pc.OO, Pc.OO, Pc.WP, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.WP, Pc.OO, Pc.WN, Pc.OO, Pc.WB, Pc.WN, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.OO, Pc.WP, Pc.OO, Pc.WQ, Pc.OO, Pc.WP, Pc.WP, Pc.OO, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.OO, Pc.WR, Pc.OO, Pc.OO, Pc.OO, Pc.WR, Pc.WK, Pc.OO, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX]]

en_passant_board_white = [[Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.BK, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.WP, Pc.BP, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.WK, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX]]

en_passant_board_black = [[Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.BK, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.WP, Pc.BP, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.WK, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.OO, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX],
                          [Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX, Pc.XX]]


def init_normal_board():
    return Board(normal_board)


def init_no_attack_board():
    return Board(no_attack_board)


def init_attack_board():
    board = Board(attack_board)
    board.state.cannot_castle[True] = True  # white castled
    board.state.king_pos[True] = (9, 8)
    return board
