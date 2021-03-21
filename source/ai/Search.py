from __future__ import print_function
from move.MoveUtils import move_to_uci_move, NONE
from board.Pieces import Pieces, promotion_color_to_value
from Evaluation import piece_value_to_placement_score, queen_placement_score_middle_white, queen_placement_score_middle_black, evaluate
import time
from collections import deque
import itertools

max_utility = 999999
count = -1
transposition_count = -1
transposition_table = {}  # {hash: (depth, score, best_move)}
can_use_hard_coded = True
EXACT, LOWERBOUND, UPPERBOUND = 0, -1, 1


def play_turn(board, opponents_uci_move, is_engine_white, time_left_sec, turn):
    if turn == 10:  # to do access turn with board.turn instead  # entering middle game
        piece_value_to_placement_score[promotion_color_to_value[('q', True)]] = queen_placement_score_middle_white
        piece_value_to_placement_score[promotion_color_to_value[('q', False)]] = queen_placement_score_middle_black
    global can_use_hard_coded
    if turn <= 3 and can_use_hard_coded:
        hard_coded_move = get_hard_coded_opening_move(board, is_engine_white, turn)
        if hard_coded_move != 'stop_using_hardcoded':
            return hard_coded_move
    previous_two_evals = deque([0, 0], maxlen=2)
    return search_best_move(board, is_engine_white, opponents_uci_move, time_left_sec, previous_two_evals)


def search_best_move(board, is_engine_white, opponents_uci_move, time_left_sec, previous_two_evals):
    start, depth_max, best_move = time.time(), 1, 'no move'
    maximum_depth = 6 if time_left_sec > 60 else 5
    #maximum_depth = 6
    while can_increase_time(depth_max, maximum_depth, time_left_sec, start) :
    #while depth_max <= maximum_depth:
        #best_eval, best_move = normal_search(board, depth_max, is_engine_white, opponents_uci_move)
        best_eval, best_move = mtdf_search(board, depth_max, is_engine_white, opponents_uci_move, previous_two_evals)
        previous_two_evals.append(best_eval)
        print("Nodes: " + str(visit_node()) + " table size: " + str(len(transposition_table)))
        print("Depth " + str(depth_max) + " move: " + move_to_uci_move(best_move) + " score: " + str(previous_two_evals[-1]))
        depth_max += 1
    transposition_table.clear()
    if best_move == 'none':
        best_move = board.get_all_moves(is_engine_white, opponents_uci_move)[0]
    return move_to_uci_move(best_move)

def can_increase_time(depth_max, maximum_depth, time_left_sec, start):
    time_elapsed = time.time() - start
    return depth_max <= maximum_depth or ((time_left_sec > 60 and time_elapsed < 0.7) or (time_left_sec > 40 and time_elapsed < 0.5) or (time_left_sec > 20 and time_elapsed < 0.4)) and depth_max < 15

def mtdf_search(board, depth_max, is_engine_white, opponents_uci_move, previous_two_evals):
    evaluation, g = evaluate(board.board), previous_two_evals[0]  # two plies ago
    lower_bound, upper_bound = -max_utility, max_utility
    while lower_bound < upper_bound:
        beta = g + 1 if g == lower_bound else g
        g = alpha_beta_bounds(board, opponents_uci_move, is_engine_white, beta - 1, beta, depth_max, evaluation)
        if g < beta:
            upper_bound = g
        else:
            lower_bound = g
    return g, transposition_table[board.current_hash][2]


def alpha_beta_bounds(board, opponents_uci_move, is_white, alpha, beta, depth, current_eval):
    # transposition_table : {K = hash, V = (depth, score, best_move, type)}
    visit_node()
    if board.current_hash in transposition_table:
        entry = transposition_table[board.current_hash]
        if entry[0] >= depth:
            use_transposition_table()
            entry = transposition_table[board.current_hash]
            if entry[3] == LOWERBOUND:
                if entry[1] >= beta:
                    return entry[1]
                alpha = max(alpha, entry[1])
            if entry[3] == UPPERBOUND:
                if entry[1] <= alpha:
                    return entry[1]
                beta = min(beta, entry[1])
        best_move_calculated = entry[2]
    else:
        best_move_calculated = NONE
    if depth == 0 or current_eval < -20000 or current_eval > 20000:
        best_move = NONE
        g = current_eval
    else:
        moves = board.get_all_moves(is_white, opponents_uci_move)
        if best_move_calculated != NONE:
            moves = itertools.chain([best_move_calculated], moves)
        if is_white:
            g, best_move, memo_hash = -max_utility-1, NONE, board.current_hash
            for move in moves:
                if g >= beta:
                    break
                val = alpha_beta_bounds(board, move_to_uci_move(move), not is_white, alpha, beta, depth - 1, move.do_move(board, current_eval))
                move.undo_move(board)
                board.current_hash = memo_hash
                if val > g:
                    g, best_move = val, move
        else:
            g, best_move, memo_hash = max_utility+1, NONE, board.current_hash
            for move in moves:
                if g <= alpha:
                    break
                val = alpha_beta_bounds(board, move_to_uci_move(move), not is_white, alpha, beta, depth - 1, move.do_move(board, current_eval))
                move.undo_move(board)
                board.current_hash = memo_hash
                if val < g:
                    g, best_move = val, move
    if best_move == NONE and depth > 0 and not board.is_king_attacked(is_white):
        g = 0  # not + or - max_utility because it is a pat!
    if g <= alpha:
        transposition_table[board.current_hash] = (depth, g, best_move, UPPERBOUND)
    elif g >= beta:
        transposition_table[board.current_hash] = (depth, g, best_move, LOWERBOUND)
    return g











