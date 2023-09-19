
################################################ IMPORTS #############################################################

from ex11_utils import *
import boggle_board_randomizer
################################################ class  ############################################################

class BoggleGame():

    def __init__(self,board:Board,words:set):
        self.__words = words
        self.__board = board
        self.__current_path:List = []
        self.__score :int = 0
        self.__legal_chosen_words:List = []
        self.__starting_time = 0


################################### GETTERS ##########################################
    def get_score(self):
        return self.__score

    def get_legal_chosen_words(self):
        """
        used to get all the words the player already chose
        """
        return self.__legal_chosen_words

    def get_path(self):
        """
        Method that returns the current path
        """
        return self.__current_path

    def get_curr_word(self)->str:
        """
        :return: the word corresponding to the current path
        """
        word = ""
        for coord in self.__current_path:
            x, y = coord
            word += self.__board[x][y]
        return word

    def is_step_legal(path, coordinate: Tuple) -> bool:
        """
        function that checks if the addition of given coordinate is legal
        :return:
        """
        if not path:
            return True
        elif coordinate in path:
            return False
        prev_x, prev_y = path[-1]
        x, y = coordinate
        if abs(prev_x - x) > 1 or abs(prev_y - y) > 1:
            return False
        return True

################################### SETTERS ##########################################

    def is_curr_path_legal(self)->bool:
        """
        Method that checks if current path is legal
        if so append corresponding word to lgal_chosen_words
        otherwise delete path coordinates
        :return: bool
        """
        if is_valid_path(self.__board,self.__current_path,self.__words):
            word = get_word(self.__board,self.__current_path)
            self.__legal_chosen_words.append(word)
            self.update_score() #uses current_path
            self.__current_path = []
            return True
        self.__current_path = []
        return False

    def start_game(self):
        """
        Method that start the game

        """
        self.__starting_time = time.time()

    def is_game_over(self)->bool:
        current_time = time.time()
        time_passed = current_time - self.__starting_time
        if time_passed>180:
            return True
        return False

    def end_game(self):
        """
        Method called when game ends
        :return: TODO: do we need this
        """
        pass

    def can_add_to_path(self,coordinate):
        """
        Method used to get coordinates from user and update path if needed
        :return:
        """

        if is_step_legal(path=self.get_path(),coordinate = coordinate):
            self.__current_path.append(coordinate)
            return True

    def is_path_legal(self):
        """
        method that checks if given word has a legal path
        :return:
        """
        word = is_valid_path(self.__board, self.__current_path, self.__words)
        if word and word not in self.__legal_chosen_words:
            self.__legal_chosen_words.append(word)
            return True
        return False

    def update_score(self):
        """
        method used to update player score
        valid_word score == len(word)**2
        :return:
        """
        self.__score += len(self.__current_path) ** 2

