from Board import Board
from BoardPositions import BoardPositions
from move.MoveUtils import do_uci_move, move_to_uci_move
from Ai import get_best_move

def main():
    print("Engine started", "\n")
    board = Board(BoardPositions.normal_board)
    white_pieces, black_pieces = board.init_pieces()
    pieces = {True: white_pieces, False: black_pieces}
    print(board)
    is_engine_white = False
    opponents_uci_move = 'a1a1' #  used for en passant purposes
    if input("Engine white?: y/n ") == 'y':
        is_engine_white = True
        n = 1
    else:
        is_engine_white = False
        n = 0
    print('')
    while True:
        if n % 2 == 0:
            opponents_uci_move = input("Enter move: ").replace(" ", "")
            print('')
            do_uci_move(opponents_uci_move, board, not is_engine_white)
        else:
            print("Engine's Turn:", end=' ')
            move = get_best_move(board, pieces, is_engine_white, opponents_uci_move, 1)
            move.do_move(board)
            move_uci = move_to_uci_move(move)
            print(move_uci + '\n')
        print(board)
        n += 1


if __name__ == "__main__":
    main()