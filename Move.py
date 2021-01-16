class Move:
    col_dict = {
        2: 'a',
        3: 'b',
        4: 'c',
        5: 'd',
        6: 'e',
        7: 'f',
        8: 'g',
        9: 'h',
    }
    row_dict = {
        2: '8',
        3: '7',
        4: '6',
        5: '5',
        6: '4',
        7: '3',
        8: '2',
        9: '1',
    }


    def __init__(self, row1, col1, row2, col2, old_value):
        self.row1 = row1
        self.col1 = col1
        self.row2 = row2
        self.col2 = col2
        self.old_value = old_value

    def __str__(self):
        return self.col_dict[self.col1] + self.row_dict[self.row1] + self.col_dict[self.col2] + self.row_dict[self.row2]

def print_moves(moves):
    for move in moves:
        print(move, end=" ")
    print('\n')
    print('Num moves: ' + str(len(moves)))

