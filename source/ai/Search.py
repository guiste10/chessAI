from __future__ import print_function
from move.MoveUtils import move_to_uci_move
from move.Moves import NullMove
from board.Pieces import Pieces, promotion_color_to_value
from Evaluation import piece_value_to_placement_score, queen_placement_score_middle_white, queen_placement_score_middle_black, king_placement_score_end_white, king_placement_score_end_black, \
    pawn_placement_score_end_white, pawn_placement_score_end_black, bishop_placement_score_end_white, bishop_placement_score_end_black
import time
from collections import deque
import itertools

max_utility = 999999
count = -1
transposition_table = {}  # {hash: (depth, score, best_move)}
can_use_hard_coded = True
EXACT, LOWERBOUND, UPPERBOUND = 0, -1, 1
THREEFOLD_REPETITION = 3


def play_turn(board, opponents_uci_move, is_engine_white, time_left_sec, turn):
    if turn == 10:
        piece_value_to_placement_score[promotion_color_to_value[('q', True)]] = queen_placement_score_middle_white
        piece_value_to_placement_score[promotion_color_to_value[('q', False)]] = queen_placement_score_middle_black
        piece_value_to_placement_score[promotion_color_to_value[('b', True)]] = bishop_placement_score_end_white
        piece_value_to_placement_score[promotion_color_to_value[('b', False)]] = bishop_placement_score_end_black
    if board.is_end_game():  # to do access turn with board.turn instead  # entering middle game
        piece_value_to_placement_score[promotion_color_to_value[('k', True)]] = king_placement_score_end_white
        piece_value_to_placement_score[promotion_color_to_value[('k', False)]] = king_placement_score_end_black
        piece_value_to_placement_score[promotion_color_to_value[('p', True)]] = pawn_placement_score_end_white
        piece_value_to_placement_score[promotion_color_to_value[('p', False)]] = pawn_placement_score_end_black
    global can_use_hard_coded
    if turn <= 3 and can_use_hard_coded:
        hard_coded_move = get_hard_coded_opening_move(board, is_engine_white, turn)
        if hard_coded_move != 'stop_using_hardcoded':
            return hard_coded_move
    previous_two_evals = deque([0, 0], maxlen=2)
    return search_best_move(board, is_engine_white, opponents_uci_move, time_left_sec, previous_two_evals)


def search_best_move(board, is_engine_white, opponents_uci_move, time_left_sec, previous_two_evals):
    start, depth_max, best_move, best_eval, zugzwang_danger = time.time(), 1, None, 0, board.zugzwang_danger()
    # depth_max = 2
    # maximum_depth = 2
    maximum_depth = 6 if time_left_sec > 10 else 4
    #while depth_max <= maximum_depth:
    while can_increase_time(depth_max, maximum_depth, time_left_sec, start, best_eval):
        best_eval, best_move = mtdf_search(board, depth_max, is_engine_white, opponents_uci_move, previous_two_evals, zugzwang_danger)
        #best_eval, best_move = normal_search(board, depth_max, is_engine_white, opponents_uci_move, zugzwang_danger)
        previous_two_evals.append(best_eval)
        print("Nodes: " + str(visit_node()) + " table size: " + str(len(transposition_table)))
        if best_move:
            print("Depth " + str(depth_max) + " move: " + move_to_uci_move(best_move) + " score: " + str(previous_two_evals[-1]))
        depth_max += 1
    from AngryNerd import print_f
    print_f("info depth " + str(depth_max-1) + " score " + str(best_eval))
    transposition_table.clear()
    if best_move is None:
        best_move = board.get_all_moves(is_engine_white, opponents_uci_move)[0]
    return move_to_uci_move(best_move)


def can_increase_time(depth_max, maximum_depth, time_left_sec, start, best_eval):
    time_elapsed = time.time() - start
    return (depth_max <= maximum_depth or
           (time_left_sec > 30 and time_elapsed < 0.7)) \
           and depth_max < 20 and -30000 < best_eval < 30000


def mtdf_search(board, depth_max, is_engine_white, opponents_uci_move, previous_two_evals, zugzwang_danger):
    lower_bound, upper_bound, g = -max_utility, max_utility, previous_two_evals[0]
    while lower_bound < upper_bound:
        gamma = g + 1 if g == lower_bound else g
        g = alpha_beta_bounds(board, opponents_uci_move, is_engine_white, gamma, depth_max, zugzwang_danger, True)
        if g < gamma:
            upper_bound = g
        else:
            lower_bound = g
    return g, transposition_table[board.current_hash][2]


