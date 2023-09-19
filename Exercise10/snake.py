# import argparse
# import game_utils
# from snake_game import SnakeGame
# from game_display import GameDisplay
from typing import Any, Optional, List, Tuple, Dict
SNAKE_COLOUR = 0
EMPTY = "_"
# should this be a class variable ?
DIRECTIONS = {"Up", "Down", "Left", "Right"}
HORIZONTAL = 1
VERTICAL = 0


class Snake:
    def __init__(self, start_coordinates: Tuple[int, int]) -> None:
        assert start_coordinates[0] >= 0 and start_coordinates[1] >= 0
        self.__length = 3
        self.__curr_head_coord: Tuple = start_coordinates  # assume start coord are kegal
        self.__orientation: int = VERTICAL
        self.__head_direction: str = "Up"

        self.curr_coord: List[Tuple] = self.get_initial_coordinates()
        self.curr_body_coord: List[Tuple] = self.curr_coord[1:]
        self.get_bigger:int = 0


    def get_coords(self)->List[Tuple]:
        """
        getter of snake coordinates
        :return: List[Tuple]
        """
        return self.curr_coord

    def set_length(self,length)->None:
        """
        setter fnction to set new length for snake
        :return: None
        """
        assert length> self.__length
        self.__length = length

    def get_length(self)->int:
        return self.__length

    def get_head_coord(self)->Tuple:
        return self.__curr_head_coord

    def get_body_coord(self)->List[Tuple]:
        return self.curr_body_coord

    def get_snake_coord(self)->List[Tuple]:
        return self.curr_coord

    def get_initial_coordinates(self) -> List:
        """
        Method that initialize list of coordinates for snake
        """

        if self.__orientation:
            coordinates = [(self.__curr_head_coord[0] - i, self.__curr_head_coord[1]) for i in range(self.__length)]
        else:
            coordinates = [(self.__curr_head_coord[0], self.__curr_head_coord[1] - i) for i in range(self.__length)]
        assert len(coordinates) == self.__length
        return coordinates

    def _get_new_head_coord(self, direction: str) -> Tuple[int, int]:
        """
        Helper function to get new coord of head given direction
        Assume inpute legal
        """
        if direction == "Up":
            new_head_coord = (
                self.__curr_head_coord[0], self.__curr_head_coord[1] + 1)
        if direction == "Down":
            new_head_coord = (
                self.__curr_head_coord[0], self.__curr_head_coord[1] - 1)
        if direction == "Left":
            new_head_coord = (
                self.__curr_head_coord[0] - 1, self.__curr_head_coord[1])
        if direction == "Right":
            new_head_coord = (
                self.__curr_head_coord[0] + 1, self.__curr_head_coord[1])

        return new_head_coord

    def move(self) -> None:
        """
        Method to move the snake in (head_direction) direction
        need to call update_head_dirc before calling thismethod
        """

        self.__curr_head_coord = self._get_new_head_coord(self.__head_direction)  #  update new head coordinates
        self.curr_coord.insert(0, self.__curr_head_coord)
        if self.get_bigger:
            self.get_bigger -= 1
            self.__length +=1
        else:
            self.curr_coord.pop()

    def update_head_direction(self, direction) -> bool:
        """
        Method used to move direction of the snake's head before moving it
        """
        if direction and direction not in DIRECTIONS:
            return False

        if (direction == "Up" and self.__head_direction == "Down") or (direction == "Down" and self.__head_direction == "Up"):
            return True

        if (direction == "Left" and self.__head_direction == "Right") or (direction == "Right" and self.__head_direction == "Left"):
            return True
        if direction:
            self.__head_direction = direction

        return True

    def cut_body(self,coordinate)->None:
        """
        method used when the body of the snake is cut at a given coordinate
        :return: None
        """
        assert coordinate in self.curr_coord
        cut_indx = self.curr_coord.index(coordinate)
        # update snake coordinates and length
        self.curr_coord = self.curr_coord[:cut_indx] # TODO:check if need to include or not.
        self.__length = len(self.curr_coord[:cut_indx])