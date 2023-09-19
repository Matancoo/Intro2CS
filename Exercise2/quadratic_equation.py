#################################################################
# WRITER : matan cohen , matatan , 208346320
# EXERCISE : intro2cs1 ex2
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: None
# NOTES: ...
#################################################################

import math

def quadratic_equation(a, b, c):
    """
    function that calculates roots of quadratic equation
    :param a: coef of x**2
    :param b: coef of x
    :param c: coef of free variable
    :return: tupple of roots if exists, else None
    """
    descriminant = b**2 - 4*a*c
    if descriminant > 0:   # two solutions
        root1 = (math.sqrt(descriminant) - b)/2*a
        root2 = (-math.sqrt(descriminant) - b)/2*a
    elif descriminant == 0: # one solution
        root1 = -b/(2*a)
        root2 = None
    else:                   # no solutions
        root1 = None
        root2 = None
    return root1, root2


def quadratic_equation_user_input():
    """
    Function that present quadratic roots solutions to user
    :return: solutions of quadratic equation
    """
    user_input = input("Insert coefficients a, b, and c: ").split(" ")
    a = int(user_input[0])
    b = int(user_input[1])
    c = int(user_input[2])

    if a == 0:
        print("The parameter 'a' may not equal 0")
        return
    discriminant = b ** 2 - 4 * a * c

    if discriminant > 0:
        x,y = quadratic_equation(a, b, c)
        print("The equation has 2 solutions:" , x ,"and", y)

    elif discriminant == 0:
        x, y = quadratic_equation(a, b, c)
        print("The equation has 1 solution:", x)

    elif discriminant<0:
        print("The equation has no solutions")
