# Dan Girshovich
# 8/12
# Calculates winning Chomp moves

class Board():
    ''' Simple representation of a Chomp board. The validity of moves or
        board state is never checked. The 'state' of the board is stored
        as the number of squares remaining in each row. For example:

                    1 1 1 1
            board = 1 1 1 0   =>  state = [4, 3, 1, 0]
                    1 0 0 0
                    0 0 0 0
    '''

    def __init__(self, num_rows, num_cols, initial_state = None):
        ''' Passing initial_state is used for cloning. '''
        self.num_rows = num_rows
        self.num_cols = num_cols
        if initial_state is None:
            self.state = [num_cols for i in range(num_rows)]
        else:
            self.state = list(initial_state)

    def chomp(self, row, col):
        ''' Takes a bite from the board. '''
        for i in range(row, self.num_rows):
            if self.state[i] > col:
                self.state[i] = col

    def is_empty(self):
        ''' Simple emptiness check. No guarantees if the board is in an
            invalid state. '''
        return self.state[0] == 0

    def get_remaining_squares(self):
        ''' Returns a list of the (row, col) pairs for the remaining squares. '''
        retval = []
        for row, row_val in enumerate(self.state):
            for col in range(0, row_val):
                retval.append((row, col))
        return retval

    def clone(self):
        ''' Returns a new board with the same state. '''
        return Board(self.num_rows, self.num_cols, self.state)

    def __hash__(self):
        ''' The hash is an integer representation of state. '''
        return int(''.join(map(str, self.state)))

class Solver():
    ''' Brute force Chomp game solver. Uses mutual recursion to test
        all possible games and save all states where player one is
        in a winning position. These states can then be used to find
        the ideal move for either player during a game. '''

    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.solved_boards = {}

    def p2move(self, board):
        ''' Makes all moves for player two. Returns true if the board 
            is in a winning position for player one, false otherwise. '''
        is_winning = True
        # check if player one just lost
        if board.is_empty():
            return False
        # check if this board has already been seen
        if hash(board) in self.solved_boards:
            return self.solved_boards[hash(board)]
        # recurse on all possible moves
        for row, col in board.get_remaining_squares():
            child = board.clone()
            child.chomp(row, col)
            # a board is winning when it's player two's move
            # only if ALL of its children are winning
            is_winning &= self.p1move(child)
        # memoize
        self.solved_boards[hash(board)] = is_winning
        return is_winning

    def p1move(self, board):
        ''' Makes all moves for player one. Returns true if the board 
            is in a winning position for player one, false otherwise. '''
        is_winning = False
        # check if player two just lost
        if board.is_empty():
            return True
        # recurse on all possible moves
        for row, col in board.get_remaining_squares():
            child = board.clone()
            child.chomp(row, col)
            # a board is winning when it's player one's move
            # only if ANY of its children are winning
            is_winning |= self.p2move(child)
        return is_winning

    def solve(self):
        starting_board = Board(self.num_rows, self.num_cols)
        self.p1move(starting_board)
        # only return boards set to True for being winning
        return filter(self.solved_boards.get, self.solved_boards)

def main():
    # example use case for a 4x7 board
    print Solver(4, 7).solve()

if __name__ == '__main__':
    main()
