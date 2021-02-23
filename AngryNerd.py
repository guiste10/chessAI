from BoardPositions import init_normal_board, init_attack_board
from move.MoveUtils import do_uci_move, move_to_uci_move
from Ai import get_best_move, visit_node, use_transposition_table
import time
# import logging
# from pathlib import Path


def play_uci():
    # Path("venv/logs").mkdir(parents=True, exist_ok=True)
    # logging.basicConfig(filename='venv/logs/uci.log', level=logging.DEBUG)
    # logging.debug('engine started executing')
    board, previous_uci_move = init_normal_board()
    is_white = True
    quit_now = False
    while not quit_now:
        line = input()
        # logging.debug(line)
        line = line.rstrip()
        if line == 'uci':
            print('id name Angry Nerd', flush=True)
            print('id author Guillaume Neirinckx', flush=True)
            print('uciok', flush=True)
        elif line == 'ucinewgame':
            board, previous_uci_move = init_normal_board()
            is_white = True
        elif line == 'isready':
            print('readyok', flush=True)
        elif line == 'quit':
            quit_now = True
        else:
            line_splitted = line.split()
            if line_splitted[0] == 'position' and line_splitted[1] == 'startpos':
                board, previous_uci_move = init_normal_board()
                is_white = True
                if len(line_splitted) > 3:
                    uci_moves = line_splitted[3:]
                    for uci_move in uci_moves:
                        do_uci_move(uci_move, board, is_white)
                        is_white, previous_uci_move = not is_white, uci_move

            elif line_splitted[0] == 'go':
                best_move, best_move_val = get_best_move(board, previous_uci_move, is_white)
                best_move_uci = move_to_uci_move(best_move)
                print('bestmove ' + best_move_uci, flush=True)


def debug_position():
    board, previous_uci_move = init_normal_board()
    is_white = True
    moves = ['e2e4','b8c6','g1f3','g8f6','e4e5','f6e4','d2d3','e4c5','d3d4','c5e6','d4d5','e6d4','f3d4','c6e5','b1c3','c7c5','d5c6']
    for move in moves:
        do_uci_move(move, board, is_white)
        is_white = not is_white
    best_move, best_move_val = get_best_move(board, previous_uci_move, is_white)
    best_move_uci = move_to_uci_move(best_move)
    print('bestmove ' + best_move_uci)


def play_on_console():
    print("Engine started", "\n")
    board, opponents_uci_move = init_normal_board()
    #board, opponents_uci_move = init_attack_board()
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
            # import cProfile
            # pr = cProfile.Profile()
            # pr.enable()
            print("\nEngine's Turn:")
            start = time.time()
            best_move, best_move_val = get_best_move(board, opponents_uci_move, is_engine_white)
            # pr.print_stats(sort="cumtime")
            if best_move == 'none':
                game_over = True
                if board.is_king_attacked(is_engine_white):
                    print("\nEngine checkmated !\n")
                else:
                    print("\nStalemate !\n")
            else:
                best_move_uci = move_to_uci_move(best_move)
                time_dif = time.time() - start
                print_stats(best_move_uci, best_move_val, time_dif)
                best_move.do_move(board)
        print(board)
        n += 1


def print_stats(best_move_uci, best_move_val, time_dif):
    print('Time: ' + str(time_dif))
    print('#nodes: ' + str(visit_node()))
    print('#nodes/sec: ' + str(visit_node() // time_dif) + '\n')
    print('# transposition table hits: ' + str(use_transposition_table()) + '\n')
    print('Move: ' + best_move_uci)
    print('Evaluation at bottom node: ' + str(best_move_val) + '\n')



if __name__ == "__main__":
    # debug_position()
    # play_on_console()
    play_uci()
