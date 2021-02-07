from Board import Board
from BoardPositions import BoardPositions
from move.MoveUtils import do_uci_move, move_to_uci_move
from Ai import get_best_move

def main():
    print("Engine started", "\n")
    board = Board(BoardPositions.normal_board)
    board.init_pieces()
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
    play_game(board, is_engine_white, n, opponents_uci_move)


def play_game(board, is_engine_white, n, opponents_uci_move):
    game_over = False
    while not game_over:
        if n % 2 == 0:
            opponents_uci_move = input("Enter move: ").replace(" ", "")
            print('')
            do_uci_move(opponents_uci_move, board, not is_engine_white)
        else:
            print("Engine's Turn:", end=' ')
            best_move_uci, best_move_val = get_best_move(board, opponents_uci_move, is_engine_white)
            if best_move_uci == 'no move':
                game_over = True
                if board.is_king_attacked(is_engine_white):
                    print("Engine checkmated !")
                else:
                    print("Stalemate !")
            else:
                do_uci_move(best_move_uci, board, is_engine_white)
                print(best_move_uci + '\n')
        print(board)
        n += 1


if __name__ == "__main__":
    main()