from __future__ import print_function
from board.BoardPositions import init_normal_board, init_attack_board
from move.MoveUtils import uci_move_to_move_object, move_to_uci_move
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
    quit_now, prev_pos_line = False, None
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
    previous_move = None
    is_white = True

    # moves1 = ['d2d4','g7g6','e2e4','f8g7','g1e2','g8f6','d1d3','b8c6','c2c3','e8g8','c1g5','d7d6','h2h4','h7h6','g5d2','d6d5','f2f3','e7e5','e4d5','f6d5','d2h6','g7h6','d4e5','c6e5','d3e4','f8e8','e4d4','h6e3','d4d1','c8f5','c3c4','e5d3','d1d3','f5d3','c4d5','d8d5','b1c3','d5d6','a1d1','e3b6','a2a4','b6a5','f3f4','d6d5','d1d2','a5c3','b2c3','d5c4','h1h3','d3e2','f1e2','c4a4','h3f3','a4c4','g2g3','a7a6','e1f2','c4c5','f2f1','e8e3','d2c2','e3f3','e2f3','a8d8','f1g2','d8b8','g3g4','c5e3','f4f5','e3d3','c2f2','g6f5','g4f5','d3f5','f2d2','f5f6','d2d4','g8h8','d4c4','b8g8','c4g4','g8g4','f3g4','f6h4','g2f3','h4f6','f3e4','f6c3','g4c8','h8g8','e4d5','c3d3']
    # moves2 = ['d5e5','d3e3','e5f6','e3h6','f6e5','h6e3','e5d5','e3d3']
    # moves3 = ['d5e5','d3d2','e5e4','d2e2','e4d5','e2d3']
    # moves33 = ['d5e5','d3d2','e5e4','d2e2','e4d5','e2d3']
    # for moves in (moves1, moves2, moves33):
    #     for uci_move in moves:
    #         previous_move = uci_move_to_move_object(uci_move, is_white, board)
    #         if moves == moves33:
    #             print(previous_move.__class__.__name__)
    #         previous_move.do_move(board)
    #         is_white = not is_white
    #     print(board.current_hash)

    moves = ['d2d4','g7g6','e2e4','f8g7','g1e2','g8f6','d1d3','b8c6','c2c3','e8g8','c1g5','d7d6','h2h4','h7h6','g5d2','d6d5','f2f3','e7e5','e4d5','f6d5','d2h6','g7h6','d4e5','c6e5','d3e4','f8e8','e4d4','h6e3','d4d1','c8f5','c3c4','e5d3','d1d3','f5d3','c4d5','d8d5','b1c3','d5d6','a1d1','e3b6','a2a4','b6a5','f3f4','d6d5','d1d2','a5c3','b2c3','d5c4','h1h3','d3e2','f1e2','c4a4','h3f3','a4c4','g2g3','a7a6','e1f2','c4c5','f2f1','e8e3','d2c2','e3f3','e2f3','a8d8','f1g2','d8b8','g3g4','c5e3','f4f5','e3d3','c2f2','g6f5','g4f5','d3f5','f2d2','f5f6','d2d4','g8h8','d4c4','b8g8','c4g4','g8g4','f3g4','f6h4','g2f3','h4f6','f3e4','f6c3','g4c8','h8g8','e4d5','c3d3','d5e5','d3e3','e5f6','e3h6','f6e5','h6e3','e5d5','e3d3','d5e5','d3d2','e5e4','d2e2','e4d5']
    for uci_move in moves:
        previous_move = uci_move_to_move_object(uci_move, is_white, board)
        previous_move.do_move(board)
        is_white = not is_white
    start = time.time()
    best_move_uci = play_turn(board, move_to_uci_move(previous_move), is_white, 200, 50)
    print('time taken: ' + str(time.time() - start))
    print('bestmove ' + best_move_uci)
    # pr.print_stats(sort="tottime")



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
                if board.is_the_king_attacked(is_engine_white):
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
    play_uci()
    #debug_position()
    #play_on_console()
