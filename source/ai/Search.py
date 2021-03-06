from move.MoveUtils import move_to_uci_move, NONE, equals_inverted_uci
from board.Pieces import Pieces, promotion_color_to_value
from ai.Evaluation import piece_value_to_placement_score, queen_placement_score_middle_white, queen_placement_score_middle_black, evaluate
import time

max_utility = 999999
count = -1
transposition_count = -1
transposition_table = {}  # {hash: (depth, score, best_move, turn)}
can_use_hard_coded = True


def play_turn(board, opponents_uci_move, is_engine_white, time_left_sec, turn, last_3_moves):
    if turn == 10:  # entering middle game
        piece_value_to_placement_score[promotion_color_to_value[('q', True)]] = queen_placement_score_middle_white
        piece_value_to_placement_score[promotion_color_to_value[('q', False)]] = queen_placement_score_middle_black
    global can_use_hard_coded
    if turn <= 3 and can_use_hard_coded:
        hard_coded_move = get_hard_coded_opening_move(board, is_engine_white, turn)
        if hard_coded_move != 'stop_using_hardcoded':
            return hard_coded_move
    return search_best_move(board, is_engine_white, opponents_uci_move, time_left_sec, last_3_moves)


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


def search_best_move(board, is_engine_white, opponents_uci_move, time_left_sec, last_3_moves):
    moves = board.get_all_moves(is_engine_white, opponents_uci_move)
    if len(moves) == 1:  # move is forced, skip evaluation
        return move_to_uci_move(moves[0])
    else:
        start, depth_max = time.time(), 1
        best_move = 'no move'
        maximum_depth = 5 if time_left_sec > 60 else 4
        while depth_max <= maximum_depth or (time_left_sec > 60 and time.time() - start < 0.9) or (time_left_sec > 40 and time.time() - start < 0.7) or (time_left_sec > 20 and time.time() - start < 0.5):
            best_move, _evaluation = alpha_beta(board, opponents_uci_move, is_engine_white, -max_utility, max_utility, depth_max, depth_max, last_3_moves)
            depth_max += 1
        if best_move == NONE:
            if len(moves) == 0:
                return NONE
            return move_to_uci_move(moves[0])
        return best_move


def alpha_beta(board, opponents_uci_move, is_white, alpha, beta, depth, depth_max, last_3_moves):
    did_enemy_cancel_his_move = equals_inverted_uci(last_3_moves[0], last_3_moves[2])
    if board.current_hash in transposition_table:
        entry = transposition_table[board.current_hash]
        if entry[0] >= depth:
            return entry[2], entry[1]
        best_move_calculated = entry[2]
    else:
        best_move_calculated = NONE
    if depth == 0:
        evaluation = evaluate(board.board)
        transposition_table[board.current_hash] = (depth, evaluation, NONE)
        return NONE, evaluation
    moves = board.get_all_moves(is_white, opponents_uci_move)
    if best_move_calculated != NONE:
        moves.insert(0, best_move_calculated)  # search best move found earlier first (+ duplicate move, but no problem because the transposition table is used)
    memo_move = last_3_moves.popleft()
    store_in_transposition_table = True
    if is_white:
        best_val, best_move = -max_utility, NONE
        for move in moves:
            uci_move = move_to_uci_move(move)
            if did_enemy_cancel_his_move and equals_inverted_uci(last_3_moves[0], uci_move):  # to avoid stalemate by threefold repetition while winning
                val = 0
                store_in_transposition_table = False
            else:
                move.do_move(board)
                last_3_moves.append(uci_move)
                _, val = alpha_beta(board, uci_move, not is_white, alpha, beta, depth - 1, depth_max, last_3_moves)
                last_3_moves.pop()
                move.undo_move(board)
                store_in_transposition_table = True
            if val > best_val:
                best_val, best_move = val, move
            alpha = max(alpha, best_val)
            if alpha >= beta:
                break
    else:
        best_val, best_move = +max_utility, NONE
        for move in moves:
            uci_move = move_to_uci_move(move)
            if did_enemy_cancel_his_move and equals_inverted_uci(last_3_moves[0], uci_move):
                val = 0
                store_in_transposition_table = False
            else:
                move.do_move(board)
                last_3_moves.append(uci_move)
                _, val = alpha_beta(board, uci_move, not is_white, alpha, beta, depth - 1, depth_max, last_3_moves)
                last_3_moves.pop()
                move.undo_move(board)
                store_in_transposition_table = True
            if val < best_val:
                best_val, best_move = val, move
            beta = min(beta, best_val)
            if beta <= alpha:
                break
    last_3_moves.appendleft(memo_move)
    if best_move == NONE and not board.is_king_attacked(is_white):
        best_val = 0  # not + or - max_utility because it is a pat!
    if store_in_transposition_table:
        transposition_table[board.current_hash] = (depth, best_val, best_move)
    return move_to_uci_move(best_move), best_val


def visit_node():
    global count
    count += 1
    return count


def use_transposition_table():
    global transposition_count
    transposition_count += 1
    return transposition_count
