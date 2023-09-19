#################################################################
# FILE : math_print.py
# WRITER : matan cohen , matatan , 208346320
# EXERCISE : intro2cs1 ex1 2023
# DESCRIPTION: A simple program that...
# STUDENTS I DISCUSSED THE EXERCISE WITH: None

# WEB PAGES I USED: None
# NOTES: ...
#################################################################

import math



def golden_ratio():
    """
    Function that prints the golden ratio
    :return: None
    """
    ans = 1 + (math.sqrt(5))
    print(ans/2)

def six_squared():
    """
    Function that prints the number 6 to the power of 2\
    :return: None
    """
    print(6**2)

def hypotenuse():
    """
    Function that prints the hypotenuse of a right angle triangle
    with sides of length 5 and 12
    :return: None
    """
    print(math.hypot(12.0,5.0))



def pi():
    """
    Functions that prints the value of pi
    :return: None
    """
    print(math.pi)

def e():
    """
    Function that prints the euler number e
    :return: None
    """
    print(math.e)

def squares_area():
    """
    Function that prints the areas of squares from vertices of length 1 to 10
    :return: None
    """

    print(1*1,2*2,3*3,4*4,5*5,6*6,7*7,8*8,9*9,10*10)




if __name__ == "__main__" :
    golden_ratio()
    six_squared()
    hypotenuse()
    pi()
    e()
    six_squared()




