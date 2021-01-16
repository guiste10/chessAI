from Pieces import Pieces
from Board import Board
from BoardPositions import BoardPositions


class ChessGame:
    def __init__(self):
        self.board = Board(BoardPositions.normal_board)
        print(self.board)

        # list of pieces with their positions (x, y, is_pinned)
        self.white_pieces, self.black_pieces = self.board.init_pieces()

        moves, self.white_pieces = self.board.get_color_moves(self.white_pieces, True, 'e4e6')
        for move in moves:
            print(move, end=" ")
        print('\n')
        print('Num moves: ' + str(len(moves)))
        a=1


