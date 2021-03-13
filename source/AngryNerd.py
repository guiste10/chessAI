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
    last_4_moves = deque(['none', 'none', 'none', 'none'], maxlen=4)
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
            last_4_moves = deque(['none', 'none', 'none', 'none'], maxlen=4)
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
                        last_4_moves.append(uci_move)
                        do_uci_move(uci_move, board, is_white)
                        is_white, previous_uci_move = not is_white, uci_move

            elif line_splitted[0] == 'go':
                if len(line_splitted) >= 5:
                    time_left_sec = int(line_splitted[2])/1000 if is_white else int(line_splitted[4])/1000
                else:
                    time_left_sec = 99999999
                best_move_uci = play_turn(board, previous_uci_move, is_white, time_left_sec, turn, last_4_moves)
                print('bestmove ' + best_move_uci, flush=True)
                transposition_table.clear()
                board, previous_uci_move = init_normal_board()
                turn += 1


def debug_position():
    board, previous_uci_move = init_normal_board()
    last_4_moves = deque(['none', 'none', 'none', 'none'], maxlen=4)
    is_white = True
    moves = ['e2e3', 'g7g6', 'g1f3', 'f8g7', 'b1c3', 'g8f6', 'e3e4', 'b7b5', 'f1b5']
    for uci_move in moves:
        last_4_moves.append(uci_move)
        do_uci_move(uci_move, board, is_white)
        is_white = not is_white
    start = time.time()
    best_move_uci = play_turn(board, previous_uci_move, is_white, 200, 50, last_4_moves)
    print('time taken: ' + str(time.time() - start))
    print('bestmove ' + best_move_uci)


def play_on_console():
    last_4_moves = deque(['none', 'none', 'none', 'none'], maxlen=4)
    print("Engine started", "\n")
    #turn, (board, opponents_uci_move) = 1, init_normal_board()
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
            last_4_moves.append(opponents_uci_move)
            do_uci_move(opponents_uci_move, board, not is_engine_white)
        else:
            print("\nEngine's Turn:")
            # import cProfile
            # pr = cProfile.Profile()
            # pr.enable()
            start = time.time()
            best_move_uci = play_turn(board, opponents_uci_move, is_engine_white, 9999, turn, last_4_moves)
            # pr.print_stats(sort="tottime")
            last_4_moves.append(best_move_uci)
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
