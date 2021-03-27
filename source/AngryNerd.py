from __future__ import print_function
from board.BoardPositions import init_normal_board, init_attack_board
from move.MoveUtils import NONE, uci_move_to_move_object, move_to_uci_move
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
    moves = ['g1f3','d7d5','g2g3','b8c6','f1g2','e7e5','e1g1','e5e4','f3e1','h7h5','d2d3','f8b4','a2a3','b4e1','f1e1','f7f5','d3e4','f5e4','c2c4','c8e6','c4d5','e6d5','b1c3','d5e6','g2e4','d8d1','e1d1','e6b3','e4c6','b7c6','d1d4','g8f6','c1f4','c6c5','d4d2','a8d8','c3b5','d8d2','f4d2','e8d7','d2c3','a7a6','c3f6','g7f6','b5c3','h8e8','g1g2','d7e6','c3e4','b3d5','f2f3','c5c4','a1d1','c7c6','e4c3','f6f5','e2e4','f5e4','f3e4','d5e4','c3e4','e8a8','d1d6','e6e5','g2f3','a8b8','d6c6','b8b3','e4c3','b3b2','c6c4','b2h2','c4c6','h2h1','c6a6','e5d4','c3e4','h1f1','f3e2','f1h1','a6a4','d4e5','e2e3','h1e1','e3d3','e1d1','e4d2','e5d5','a4a5','d5e6','a5h5','e6f6','h5d5','d1a1','d2e4','f6e6','d5a5','a1d1','d3e2','d1d4','e2e3','d4d1','a5a7','d1e1','e3f3','e6e5','a7e7','e5d4','e7d7','d4e5','d7b7','e1f1','f3e3','f1e1','e3f3','e1f1','f3e3','f1e1','e3d3','e1d1','d3c2','d1a1','c2b2','a1d1','b7e7','e5f5','b2c3','d1d5','c3c4','d5a5','e4d6','f5g4','c4b4','a5h5','e7g7','g4f3','d6e8','h5d5','b4c4','d5a5','c4b4','a5d5','b4c4','d5e5','e8d6','e5e3','a3a4','f3g2','d6f5','e3a3','c4b4','a3d3','a4a5','g2f3','a5a6','f3e4','a6a7','d3d8','f5h4','d8a8','g7f7','e4d5','b4c3','d5e6','f7h7','e6f6','h4f3','f6g6','h7d7','g6f6','d7c7','a8g8','c7c6','f6e7']
    for uci_move in moves:
        previous_move = uci_move_to_move_object(uci_move, is_white, board)
        previous_move.do_move(board)
        is_white = not is_white
    start = time.time()
    best_move_uci = play_turn(board, move_to_uci_move(previous_move), is_white, 200, 50)
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
