P = 100
N = 320
B = 330
R = 500
Q = 900
K = 20000

piece_value_to_piece_score = {1: P, 2: R, 3: N, 4: B, 5: Q, 6: K, -1: -P, -2: -R, -3: -N, -4: -B, -5: -Q, -6: -K}

pawn_placement_score_white = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, 0,  0,  0,  0,  0,  0,  0,  0, -1, -1],
[-1, -1, 50, 50, 50, 50, 50, 50, 50, 50, -1, -1],
[-1, -1, 10, 10, 20, 30, 30, 20, 10, 10, -1, -1],
[-1, -1, 5,  5, 10, 25, 25, 10,  5,  5, -1, -1],
[-1, -1, 0,  0,  0, 20, 20,  0,  0,  0, -1, -1],
[-1, -1, 5, -5,-10,  0,  0,-10, -5,  5, -1, -1],
[-1, -1, 5, 10, 10,-20,-20, 10, 10,  5, -1, -1],
[-1, -1, 0,  0,  0,  0,  0,  0,  0,  0, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

pawn_placement_score_black = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, 0,  0,  0,  0,  0,  0,  0,  0, -1, -1],
[-1, -1, -5, -10, -10,20,20, -10, -10,  -5, -1, -1],
[-1, -1, -5, 5,10,  0,  0,10, 5,  -5, -1, -1],
[-1, -1, 0,  0,  0, -20, -20,  0,  0,  0, -1, -1],
[-1, -1, -5,  -5, -10, -25, -25, -10,  -5,  -5, -1, -1],
[-1, -1, -10, -10, -20, -30, -30, -20, -10, -10, -1, -1],
[-1, -1, -50, -50, -50, -50, -50, -50, -50, -50, -1, -1],
[-1, -1, 0,  0,  0,  0,  0,  0,  0,  0, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

knight_placement_score_white = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -50,-40,-30,-30,-30,-30,-40,-50, -1, -1],
[-1, -1, -40,-20,  0,  0,  0,  0,-20,-40, -1, -1],
[-1, -1, -30,  0, 10, 15, 15, 10,  0,-30, -1, -1],
[-1, -1, -30,  5, 15, 20, 20, 15,  5,-30, -1, -1],
[-1, -1, -30,  0, 15, 20, 20, 15,  0,-30, -1, -1],
[-1, -1, -30,  5, 10, 15, 15, 10,  5,-30, -1, -1],
[-1, -1, -40,-20,  0,  5,  12,  0,-20,-40, -1, -1],
[-1, -1, -50,-40,-30,-30,-30,-30,-40,-50, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

knight_placement_score_black = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, 50,40,30,30,30,30,40,50, -1, -1],
[-1, -1, 40,20,  0,  -5,  -12,  0,20,40, -1, -1],
[-1, -1, 30,  -5, -10, -15, -15, -10,  -5,30, -1, -1],
[-1, -1, 30,  0, -15, -20, -20, -15,  0,30, -1, -1],
[-1, -1, 30,  -5, -15, -20, -20, -15,  -5,30, -1, -1],
[-1, -1, 30,  0, -10, -15, -15, -10,  0,30, -1, -1],
[-1, -1, 40,20,  0,  0,  0,  0,20,40, -1, -1],
[-1, -1, 50,40,30,30,30,30,40,50, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

bishop_placement_score_white = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -20,-10,-10,-10,-10,-10,-10,-20, -1, -1],
[-1, -1, -10,  0,  0,  0,  0,  0,  0,-10, -1, -1],
[-1, -1, -10,  0,  5, 10, 10,  5,  0,-10, -1, -1],
[-1, -1, -10,  4,  5, 10, 10,  5,  4,-10, -1, -1],
[-1, -1, -10,  0, 10, 10, 10, 10,  0,-10, -1, -1],
[-1, -1, -10, 10, 10, 10, 10, 10, 10,-10, -1, -1],
[-1, -1, -10,  5,  0,  5,  5,  0,  25,-10, -1, -1],
[-1, -1, -20,-10,-10,-10,-10,-10,-10,-20, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

bishop_placement_score_black = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, 20,10,10,10,10,10,10,20, -1, -1],
[-1, -1, 10,  -5,  0,  -5,  -5,  0,  -25,10, -1, -1],
[-1, -1, 10, -10, -10, -10, -10, -10, -10,10, -1, -1],
[-1, -1, 10,  0, -10, -10, -10, -10,  0,10, -1, -1],
[-1, -1, 10,  -4,  -5, -10, -10,  -5,  -4,10, -1, -1],
[-1, -1, 10,  0,  -5, -10, -10,  -5,  0,10, -1, -1],
[-1, -1, 10,  0,  0,  0,  0,  0,  0,10, -1, -1],
[-1, -1, 20,10,10,10,10,10,10,20, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]


