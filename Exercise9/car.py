from mypy import *
from typing import Set, List, Optional, Tuple, Dict

ORIENTATION: Set = {0, 1}


class Car:
    """
    car class used to initiate car objects for our rushour game
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # TODO: do i want any of these to be private ?
        # I dont get when to make variable/method private

        try:
            row, col = int(location[0]), int(location[1])
            length, orientation = int(length), int(orientation)
        except Exception as err:
            print("wrong input:(location or length or orientation) ", err)

        if length <= 0:
            raise ValueError("length of car must be positive")

        if orientation not in ORIENTATION:
            raise ValueError(
                "car orientation must be horizonatal (1) or vertical (0)")
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation


################################ GETTERS #########################
    # TODO: should I return these if i dont want them to be touched ?


    def get_name(self) -> str:
        """
        return: the name of this car.
        """
        return self.__name

    def get_length(self) -> int:
        """
        return: the length of this car.
        """
        return self.__length  # immutable

    def get_location(self) -> tuple:
        """
        :return: the location of this car.
        """
        return self.__location  # immutable

    def get_orientation(self) -> int:
        """
        :return: the orientation of this car.
        """
        return self.__orientation  # immutable

    def car_coordinates(self) -> List:
        """
        :return: A list of coordinates the car is in
        """
        coordinates: List = []
        if self.__orientation:                # car is vertical
            for i in range(self.__length):
                coordinates.append((self.__location[0], self.__location[1]+i))

        else:                                 # car is horizontal
            for i in range(self.__length):
                coordinates.append((self.__location[0]+i, self.__location[1]))

        return coordinates

    def possible_moves(self) -> Dict:
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        possible_moves: Dict = dict()
        if self.__orientation:
            possible_moves["l"] = "causes the car to move left"
            possible_moves["r"] = "causes the car to move right"
        else:
            possible_moves["u"] = "causes the car to move up"
            possible_moves["d"] = "causes the car to move down"

        return possible_moves

    def movement_requirements(self, move_key) -> List:
        """ 
        :param move_key: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """

        car_coordinates: List = self.car_coordinates()
        initial_coordinate = car_coordinates[0]
        last_coordinate = car_coordinates[-1]
        possible_moves = self.possible_moves().keys()

        if move_key not in possible_moves:
            raise Exception("This car cannot move in this direction!")

        if move_key == "u":
            next_coordinate = (initial_coordinate[0]-1, initial_coordinate[1])
        if move_key == "d":
            next_coordinate = (last_coordinate[0]+1, last_coordinate[1])

        if move_key == "l":
            next_coordinate = (initial_coordinate[0], initial_coordinate[1]-1)
        if move_key == "r":
            next_coordinate = (last_coordinate[0], last_coordinate[1]+1)

        return [next_coordinate]

    def move(self, move_key) -> bool:
        """ 
        :param move_key: a string representing the key of the required move.
        :return: true upon success, false otherwise
        """
        try:
            next_car_loc: Tuple = self.movement_requirements(move_key)[0]
        except Exception:
            return False

        if move_key == 'u':
            self.__location = (self.__location[0] - 1, self.__location[1])

        elif move_key == 'd':
            self.__location = (self.__location[0] + 1, self.__location[1])

        elif move_key == 'r':
            self.__location = (self.__location[0], self.__location[1] + 1)
        elif move_key == 'l':
            self.__location = (self.__location[0], self.__location[1] - 1)
        return True
