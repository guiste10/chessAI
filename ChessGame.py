from Pieces import Pieces
from Board import Board



class ChessGame:
    def __init__(self):
        self.board = Board()
        print(self.board)
        # castling rights
        self.white_castled = False
        self.black_castled = False
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_king_rook_moved = False
        self.black_king_rook_moved = False
        self.white_queen_rook_moved = False
        self.black_queen_rook_moved = False

        # list of pieces with their positions (x, y, is_pinned)
        (self.white_pieces, self.black_pieces) = self.board.init_pieces()

        moves, self.white_pieces = self.board.get_color_moves(self.white_pieces, True)
        b = 2


