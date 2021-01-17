from unittest import TestCase
from Board import Board
from BoardPositions import BoardPositions


class TestBoard(TestCase):
    def test_get_color_moves(self):
        board = Board(BoardPositions.normal_board)
        self.white_pieces, self.black_pieces = board.init_pieces()
        white_moves, self.white_pieces = board.get_color_moves(self.white_pieces, True, 'e4e6')
        black_moves, self.black_pieces = board.get_color_moves(self.black_pieces, False, 'e4e6')
        self.assertEqual(20, len(white_moves))
        self.assertEqual(20, len(black_moves))




        board = Board(BoardPositions.no_attack_board)
        self.white_pieces, self.black_pieces = board.init_pieces()
        white_moves, self.white_pieces = board.get_color_moves(self.white_pieces, True, 'e4e6')
        black_moves, self.black_pieces = board.get_color_moves(self.black_pieces, False, 'e4e6')
        self.assertEqual(29, len(white_moves))
        # print_moves(black_moves)
        self.assertEqual(29, len(black_moves))


