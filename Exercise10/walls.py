from typing import Any, Optional, List, Tuple, Dict

VERTICAL_DIRECTIONS = {"Up", "Down"}
HORIZONTAL_DIRECTIONS = {"Left", "Right"}


class Wall:
    def __init__(self, center_coord: Tuple[int, int], direction: str):
        self.__center_coord = center_coord
        self.__direction = direction
        self.__length = 3

    def get_coordinates(self):
        x_center, y_center = self.__center_coord[0],self.__center_coord[1]
        wall_coordinates: List[Tuple[int, int]] = []
        direction = self.__direction

        if direction in HORIZONTAL_DIRECTIONS:
            #TODO: how to deal with walls
            wall_coordinates.append((x_center-1, y_center))
            wall_coordinates.append((x_center, y_center))
            wall_coordinates.append((x_center+1, y_center))
            # wall_coordinates.append((x_center, y_center))
            # wall_coordinates.append((x_center+1, y_center))
            # wall_coordinates.append((x_center+2, y_center))
        elif direction in VERTICAL_DIRECTIONS:
            wall_coordinates.append((x_center, y_center - 1))
            wall_coordinates.append((x_center, y_center))
            wall_coordinates.append((x_center, y_center+1))
            # wall_coordinates.append((x_center, y_center))
            # wall_coordinates.append((x_center, y_center+1))
            # wall_coordinates.append((x_center, y_center +2))
        return wall_coordinates

    def move(self): #TODO: check
        """
        Method used to move board in given direction
        Updates center_Coord
        :return: None
        """
        wall_coords = self.get_coordinates()
        if self.__direction  == "Up" or self.__direction== "Right":
            self.__center_coord = wall_coords[-1]
        else:
            self.__center_coord = wall_coords[0]


