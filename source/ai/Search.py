from move.MoveUtils import move_to_uci_move, NONE, equals_inverted_uci
from board.Pieces import Pieces, promotion_color_to_value
from ai.Evaluation import piece_value_to_placement_score, queen_placement_score_middle_white, queen_placement_score_middle_black, evaluate
import time
from collections import deque
import itertools

max_utility = 999999
count = -1
transposition_count = -1
transposition_table = {}  # {hash: (depth, score, best_move)}
can_use_hard_coded = True


def play_turn(board, opponents_uci_move, is_engine_white, time_left_sec, turn, last_8_moves):
    # if turn == 10: to do access turn with board.turn instead  # entering middle game
    #     piece_value_to_placement_score[promotion_color_to_value[('q', True)]] = queen_placement_score_middle_white
    #     piece_value_to_placement_score[promotion_color_to_value[('q', False)]] = queen_placement_score_middle_black
    global can_use_hard_coded
    if turn <= 3 and can_use_hard_coded:
        hard_coded_move = get_hard_coded_opening_move(board, is_engine_white, turn)
        if hard_coded_move != 'stop_using_hardcoded':
            return hard_coded_move
    previous_two_evals = deque([0, 0], maxlen=2)
    return search_best_move(board, is_engine_white, opponents_uci_move, time_left_sec, last_8_moves, previous_two_evals, turn)


def search_best_move(board, is_engine_white, opponents_uci_move, time_left_sec, last_8_moves, previous_two_evals, turn):
    moves = board.get_all_moves(is_engine_white, opponents_uci_move)
    start, depth_max, best_move = time.time(), 1, 'no move'
    maximum_depth = 6 if time_left_sec > 60 else 5
    while can_increase_time(depth_max, maximum_depth, time_left_sec, start, turn) :
        previous_two_evals, best_move = aspiration_search(board, depth_max, is_engine_white, last_8_moves, opponents_uci_move, previous_two_evals)
        # print("Depth " + str(depth_max) + " score " + str(previous_two_evals[-1]))
        depth_max += 1
    if best_move == NONE:
        return move_to_uci_move(next(moves))
    return move_to_uci_move(best_move)

def can_increase_time(depth_max, maximum_depth, time_left_sec, start, turn):
    return depth_max <= maximum_depth or ((time_left_sec > 60 and time.time() - start < 0.7) or (time_left_sec > 40 and time.time() - start < 0.5) or (time_left_sec > 20 and time.time() - start < 0.4)) and depth_max < 15


def aspiration_search1(board, depth_max, is_engine_white, last_3_moves, opponents_uci_move, previous_two_evals):
    delta_left = delta_right = 25
    previous_eval = previous_two_evals[0]
    while True:
        lower_bound, upper_bound = previous_eval - delta_left, previous_eval + delta_right
        best_eval = alpha_beta(board, opponents_uci_move, is_engine_white, lower_bound, upper_bound, depth_max, last_3_moves, evaluate(board.board))
        best_move = transposition_table[board.current_hash][2]
        if lower_bound <= best_eval <= upper_bound:
            break
        if lower_bound > best_eval:  # fail low
            delta_left = delta_left * 3
        else:  # fail high
            delta_right = delta_right * 3
    previous_two_evals.append(best_eval)
    return previous_two_evals, best_move

def aspiration_search(board, depth_max, is_engine_white, last_3_moves, opponents_uci_move, previous_two_evals):
    best_eval = alpha_beta(board, opponents_uci_move, is_engine_white, -max_utility, max_utility, depth_max, last_3_moves, evaluate(board.board))
    previous_two_evals.append(best_eval)
    best_move = transposition_table[board.current_hash][2]
    return previous_two_evals, best_move


def alpha_beta(board, opponents_uci_move, is_white, alpha, beta, depth, last_8_moves, current_eval):
    # visit_node()
    if equals_inverted_uci(last_8_moves[0], last_8_moves[2]) and equals_inverted_uci(last_8_moves[1], last_8_moves[3]) and equals_inverted_uci(last_8_moves[2],
                                                                                                                                               last_8_moves[4]) and equals_inverted_uci(last_8_moves[3],
                                                                                                                                                                                        last_8_moves[
                                                                                                                                                                                            5]) and equals_inverted_uci(
        last_8_moves[4], last_8_moves[6]) and equals_inverted_uci(last_8_moves[5], last_8_moves[7]):
        return 0  # stalemate by threefold repetition
    elif board.current_hash in transposition_table:
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
    memo_move, memo_hash = last_8_moves.popleft(), board.current_hash
    if is_white:
        best_val, best_move = -max_utility, NONE
        for move in moves:
            uci_move = move_to_uci_move(move)
            last_8_moves.append(uci_move)
            val = alpha_beta(board, uci_move, not is_white, alpha, beta, depth - 1, last_8_moves, move.do_move(board, current_eval))
            move.undo_move(board)
            board.current_hash = memo_hash
            last_8_moves.pop()
            if val > best_val:
                best_val, best_move = val, move
            alpha = max(alpha, best_val)
            if alpha >= beta:
                break
    else:
        best_val, best_move = +max_utility, NONE
        for move in moves:
            uci_move = move_to_uci_move(move)
            last_8_moves.append(uci_move)
            val = alpha_beta(board, uci_move, not is_white, alpha, beta, depth - 1, last_8_moves, move.do_move(board, current_eval))
            move.undo_move(board)
            board.current_hash = memo_hash
            last_8_moves.pop()
            if val < best_val:
                best_val, best_move = val, move
            beta = min(beta, best_val)
            if beta <= alpha:
                break
    last_8_moves.appendleft(memo_move)
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
