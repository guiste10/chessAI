from move.MoveUtils import move_to_uci_move
import Evaluation

max_utility = 999999
maximum_depth = 4  # not counting evaluation nodes (e.g. for maximum_depth = 4: max (at depth 0),min,max,min,evaluate (at depth 4))
count = -1
transposition_count = -1


def get_best_move(board, opponents_uci_move, is_engine_white):
    best_move = 'no move'
    transposition_table = {}  # {hash: (depth, score)}
    # for depth_max in range(maximum_depth, maximum_depth + 1):  # debug
    for depth_max in range(1, maximum_depth + 1):
        best_move = alpha_beta_at_root(board, opponents_uci_move, is_engine_white, depth_max, transposition_table)  # print(board.current_hash)
    transposition_table.clear()
    return best_move


def visit_node():
    global count
    count += 1
    return count


def use_transposition_table():
    global transposition_count
    transposition_count += 1
    return transposition_count


def alpha_beta_at_root(board, opponents_uci_move, is_engine_white, depth_max, transposition_table):
    best_move = 'no move'
    best_move_val = -max_utility if is_engine_white else max_utility
    moves = board.get_color_moves(is_engine_white, opponents_uci_move)
    visit_node()
    if len(moves) == 1:
        return move_to_uci_move(moves[0])
    for move in moves:
        move.do_move(board)
        val = alpha_beta(board, opponents_uci_move, not is_engine_white, -max_utility, max_utility, depth_max - 1, transposition_table)
        transposition_table[board.current_hash] = (depth_max-1, val)
        move.undo_move(board)
        if is_engine_white:
            if val > best_move_val:
                best_move, best_move_val = move, val
        else:
            if val < best_move_val:
                best_move, best_move_val = move, val
    return best_move, best_move_val


def alpha_beta(board, opponents_uci_move, is_engine_white, alpha, beta, depth, transposition_table):
    if board.current_hash in transposition_table:
        if transposition_table[board.current_hash][0] >= depth:
            use_transposition_table()
            return transposition_table[board.current_hash][1]
    visit_node()
    if depth == 0:
        return Evaluation.evaluate(board.board)
    if is_engine_white:
        best_val = -max_utility
        moves = board.get_color_moves(is_engine_white, opponents_uci_move)
        for move in moves:
            uci_move = move_to_uci_move(move)
            move.do_move(board)
            val = alpha_beta(board, uci_move, not is_engine_white, alpha, beta, depth - 1, transposition_table)
            transposition_table[board.current_hash] = (depth-1, val)
            move.undo_move(board)
            best_val = max(best_val, val)
            alpha = max(alpha, best_val)
            if alpha >= beta:
                break
        return best_val
    else:
        best_val = +max_utility
        moves = board.get_color_moves(is_engine_white, opponents_uci_move)
        for move in moves:
            uci_move = move_to_uci_move(move)
            move.do_move(board)
            val = alpha_beta(board, uci_move, not is_engine_white, alpha, beta, depth - 1, transposition_table)
            transposition_table[board.current_hash] = (depth-1, val)
            move.undo_move(board)
            best_val = min(best_val, val)
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val
