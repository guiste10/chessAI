from Pieces import Pieces


class Move:
    def __init__(self, row_1, col_1, row_2, col_2):
        self.row_1 = row_1
        self.col_1 = col_1
        self.row_2 = row_2
        self.col_2 = col_2

    def __str__(self):
        return self.col_to_uci_dict[self.col_1] + self.row_to_uci_dict[self.row_1] \
             + self.col_to_uci_dict[self.col_2] + self.row_to_uci_dict[self.row_2]


class EnPassant(Move):
    def __init__(self, row_1, col_1, row_2, col_2):
        super().__init__(row_1, col_1, row_2, col_2)


class Castle(Move):
    def __init__(self, row_1, col_1, row_2, col_2, king_side):
        super().__init__(row_1, col_1, row_2, col_2)
        self.king_side = king_side


class Capture(Move):
    def __init__(self, row_1, col_1, row_2, col_2, to_piece):
        super().__init__(row_1, col_1, row_2, col_2)
        self.to_piece = to_piece


class Promotion(Move):
    def __init__(self, row_1, col_1, row_2, col_2, promotion_piece, to_piece=Pieces.OO):
        super().__init__(row_1, col_1, row_2, col_2)
        self.promotion_piece = promotion_piece
        self.to_piece = to_piece
