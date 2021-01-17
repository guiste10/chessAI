from Pieces import Pieces, promotion_to_piece, piece_to_promotion

col_to_uci_dict = {2: 'a', 3: 'b', 4: 'c', 5: 'd', 6: 'e', 7: 'f', 8: 'g', 9: 'h', }
uci_to_col_dict = {'a': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'h': 9}
row_to_uci_dict = {2: '8', 3: '7', 4: '6', 5: '5', 6: '4', 7: '3', 8: '2', 9: '1', }
uci_to_row_dict = {'8': 2, '7': 3, '6': 4, '5': 5, '4': 6, '3': 7, '2': 8, '1': 9}


def print_moves(moves):
    for move in moves:
        print(move, end=" ")
    print('\n')
    print('Num moves: ' + str(len(moves)))


def uci_move_to_move(uci_move, board, is_white):
    (row_1, col_1, row_2, col_2) = (
        uci_to_row_dict[uci_move[0]], uci_to_col_dict[uci_move[1]], uci_to_row_dict[uci_move[2]],
        uci_to_col_dict[uci_move[3]])
    to_piece = board[row_2][col_2]
    not_promoted_piece = board[row_1][col_1]
    if len(uci_move) > 4:
        promoted_piece = promotion_to_piece[(uci_move[4], is_white)]
    else:
        promoted_piece = board[row_1][col_1]
    return Move(row_1, col_1, row_2, col_2, to_piece, not_promoted_piece, promoted_piece)


def move_to_uci_move(move):
    (row_1, col_1, row_2, col_2, not_promoted_piece, promoted_piece) = (
        move.row_1, move.col_1, move.row_2, move.col_2, move.not_promoted_piece, move.promoted_piece)
    uci_move = row_to_uci_dict[row_1] + col_to_uci_dict[col_1] + row_to_uci_dict[row_2] + col_to_uci_dict[col_2]
    if not_promoted_piece == promoted_piece:
        return uci_move
    else:  # pawn promotion
        print('pawn promotion')
        return uci_move + piece_to_promotion[promoted_piece]


def do_move(board, move):
    board[move.row_2][move.col_2] = move.promoted_piece
    board[move.row_1][move.col_1] = Pieces.OO


def undo_move(board, move):
    board[move.row_1][move.col_1] = move.not_promoted_piece
    board[move.row_2][move.col_2] = move.to_piece
