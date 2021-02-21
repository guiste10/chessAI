import numpy as np


def rand_int_64():
    return np.random.randint(2147483647, 9223372036854775807, dtype=np.int64)


# access hash: piece_hash_for_squares[piece_val][row][col]
piece_hash_for_squares = {piece_val:{row:{col:rand_int_64() for col in range(2, 10)} for row in range(2, 10)} for piece_val in range(-6, 7)}

side_hash = {True: rand_int_64(), False: rand_int_64()}

file_hash = {col:rand_int_64() for col in range(2, 10)}

# castling rights change because king, qRook or kRook at column 'col' moves for white or black
castling_rights_hash = {color:{king_side:rand_int_64() for king_side in (True, False)} for color in (True, False)}

# a = rand_int_64()
# b = rand_int_64()
# c = a ^ b
# print(a)
# a = c ^ b
# print(a)


def init_hash(board):
    hash_val = 0
    for row in range(2, 10):
        for col in range(2, 10):
            hash_val ^= piece_hash_for_squares[board[row][col]][row][col]
    return hash_val
