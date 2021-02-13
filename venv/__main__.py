from Board import Board
from BoardPositions import init_normal_board, init_attack_board
from move.MoveUtils import do_uci_move, move_to_uci_move
from Ai import get_best_move, visit_node

def main():
    print("Engine started", "\n")
    #board = init_normal_board()
    board = init_attack_board()
    print(board)
    is_engine_white = False
    opponents_uci_move = 'none' #  used for en passant purposes
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
            # import cProfile
            # pr = cProfile.Profile()
            # pr.enable()
            print("Engine's Turn:")
            best_move_uci = get_best_move(board, opponents_uci_move, is_engine_white)
            #pr.print_stats(sort="cumtime")
            if best_move_uci == 'no move':
                game_over = True
                if board.is_king_attacked(is_engine_white):
                    print("Engine checkmated !")
                else:
                    print("Stalemate !")
            else:
                do_uci_move(best_move_uci, board, is_engine_white)
                print(best_move_uci)
        print(board)
        n += 1


if __name__ == "__main__":
    main()