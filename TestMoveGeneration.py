from unittest import TestCase
from Board import Board
from BoardPositions import BoardPositions
from move.MoveUtils import print_moves


# print_moves(black_moves)

class TestMoveGeneration(TestCase):
    def test_get_color_moves(self):
        board = Board(BoardPositions.normal_board)
        self.white_pieces, self.black_pieces = board.init_pieces()
        white_moves, self.white_pieces = board.get_color_moves(self.white_pieces, True, 'a1a1')
        black_moves, self.black_pieces = board.get_color_moves(self.black_pieces, False, 'a1a1')
        self.assertEqual(20, len(white_moves))
        self.assertEqual(20, len(black_moves))

    def test_get_color_moves_2(self):
        board = Board(BoardPositions.no_attack_board)
        self.white_pieces, self.black_pieces = board.init_pieces()
        white_moves, self.white_pieces = board.get_color_moves(self.white_pieces, True, 'a1a1')
        black_moves, self.black_pieces = board.get_color_moves(self.black_pieces, False, 'a1a1')
        self.assertEqual(29, len(white_moves))
        self.assertEqual(29, len(black_moves))

    def test_get_color_moves_3(self):
        board = Board(BoardPositions.attack_board)
        self.white_pieces, self.black_pieces = board.init_pieces()
        white_moves, self.white_pieces = board.get_color_moves(self.white_pieces, True, 'a1a1')
        black_moves, self.black_pieces = board.get_color_moves(self.black_pieces, False, 'a1a1')
        self.assertEqual(41, len(white_moves))  # add 2 when castle ready
        self.assertEqual(41, len(black_moves))

    def test_get_color_moves_4(self):
        board = Board(BoardPositions.en_passant_board_white)
        self.white_pieces, self.black_pieces = board.init_pieces()
        white_moves, self.white_pieces = board.get_color_moves(self.white_pieces, True, 'b7b5')
        self.assertEqual(5, len(white_moves))
        board = Board(BoardPositions.en_passant_board_black)
        self.white_pieces, self.black_pieces = board.init_pieces()
        black_moves, self.black_pieces = board.get_color_moves(self.black_pieces, False, 'a2a4')
        self.assertEqual(5, len(black_moves))
