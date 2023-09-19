################################ Imports ######################################
import helper as h
import copy
import random

################################ Main functions ###############################


def init_board(rows, columns):
    """
    creates a rows * colums size board with WATER constant
    return: list of lists
    """
    board = [[h.WATER for col in range(columns)] for row in range(rows)]

    return board


def cell_loc(name):
    """
    Given user inpute str (name) the fuction converts it to a coordinate tupple for the board.
    Assume inpute is string of format "letter" + "Number"
    """
    letter = name[0].upper()
    row_index = int(float(name[1])) - 1
    column_index = ord(letter) - 65

    # check if indices are legal
    if column_index < 0 or row_index < 0:
        return
    if column_index > 25 or row_index > 98:
        return

    return (row_index, column_index)


def valid_ship(board, size, loc):
    """
    Function that checks if a given ship of size: size,  can be inserted vertic ally starting at location: loc
    """
    rows_max_index = len(board) - 1
    colums_max_index = len(board[0]) - 1

    start_row, start_col = loc[0], loc[1]

    ship_end = loc[0] + size, loc[1]
    end_row = ship_end[0] - 1

    # board bounds

    # rows
    if end_row > rows_max_index:
        return False
    if start_row > rows_max_index or start_row < 0:
        return False
    # cols
    if start_col > colums_max_index or start_col < 0:
        return False

    # content bound
    for i in range(size):
        if board[start_row + i][start_col] != h.WATER:
            return False

    return True


def create_player_board(rows, columns, ship_sizes):
    """
    initilaize board for player and allow player to inpute ships based 
    on ship_size. # A1: number of ships = len(ship_sizes)
    """
    board = init_board(h.NUM_ROWS, h.NUM_COLUMNS)
    ships_num = len(ship_sizes)

    while ships_num:
        current_ship_size = int(ship_sizes[ships_num - 1])
        h.print_board(board)
        player_inpute = h.get_input(
            " please enter a starting location 'column letter + row number' for a ship of size " + str(current_ship_size))

        # loop until player inputes a legal address
        while True:
            if is_inpute_legal(board, player_inpute):
                # check if ship coordinates are legal on board
                coordinates = cell_loc(player_inpute)
                if valid_ship(board, current_ship_size, coordinates):
                    break
            h.print_board(board)
            player_inpute = h.get_input(
                " Illegal location! please enter a different starting location for a ship of size " + str(current_ship_size))

        coordinates = cell_loc(player_inpute)
        update_board(board, coordinates, current_ship_size)
        ships_num -= 1
    return board


def fire_torpedo(board, loc):
    """
    Function that simulates firing a torpedo by chnaging
    the constant BOMB, based on where the bomb landed (loc)
    """
    rows_max_idx = len(board) - 1
    colums_max_idx = len(board[0]) - 1
    loc_row = int(float(loc[0]))  # TODO: check in debug if need int + fgloat
    loc_col = int(float(loc[1]))
    if loc_row > rows_max_idx or loc_col > colums_max_idx:
        return board

    if loc_col < 0 or loc_row < 0:
        return board

    fire_at = board[loc[0]][loc[1]]
    if fire_at == h.WATER:
        board[loc[0]][loc[1]] = h.HIT_WATER
    if fire_at == h.SHIP:
        board[loc[0]][loc[1]] = h.HIT_SHIP

    return board