def normal_search(board, depth_max, is_engine_white, opponents_uci_move):
    best_eval = alpha_beta(board, opponents_uci_move, is_engine_white, -max_utility, max_utility, depth_max, evaluate(board.board))
    return best_eval, transposition_table[board.current_hash][2]

def alpha_beta(board, opponents_uci_move, is_white, alpha, beta, depth, current_eval):
    # transposition_table : {K = hash, V = (depth, score, best_move)}

    visit_node()
    if board.current_hash in transposition_table:
        entry = transposition_table[board.current_hash]
        if entry[0] >= depth:
            return entry[1]
        best_move_calculated = entry[2]
    else:
        best_move_calculated = NONE
    if depth == 0 or current_eval < -20000 or current_eval > 20000:
        transposition_table[board.current_hash] = (depth, current_eval, NONE)
        return current_eval
    moves = board.get_all_moves(is_white, opponents_uci_move)
    if best_move_calculated != NONE:
        moves = itertools.chain([best_move_calculated], moves)
    memo_hash = board.current_hash
    if is_white:
        best_val, best_move = -max_utility-1, NONE
        for move in moves:
            uci_move = move_to_uci_move(move)
            val = alpha_beta(board, uci_move, not is_white, alpha, beta, depth - 1, move.do_move(board, current_eval))
            move.undo_move(board)
            board.current_hash = memo_hash
            if val > best_val:
                best_val, best_move = val, move
            alpha = max(alpha, best_val)
            if alpha >= beta:
                break
    else:
        best_val, best_move = max_utility+1, NONE
        for move in moves:
            uci_move = move_to_uci_move(move)
            val = alpha_beta(board, uci_move, not is_white, alpha, beta, depth - 1, move.do_move(board, current_eval))
            move.undo_move(board)
            board.current_hash = memo_hash
            if val < best_val:
                best_val, best_move = val, move
            beta = min(beta, best_val)
            if beta <= alpha:
                break
    if best_move == NONE and not board.is_king_attacked(is_white):
        best_val = 0  # not + or - max_utility because it is a pat!
    transposition_table[board.current_hash] = (depth, best_val, best_move)
    return best_val


def visit_node():
    global count
    count += 1
    return count


def use_transposition_table():
    global transposition_count
    transposition_count += 1
    return transposition_count


def get_hard_coded_opening_move(board, is_white, turn):
    if is_white:
        if turn == 1:
            return 'g1f3'
        elif turn == 2:
            if board.board[5][6] >= 0 and board.board[5][8] >= 0 and board.board[5][9] >= 0:
                return 'g2g3'
        elif turn == 3:
            if board.board[5][6] >= 0 and board.board[5][8] >= 0 and board.board[7][9] >= 0:
                return 'f1g2'
    else:
        if turn == 1:
            return 'g7g6'
        elif turn == 2:
            if board.board[8][3] == Pieces.WB:
                return 'g8f6'  # place knight
            else:
                return 'f8g7'  # place bishop
        elif turn == 3 and not board.is_king_attacked(is_white):
            if board.board[3][8] == Pieces.BB:  # black bishop placed
                if board.board[5][6] != Pieces.WP and board.board[5][8] != Pieces.WP:
                    return 'g8f6'  # place knight
            else:  # black knight is already placed on f6
                if board.board[5][6] != Pieces.WP and board.board[5][8] != Pieces.WP:
                    return 'f8g7'  # place bishop
    global can_use_hard_coded
    can_use_hard_coded = False
    return 'stop_using_hardcoded'