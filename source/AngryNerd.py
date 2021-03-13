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
    last_8_moves = deque(['none', 'none', 'none', 'none','none', 'none', 'none', 'none'], maxlen=8)
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
            last_8_moves = deque(['none', 'none', 'none', 'none','none', 'none', 'none', 'none'], maxlen=8)
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
                        last_8_moves.append(uci_move)
                        do_uci_move(uci_move, board, is_white)
                        is_white, previous_uci_move = not is_white, uci_move

            elif line_splitted[0] == 'go':
                if len(line_splitted) >= 5:
                    time_left_sec = int(line_splitted[2])/1000 if is_white else int(line_splitted[4])/1000
                else:
                    time_left_sec = 99999999
                best_move_uci = play_turn(board, previous_uci_move, is_white, time_left_sec, turn, last_8_moves)
                print('bestmove ' + best_move_uci, flush=True)
                transposition_table.clear()
                board, previous_uci_move = init_normal_board()
                turn += 1


def debug_position():
    board, previous_uci_move = init_normal_board()
    last_8_moves = deque(['none', 'none', 'none', 'none','none', 'none', 'none', 'none'], maxlen=8)
    is_white = True
    moves = ['g1f3','g8f6','g2g3','d7d5','f1g2','c7c6','e1g1','c8g4','d2d3','b8d7','b1c3','d8b6','c1g5','b6b2','d1d2','e8c8','a1b1','b2a3','e2e4','g4f3','g2f3','d5d4','c3e2','e7e5','d2d1','f8d6','f3g2','c8b8','b1b3','a3a2','d1b1','a2b1','f1b1','d7c5','g3g4','c5b3','b1b3','c6c5','c2c3','h8e8','c3d4','c5d4','f2f4','d8c8','f4e5','d6e5','g5f6','g7f6','b3b2','a7a6','b2d2','e8g8','h2h3','h7h6','d2a2','c8c5','a2b2','c5a5','b2b1','a5a2','g1f2','a2d2','b1b3','h6h5','f2f3','h5g4','h3g4','g8h8','f3f2','h8h2','f2e1','d2a2','e1f1','a2e2','f1e2','h2g2','e2d1','g2g4','d1c2','f6f5','e4f5','g4f4','b3a3','f4f5','a3a5','f5f1','a5e5','f1f2','c2d1','f2f1','d1c2','f1f2']
    for uci_move in moves:
        last_8_moves.append(uci_move)
        do_uci_move(uci_move, board, is_white)
        is_white = not is_white
    start = time.time()
    board.board[9][9] = 5
    best_move_uci = play_turn(board, previous_uci_move, is_white, 200, 50, last_8_moves)
    print('time taken: ' + str(time.time() - start))
    print('bestmove ' + best_move_uci)


def play_on_console():
    last_8_moves = deque(['none', 'none', 'none', 'none','none', 'none', 'none', 'none'], maxlen=8)
    print("Engine started", "\n")
    turn, (board, opponents_uci_move) = 10, init_normal_board()
    #turn, (board, opponents_uci_move), Search.can_use_hard_coded = 4, init_attack_board(), False
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
            last_8_moves.append(opponents_uci_move)
            do_uci_move(opponents_uci_move, board, not is_engine_white)
        else:
            print("\nEngine's Turn:")
            # import cProfile
            # pr = cProfile.Profile()
            # pr.enable()
            start = time.time()
            best_move_uci = play_turn(board, opponents_uci_move, is_engine_white, 9999, turn, last_8_moves)
            # pr.print_stats(sort="tottime")
            last_8_moves.append(best_move_uci)
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
