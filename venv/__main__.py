from Board import Board
from BoardPositions import BoardPositions


def main():
    print("Engine started", "\n")
    board = Board(BoardPositions.normal_board)
    print(board)
    n = 0 # engine is black by default
    while n < 100:
        if n % 2 == 0:
            move = input("Enter move: ")
            move = chess.Move.from_uci(move)
            board.push(move)
        else:
            print("Computers Turn:")
            move = minimaxRoot(4, board, True)
            move = chess.Move.from_uci(str(move))
            board.push(move)
        print(board)
        n += 1


if __name__ == "__main__":
    main()