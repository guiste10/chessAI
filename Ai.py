
import time


    #     board = Board(BoardPositions.normal_board)
    #     board.state.cannot_castle[True] = True  # white castled
    #     board.state.king_pos[True] = (9, 8)
    #     print(board)
    #
    #     # list of pieces with their positions (x, y)
    #     white_pieces, black_pieces = board.init_pieces()
    #     pieces = {True: white_pieces, False: black_pieces}
    #
    #     start = time.time()
    #     for i in range(1, 10000):
    #         moves, white_pieces = board.get_color_moves(white_pieces, True, 'a1a1')
    #     print('time: ' + str(time.time()-start))

        #moves, self.white_pieces = self.board.get_color_moves(self.white_pieces, True, 'e4e6')

def get_best_move(board, pieces, is_engine_white, opponents_uci_move, depth):
    moves = board.get_color_moves(pieces, is_engine_white, opponents_uci_move)
    return moves[0]




def evaluate(board):
    return 0



