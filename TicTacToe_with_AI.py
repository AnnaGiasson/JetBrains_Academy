class TicTacToe():
    def __init__(self):
        self.game_state = "Game not finished"
        return None

    def print_board(self):
        print('---------\n'
              '| {} {} {} |\n'
              '| {} {} {} |\n'
              '| {} {} {} |\n'
              '---------'.format(*self.board[0],
                                 *self.board[1],
                                 *self.board[2]))
        return None

    def three_matchs(self, fields):
        if (len(set(fields)) == 1) and (set(fields).pop() in ['X', 'O']):
            return True
        return False

    def check_victory(self):

        for row in self.board:
            if self.three_matchs(row):
                return True  # winning row
        for col in range(len(self.board[0])):
            if self.three_matchs([row[col] for row in self.board]):
                return True  # winning column

        if self.three_matchs([self.board[x][x] for x in [0, 1, 2]]):
            return True  # winning diagonal
        if self.three_matchs([self.board[x][2 - x] for x in [0, 1, 2]]):
            return True  # winning reverse diagonal
        return False

    def check_board_full(self):
        occupancy = []
        for y in range(1, len(self.board) + 1):
            for x in range(1, len(self.board[0]) + 1):
                occupancy.append(self.is_occupied([x, y]))

        return all(occupancy)

    def validiate_input(self, user_input):

        if user_input.replace(' ', '').isnumeric():
            coords = [int(num) for num in user_input.split()]

            if any(coord not in [1, 2, 3] for coord in coords):
                print('Coordinates should be from 1 to 3!')
                return False
            return True

        print('You should enter numbers!')
        return False

    def is_occupied(self, coords):
        return not (self.board[2 - (coords[1] - 1)][coords[0] - 1] == ' ')

    def start_game(self):

        init_state = input('Enter cells: ').replace('_', ' ')
        self.board = [list(init_state[i:i + 3]) for i in [0, 3, 6]]
        self.print_board()

        # determine who goes first
        move = 'O' if init_state.count('X') > init_state.count('O') else 'X'

        while self.game_state == "Game not finished":

            user_input = input('Enter the coordinates: ')
            if self.validiate_input(user_input):
                coords = [int(num) for num in user_input.split()]

                if self.is_occupied(coords):
                    print('This cell is occupied! Choose another one!')
                    continue
                else:
                    self.board[2 - (coords[1] - 1)][coords[0] - 1] = move
                    self.print_board()
                    if self.check_victory():
                        self.game_state = f'{move} wins'
                    elif self.check_board_full():
                        self.game_state = "Draw"

                    print(self.game_state)
                    break  # for the first step online

                move = 'O' if (move == 'X') else 'X'  # for next turn

        return None


if __name__ == "__main__":
    game = TicTacToe()
    game.start_game()
