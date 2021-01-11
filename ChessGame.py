from PieceTypes import PieceTypes;

class ChessGame:
    def __init__(self):
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, PieceTypes.BR, PieceTypes.BN, PieceTypes.BB, PieceTypes.BQ, PieceTypes.BK, PieceTypes.BB, PieceTypes.BN, PieceTypes.BR, 0, 0],
            [0, 0, PieceTypes.BP, PieceTypes.BP, PieceTypes.BP, PieceTypes.BP, PieceTypes.BP, PieceTypes.BP, PieceTypes.BP, PieceTypes.BP, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, PieceTypes.WP, PieceTypes.WP, PieceTypes.WP, PieceTypes.WP, PieceTypes.WP, PieceTypes.WP, PieceTypes.WP, PieceTypes.WP, 0, 0],
            [0, 0, PieceTypes.WR, PieceTypes.WN, PieceTypes.WB, PieceTypes.WQ, PieceTypes.WK, PieceTypes.WB, PieceTypes.WN, PieceTypes.WR, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        # castling rights
        self.white_castled = False
        self.black_castled = False
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_king_rook_moved = False
        self.black_king_rook_moved = False
        self.white_queen_rook_moved = False
        self.black_queen_rook_moved = False

        # list of pieces with their positions (piece_type, pos_x, pos_y, is_pinned)
        self.white_pieces_alive = 1
        self.black_pieces_alive = 1


