from typing import Any, Optional, List, Tuple, Dict


class Apple:
    def __init__(self, apple_coord):
        self.__coord = apple_coord

    def get_coordinates(self):
        return self.__coord
