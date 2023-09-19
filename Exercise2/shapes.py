#################################################################
# WRITER : matan cohen , matatan , 208346320
# EXERCISE : intro2cs1 ex2
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: None
# NOTES: ...
#################################################################
import math

def shape_area():
    """
    Function that calculates area of chosen shape based on user input
    :return: area of chosen form, else None
    """
    form = int(input("Choose shape (1=circle, 2=rectangle, 3=triangle): "))

    if form == 1:
        radius = int(input())
        return math.pi * radius**2
    if form == 2:
        side1 = int(input())
        side2 = int(input())
        return side1 * side2

    if form == 3:
        side = int(input())
        const = math.sqrt(3)/4
        return const * side**2

    return None     #if form isnt 1,2,3 then return None

