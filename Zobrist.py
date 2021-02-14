import numpy as np


def rand_int_64():
    return np.random.randint(2147483647, 9223372036854775807, dtype=np.int64)


# transformation needed for piece at row, col with piece_val e.g. -5 : row -2, col-2, piece_val+6
# access hash: piece_hash_for_squares[piece_val][row-2][col-2]
piece_hash_for_squares = [[[rand_int_64() for _ in range(0, 8)] for _ in range(0, 8)] for _ in range(0, 13)]

side_hash = {True: rand_int_64(), False: rand_int_64()}

# transformation: col - 2
file_hash = [rand_int_64() for _ in range(0, 8)]

# castling rights change because king, qRook or kRook moves (0,1,2) for white or black
castling_rights_hash = [[rand_int_64() for _ in range(0, 3)] for _ in (True, False)]

# start = rand_int_64()
# print(start)
# side = rand_int_64()
# piece = rand_int_64()
# start ^= side ^ piece
# print(start)
# start ^= side ^ piece  # or piece ^ side
# print(start)


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
            hash_val ^= piece_hash_for_squares[board[row][col]][row-2][col-2]
    return hash_val


def update_hash(board, move):
    pass
