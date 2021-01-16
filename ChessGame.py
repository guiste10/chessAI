from Pieces import Pieces
from Board import Board



class ChessGame:
    def __init__(self):
        self.board = Board()
        print(self.board)

        # list of pieces with their positions (x, y, is_pinned)
        (self.white_pieces, self.black_pieces) = self.board.init_pieces()

        moves, self.white_pieces = self.board.get_color_moves(self.white_pieces, True)
        print(len(moves))


