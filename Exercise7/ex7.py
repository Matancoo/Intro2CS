
##############################################################################
# FILE: ex7.py
# EXERCISE: Intro2cs ex7 2022-2023
# WRITER: matan cohen
# DESCRIPTION: Ex7 only file
# additional files: ...
##############################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
import ex7_helper as h
from typing import *

##############################################################################
#                                 CONSTANTS                                  #
##############################################################################


##############################################################################
#                                 HELPER FUNCTIONS                                  #
##############################################################################


def subtract_2(x: int) -> int:
    """
    helper function to subtract two form x
    """
    return h.subtract_1(h.subtract_1(x))


# def does_devide(x: h.N, y: int) -> bool:
#     n = 1
#     return _helper_does_divide(x, y, n)


# def _helper_does_divide(x: h.N, y: int, n: int):
#     yn = log_mult(y, n)
#     if yn > x:
#         return False
#     elif yn == x:
#         return True
#     return _helper_does_divide(x, y, h.add(n, 1))


def _helper_reverse_list(lst: list[h.N], reversed_lst: list[h.N]) -> list[h.N]:
    """
    Helper function for reverseing list order
    """
    if len(lst) == 1:
        reversed_lst.append(lst[0])
    else:
        _helper_reverse_list(lst[1:], reversed_lst)
        reversed_lst.append(lst[0])
    return reversed_lst


def _compute_first_power_of_b_geq_x(b: int, x: int, n: int) -> int:
    """
    Helper function that returns the fist power of bn such that bn>=x

    """
    # Returns t = b^n where n is least such that b^n >= x
    # This is the same as:
    # while t < x: # Runs log_b(x)
    #     t = log_mult(t, b) # log(b)
    # runtime: log_b(x) * log(b)
    if n >= x:
        return n
    return _compute_first_power_of_b_geq_x(b, x, log_mult(n, b))


def _check_sub_list(l1: List[int], l2: List[int]) -> bool:
    """
    Helper functiont hat checkes if two sublists l1, l2 are equal
    """
    bool = False
    if len(l1) != len(l2):
        return False

    if len(l1) == len(l2) == 0:
        return True

    if l1[0] == l2[0]:
        bool = True

    return bool and _check_sub_list(l1[1:], l2[1:])


def _magic_help(n: int, lst1: List[Any], lst2: List[Any]) -> None:
    """
    helper function that returns [[],[[]]....]
    Asuume n>=0
    """
    assert n >= 0, " n is negative number"

    if n != 0:
        # run until the end of recurssion tree
        # NOTE: dont know if [:] necessary in function call
        return _magic_help(n-1, lst1[:], lst2[:])
    lst2.append(lst1[:])
    ls1 = lst2[:]


def _number_of_ones_in_one_integer(n: int) -> int:
    """
    helper function that calculates number of ones for the number n
    run recurssivly on each digit of n and check if eq 1
    """
    if n == 0:  # base case
        return 0

    indicator, unit_num = 0, n % 10
    if unit_num == 1:
        indicator = 1
    n = n//10
    return _number_of_ones_in_one_integer(n) + indicator

##############################################################################
#                                 EXERCISE FUNCTIONS                         #
##############################################################################


def mult(x: h.N, y: int) -> h.N:
    """
    returns  x*y
    Helper functions : add/subtract_1
    no mathematical operations used
    """
    if y == 1:
        return x
    y = h.subtract_1(y)
    return h.add(x, mult(x, y))


def is_even(n: int) -> bool:
    """
    returns True if n is even
    Helper functions : subtract_1
    """

    if n == 0:
        return True
    return not is_even(n-1)

    # if n == 0:        #NOTE working version yet less elegant
    #     return True
    # if n == 1:
    #     return False

    # n = subtract_2(n)
    # return is_even(n)


def log_mult(x: h.N, y: int) -> h.N:
    """
    returns x*y
    running time O(log(n))
    Helper functions : is_odd/add/divide_by_2
    """
    if y == 1:
        return x

    if h.is_odd(y):
        y1 = h.divide_by_2(y)
        y2 = h.add(y1, 1)
        return h.add(log_mult(x, y1), log_mult(x, y2))

    else:
        y1 = h.divide_by_2(y)
        return h.add(log_mult(x, y1), log_mult(x, y1))


def is_power(b: int, x: int) -> bool:
    """
    returns bool if power
    running time .O(log(b) * log(x)
    Helper functions : all fucntions in helper
    """
    val = _compute_first_power_of_b_geq_x(
        b, x, 1)  # NOTE mypy issue if write a oneliner here
    return val == x


def reverse(s: str) -> str:
    """
    returns reversed(str)
    Helper functions : append_to_end (no use of list/slicing/+/ no string operations)
    """

    if len(s) == 1:
        return s
    first = s[0]
    new_s = reverse(s[1:])
    return h.append_to_end(new_s, first)


def play_hanoi(hanoi: Any, n: int, src: Any, dest: Any, temp: Any) -> None:
    """
    hanoi:  object to simulate game
    n: number of disks (each of different size)
    src: object representing rode1 FROM which we move dicks
    dest: object representing rode2 TO which we move disks
    temp: object representing rode3 in the game (intermidiate rode)

    """
    if n == 0:
        return  # TODO: check if this is right
    if n == 1:
        hanoi.move(src, dest)

    else:
        play_hanoi(hanoi, n-1, src=src, dest=temp, temp=dest)
        hanoi.move(src, dest)
        play_hanoi(hanoi, n-1, src=temp, dest=dest, temp=src)


def number_of_ones(n: int) -> int:
    """
    returns # times 1 appears in [n] for different numbers (no repetitions)
    running time 
    Helper functions : %,+,-,// (no turning into str)
    """
    if n == 0:
        return 0
    return _number_of_ones_in_one_integer(n) + number_of_ones(n-1)


def compare_2d_lists(l1: list[list[int]], l2: list[list[int]]) -> bool:
    """
    Fucntion that returns whether two lists are equal
    running time 
    Helper functions : _check_sublist
    TODO: check funciton doesnt change lists 
    """

    if len(l1) != len(l2):
        return False

    if len(l1) == len(l2) == 0:  # ending condition
        return True
    return _check_sub_list(l1[0], l2[0]) and compare_2d_lists(l1[1:], l2[1:])


def magic_list(n: int) -> list[Any]:
    """
    Function that returns a list of th form [[],[[]]....]
    where each element contains all the previous ones
    Helper function: _magic_help
    """  # TODO: debug
    lst1: list[Any] = []
    lst2: list[Any] = []

    if n == 0:
        return []

    _magic_help(n, lst1, lst2)
    return lst2
