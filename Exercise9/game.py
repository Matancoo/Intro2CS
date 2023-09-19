from board import Board
from car import Car
from helper import *
from typing import Set, List, Optional, Tuple, Dict
import sys

EXIT: Tuple = (3, 7)
BOARD_SIZE: int = 7
EMPTY: str = "_"
DIRECTIONS: Tuple = ("u", "d", "l", 'r')
ORIENTATION: Set = {0, 1}
LEGAL_NAMES = {"Y", "B", "O", "G", "W", "R"}


class Game:
    """
    Class that simulates the Rushour game by calling car and board classes
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # init empty board
        self.board: Board = board

    def input_cars_in_board(self, cars_dict: Dict) -> bool:  # DEBUG
        """
        Assume board is empty
        Helper funtion that given a dictionary of cars, updates board
        cars_dict = {name: (length,head_location,orientation)}
        """
        for item in cars_dict.items():
            name = item[0]
            length = item[1][0]
            head_location = item[1][1]
            orientation = item[1][2]

            try:  # NOTE: would have been more elegant to use function that return bool + updates instead of exceptions
                car = Car(name, length, head_location, orientation)
            except Exception:
                continue
            # inpute passed the requirements from class Car
            # check game requirement for car:
            if name not in LEGAL_NAMES:
                continue
            if not 2 <= int(length) <= 4:
                continue

            # add car to board
            if self.board.add_car(car):
                continue
        if len(self.board.cars) == 0:
            print("no viable cars in board")
            return False
        return True

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        print(self.board)
        actual_cars_names = [car.get_name() for car in self.board.cars]
        user_inpute = input("enter: car_name,move_direction")

        if user_inpute == "!":
            print("game has ended")
            return True

        if len(user_inpute) != 3 or (user_inpute[0] not in actual_cars_names) or (user_inpute[2] not in DIRECTIONS):
            print("user inpute wrong")
            return False

        if self.player_has_won(user_inpute[0], user_inpute[2]):
            print(self.board)
            print("player has won")
            return True

        if not self.board.move_car(user_inpute[0], user_inpute[2]):
            print("could not move car in board")
            return False

        print(self.board)
        return False

    def player_has_won(self, name, move_key):
        """
        helper fucntion to check if player has won
        used in play
        """
        car = self.board.get_car(name)
        if car.get_orientation():
            if car.movement_requirements(move_key)[0] == EXIT:
                return True
        return False

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while True:
            if self.__single_turn():
                print("End of Game")
                break


if __name__ == "__main__":
    # TODO: I assume no two cars have the same name
    # TODO: hard to propagate exceptions as the API forces us to return bools values
    print(sys.argv)
    user_arguments = sys.argv[1:]

    # TODO: input only relative path here
    cars_dict: Dict = load_json("car_config.json")
    board = Board()
    game = Game(board)
    if game.input_cars_in_board(cars_dict):
        game.play()
