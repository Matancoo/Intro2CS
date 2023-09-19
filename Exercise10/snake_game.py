from game_display import GameDisplay
from snake import Snake
from typing import Any, Optional, List, Tuple, Dict
from walls import Wall
import argparse
from game_utils import *
from apple import Apple
import math
DIRECTIONS = {"Up", "Down", "Left", "Right"}
# TODO: check if I increase snake by 4 instead of 3 (count 0)

class SnakeGame:
    def __init__(self, args: argparse.Namespace) -> None:
        self.board_width: int = args.width
        self.board_height: int = args.height
        self.num_of_apples_to_add: int = args.apples
        self.num_of_walls_to_add: int = args.walls
        self.walls: List = []
        self.apples: List = []
        self.max_rounds : int= args.rounds
        self.curr_round: int= 0
        self.__key_clicked = None
        self.debug = args.debug
        self.snake_score: int = 0

        # init snake object
        self.__x :int=self.board_width//2
        self.__y : int= self.board_height//2
        start_coordinates = (self.__x, self.__y)
        self.snake = Snake(start_coordinates)


        # init walls with one wall
        if self.num_of_walls_to_add:
            x_coord, y_coord, direction = get_random_wall_data()
            new_wall = Wall((x_coord, y_coord), direction)
            if self._is_wall_valid(new_wall):
                self.walls.append(new_wall)
                self.num_of_walls_to_add -=1


        # init apples with one apple
        if self.num_of_apples_to_add:
            apple_coord = get_random_apple_data()
            new_apple = Apple(apple_coord)
            if self._is_apple_valid(new_apple):
                self.apples.append(new_apple)
                self.num_of_apples_to_add -= 1


    def coord_not_in_board(self,coord:Tuple)->bool:
        """
        Method that checks if given coord not in board
        :return: bool
        """
        x,y = coord[0],coord[1]
        return (x<0 or x>= self.board_width or y<0 or y>=self.board_height)

    def read_key(self, key_clicked: Optional[str]) -> None:
        self.__key_clicked = key_clicked

    def _create_legal_wall(self)->Wall:#DEBUG
        """
        Method used to create a new wall object as in specification
        :return: Wall
        """
        walls_coords = {coord for wall in self.walls for coord in wall.get_coordinates()}
        snake_coords = set(self.snake.get_snake_coord())
        apples_coords = {apple.get_coordinates() for apple in self.apples}
        illegal_coords = walls_coords | snake_coords | apples_coords
        while True:
            x_center, y_center, direction = get_random_wall_data()
            new_wall = Wall((x_center, y_center), direction)
            new_wall_coords = new_wall.get_coordinates()
            is_legal = True
            for coord in new_wall_coords:#TODO: see if I can change this and make it better
                if coord in illegal_coords or self.coord_not_in_board(coord):
                    is_legal = False
            if is_legal:
                return new_wall

    def _create_legal_apple(self)->Apple:#DEBUG
        """
        method used to creare a new apple as in specification
        :return: Apple
        """
        walls_coords = {coord for wall in self.walls for coord in wall.get_coordinates()}
        snake_coords = set(self.snake.get_snake_coord())
        apples_coords = {apple.get_coordinates() for apple in self.apples}
        illegal_coords = walls_coords|snake_coords|apples_coords
        while True:
            new_apple_coord = get_random_apple_data()
            if new_apple_coord not in illegal_coords and not self.coord_not_in_board(new_apple_coord):
                apple = Apple(new_apple_coord)
                break
        return apple

    def _is_apple_valid(self,apple:Apple)->bool:
        """
        Method that checks if given apple is valid
        :return:
        """
        walls_coords = {coord for wall in self.walls for coord in wall.get_coordinates()}
        snake_coords = set(self.snake.get_snake_coord())
        apples_coords = {apple.get_coordinates() for apple in self.apples}
        illegal_coords = walls_coords | snake_coords | apples_coords
        new_apple_coord = apple.get_coordinates()
        if new_apple_coord in illegal_coords or self.coord_not_in_board(new_apple_coord):
            return False
        return True

    def _is_wall_valid(self,wall:Wall)->bool:
        """
        Mehtod that checks if given wall is valid
        :return:
        """
        walls_coords = {coord for wall in self.walls for coord in wall.get_coordinates()}
        snake_coords = set(self.snake.get_snake_coord())
        apples_coords = {apple.get_coordinates() for apple in self.apples}
        illegal_coords = walls_coords | snake_coords | apples_coords
        for coord in wall.get_coordinates():
            if coord in illegal_coords or self.coord_not_in_board(coord):
                return False
        return True

    def update_walls(self)->None:
        """
        Methode used to add walls if actual wall number < self.wall_num
        :return: None
        """
        if self.num_of_walls_to_add:
            x_coord,y_coord,direction = get_random_wall_data()
            new_wall = Wall((x_coord,y_coord),direction)
            if self._is_wall_valid(new_wall):
                self.walls.append(new_wall)
                self.num_of_walls_to_add -= 1

    def _all_coords_not_in_board(self,wall_coordinates)->bool:
        """
        Internal
        method to check if all coordinates of a given vall are out of the bounds of the board
        :return:
        """
        for coord in wall_coordinates:
            if self.coord_not_in_board(coord):
                continue
            else:
                return False
        self.num_of_walls_to_add +=1
        return True

    def move_walls(self)->None:
        """
        method to move walls
        :return: None
        """

        for wall in self.walls:
            wall.move()
        # update walls
        self.walls = [wall for wall in self.walls if not self._all_coords_not_in_board(wall.get_coordinates())]

    def update_apples(self)->None:
        """
        methode that add apple in board is actual apple number < self.apple_num
        :return:None
        """
        if self.num_of_apples_to_add:
            new_apple_coord = get_random_apple_data()
            apple = Apple(new_apple_coord)
            if self._is_apple_valid(apple): # else it will update apples in the next round
                self.apples.append(apple)
                self.num_of_apples_to_add -= 1

    def update_score(self)->None:
        """
        method used to update score only if snake ate apple.
        the score is calculated on the length of the snake prior to eating the apple
        (we update snake length in the snake move method bfore updating score)
        :return:
        """
        prev_snake_length = self.snake.get_length() -1
        self.snake_score += math.floor(math.sqrt(prev_snake_length))

    def update_objects(self) -> None:
        """
        Function that update objects based on inpute key
        if key is wrong -> None
        :return: None
        """
        curr_move = self.__key_clicked

        snake_coord = self.snake.get_snake_coord()
        snake_head = snake_coord[0]
        if self.snake.update_head_direction(curr_move):
            self.snake.move()

        # update_walls
        if self.curr_round % 2 == 0:
            self.move_walls()
        self.update_walls()  # TODO: changed wall update position

        # if apple was eaten -> update snake
        good_apples = []
        for apple in self.apples:
            if apple.get_coordinates() in [coord for wall in self.walls for coord in wall.get_coordinates()]:
                self.num_of_apples_to_add +=1
                continue
            if snake_head != apple.get_coordinates():
                good_apples.append(apple)
            else:
                self.snake.get_bigger += 3
                self.num_of_apples_to_add +=1
                self.update_score()

        self.apples = good_apples

        self.update_apples()  # add apple if needed

    def draw_board(self, gd: GameDisplay) -> None:
        """
        Method used to draw board gui
        :param gd: GameDisplay
        :return: None
        """
        if not self.debug:
        # draw snake
            snake_coords = self.snake.get_coords()
            for coord in snake_coords:
                if self.coord_not_in_board(coord):
                    continue
                gd.draw_cell(coord[0], coord[1], "black")

        # draw wall
        for wall in self.walls:
            for wall_coord in wall.get_coordinates():
                if self.coord_not_in_board(wall_coord):
                    continue
                gd.draw_cell(wall_coord[0], wall_coord[1], 'blue')

        # draw apples
        for apple in self.apples:
            apple_coord = apple.get_coordinates()
            gd.draw_cell(apple_coord[0], apple_coord[1], 'green')

    def end_round(self) -> None:
        """
        Methojd that updates current round
        :return: None
        """
        self.curr_round += 1

    def is_over(self) -> bool:
        """
        Method that checks if game is over
        :return: bool
        """
        if self.max_rounds == 0:
            return True
        elif self.max_rounds != -1 and  self.curr_round == self.max_rounds +1 :
            return True


        snake_coords = self.snake.get_snake_coord()
        snake_head_coord = snake_coords[0]
        snake_body_coord = snake_coords[1:]

        # check snake in board
        if self.coord_not_in_board(snake_head_coord):
            # self.snake.curr_coord.pop(0) #POP the head
            return True
        # check self collisions
        elif len(snake_coords) != len(set(snake_coords)):
            return True

        # check wall collisions
        for wall in self.walls:
            # head collision --> end of game:
            if snake_head_coord in wall.get_coordinates():
                    return True
            # body collisions --> moving wall, cut body
            for coord in snake_body_coord:
                if coord in wall.get_coordinates():
                    self.snake.cut_body(coord)
                    break
            if self.snake.get_length() == 1:
                    return True

        return False

