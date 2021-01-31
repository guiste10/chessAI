from Pieces import Pieces as Pcs


class BoardPositions:
    normal_board = [[Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.BR, Pcs.BN, Pcs.BB, Pcs.BQ, Pcs.BK, Pcs.BB, Pcs.BN, Pcs.BR, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.BP, Pcs.BP, Pcs.BP, Pcs.BP, Pcs.BP, Pcs.BP, Pcs.BP, Pcs.BP, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.WP, Pcs.WP, Pcs.WP, Pcs.WP, Pcs.WP, Pcs.WP, Pcs.WP, Pcs.WP, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.WR, Pcs.WN, Pcs.WB, Pcs.WQ, Pcs.WK, Pcs.WB, Pcs.WN, Pcs.WR, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX]]

    no_attack_board = [[Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                       [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                       [Pcs.XX, Pcs.XX, Pcs.BR, Pcs.BN, Pcs.BB, Pcs.BQ, Pcs.BK, Pcs.BB, Pcs.OO, Pcs.BR, Pcs.XX, Pcs.XX],
                       [Pcs.XX, Pcs.XX, Pcs.BP, Pcs.BP, Pcs.BP, Pcs.OO, Pcs.BP, Pcs.BP, Pcs.BP, Pcs.BP, Pcs.XX, Pcs.XX],
                       [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.BN, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                       [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.BP, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                       [Pcs.XX, Pcs.XX, Pcs.WP, Pcs.OO, Pcs.OO, Pcs.WP, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                       [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.WP, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                       [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.WP, Pcs.OO, Pcs.WP, Pcs.WP, Pcs.WP, Pcs.WP, Pcs.XX, Pcs.XX],
                       [Pcs.XX, Pcs.XX, Pcs.WR, Pcs.WN, Pcs.WB, Pcs.WQ, Pcs.WK, Pcs.WB, Pcs.WN, Pcs.WR, Pcs.XX, Pcs.XX],
                       [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                       [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX]]

    attack_board = [[Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.BR, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.BK, Pcs.OO, Pcs.OO, Pcs.BR, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.BP, Pcs.BP, Pcs.OO, Pcs.BB, Pcs.BB, Pcs.BP, Pcs.BP, Pcs.OO, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.BQ, Pcs.BN, Pcs.OO, Pcs.BP, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.BP, Pcs.WP, Pcs.WB, Pcs.OO, Pcs.BP, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.WP, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.WP, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.WP, Pcs.OO, Pcs.WN, Pcs.OO, Pcs.WB, Pcs.WN, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.WP, Pcs.OO, Pcs.WQ, Pcs.OO, Pcs.WP, Pcs.WP, Pcs.OO, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.WR, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.WR, Pcs.WK, Pcs.OO, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                    [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX]]

    en_passant_board_white = [[Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.BK, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.WP, Pcs.BP, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.WK, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX]]

    en_passant_board_black = [[Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.BK, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.WP, Pcs.BP, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.WK, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.OO, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX],
                              [Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX, Pcs.XX]]
