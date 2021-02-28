from BoardPositions import init_normal_board, init_attack_board
from move.MoveUtils import do_uci_move, move_to_uci_move
import Ai
from Ai import play_turn, visit_node, transposition_table, use_transposition_table
import time
from collections import deque


import logging
from pathlib import Path


def play_uci():
    Path("venv/logs").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename='venv/logs/uci.log', level=logging.DEBUG)
    logging.debug('engine started executing')
    board, previous_uci_move = init_normal_board()
    is_white, Ai.can_use_hard_coded, turn = True, True, 1
    quit_now = False
    last_3_moves = deque(['none', 'none', 'none'], maxlen=3)
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
            Ai.can_use_hard_coded, turn = True, 1
            last_3_moves = deque(['none', 'none', 'none'], maxlen=3)
        elif line == 'isready':
            print('readyok', flush=True)
        elif line == 'quit':
            quit_now = True
        else:
            line_splitted = line.split()
            if line_splitted[0] == 'position' and line_splitted[1] == 'startpos' and len(line_splitted) > 2:
                is_white = True
                if len(line_splitted) > 3:
                    uci_moves = line_splitted[3:]
                    for uci_move in uci_moves:
                        last_3_moves.append(uci_move)
                        do_uci_move(uci_move, board, is_white)
                        is_white, previous_uci_move = not is_white, uci_move

            elif line_splitted[0] == 'go':
                if len(line_splitted) >= 5:
                    time_left_sec = int(line_splitted[2])/1000 if is_white else int(line_splitted[4])/1000
                else:
                    time_left_sec = 99999999
                best_move_uci = play_turn(board, previous_uci_move, is_white, time_left_sec, turn, last_3_moves)
                print('bestmove ' + best_move_uci, flush=True)
                transposition_table.clear()
                board, previous_uci_move = init_normal_board()
                turn += 1


def debug_position():
    board, previous_uci_move = init_normal_board()
    last_3_moves = deque(['none', 'none', 'none'], maxlen=3)
    is_white = True
    moves = ['g1f3','e7e6','g2g3','d7d5','f1g2','g8f6','a2a3','c7c5','e1g1','b8c6','d2d3','b7b6','b1c3','e6e5','c1g5','h7h6','g5f6','g7f6','e2e4','c6e7','c3d5','e7g6','b2b4','c8b7','b4c5','b6c5','d5e3','h6h5','f1e1','h5h4','d1b1','d8d7','f3h4','a8b8','h4g6','h8h7','g6f8','e8f8']

    for move in moves:
        do_uci_move(move, board, is_white)
        is_white = not is_white
    best_move = play_turn(board, previous_uci_move, is_white, 9999, 50, last_3_moves)
    best_move_uci = move_to_uci_move(best_move)
    print('bestmove ' + best_move_uci)


def play_on_console():
    turn, Ai.can_use_hard_coded = 1, False
    last_3_moves = deque(['none', 'none', 'none'], maxlen=3)
    print("Engine started", "\n")
    #board, opponents_uci_move = init_normal_board()
    board, opponents_uci_move = init_attack_board()
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
            last_3_moves.append(opponents_uci_move)
            do_uci_move(opponents_uci_move, board, not is_engine_white)
        else:
            # import cProfile
            # pr = cProfile.Profile()
            # pr.enable()
            print("\nEngine's Turn:")
            start = time.time()
            best_move_uci = play_turn(board, opponents_uci_move, is_engine_white, 9999, turn, last_3_moves)
            last_3_moves.append(best_move_uci)
            # pr.print_stats(sort="cumtime")
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
        print('# transposition table hits: ' + str(use_transposition_table()) + '\n')


if __name__ == "__main__":
    #debug_position()
    #play_on_console()
    play_uci()

