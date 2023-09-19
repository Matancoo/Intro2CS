from car import Car
from mypy import *
from typing import Set, List, Optional, Tuple, Dict, ClassVar

EXIT: Tuple = (3, 7)
BOARD_SIZE: int = 7
EMPTY: str = "_"
DIRECTIONS: Tuple = ("u", "d", "l", 'r')
ORIENTATION = {0, 1}


class Board:
    """
    Class that simulates a board used in the RusHour game

    """
    board_size: ClassVar = 7

    def __init__(self):
        self.board = [
            [EMPTY] * self.board_size for row in range(self.board_size)]

        self.cars: List[Car] = []
        self.exit_content = EMPTY

    def get_car(self, name):
        for car in self.cars:
            if car.get_name() == name:
                return car

    def __str__(self) -> str:  # TODO: DOESNT WORK
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        return "\n".join(str(row) for row in self.board)

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        coordinates = [(i, j) for i in range(self.board_size)
                       for j in range(self.board_size)]
        # TODO: check case where board size == 0
        coordinates.append(EXIT)
        return coordinates

    def possible_moves(self) -> List[Tuple]:  # TODO: DEBUG
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,move_key,description)
                 representing legal moves
        """
        possible_moves: List = []
        for car in self.cars:
            for move in car.possible_moves().keys():
                if car.movement_requirements(move)[0] in self.cell_list():
                    if self.cell_content(car.movement_requirements(move)[0]) is None:
                        possible_moves.append(
                            (car.get_name(), move, car.possible_moves()[move]))

        return possible_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return EXIT

    def cell_content(self, coordinate) -> Optional[str]:
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        used in is_valid
        ASSUMES THE COORDINATE (3,7) IS NOT TAKEN AS ARGUMENT
        """
        row, col = coordinate[0], coordinate[1]
        if coordinate in self.cell_list():
            if coordinate == EXIT:
                if self.exit_content != EMPTY:
                    return self.exit_content
                return None
            elif self.board[row][col] != EMPTY:
                return self.board[row][col]
        return None

    def is_valid(self, coordinate) -> bool:
        """
        Helper function to check if given coordinate is legal
        Used in add_car, move_car
        """
        if coordinate not in self.cell_list():  # include target
            print("this parking space is not part of the parking place!")
            return False

        if self.cell_content(coordinate) is not None:
            print("go find your own parking! Another car was here first")
            return False
        return True

    def add_car(self, car: Car) -> bool:
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """

        car_coordinates = car.car_coordinates()
        car_name = car.get_name()

        for boardcar in self.cars:
            if car_name == boardcar.get_name():
                print("the name of this car already exists in board")
                return False
            if car == boardcar:
                print("this car instance already exists in board")
        for coordinate in car_coordinates:
            if not self.is_valid(coordinate):
                return False

        # update board
        for coordinate in car_coordinates:
            self.board[coordinate[0]][coordinate[1]] = car_name
        # add car
        self.cars.append(car)
        return True

    def move_car(self, name, move_key) -> bool:
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param move_key: Key of move in car to activate
        :return: True upon success, False otherwise
        """

        # check car exists in board (necessary?)
        names_of_cars_in_board = [car.get_name()for car in self.cars]
        if name not in names_of_cars_in_board:
            return False

        car = self.get_car(name)
        next_coordinates = car.movement_requirements(move_key)[0][:]

        # deals with the case (3,7)
        if next_coordinates == EXIT:
            self.exit_content = name
            return True

        # check if car can be moved in board
        if not car.move(move_key):  # NOTE: move also updates car coordinates
            return False

        if not self.is_valid(next_coordinates):
            return False

        # delete car from board
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == name:
                    self.board[i][j] = EMPTY

        # add newly displaced car to board
        for coordinate in car.car_coordinates():
            if not self.is_valid(coordinate):
                return False
            self.board[coordinate[0]][coordinate[1]] = name

        return True
