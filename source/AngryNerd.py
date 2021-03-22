from __future__ import print_function
from board.BoardPositions import init_normal_board, init_attack_board
from move.MoveUtils import NONE, uci_move_to_move_object
from ai import Search
from ai.Search import play_turn, visit_node
import time
import sys

import logging
import os


def play_uci():
    directory = 'engine_logs'
    if not os.path.exists(directory):
        os.makedirs(directory)
    logging.basicConfig(filename='engine_logs/uci.log', level=logging.DEBUG)
    logging.debug('engine started executing')
    board, previous_uci_move = init_normal_board()
    is_white, Search.can_use_hard_coded, turn = True, True, 1
    quit_now, prev_pos_line = False, NONE
    while not quit_now:
        line = raw_input().rstrip()
        logging.debug(line)
        if line == 'uci':
            print_f('id name Angry Nerd')
            print_f('id author Guillaume Neirinckx')
            print_f('uciok')
        elif line == 'ucinewgame':
            board, previous_uci_move = init_normal_board()  # todo clear history
            Search.can_use_hard_coded, turn = True, 1
        elif line == 'isready':
            print_f('readyok')
        elif line == 'quit':
            quit_now = True
        else:
            line_splitted = line.split()
            if line != prev_pos_line and line_splitted[0] == 'position' and line_splitted[1] == 'startpos':
                prev_pos_line = line
                if len(line_splitted) == 2:
                    is_white = True
                elif len(line_splitted) == 4:
                    is_white = False
                if len(line_splitted) > 2:
                    previous_uci_move = line_splitted[-1]
                    previous_move = uci_move_to_move_object(previous_uci_move, not is_white, board)
                    previous_move.do_move(board)
                    # todo add to history
            elif line_splitted[0] == 'go':
                if len(line_splitted) >= 5:
                    time_left_sec = int(line_splitted[2])/1000 if is_white else int(line_splitted[4])/1000
                else:
                    time_left_sec = 99999999
                best_move_uci = play_turn(board, previous_uci_move, is_white, time_left_sec, turn)
                print_f('bestmove ' + best_move_uci)
                # todo add to history
                best_move = uci_move_to_move_object(best_move_uci, is_white, board)
                best_move.do_move(board)
                turn += 1

def print_f(msg):
    print(msg)
    sys.stdout.flush()



def debug_position():
    #import cProfile
    # pr = cProfile.Profile()
    # pr.enable()
    board, previous_uci_move = init_normal_board()
    is_white = True
    moves = ['d2d4','g7g6','g1f3','f8g7','b1c3','g8f6','h2h3','d7d5','f3e5','f6e4','a2a4','e4c3','d1d2','c3e4','d2f4','e8g8','f4h4','c7c5','c1e3','c5d4','e5g6','f7g6','e3d2','g7e5','e2e3','e5g3','h4h7','g8h7','e1c1']
    for uci_move in moves:
        previous_move = uci_move_to_move_object(uci_move, is_white, board)
        previous_move.do_move(board)
        is_white = not is_white
    start = time.time()
    best_move_uci = play_turn(board, previous_uci_move, is_white, 200, 50)
    print('time taken: ' + str(time.time() - start))
    print('bestmove ' + best_move_uci)
    #pr.print_stats(sort="tottime")



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
            move = uci_move_to_move_object(opponents_uci_move, is_engine_white, board)
            move.do_move(board)
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
                move = uci_move_to_move_object(best_move_uci, is_engine_white, board)
                move.do_move(board)
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

if __name__ == "__main__":
    #debug_position()
    #play_on_console()
    play_uci()