def alpha_beta_bounds(board, opponents_uci_move, is_white, gamma, depth, zugzwang_danger, is_root=False):
    # transposition_table : {K = hash, V = (depth, score, best_move, type)}
    visit_node()
    if board.current_hash in board.history and board.history[board.current_hash] == THREEFOLD_REPETITION:
        return 0
    if board.current_hash in transposition_table:
        entry = transposition_table[board.current_hash]
        if entry[0] >= depth:
            entry = transposition_table[board.current_hash]
            if entry[3] == LOWERBOUND:
                if entry[1] >= gamma:
                    return entry[1]
                gamma = max(gamma - 1, entry[1]) + 1
            if entry[3] == UPPERBOUND:
                if entry[1] <= gamma - 1:
                    return entry[1]
                gamma = min(gamma, entry[1])
        best_move_calculated = entry[2]
    else:
        best_move_calculated = None
    if depth <= 0 or board.current_eval < -20000 or board.current_eval > 20000:
        g, best_move = board.current_eval, None
    else:
        moves = board.get_all_moves(is_white, opponents_uci_move, depth)
        if best_move_calculated is not None:
            moves = itertools.chain([best_move_calculated], moves)

        best_move, memo_hash, memo_eval = None, board.current_hash, board.current_eval
        if depth > 0 and not is_root and not board.is_king_attacked and not zugzwang_danger:  # do null move
            null_move = NullMove(is_white)
            null_move.do_move(board)
            g = alpha_beta_bounds(board, None, not is_white, gamma, depth - 3, zugzwang_danger)
            null_move.undo_move(board)
        else:
            g = -max_utility if is_white else max_utility
        #g = -max_utility if is_white else max_utility
        if is_white:
            for move in moves:
                if g >= gamma:
                    break
                move.do_move(board)
                val = alpha_beta_bounds(board, move_to_uci_move(move), not is_white, gamma, depth - 1, zugzwang_danger)
                move.undo_move(board)
                board.current_hash, board.current_eval = memo_hash, memo_eval
                if val > g:
                    g, best_move = val, move
        else:
            for move in moves:
                if g <= gamma - 1:
                    break
                move.do_move(board)
                val = alpha_beta_bounds(board, move_to_uci_move(move), not is_white, gamma, depth - 1, zugzwang_danger)
                move.undo_move(board)
                board.current_hash, board.current_eval = memo_hash, memo_eval
                if val < g:
                    g, best_move = val, move
    if max_utility == abs(g) and depth > 0 and not board.is_king_attacked:
        g = 0  # not + or - max_utility, it is a pat!
    if g < gamma:
        transposition_table[board.current_hash] = (depth, g, best_move, UPPERBOUND)
    else:
        transposition_table[board.current_hash] = (depth, g, best_move, LOWERBOUND)
    return g


def visit_node():
    global count
    count += 1
    return count


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
        elif turn == 3 and not board.is_the_king_attacked(is_white):
            if board.board[3][8] == Pieces.BB:  # black bishop placed
                if board.board[5][6] != Pieces.WP and board.board[5][8] != Pieces.WP:
                    return 'g8f6'  # place knight
            else:  # black knight is already placed on f6
                if board.board[5][6] != Pieces.WP and board.board[5][8] != Pieces.WP:
                    return 'f8g7'  # place bishop
    global can_use_hard_coded
    can_use_hard_coded = False
    return 'stop_using_hardcoded'



def normal_search(board, depth_max, is_engine_white, opponents_uci_move):
    best_eval = alpha_beta(board, opponents_uci_move, is_engine_white, -max_utility, max_utility, depth_max, True)
    return best_eval, transposition_table[board.current_hash][2]

def alpha_beta(board, opponents_uci_move, is_white, alpha, beta, depth, is_root=False):
    # transposition_table : {K = hash, V = (depth, score, best_move)}
    visit_node()
    if board.current_hash in transposition_table:
        entry = transposition_table[board.current_hash]
        if entry[0] >= depth:
            return entry[1]
        best_move_calculated = entry[2]
    else:
        best_move_calculated = None
    if depth <= 0 or board.current_eval < -20000 or board.current_eval > 20000:
        transposition_table[board.current_hash] = (depth, board.current_eval, None)
        return board.current_eval
    moves = board.get_all_moves(is_white, opponents_uci_move)
    if best_move_calculated is not None:
        moves = itertools.chain([best_move_calculated], moves)
    best_move, memo_hash, memo_eval = None, board.current_hash, board.current_eval
    if depth > 0 and not is_root and not board.is_king_attacked:  # do null move
        null_move = NullMove(is_white)
        null_move.do_move(board)
        g = alpha_beta(board, None, not is_white, alpha, beta, depth - 2)
        null_move.undo_move(board)
    else:
        g = -max_utility if is_white else max_utility
    if is_white:
        for move in moves:
            uci_move = move_to_uci_move(move)
            move.do_move(board)
            val = alpha_beta(board, uci_move, not is_white, alpha, beta, depth - 1)
            move.undo_move(board)
            board.current_hash, board.current_eval = memo_hash, memo_eval
            if val > g:
                g, best_move = val, move
            alpha = max(alpha, g)
            if alpha >= beta:
                break
    else:
        g = max_utility
        for move in moves:
            uci_move = move_to_uci_move(move)
            move.do_move(board)
            val = alpha_beta(board, uci_move, not is_white, alpha, beta, depth - 1)
            move.undo_move(board)
            board.current_hash, board.current_eval = memo_hash, memo_eval
            if val < g:
                g, best_move = val, move
            beta = min(beta, g)
            if beta <= alpha:
                break
    if max_utility == abs(g) and depth > 0 and not board.is_king_attacked:
        g = 0  # not + or - max_utility because it is a pat!
    transposition_table[board.current_hash] = (depth, g, best_move)
    return g
