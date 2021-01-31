from Pieces import Pieces, value_to_piece_short, promotion_color_to_value

col_to_uci_dict = {2: 'a', 3: 'b', 4: 'c', 5: 'd', 6: 'e', 7: 'f', 8: 'g', 9: 'h', }
uci_to_col_dict = {'a': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'h': 9}
row_to_uci_dict = {2: '8', 3: '7', 4: '6', 5: '5', 6: '4', 7: '3', 8: '2', 9: '1', }
uci_to_row_dict = {'8': 2, '7': 3, '6': 4, '5': 5, '4': 6, '3': 7, '2': 8, '1': 9}


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


def uci_move_to_move(uci_move):
    return (uci_to_col_dict[uci_move[0]], uci_to_row_dict[uci_move[1]], uci_to_col_dict[uci_move[2]],
            uci_to_row_dict[uci_move[3]])


def do_uci_move(uci_move, board, is_white):
    (col_1, row_1, col_2, row_2) = uci_move_to_move(uci_move)
    if len(uci_move) > 4:  # promotion
        board[row_1][col_1] = Pieces.OO
        board[row_2][col_2] = promotion_color_to_value[(uci_move[4], is_white)]
    elif value_to_piece_short[board[row_1][col_1]] == 'k' and abs(col_2 - col_1) == 2:  # castle
        if col_2 - col_1 == 2:
            castle_kingside(board, row_1, col_1)
        else:
            castle_queenside(board, row_1, col_1)
    else:  # en passant/move/capture
        if value_to_piece_short[board[row_1][col_1]] == 'p' and col_1 != col_2 and board[row_2][col_2] == Pieces.OO:
            board[row_2][col_1] = Pieces.OO  # en passant kill
        board[row_1][col_1] = Pieces.OO
        board[row_2][col_2] = board[row_1][col_1]


def move_to_uci_move(move):
    (row_1, col_1, row_2, col_2) = (move.row_1, move.col_1, move.row_2, move.col_2)
    uci_move = row_to_uci_dict[row_1] + col_to_uci_dict[col_1] + row_to_uci_dict[row_2] + col_to_uci_dict[col_2]
    if move.__class__.__name__ != 'Promotion':
        return uci_move
    else:
        return uci_move + value_to_piece_short[move.promotion]


def print_moves(moves):
    for move in moves:
        print(move, end=" ")
    print('\n')
    print('Num moves: ' + str(len(moves)))