import copy
import Pieces


class BoardState:
    def __init__(self):
        self.king_pos = copy.deepcopy(Pieces.king_start_pos)
        self.cannot_castle = {True: False, False: False}
        self.rook_moved = {(2, 2): False, (2, 9): False, (9, 2): False, (9, 9): False}
