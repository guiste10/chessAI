class GameSate:
    def __init__(self, king_pos, castled, queen_rook_moved, king_rook_moved):
        self.king_pos = king_pos
        self.castled = castled
        self.queen_rook_moved = queen_rook_moved
        self.king_rook_moved = king_rook_moved
