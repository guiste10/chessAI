from Pieces import Pieces as P


class BoardPositions:
    normal_board = [[P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.BR, P.BN, P.BB, P.BQ, P.BK, P.BB, P.BN, P.BR, P.XX, P.XX],
        [P.XX, P.XX, P.BP, P.BP, P.BP, P.BP, P.BP, P.BP, P.BP, P.BP, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.WP, P.WP, P.WP, P.WP, P.WP, P.WP, P.WP, P.WP, P.XX, P.XX],
        [P.XX, P.XX, P.WR, P.WN, P.WB, P.WQ, P.WK, P.WB, P.WN, P.WR, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX]]

    no_attack_board = [[P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.BR, P.BN, P.BB, P.BQ, P.BK, P.BB, P.OO, P.BR, P.XX, P.XX],
        [P.XX, P.XX, P.BP, P.BP, P.BP, P.OO, P.BP, P.BP, P.BP, P.BP, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.BN, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.BP, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.WP, P.OO, P.OO, P.WP, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.WP, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.WP, P.OO, P.WP, P.WP, P.WP, P.WP, P.XX, P.XX],
        [P.XX, P.XX, P.WR, P.WN, P.WB, P.WQ, P.WK, P.WB, P.WN, P.WR, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX]]

    attack_board = [[P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.BR, P.OO, P.OO, P.OO, P.BK, P.OO, P.OO, P.BR, P.XX, P.XX],
        [P.XX, P.XX, P.BP, P.BP, P.OO, P.BB, P.BB, P.BP, P.BP, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.BQ, P.BN, P.OO, P.BP, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.BP, P.WP, P.WB, P.OO, P.BP, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.WP, P.OO, P.OO, P.OO, P.WP, P.XX, P.XX],
        [P.XX, P.XX, P.WP, P.OO, P.WN, P.OO, P.WB, P.WN, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.WP, P.OO, P.WQ, P.OO, P.WP, P.WP, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.WR, P.OO, P.OO, P.OO, P.WR, P.WK, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX]]

    en_passant_board_white = [[P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.BK, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.WP, P.BP, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.WK, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX]]

    en_passant_board_black = [[P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.BK, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.WP, P.BP, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.WK, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.OO, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX]]
