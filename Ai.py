from move.MoveUtils import move_to_uci_move
import Evaluation
import time

max_utility = 999999
maximum_depth = 4  # not counting evaluation nodes (e.g. for maximum_depth = 4: max (at depth 0),min,max,min,evaluate (at depth 4))
count = -1
transposition_count = -1


def get_best_move(board, opponents_uci_move, is_engine_white):
    best_move = 'no move'
    best_score = 0
    transposition_table = {}  # {hash: (depth, score, best_move)}
    start = time.time()
    depth_max = 1
    while depth_max <= maximum_depth or (time.time()-start) < 1:
        best_move, best_score = alpha_beta(board, opponents_uci_move, is_engine_white, -max_utility, max_utility, depth_max, depth_max, transposition_table)
        depth_max += 1

    transposition_table.clear()
    if best_move == 'none':
        moves = board.get_color_moves(is_engine_white, opponents_uci_move)
        if len(moves) == 0:
            return 'none', 0
        return moves[0], 0
    return best_move, best_score


def alpha_beta(board, opponents_uci_move, is_engine_white, alpha, beta, depth, depth_max, transposition_table):
    if board.current_hash in transposition_table:
        if transposition_table[board.current_hash][0] >= depth:
            use_transposition_table()
            return transposition_table[board.current_hash][2], transposition_table[board.current_hash][1]
        best_move_calculated = transposition_table[board.current_hash][2]
    else:
        best_move_calculated = 'none'
    visit_node()
    if depth == 0:
        evaluation = Evaluation.evaluate(board.board)
        transposition_table[board.current_hash] = (depth, evaluation, 'none')
        return 'none', evaluation
    moves = board.get_color_moves(is_engine_white, opponents_uci_move)
    if len(moves) == 1 and depth == depth_max:  # engine's first move is forced
        return moves[0], 0
    if best_move_calculated != 'none':
        moves.insert(0, best_move_calculated)  # search best move found earlier first (+ duplicate move)

    if is_engine_white:
        best_val, best_move = -max_utility, 'none'
        for move in moves:
            uci_move = move_to_uci_move(move)
            move.do_move(board)
            _, val = alpha_beta(board, uci_move, not is_engine_white, alpha, beta, depth - 1, depth_max, transposition_table)
            move.undo_move(board)
            if val > best_val:
                best_val, best_move = val, move
            alpha = max(alpha, best_val)
            if alpha >= beta:
                break
    else:
        best_val, best_move = +max_utility, 'none'
        for move in moves:
            uci_move = move_to_uci_move(move)
            move.do_move(board)
            _, val = alpha_beta(board, uci_move, not is_engine_white, alpha, beta, depth - 1, depth_max, transposition_table)
            move.undo_move(board)
            if val < best_val:
                best_val, best_move = val, move
            beta = min(beta, best_val)
            if beta <= alpha:
                break
    if best_move == 'none' and not board.is_king_attacked(is_engine_white):
        best_val = 0  # not + or - max_utility because it is a pat!
    transposition_table[board.current_hash] = (depth, best_val, best_move)
    return best_move, best_val


def visit_node():
    global count
    count += 1
    return count


def use_transposition_table():
    global transposition_count
    transposition_count += 1
    return transposition_count
