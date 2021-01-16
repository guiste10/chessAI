from Pieces import Pieces as P

class BoardPositions:
    normal_board =  [
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
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

    no_attack_board = [
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
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

    en_passant_board =  [
        [P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX, P.XX],
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