#################################################################
# WRITER : matan cohen , matatan , 208346320
# EXERCISE : intro2cs1 ex2
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: None
# NOTES:Q8) I chose to check the values (1,5,1). I wrote my function with two main if statements a<=c, a>=c
#           I need to check the case where a = c which was not checked.
#           I chose to check the values (-1,-6,17) to see if the function can adequately deal with negative numbers.
#################################################################
import math

def largest_and_smallest(a, b, c):
    """
    Function that calculates largest and smallest number out of three numbers
    :param num1: first number
    :param num2: second number
    :param num3: third number
    :return: largest number, smallest number
    """
    if a<=c:
        if b<=a:
            return c, b
        elif b<=c:
            return c, a
        return b, a
    elif a>=c:
        if b<=c:
            return a, b
        elif b<=a:
            return a, c



def check_largest_and_smallest()->bool:
    """
    Function that test the above function (largest_and_smallest)
    :return: bool value for pass/unpass test
    """
    if largest_and_smallest(17,1,6) == (17,1):
        if largest_and_smallest(1,17,6) ==(17,1):
            if largest_and_smallest(1,1,2) == (2,1):
                # my own values
                if largest_and_smallest(1,5,1) == (5,1):
                    if largest_and_smallest(-1,-6,17) == (17,-6):
                        return True
    return False