def main():
    """
    Function that simulates a battleship game against the computer
    """
    while True:  # outer loop to restart game
        player_left_ships_area = sum(h.SHIP_SIZES)
        computer_left_ships_area = sum(h.SHIP_SIZES)
        coordinate_lst = [[i, j] for i in range(
            0, h.NUM_ROWS) for j in range(0, h.NUM_COLUMNS)]
        player_board = create_player_board(
            h.NUM_ROWS, h.NUM_COLUMNS, h.SHIP_SIZES)
        computer_board = init_computer_board(
            h.NUM_ROWS, h.NUM_COLUMNS, h.SHIP_SIZES)

        while player_left_ships_area and computer_left_ships_area:
            print_board(player_board, computer_board)

            # player's Turn
            player_input = h.get_input(
                " Enter column letter followed by row number for attack ")

            # deals with wrong input
            while True:
                if is_inpute_legal(computer_board, player_input):
                    break
                player_input = h.get_input(
                    " Wrong coordinates please try again! LETS DESTROY THEM ALL")

            player_attack_loc = cell_loc(player_input)

            # deal with attack on same position
            if computer_board[0][player_attack_loc[1]] != h.HIT_SHIP:
                computer_board = fire_torpedo(
                    computer_board, player_attack_loc)
                if computer_board[player_attack_loc[0]][player_attack_loc[1]] == h.HIT_SHIP:
                    computer_left_ships_area -= 1

            computer_attack_loc = h.choose_torpedo_target(
                player_board, coordinate_lst)

            # deal with attack on same position
            if player_board[computer_attack_loc[0]][computer_attack_loc[1]] != h.HIT_SHIP:
                player_board = fire_torpedo(player_board, computer_attack_loc)
                if player_board[computer_attack_loc[0]][computer_attack_loc[1]] == h.HIT_SHIP:
                    player_left_ships_area -= 1

        if player_left_ships_area:
            winning_player = "You"
        if computer_left_ships_area:
            winning_player = "The Machines"
        if not (player_left_ships_area or computer_left_ships_area):  # both must be 0 -->
            winning_player = "Nobody"
        h.print_board(player_board, computer_board)
        while True:
            input = h.get_input('The Winner of the battle is ' +
                                winning_player + '\nWould you like to play again? ')
            if input in {'Y', 'N'}:
                break
        if input == 'N':
            break
    #

################################ Helpers ######################################


def update_board(board, coordinates, ship_size):
    """
    helper function that updates board with given ship size 
    at given coordinates (row,col)
    Function doent return anything only changes board (mutable)
    used in create_player_board
    """
    row_idx = coordinates[0]
    col_idx = coordinates[1]
    for i in range(ship_size):
        board[row_idx+i][col_idx] = h.SHIP


def is_inpute_legal(board, loc) -> bool:
    """
    Helper function to check if user input is legal
    used in create_player_board, 
    """
    if len(loc) != 2:
        return False
    column_letter = loc[0]
    row_number = loc[1]
    if not h.is_int(row_number):
        return False
    row_number = int(row_number)
    if row_number <= 0 or row_number > len(board):
        return False
    max_upper_letter = 65 + len(board[0])
    max_low_letter = 98 + len(board[0])
    # accepets only upper and lower letters in that ord range
    if not ((65 <= ord(column_letter) <= max_low_letter) or (ord(column_letter) <= max_low_letter)):
        return False
    return True


def init_computer_board(rows, cols, ship_sizes):
    """
    helper function to create computer board
    """
    board = init_board(rows, cols)
    ships_num = len(ship_sizes)
    while ships_num:
        current_ship_size = int(ship_sizes[ships_num - 1])
        # chose right cell in board to insert ship of current_size
        legal_locations = [(i, j) for i in range(rows) for j in range(
            cols) if valid_ship(board, current_ship_size, (i, j))]
        cell = h.choose_ship_location(
            board, current_ship_size, legal_locations)

        update_board(board, cell, current_ship_size)
        ships_num -= 1
    return board


def print_board(player_board, computer_board):
    """
    helper function that uses h.print_board. 
    """
    hidden_board = copy.deepcopy(
        computer_board)
    for i in range(len(hidden_board)):
        for j in range(len(hidden_board[i])):
            if hidden_board[i][j] != h.HIT_SHIP and hidden_board[i][j] != h.HIT_WATER:
                hidden_board[i][j] = h.WATER
    h.print_board(player_board, hidden_board)


if __name__ == '__main__':
    main()
