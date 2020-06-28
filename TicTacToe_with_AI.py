import random


class TicTacToe():
    def __init__(self):
        self.move, self.game_state = 'X', ''
        self.players = {'X': 'user', 'O': 'easy'}
        self.board = [list('   ') for _ in range(3)]
        random.seed()
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

    def remaining_moves(self):
        i = [1, 2, 3]
        return [[x, y] for x in i for y in i if not self.is_occupied([x, y])]

    def validiate_user_input(self, user_input):

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

    def computer_move(self, difficulty):
        print('Making move level "easy"')
        return random.choice(self.remaining_moves())

    def _play(self):
        self.print_board()

        while self.game_state == "":
            if self.players[self.move] == 'user':
                user_input = input('Enter the coordinates: ')
                if self.validiate_user_input(user_input):
                    coords = [int(num) for num in user_input.split()]
                else:
                    continue
            else:
                coords = self.computer_move(self.players[self.move])

            if self.is_occupied(coords):
                if self.players[self.move] == 'user':
                    print('This cell is occupied! Choose another one!')
                continue
            else:
                self.board[2 - (coords[1] - 1)][coords[0] - 1] = self.move
                self.print_board()
                if self.check_victory():
                    self.game_state = f'{self.move} wins'
                elif len(self.remaining_moves()) == 0:
                    self.game_state = "Draw"

                print(self.game_state)
                self.move = 'O' if (self.move == 'X') else 'X'  # for next turn
        self.__init__()  # for next game
        return None

    def check_input_command(self, user_input):
        words = user_input.split()
        options = ['user', 'easy']
        if len(words) != 3:
            return False
        if words[0] != 'start':
            return False
        if (words[1] not in options) or (words[2] not in options):
            return False
        return True

    def start_game(self):

        while True:
            user_input = input('Input command: ')
            if self.check_input_command(user_input):
                break
            print('Bad parameters!')
        self.players['X'], self.players['O'] = user_input.split()[1:]
        self._play()
        return None


if __name__ == "__main__":
    game = TicTacToe()
    game.start_game()
