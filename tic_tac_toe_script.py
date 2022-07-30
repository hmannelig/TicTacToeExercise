import random
import re


class Player:
    name = ""
    token = ""

    def __init__(self, name, token):
        self.name = name
        self.token = token

    def make_move(self, pos_taken, board_representation):
        question = str.format("It's {}'s turn, make your move! Where would you like to put {}? ", self.name, self.token)
        pos = int(input(question)) - 1

        while pos_taken[pos]:
            print(str.format("Position {} has been already taken, please, select another position!", pos))
            pos = int(input(question)) - 1

        pos_taken[pos] = self.token
        board_representation[pos] = self.token


class CPU(Player):

    def make_move(self, pos_taken, board_representation):
        pos = random.randint(0, 8)

        while pos_taken[pos]:
            pos = random.randint(0, 8)

        pos_taken[pos] = self.token
        board_representation[pos] = self.token


class EnhancedCPU(Player):
    __winning_scenarios = {}
    regex = ''

    def __init__(self, *args, **kwargs):
        super(EnhancedCPU, self).__init__(*args, **kwargs)

        self.regex = '[^' + self.token + ']'

        match_one = ''.join(['*', self.token * 2])
        match_two = ''.join([self.token, '*', self.token])
        match_three = ''.join([self.token * 2, '*'])

        self.__winning_scenarios = {
            match_one: [0, 0, 6],  # *OO
            match_two: [1, 3, 4],  # O*O
            match_three: [2, 6, 2]  # OO*
        }

    def make_move(self, pos_taken, board_representation):

        winning_move = self.__get_winning_move(pos_taken)

        if winning_move >= 0:
            pos_taken[winning_move] = self.token
            board_representation[winning_move] = self.token

        else:
            pos = random.randint(0, 8)

            while pos_taken[pos]:
                pos = random.randint(0, 8)

            pos_taken[pos] = self.token
            board_representation[pos] = self.token

    def __get_winning_move(self, pos_taken):

        horizontal_move = self.__get_horizontal_move(pos_taken=pos_taken)
        if horizontal_move >= 0:
            print("The enhanced CPU found a winning horizontal move in position: ", horizontal_move + 1)
            return horizontal_move

        vertical_move = self.__get_vertical_move(pos_taken=pos_taken)
        if vertical_move >= 0:
            print("The enhanced CPU found a winning vertical move in position: ", vertical_move + 1)
            return vertical_move

        diagonal_move = self.__get_diagonal_move(pos_taken=pos_taken)
        if diagonal_move >= 0:
            print("The enhanced CPU found a winning diagonal move in position: ", diagonal_move + 1)
            return diagonal_move

        return -1

    def __get_horizontal_move(self, pos_taken):

        first_row, second_row, third_row = self.__get_positions_as_string(pos=pos_taken[:3]), \
                                           self.__get_positions_as_string(pos=pos_taken[3:6]), \
                                           self.__get_positions_as_string(pos=pos_taken[6:])

        if first_row in self.__winning_scenarios:
            smart_move = self.__winning_scenarios[first_row][0]
            if not pos_taken[smart_move]:
                return smart_move

        if second_row in self.__winning_scenarios:
            smart_move = self.__winning_scenarios[second_row][0] + 3
            if not pos_taken[smart_move]:
                return smart_move

        if third_row in self.__winning_scenarios:
            smart_move = self.__winning_scenarios[third_row][0] + 6
            if not pos_taken[smart_move]:
                return smart_move

        return -1

    def __get_vertical_move(self, pos_taken):

        first_column, second_column, third_column = self.__get_positions_as_string(pos=pos_taken,
                                                                                   start_pos=0,
                                                                                   max_pos=7,
                                                                                   pos_increase=3), \
                                                    self.__get_positions_as_string(pos=pos_taken,
                                                                                   start_pos=1,
                                                                                   max_pos=8,
                                                                                   pos_increase=3), \
                                                    self.__get_positions_as_string(pos=pos_taken,
                                                                                   start_pos=2,
                                                                                   max_pos=9,
                                                                                   pos_increase=3)

        if first_column in self.__winning_scenarios:
            smart_move = self.__winning_scenarios[first_column][1]
            if not pos_taken[smart_move]:
                return smart_move

        if second_column in self.__winning_scenarios:
            smart_move = self.__winning_scenarios[second_column][1] + 1
            if not pos_taken[smart_move]:
                return smart_move

        if third_column in self.__winning_scenarios:
            smart_move = self.__winning_scenarios[third_column][1] + 2
            if not pos_taken[smart_move]:
                return smart_move

        return -1

    def __get_diagonal_move(self, pos_taken):

        descending_diagonal, ascending_diagonal = self.__get_positions_as_string(pos=pos_taken,
                                                                                 start_pos=0,
                                                                                 max_pos=9,
                                                                                 pos_increase=4), \
                                                  self.__get_positions_as_string(pos=pos_taken,
                                                                                 start_pos=6,
                                                                                 max_pos=1,
                                                                                 pos_increase=-2)

        if descending_diagonal in self.__winning_scenarios:
            smart_move = self.__winning_scenarios[descending_diagonal][0] + \
                         self.__winning_scenarios[descending_diagonal][1]
            if not pos_taken[smart_move]:
                return smart_move

        if ascending_diagonal in self.__winning_scenarios:
            smart_move = self.__winning_scenarios[ascending_diagonal][2]
            if not pos_taken[smart_move]:
                return smart_move

        return -1

    def __get_positions_as_string(self, **kwargs):
        pos = kwargs["pos"]

        if kwargs.get("start_pos"):
            string = ''.join([' ' if pos[n] is '' else pos[n] for n in
                              range(kwargs["start_pos"], kwargs["max_pos"], kwargs["pos_increase"])])
        else:
            string = ''.join([' ' if x is '' else x for x in pos])

        return re.sub(self.regex, '*', string)


