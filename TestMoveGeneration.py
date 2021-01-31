from unittest import TestCase
from Board import Board
from BoardPositions import BoardPositions


# print_moves(black_moves)

class TestMoveGeneration(TestCase):
    def test_get_color_moves_1(self):
        board = Board(BoardPositions.normal_board)
        white_pieces, black_pieces = board.init_pieces()
        white_moves, white_pieces = board.get_color_moves(white_pieces, True, 'a1a1')
        black_moves, black_pieces = board.get_color_moves(black_pieces, False, 'a1a1')
        self.assertEqual(20, len(white_moves))
        self.assertEqual(20, len(black_moves))

    def test_get_color_moves_2(self):
        board = Board(BoardPositions.no_attack_board)
        white_pieces, black_pieces = board.init_pieces()
        white_moves, white_pieces = board.get_color_moves(white_pieces, True, 'a1a1')
        black_moves, black_pieces = board.get_color_moves(black_pieces, False, 'a1a1')
        self.assertEqual(29, len(white_moves))
        self.assertEqual(29, len(black_moves))

    def test_get_color_moves_3(self):
        board = Board(BoardPositions.attack_board)
        board.game_state.castled[True] = True  # white castled
        board.game_state.king_pos[True] = (9, 8)
        white_pieces, black_pieces = board.init_pieces()
        white_moves, white_pieces = board.get_color_moves(white_pieces, True, 'a1a1')
        black_moves, black_pieces = board.get_color_moves(black_pieces, False, 'a1a1')
        self.assertEqual(41, len(white_moves))
        self.assertEqual(43, len(black_moves))

    def test_get_color_moves_4(self):
        board = Board(BoardPositions.en_passant_board_white)
        board.game_state.castled[True] = True  # white's king castled or moved
        board.game_state.castled[False] = True  # black's king castled or moved
        white_pieces, black_pieces = board.init_pieces()
        white_moves, white_pieces = board.get_color_moves(white_pieces, True, 'b7b5')
        self.assertEqual(5, len(white_moves))
        board = Board(BoardPositions.en_passant_board_black)
        board.game_state.castled[True] = True  # white's king castled or moved
        board.game_state.castled[False] = True  # black's king castled or moved
        white_pieces, black_pieces = board.init_pieces()
        black_moves, black_pieces = board.get_color_moves(black_pieces, False, 'a2a4')
        self.assertEqual(5, len(black_moves))

    def test_is_attacked_for_white(self):
        board = Board(BoardPositions.attack_board)
        is_white = True
        self.assertEqual(board.is_square_attacked(2, 3, is_white), True)
        self.assertEqual(board.is_square_attacked(2, 4, is_white), True)
        self.assertEqual(board.is_square_attacked(2, 5, is_white), True)
        self.assertEqual(board.is_square_attacked(2, 7, is_white), True)
        self.assertEqual(board.is_square_attacked(2, 8, is_white), True)
        self.assertEqual(board.is_square_attacked(3, 4, is_white), True)
        self.assertEqual(board.is_square_attacked(3, 9, is_white), True)
        self.assertEqual(board.is_square_attacked(4, 2, is_white), True)
        self.assertEqual(board.is_square_attacked(4, 5, is_white), True)
        self.assertEqual(board.is_square_attacked(4, 7, is_white), True)
        self.assertEqual(board.is_square_attacked(4, 8, is_white), True)
        self.assertEqual(board.is_square_attacked(4, 9, is_white), True)
        self.assertEqual(board.is_square_attacked(5, 2, is_white), True)
        self.assertEqual(board.is_square_attacked(5, 3, is_white), True)
        self.assertEqual(board.is_square_attacked(5, 4, is_white), True)
        self.assertEqual(board.is_square_attacked(5, 8, is_white), True)
        self.assertEqual(board.is_square_attacked(6, 2, is_white), False)
        self.assertEqual(board.is_square_attacked(6, 3, is_white), True)
        self.assertEqual(board.is_square_attacked(6, 4, is_white), True)
        self.assertEqual(board.is_square_attacked(6, 6, is_white), True)
        self.assertEqual(board.is_square_attacked(6, 7, is_white), False)
        self.assertEqual(board.is_square_attacked(6, 8, is_white), True)
        self.assertEqual(board.is_square_attacked(7, 3, is_white), True)
        self.assertEqual(board.is_square_attacked(7, 5, is_white), False)
        self.assertEqual(board.is_square_attacked(7, 8, is_white), False)
        self.assertEqual(board.is_square_attacked(7, 9, is_white), False)
        self.assertEqual(board.is_square_attacked(8, 2, is_white), False)
        self.assertEqual(board.is_square_attacked(8, 4, is_white), False)
        self.assertEqual(board.is_square_attacked(8, 6, is_white), False)
        self.assertEqual(board.is_square_attacked(8, 9, is_white), False)
        self.assertEqual(board.is_square_attacked(9, 2, is_white), False)
        self.assertEqual(board.is_square_attacked(9, 4, is_white), False)
        self.assertEqual(board.is_square_attacked(9, 5, is_white), False)
        self.assertEqual(board.is_square_attacked(9, 6, is_white), False)
        self.assertEqual(board.is_square_attacked(9, 9, is_white), False)

    def test_is_attacked_for_black(self):
        board = Board(BoardPositions.attack_board)
        is_white = False
        self.assertEqual(board.is_square_attacked(2, 3, is_white), False)
        self.assertEqual(board.is_square_attacked(2, 4, is_white), False)
        self.assertEqual(board.is_square_attacked(2, 5, is_white), False)
        self.assertEqual(board.is_square_attacked(2, 7, is_white), False)
        self.assertEqual(board.is_square_attacked(2, 8, is_white), False)
        self.assertEqual(board.is_square_attacked(3, 4, is_white), False)
        self.assertEqual(board.is_square_attacked(3, 9, is_white), True)
        self.assertEqual(board.is_square_attacked(4, 2, is_white), False)
        self.assertEqual(board.is_square_attacked(4, 5, is_white), True)
        self.assertEqual(board.is_square_attacked(4, 7, is_white), True)
        self.assertEqual(board.is_square_attacked(4, 8, is_white), True)
        self.assertEqual(board.is_square_attacked(4, 9, is_white), True)
        self.assertEqual(board.is_square_attacked(5, 2, is_white), False)
        self.assertEqual(board.is_square_attacked(5, 3, is_white), True)
        self.assertEqual(board.is_square_attacked(5, 4, is_white), True)
        self.assertEqual(board.is_square_attacked(5, 8, is_white), True)
        self.assertEqual(board.is_square_attacked(6, 2, is_white), True)
        self.assertEqual(board.is_square_attacked(6, 3, is_white), True)
        self.assertEqual(board.is_square_attacked(6, 4, is_white), False)
        self.assertEqual(board.is_square_attacked(6, 6, is_white), True)
        self.assertEqual(board.is_square_attacked(6, 7, is_white), True)
        self.assertEqual(board.is_square_attacked(6, 8, is_white), True)
        self.assertEqual(board.is_square_attacked(7, 3, is_white), False)
        self.assertEqual(board.is_square_attacked(7, 5, is_white), True)
        self.assertEqual(board.is_square_attacked(7, 8, is_white), True)
        self.assertEqual(board.is_square_attacked(7, 9, is_white), True)
        self.assertEqual(board.is_square_attacked(8, 2, is_white), True)
        self.assertEqual(board.is_square_attacked(8, 4, is_white), True)
        self.assertEqual(board.is_square_attacked(8, 6, is_white), True)
        self.assertEqual(board.is_square_attacked(8, 9, is_white), True)
        self.assertEqual(board.is_square_attacked(9, 2, is_white), True)
        self.assertEqual(board.is_square_attacked(9, 4, is_white), True)
        self.assertEqual(board.is_square_attacked(9, 5, is_white), True)
        self.assertEqual(board.is_square_attacked(9, 6, is_white), True)
        self.assertEqual(board.is_square_attacked(9, 9, is_white), True)
