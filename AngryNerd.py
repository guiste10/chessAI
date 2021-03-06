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
            if line_splitted[0] == 'position' and line_splitted[1] == 'startpos':
                is_white = True
                if len(line_splitted) > 2:
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
    moves = ['d2d4','g7g6','c2c4','f8g7','g1f3','g8f6','e2e3','e8g8','b1c3','d7d6','f1d3','e7e5','e1g1','e5d4','e3d4','h7h6','b2b3','b8c6','c1b2','c8f5','d3f5','g6f5','f1e1','a8b8','d1d3','d8d7','e1e2','b8d8','a1e1','f5f4','c3e4','f6e4','e2e4','d7g4','h2h3','g4f5','b2c1','d8e8','d3e2','c6d4','f3d4','f5e4','e2e4','e8e4','e1e4','f7f5','e4f4','g7e5','f4h4','e5f6','c1h6','f6h4','h6f8','g8f8','d4f3','h4f6','g1h2','f8g8','g2g3','a7a6','g3g4','f5g4','h3g4','a6a5','g4g5','f6e7','h2g3','g8f7','f3d4','e7g5','f2f4','g5h6','g3g4','f7g8','f4f5','h6e3','d4e6','c7c6','e6d8','b7b5','d8c6','b5c4','b3c4','a5a4','g4h5','g8f7','c6a7','e3a7','h5g4','a7b6','g4f3','f7f6','f3e4','b6c7','e4d5','f6f5','d5c6','c7d8','c6d7','d8f6','d7d6','f6d4','d6d5','d4e3','c4c5','f5f6','c5c6','e3f4','d5c4','f4d6','c4b5','a4a3','b5b6','f6e7','c6c7','e7d7','c7c8q','d7c8','b6b5','c8b8','b5a4','d6c5','a4b5','c5d6','b5a4','d6c5','a4b5']
    for uci_move in moves:
        last_3_moves.append(uci_move)
        do_uci_move(uci_move, board, is_white)
        is_white = not is_white
    best_move_uci = play_turn(board, previous_uci_move, is_white, 20, 50, last_3_moves)
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
    play_on_console()
    #play_uci()
