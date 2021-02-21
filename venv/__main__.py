from Board import Board
from BoardPositions import init_normal_board, init_attack_board
from move.MoveUtils import do_uci_move, move_to_uci_move
from Ai import get_best_move, visit_node, use_transposition_table
import time
import fileinput
import logging
import os


def play_uci():
    os.makedirs("logs")
    logger = logging.getLogger('factory')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('log/factory.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    board, previous_uci_move = init_normal_board()
    is_white = True
    for line in fileinput.input():
        logger.debug(line)
        line = line.rstrip()
        if line == 'uci':
            print('id name Angry-nerd')
            print('id author Guillaume Neirinckx')
            print('uciok')
        elif line == 'ucinewgame':
            pass
        elif line == 'isready':
            print('readyok')
        else:
            line_splitted = line.split()
            if line[0] == 'position':
                pass
            elif line[0] == 'go':
                best_move, best_move_val = get_best_move(board, opponents_uci_move, is_engine_white)
                best_move_uci = move_to_uci_move(best_move)
                print(best_move_uci)



def play_on_console():
    print("Engine started", "\n")
    # board, opponents_uci_move = init_normal_board()
    board, opponents_uci_move = init_attack_board()
    print(board)
    is_engine_white = False
    if input("Is the engine white?: y/n ") == 'y':
        is_engine_white = True
        n = 1
    else:
        is_engine_white = False
        n = 0
    print('')
    game_over = False
    while not game_over:
        if n % 2 == 0:
            opponents_uci_move = input("Enter move: ").replace(" ", "")
            do_uci_move(opponents_uci_move, board, not is_engine_white)
        else:
            # import cProfile
            # pr = cProfile.Profile()
            # pr.enable()
            print("\nEngine's Turn:")
            start = time.time()
            best_move, best_move_val = get_best_move(board, opponents_uci_move, is_engine_white)
            best_move_uci = move_to_uci_move(best_move)
            time_dif = time.time() - start
            print_stats(best_move_uci, best_move_val, time_dif)
            #pr.print_stats(sort="cumtime")
            if best_move_uci == 'no move':
                game_over = True
                if board.is_king_attacked(is_engine_white):
                    print("Engine checkmated !")
                else:
                    print("Stalemate !")
            else:
                best_move.do_move(board)
        print(board)
        n += 1


def print_stats(best_move_uci, best_move_val, time_dif):
    print('Time: ' + str(time_dif))
    print('#nodes: ' + str(visit_node()))
    print('#nodes/sec: ' + str(visit_node() // time_dif) + '\n')
    print('Move: ' + best_move_uci)
    print('Evaluation at bottom node: ' + str(best_move_val))
    print('# transposition table hits: ' + str(use_transposition_table()) + '\n')


if __name__ == "__main__":
    play_on_console()
    # play_uci()