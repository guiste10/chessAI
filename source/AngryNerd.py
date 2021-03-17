from board.BoardPositions import init_normal_board, init_attack_board
from move.MoveUtils import do_uci_move
from ai import Search
from ai.Search import play_turn, visit_node, transposition_table, use_transposition_table
import time
from collections import deque


import logging
from pathlib import Path


def play_uci():
    Path("venv/logs").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename='venv/logs/uci.log', level=logging.DEBUG)
    logging.debug('engine started executing')
    board, previous_uci_move = init_normal_board()
    is_white, Search.can_use_hard_coded, turn = True, True, 1
    quit_now = False
    while not quit_now:
        line = input()
        logging.debug(line)
        line = line.rstrip()
        if line == 'uci':
            print('id name Angry Nerd', flush=True)
            print('id author Guillaume Neirinckx', flush=True)
            print('uciok', flush=True)
        elif line == 'ucinewgame':
            board, previous_uci_move = init_normal_board()
            Search.can_use_hard_coded, turn = True, 1
        elif line == 'isready':
            print('readyok', flush=True)
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
                print('bestmove ' + best_move_uci, flush=True)
                transposition_table.clear()
                board, previous_uci_move = init_normal_board()
                turn += 1


def debug_position():
    board, previous_uci_move = init_normal_board()
    is_white = True
    moves = ['d2d4','g7g6','c2c4','f8g7','e2e3','g8f6','b1c3','b8c6','d4d5','c6e5','d1d4','d7d6','b2b3','f6h5','c1b2','e5g4','d4d2','e7e6','d5e6','c8e6','c3d5','g7b2','a1d1','b2g7','h2h3','g4e5','d2a5','e5c6','a5b5','e8g8','g1e2','a8b8','b5a4','f8e8','e2c3','b8c8','a4b5','c8b8','f1e2','d8g5','b5a4','g5g2','e1d2','g7c3','d2c3','e6d5','c4d5','b7b5','a4h4','e8e4','d1g1','g2g1','h4e4','g1f2','e4f3','f2f3','e2f3','c6e7','b3b4','h5g3','h1e1','b8e8','e1g1','g3f5','c3d2','f5h4','f3e4','f7f5','e4g2','h4g2','g1g2','e7d5','a2a3','d5e3','g2g5','e8e4','d2c3','d6d5','c3d3','e3c4','g5g3']
    for uci_move in moves:
        do_uci_move(uci_move, board, is_white)
        is_white = not is_white
    start = time.time()
    best_move_uci = play_turn(board, previous_uci_move, is_white, 200, 50)
    print('time taken: ' + str(time.time() - start))
    #print('bestmove ' + best_move_uci)


def play_on_console():
    print("Engine started", "\n")
    # turn, (board, opponents_uci_move) = 10, init_normal_board()
    turn, (board, opponents_uci_move), Search.can_use_hard_coded = 4, init_attack_board(), False
    print(board)
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
            transposition_table.clear()
        print(board)
        n += 1


def print_stats(time_dif, turn):
    if turn > 3:
        print('Time: ' + str(time_dif))
        print('#nodes: ' + str(visit_node()))
        print('#nodes/sec: ' + str(visit_node() // time_dif) + '\n')
        # print('# transposition table hits: ' + str(use_transposition_table()) + '\n')


if __name__ == "__main__":
    #debug_position()
    #play_on_console()
    play_uci()