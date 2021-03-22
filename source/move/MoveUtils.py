from __future__ import print_function
from board.Pieces import Pieces, value_to_piece_short, promotion_color_to_value, king_start_pos, rook_start_pos

col_to_uci_dict = {2: 'a', 3: 'b', 4: 'c', 5: 'd', 6: 'e', 7: 'f', 8: 'g', 9: 'h', }
uci_to_col_dict = {'a': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'h': 9}
row_to_uci_dict = {2: '8', 3: '7', 4: '6', 5: '5', 6: '4', 7: '3', 8: '2', 9: '1', }
uci_to_row_dict = {'8': 2, '7': 3, '6': 4, '5': 5, '4': 6, '3': 7, '2': 8, '1': 9}

NONE = 'none'


def castle_queenside(board, row_1, col_1):
    board[row_1][col_1 - 2] = board[row_1][col_1]
    board[row_1][col_1] = Pieces.OO
    board[row_1][col_1 - 1] = board[row_1][col_1 - 4]
    board[row_1][col_1 - 4] = Pieces.OO


def castle_kingside(board, row_1, col_1):
    board[row_1][col_1 + 2] = board[row_1][col_1]
    board[row_1][col_1] = Pieces.OO
    board[row_1][col_1 + 1] = board[row_1][col_1 + 3]
    board[row_1][col_1 + 3] = Pieces.OO


def uci_move_to_move_simple(uci_move):
    return (uci_to_col_dict[uci_move[0]], uci_to_row_dict[uci_move[1]], uci_to_col_dict[uci_move[2]],
            uci_to_row_dict[uci_move[3]])

def uci_move_to_move_object(uci_move, is_opponent_white, board):
    from Moves import Move, KingMove, MoveCastlingRightsChange, Castle, EnPassant, Promotion
    (col_1, row_1, col_2, row_2) = uci_move_to_move_simple(uci_move)
    to_piece = board.board[row_2][col_2]
    if len(uci_move) > 4:  # promotion
        return Promotion(row_1, col_1, row_2, col_2, is_opponent_white, to_piece)
    if value_to_piece_short[board.board[row_1][col_1]] == 'k':
        if abs(col_2 - col_1) == 2:  # castle
            return Castle(True, is_opponent_white) if col_2 - col_1 == 2 else Castle(False, is_opponent_white)
        elif board.cannot_castle[is_opponent_white] or board.both_rooks_moved(is_opponent_white):
            return KingMove(row_1, col_1, row_2, col_2, is_opponent_white, to_piece)
        return MoveCastlingRightsChange(row_1, col_1, row_2, col_2, is_opponent_white, to_piece)
    if value_to_piece_short[board.board[row_1][col_1]] == 'r':
        if board.cannot_castle[is_opponent_white] or (row_1, col_1) not in rook_start_pos[is_opponent_white] or board.rook_moved[(row_1, col_1)]:
            return Move(row_1, col_1, row_2, col_2, is_opponent_white, to_piece)
        return MoveCastlingRightsChange(row_1, col_1, row_2, col_2, is_opponent_white, to_piece)
    if value_to_piece_short[board.board[row_1][col_1]] == 'p' and col_1 != col_2 and board.board[row_2][col_2] == Pieces.OO:  # en passant
        return EnPassant(row_1, col_1, row_2, col_2, is_opponent_white)
    return Move(row_1, col_1, row_2, col_2, is_opponent_white, to_piece)


def move_to_uci_move(move):
    if move == 'none':
        return 'none'
    if move.__class__.__name__ == 'Castle':
        row_1, col_1 = king_start_pos[move.is_white]
        row_2, col_2 = (row_1, col_1 + 2) if move.kingside else (row_1, col_1 - 2)
    else:
        (row_1, col_1, row_2, col_2) = (move.row_1, move.col_1, move.row_2, move.col_2)
    uci_move = col_to_uci_dict[col_1] + row_to_uci_dict[row_1] + col_to_uci_dict[col_2] + row_to_uci_dict[row_2]
    if move.__class__.__name__ != 'Promotion':
        return uci_move
    else:
        return uci_move + value_to_piece_short[move.promotion_piece]


def print_moves(moves):
    for move in moves:
        print(move_to_uci_move(move), end=' ')
    print('\n')
    print('Num moves: ' + str(len(moves)))
