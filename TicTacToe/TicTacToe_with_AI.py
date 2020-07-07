import random


class ComputerPlayerEasy():

    def index_board(self, board):
        for y, row in enumerate(board):
            for x, elem in enumerate(row):
                yield (x, y), elem

    def random_vacancy(self, board):
        board_spots = self.index_board(board)
        empty_spots = [coords for coords, mark in board_spots if mark == ' ']
        return random.choice(empty_spots)  # coords

    def make_move(self, board):
        print('Making move level "easy"')
        return self.random_vacancy(board)


class ComputerPlayerMedium(ComputerPlayerEasy):

    def __init__(self, mark):
        self.mark = mark
        return None

    def get_winning_move(self, board, move):

        board_spots = list(self.index_board(board))
        empty_spots = [coords for coords, mark in board_spots if mark == ' ']
        all_marks = list(filter(lambda pos: pos[1] == move, board_spots))

        for y in range(len(board)):  # check rows
            if [coord[1] for coord, _ in all_marks].count(y) == 2:
                if list(filter(lambda c: c[1] == y, empty_spots)):
                    return list(filter(lambda c: c[1] == y, empty_spots))[0]

        for x in range(len(board[0])):  # check columns
            if [coord[0] for coord, _ in all_marks].count(x) == 2:
                if list(filter(lambda c: c[0] == x, empty_spots)):
                    return list(filter(lambda c: c[0] == x, empty_spots))[0]

        # check main diagonal
        if [co[0] == co[1] for co, _ in all_marks].count(True) == 2:
            if list(filter(lambda c: c[0] == c[1], empty_spots)):
                return list(filter(lambda c: c[0] == c[1], empty_spots))[0]
        # check reverse diagonal
        if [co[0] == 2 - co[1] for co, _ in all_marks].count(True) == 2:
            if list(filter(lambda c: c[0] == 2 - c[1], empty_spots)):
                return list(filter(lambda c: c[0] == 2 - c[1], empty_spots))[0]
        return []

    def make_move(self, board):
        print('Making move level "medium"')
        comp_wins = self.get_winning_move(board, self.mark)
        if comp_wins:
            return comp_wins

        opp_will_win = self.get_winning_move(board,
                                             'X' if self.mark == 'O' else 'O')
        if opp_will_win:
            return opp_will_win

        return self.random_vacancy(board)


class ComputerPlayerHard(ComputerPlayerMedium):

    def evaluate_state(self, board):

        board_spots = list(self.index_board(board))

        # check if a player won
        for move in ['X', 'O']:
            all_marks = list(filter(lambda pos: pos[1] == move, board_spots))

            for y in range(len(board)):  # check rows
                if [coord[1] for coord, _ in all_marks].count(y) == 3:
                    return ('win', move)

            for x in range(len(board[0])):  # check columns
                if [coord[0] for coord, _ in all_marks].count(x) == 3:
                    return ('win', move)

            # check main diagonal
            if [co[0] == co[1] for co, _ in all_marks].count(True) == 3:
                return ('win', move)
            # check reverse diagonal
            if [co[0] == 2 - co[1] for co, _ in all_marks].count(True) == 3:
                return ('win', move)

        # check if a draw
        empty_spots = [coords for coords, mark in board_spots if mark == ' ']
        if not empty_spots:
            return ('draw', '')
        else:
            return ('', '')  # game still in progress

    def minimax(self, board, turn, mode):

        state = self.evaluate_state(board)

        if state[0] == 'win':
            return 10 if state[1] == self.mark else -10
        if state[0] == 'draw':
            return 0

        board_spots = self.index_board(board)
        empty_spots = [coords for coords, mark in board_spots if mark == ' ']
        move_scores = {}

        for move in empty_spots:
            temp_board = [row.copy() for row in board]
            temp_board[move[1]][move[0]] = turn
            move_scores[move] = self.minimax(temp_board,
                                             'O' if turn == 'X' else 'X',
                                             'min' if mode == 'max' else 'max')
        if mode == 'max':
            return max(move_scores.values())
        elif mode == 'min':
            return min(move_scores.values())

    def make_move(self, board):
        print('Making move level "hard"')

        board_spots = self.index_board(board)
        empty_spots = [coords for coords, mark in board_spots if mark == ' ']
        move_scores = {}

        for move in empty_spots:
            temp_board = [row.copy() for row in board]
            temp_board[move[1]][move[0]] = self.mark
            move_scores[move] = self.minimax(temp_board,
                                             'O' if self.mark == 'X' else 'X',
                                             'min')

        target_score = max(move_scores.values())
        for move, score in move_scores.items():
            if score == target_score:
                return move


class TicTacToe():
    def __init__(self):
        self.move, self.game_state = 'X', ''
        self.players = {'X': None, 'O': None}
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

    def three_matchs(self, elems):
        if (len(set(elems)) == 1) and (set(elems).pop() in ['X', 'O']):
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
        i = [0, 1, 2]
        return [[x, y] for x in i for y in i if not self.is_occupied([x, y])]

    def validiate_user_input(self, user_input):

        if user_input.replace(' ', '').isnumeric():
            coords = [int(num) for num in user_input.split()]

            if any(coord not in [1, 2, 3] for coord in coords):
                print('Coordinates should be from 1 to 3!')
                return False
            else:
                coords = [coords[0] - 1, 2 - coords[1] + 1]
                if coords not in self.remaining_moves():
                    print('This cell is occupied! Choose another one!')
                    return False
                return True

        print('You should enter numbers!')
        return False

    def is_occupied(self, coords):
        return not (self.board[coords[1]][coords[0]] == ' ')

    def user_move(self):
        while True:
            user_input = input('Enter the coordinates: ')
            if self.validiate_user_input(user_input):
                coords = [int(num) for num in user_input.split()]
                coords = [coords[0] - 1, 2 - coords[1] + 1]
                return coords
        return None

    def run_session(self):
        self.print_board()

        while self.game_state == "":
            if self.players[self.move] == 'user':
                coords = self.user_move()
            else:
                coords = self.players[self.move].make_move(self.board)

            self.board[coords[1]][coords[0]] = self.move
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
        options = ['user', 'easy', 'medium', 'hard']
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

        for mark in self.players:
            if self.players[mark] == 'easy':
                self.players[mark] = ComputerPlayerEasy()
            elif self.players[mark] == 'medium':
                self.players[mark] = ComputerPlayerMedium(mark)
            elif self.players[mark] == 'hard':
                self.players[mark] = ComputerPlayerHard(mark)

        self.run_session()
        return None


if __name__ == "__main__":
    game_session = TicTacToe()
    game_session.start_game()
