from typing import List, Tuple, Iterable, Optional
import math
import functools
import time
from boggle_board_randomizer import *
Board = List[List[str]]
Path = List[Tuple[int, int]]

#################################################### HELPER FUNCTIONS ##################################################


def is_coordinate_in_board(board: Board, coordinate: tuple) -> bool:
    """
    This method checks return True if a given coord is in the given board, and false otherwise
    """
    row, col = coordinate
    return (0 <= row < len(board)) and (0 <= col < len(board[0]))


def get_word(board, path: List[Tuple]):
    """
    This method get a path on a given board and return the word the path creat.
    """
    word = ""
    for coord in path:
        x, y = coord
        word += board[x][y]
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

############################################# 3 EXERCISE ################################################################


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """
    function that checks if given path is legal and creat a legal word.
    If so, it return the word. else, it return None.
    """
    if len(path) == 0:
        return

    word = ""
    for i in range(len(path)-1):
        if not is_coordinate_in_board(board, path[i]) or not is_coordinate_in_board(board, path[i+1]):
            return None

        # check if advance is legal
        curr_row, curr_col = path[i]
        next_row, next_col = path[i + 1]
        if abs(next_row-curr_row) > 1 or abs(next_col-curr_col) > 1:
            return None
        word += board[curr_row][curr_col]

    last_row, last_col = path[-1]
    word += board[last_row][last_col]

    if word in words:
        return word


def _find_length_n_paths(n: int, board: Board, start_coor: Tuple[int], current_path: List[Tuple[int]], words: Iterable[str], all_valid_paths: List[List[Tuple]]):
    """This is an helper method to find_length_n_paths.
    It update all_valid_paths according to the valid paths from size n on board. """

    row, col = start_coor
    current_path.append(start_coor)

    # base condition
    if not is_coordinate_in_board(board, start_coor):
        # current_path.pop(-1)
        return
    if start_coor in current_path[:-1]:
        # current_path.pop(-1)
        return
    if len(current_path) == n:
        if is_valid_path(board, current_path, words):
            if current_path not in all_valid_paths:
                all_valid_paths.append(current_path[:])
        return

    possible_moves = [(row + 1, col + 1), (row + 1, col), (row, col + 1), (row - 1, col - 1),
                      (row - 1, col), (row, col - 1), (row + 1, col - 1), (row - 1, col + 1)]

    for move in possible_moves:
        _find_length_n_paths(n, board, move, current_path,
                             words, all_valid_paths)
        current_path.pop(-1)
        row, col = current_path[-1]


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    This method return a list of all legal paths of size n on board.
    """
    all_valid_paths: List[List[Tuple]] = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            start_coord = (row, col)
            _find_length_n_paths(n, board, start_coord,
                                 [], words, all_valid_paths)

    return all_valid_paths


def _find_length_n_words(n: int, board: Board, start_coor: Tuple[int], curr_path: List[Tuple[int]], words: Iterable[str], all_valid_paths: List[List[Tuple]]):
    """
    This is an helper method to find_length_n_words.
    It update the all_valid_paths according to the valid paths of words from size n on board.
    """
    row, col = start_coor

    curr_path.append(start_coor)

    # base condition
    if not is_coordinate_in_board(board, start_coor):
        return
    if start_coor in curr_path[:-1]:
        return
    if len(curr_path) > n:
        return
    curr_word = get_word(board, curr_path)
    if len(curr_word) > n:
        return

    bool_indicator = sum(list(map(lambda x: x.startswith(curr_word), words)))
    if not bool_indicator:  # return if no word in dict start with current word
        return

    if len(curr_word) == n:
        if is_valid_path(board, curr_path, words):
            if curr_path not in all_valid_paths:
                all_valid_paths.append(curr_path[:])
                return

    possible_moves = [(row + 1, col + 1), (row + 1, col), (row, col + 1), (row - 1, col - 1),
                      (row - 1, col), (row, col - 1), (row + 1, col - 1), (row - 1, col + 1)]

    for move in possible_moves:
        _find_length_n_words(n, board, move, curr_path, words, all_valid_paths)
        curr_path.pop(-1)
        row, col = curr_path[-1]


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    This method return all the legal paths of words from size n on the given board.
    """
    all_valid_paths: List[List[Tuple]] = []
    # run on all coordinates in board
    for row in range(len(board)):
        for col in range(len(board[0])):
            start_coord = (row, col)
            _find_length_n_words(n, board, start_coord,
                                 [], words, all_valid_paths)

    return all_valid_paths


def max_score_paths(board, words):
    """
     This method return a list of legal paths who generate the highest score of the game with the given board and legal words collection.
     TECHNIC:
     1. take every coordinate on the board as a starting_letter
     2. send the starting_letter to the helper method that update the max_paths_dict of every word that starts in the starting_letter word.
     3. return a list of all the values in max_paths_dict, thats are the max path of every legal word on the board.
     """
    words_by_max_path = dict()

    for row in range(len(board)):
        for col in range(len(board[0])):
            starting_letter = board[row][col]
            _max_score_paths(board, words, starting_letter, [
                (row, col)], words_by_max_path)

    return [words_by_max_path[word] for word in words_by_max_path]


def _max_score_paths(board, words, curr_word, curr_path, words_by_max_path):
    """
    This is an helper method to max_score_paths.
    Every step update max_paths_dict according to the max path of the current relevent words.
    TECHNIC:
    1. for every possible step from the last coordinate of the curr_path:
        a. add the step to the curr_path and its value to the curr_word
        b. check if there are legal words that starts in the curr_word
        c. if so - find the max path of them in reqursia.
            else - "clean" and go to the next step
    2. if a legal word was found - add cuur_path to the dictionary if it is a new word or if the path is longer.
    3. "clean" - pop the added coordinate from the path and its value from the word,
            so we can iterate on all the possible steps.
    """

    # check if the curr_word that the curr_path generated is a legal word
    if curr_word in words:
        if curr_word in words_by_max_path.keys():  # check if the curr_word was already found
            if len(curr_path) > len(words_by_max_path[curr_word]):
                words_by_max_path[curr_word] = curr_path[:]
        else:
            words_by_max_path[curr_word] = curr_path[:]

    possible_moves = [(curr_path[-1][0] + 1, curr_path[-1][1] + 1), (curr_path[-1][0] + 1, curr_path[-1]
                                                                     [1]), (curr_path[-1][0], curr_path[-1][1] + 1), (curr_path[-1][0] - 1, curr_path[-1][1] - 1), (curr_path[-1][0] - 1, curr_path[-1][1]), (curr_path[-1][0], curr_path[-1][1] - 1), (curr_path[-1][0] - 1, curr_path[-1][1]+1), (curr_path[-1][0]+1, curr_path[-1][1] - 1)]
    # get all legal moves on board from the last step
    possible_moves = [
        move for move in possible_moves if is_coordinate_in_board(board, move) and move not in curr_path]
    for move in possible_moves:
        i, j = move
        curr_path.append(move)
        curr_word += board[i][j]
        # get all the valid words that start with the current word
        relevant_words = {
            legal_word for legal_word in words if legal_word.startswith(curr_word)}
        if len(relevant_words) != 0:
            _max_score_paths(
                board, relevant_words, curr_word, curr_path, words_by_max_path)
        curr_path.pop()
        illegal_addition = board[i][j]
        end_word_in = len(curr_word)-len(illegal_addition)
        curr_word = curr_word[: end_word_in]
