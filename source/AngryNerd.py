from __future__ import print_function
from board.BoardPositions import init_normal_board, init_attack_board
from move.MoveUtils import do_uci_move
from ai import Search
from ai.Search import play_turn, visit_node, transposition_table, use_transposition_table
import time
import sys

import logging
from pathlib import Path
import os


def play_uci():
    directory = 'engine_logs'
    if not os.path.exists(directory):
        os.makedirs(directory)
    logging.basicConfig(filename='engine_logs/uci.log', level=logging.DEBUG)
    logging.debug('engine started executing')
    board, previous_uci_move = init_normal_board()
    is_white, Search.can_use_hard_coded, turn = True, True, 1
    quit_now = False
    while not quit_now:
        line = raw_input()
        logging.debug(line)
        line = line.rstrip()
        if line == 'uci':
            print_f('id name Angry Nerd')
            print_f('id author Guillaume Neirinckx')
            print_f('uciok')
        elif line == 'ucinewgame':
            board, previous_uci_move = init_normal_board()
            Search.can_use_hard_coded, turn = True, 1
        elif line == 'isready':
            print_f('readyok')
        elif line == 'quit':
            quit_now = True
        else:
            line_splitted = line.split()
            if line_splitted[0] == 'position' and line_splitted[1] == 'startpos':
                is_white = True
                if len(line_splitted) > 2:
                    uci_moves = line_splitted[3:]
                    for uci_move in uci_moves:
                        do_uci_move(uci_move, board, is_white)
                        is_white, previous_uci_move = not is_white, uci_move

            elif line_splitted[0] == 'go':
                if len(line_splitted) >= 5:
                    time_left_sec = int(line_splitted[2])/1000 if is_white else int(line_splitted[4])/1000
                else:
                    time_left_sec = 99999999
                best_move_uci = play_turn(board, previous_uci_move, is_white, time_left_sec, turn)
                print_f('bestmove ' + best_move_uci)
                board, previous_uci_move = init_normal_board()
                turn += 1

def print_f(msg):
    print(msg)
    sys.stdout.flush()



def debug_position():
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    board, previous_uci_move = init_normal_board()
    is_white = True
    moves = ['d2d3','g7g6','h2h4','f8g7','b1d2','g8f6','c2c4','b8c6','e2e4','e8g8','g1f3','d7d6','g2g3','c8g4','h4h5','g4h5','d1b3','h5f3','d2f3','a8b8','b3d1','e7e5','c1g5']
    for uci_move in moves:
        do_uci_move(uci_move, board, is_white)
        is_white = not is_white
    start = time.time()
    best_move_uci = play_turn(board, previous_uci_move, is_white, 200, 50)
    print('time taken: ' + str(time.time() - start))
    print('bestmove ' + best_move_uci)
    pr.print_stats(sort="tottime")



def play_on_console():
    print("Engine started", "\n")
    # turn, (board, opponents_uci_move) = 10, init_normal_board()
    turn, (board, opponents_uci_move), Search.can_use_hard_coded = 4, init_attack_board(), False
    print(board)
    if raw_input("Is the engine white?: y/n ") == 'y':
        is_engine_white = True
        n = 1
    else:
        is_engine_white = False
        n = 0
    print('')
    game_over = False
    while not game_over:
        if n % 2 == 0:
            opponents_uci_move = raw_input("Enter move: ").replace(" ", "")
            do_uci_move(opponents_uci_move, board, not is_engine_white)
        else:
            print("\nEngine's Turn:")
            # import cProfile
            # pr = cProfile.Profile()
            # pr.enable()
            start = time.time()
            best_move_uci = play_turn(board, opponents_uci_move, is_engine_white, 9999, turn)
            # pr.print_stats(sort="tottime")
            if best_move_uci == 'none':
                game_over = True
                if board.is_king_attacked(is_engine_white):
                    print("\nEngine checkmated !\n")
                else:
                    print("\nStalemate !\n")
            else:
                do_uci_move(best_move_uci, board, is_engine_white)
                print('Move: ' + best_move_uci)
                print_stats(time.time() - start, turn)
                turn += 1
        print(board)
        n += 1


def print_stats(time_dif, turn):
    if turn > 3:
        print('Time: ' + str(time_dif))
        print('#nodes: ' + str(visit_node()))
        print('#nodes/sec: ' + str(visit_node() // time_dif) + '\n')
        print('# transposition table hits: ' + str(use_transposition_table()) + '\n')


if __name__ == "__main__":
    debug_position()
    #play_on_console()
    #play_uci()