def display_menu():
    print("|------------------------------|",
          "|    Welcome to Tic Tac Toe    |",
          "|------------------------------|",
          "|      Select the mode         |",
          "|  -1: Player VS Player        |",
          "|  -2: Player VS CPU           |",
          "|  -3: Player VS CPU (Hard)    |",
          "|  -4: Exit                    |",
          "|------------------------------|", sep="\n")


def display_board(board):
    template = '|     |     |     |\n' \
               '|  {}  |  {}  |  {}  |\n' \
               '|     |     |     |'
    split = '___________________';

    f_row = template.format(board[0], board[1], board[2])
    s_row = template.format(board[3], board[4], board[5])
    t_row = template.format(board[6], board[7], board[8])

    print("\n", f_row, split, s_row, split, t_row, "\n", sep="\n")


def is_horizontal_strike(player: Player, board_pos):
    first_row, second_row, third_row = ''.join(board_pos[:3]), \
                                       ''.join(board_pos[3:6]), \
                                       ''.join(board_pos[6:])
    return player.token * 3 in [first_row, second_row, third_row]


def is_vertical_strike(player: Player, board_pos):
    first_column, second_column, third_column = ''.join([board_pos[n] for n in range(0, 7, 3)]), \
                                                ''.join([board_pos[n] for n in range(1, 8, 3)]), \
                                                ''.join([board_pos[n] for n in range(2, 9, 3)])
    return player.token * 3 in [first_column, second_column, third_column]


def is_diagonal_strike(player: Player, board_pos):
    descending_diagonal, ascending_diagonal = ''.join([board_pos[n] for n in range(0, 9, 4)]), \
                                              ''.join([board_pos[n] for n in range(2, 7, 2)])
    return player.token * 3 in [descending_diagonal, ascending_diagonal]


def is_winner(player: Player, board_pos):
    print("Checking if", Player.name, "is the winner...")
    return is_horizontal_strike(player, board_pos) or is_vertical_strike(Player, board_pos) or is_diagonal_strike(player, board_pos)


def run_game(player_one: Player, player_two: Player):
    game_round = 1
    max_rounds = 6
    pos_taken = ['', '', '', '', '', '', '', '', '']
    board_representation = ['1', '2', '3',
                            '4', '5', '6',
                            '7', '8', '9']
    while game_round < max_rounds:
        print("\n", game_round, "° ROUND")

        display_board(board_representation)
        player_one.make_move(pos_taken, board_representation)

        if is_winner(player_one, pos_taken):
            display_board(board_representation)
            print(str.format("{} is the winner! Game is over.", player_one.name))
            break

        display_board(board_representation)
        player_two.make_move(pos_taken, board_representation)

        if is_winner(player_two, pos_taken):
            display_board(board_representation)
            print(str.format("{} is the winner! Game is over.", player_two.name))
            break

        game_round += 1


def start_game():
    player_1 = Player(name="Player 1", token="X")
    player_2 = Player(name="Player 2", token="O")

    cpu = CPU(name="CPU", token="O")
    enhanced_cpu = EnhancedCPU(name="Enhanced CPU", token="O")

    display_menu()

    game_mode = int(input(" >> Please, select game mode: "))

    while game_mode != 4:
        if game_mode == 1:
            run_game(player_1, player_2)
        elif game_mode == 2:
            run_game(player_1, cpu)
        elif game_mode == 3:
            run_game(player_1, enhanced_cpu)

    print("Exiting the program...")
    quit()


start_game()