rook_placement_score_white = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, 0,  0,  0,  0,  0,  0,  0,  0, -1, -1],
[-1, -1, 5, 10, 10, 10, 10, 10, 10,  5, -1, -1],
[-1, -1, -5,  0,  0,  0,  0,  0,  0, -5, -1, -1],
[-1, -1, -5,  0,  0,  0,  0,  0,  0, -5, -1, -1],
[-1, -1, -5,  0,  0,  0,  0,  0,  0, -5, -1, -1],
[-1, -1, -5,  0,  0,  0,  0,  0,  0, -5, -1, -1],
[-1, -1, -5,  0,  0,  0,  0,  0,  0, -5, -1, -1],
[-1, -1, 0,  0,  0,  5,  5,  3,  0,  0, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

rook_placement_score_black = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, 0,  0,  0,  -5,  -5,  -3,  0,  0, -1, -1],
[-1, -1, 5,  0,  0,  0,  0,  0,  0, 5, -1, -1],
[-1, -1, 5,  0,  0,  0,  0,  0,  0, 5, -1, -1],
[-1, -1, 5,  0,  0,  0,  0,  0,  0, 5, -1, -1],
[-1, -1, 5,  0,  0,  0,  0,  0,  0, 5, -1, -1],
[-1, -1, 5,  0,  0,  0,  0,  0,  0, 5, -1, -1],
[-1, -1, -5, -10, -10, -10, -10, -10, -10,  -5, -1, -1],
[-1, -1, 0,  0,  0,  0,  0,  0,  0,  0, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

queen_placement_score_white = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -20,-10,-10, -5, -5,-10,-10,-20, -1, -1],
[-1, -1, -10,  0,  0,  0,  0,  0,  0,-10, -1, -1],
[-1, -1, -10,  0,  5,  5,  5,  5,  0,-10, -1, -1],
[-1, -1, -5,  0,  5,  5,  5,  5,  0, -5, -1, -1],
[-1, -1, 0,  0,  5,  5,  5,  5,  0, -5, -1, -1],
[-1, -1, -10,  5,  5,  5,  5,  5,  0,-10, -1, -1],
[-1, -1, -10,  0,  5,  0,  0,  0,  0,-10, -1, -1],
[-1, -1, -20,-10,-10, 0, -5,-10,-10,-20, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

queen_placement_score_black = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, 20,10,10, 0, 5,10,10,20, -1, -1],
[-1, -1, 10,  0,  -5,  0,  0,  0,  0,10, -1, -1],
[-1, -1, 10,  -5,  -5,  -5,  -5,  -5,  0,10, -1, -1],
[-1, -1, 0,  0,  -5,  -5,  -5,  -5,  0, 5, -1, -1],
[-1, -1, 5,  0,  -5,  -5,  -5,  -5,  0, 5, -1, -1],
[-1, -1, 10,  0,  -5,  -5,  -5,  -5,  0,10, -1, -1],
[-1, -1, 10,  0,  0,  0,  0,  0,  0,10, -1, -1],
[-1, -1, 20,10,10, 5, 5,10,10,20, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

king_placement_score_middle_game_white = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -30,-40,-40,-50,-50,-40,-40,-30, -1, -1],
[-1, -1, -30,-40,-40,-50,-50,-40,-40,-30, -1, -1],
[-1, -1, -30,-40,-40,-50,-50,-40,-40,-30, -1, -1],
[-1, -1, -30,-40,-40,-50,-50,-40,-40,-30, -1, -1],
[-1, -1, -20,-30,-30,-40,-40,-30,-30,-20, -1, -1],
[-1, -1, -10,-20,-20,-20,-20,-20,-20,-10, -1, -1],
[-1, -1, 20, 20,  0,  0,  0,  0, 20, 20, -1, -1],
[-1, -1, 20, 30,  -5,  0,  0,  -5, 40, 20, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

king_placement_score_middle_game_black = \
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -20, -30,  5,  0,  0,  5, -40, -20, -1, -1],
[-1, -1, -20, -20,  0,  0,  0,  0, -20, -20, -1, -1],
[-1, -1, 10,20,20,20,20,20,20,10, -1, -1],
[-1, -1, 20,30,30,40,40,30,30,20, -1, -1],
[-1, -1, 30,40,40,50,50,40,40,30, -1, -1],
[-1, -1, 30,40,40,50,50,40,40,30, -1, -1],
[-1, -1, 30,40,40,50,50,40,40,30, -1, -1],
[-1, -1, 30,40,40,50,50,40,40,30, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

piece_value_to_placement_score = {1: pawn_placement_score_white,
                                  2: rook_placement_score_white,
                                  3: knight_placement_score_white,
                                  4: bishop_placement_score_white,
                                  5: queen_placement_score_white,
                                  6: king_placement_score_middle_game_white,
                                  -1: pawn_placement_score_black,
                                  -2: rook_placement_score_black,
                                  -3: knight_placement_score_black,
                                  -4: bishop_placement_score_black,
                                  -5: queen_placement_score_black,
                                  -6: king_placement_score_middle_game_black}


def evaluate(board):
    score = 0
    for row in range(2, 10):
        for col in range(2, 10):
            if board[row][col] != 0:
                score += piece_value_to_piece_score[board[row][col]] + piece_value_to_placement_score[board[row][col]][row][col]
    return score
