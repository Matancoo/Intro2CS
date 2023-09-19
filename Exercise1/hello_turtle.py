#################################################################
# FILE : hello_turtle.py
# WRITER : matan cohen , matatan , 208346320
# EXERCISE : intro2cs1 ex1 2023-
# DESCRIPTION: A simple program that...
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: https://docs.python.org/3/library/turtle.html
# NOTES: ...
#################################################################§5o7
import turtle


def draw_triangle():
    """
    Functions that draws a triangle
    :return: None
    """
    turtle.forward(45)
    turtle.right(120)
    turtle.forward(45)
    turtle.right(120)
    turtle.forward(45)
    turtle.right(120)




def draw_sail():
    """
    Function that draws snail
    :return: None
    """
    turtle.left(90)
    turtle.forward(50)
    turtle.right(150)
    draw_triangle()
    turtle.right(30)
    turtle.up()
    turtle.forward(50)
    turtle.down()
    turtle.left(90)








def draw_ship():
    """
    Function that draws ship
    :return: None
    """
    turtle.right(90)
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)

    turtle.right(120)
    turtle.forward(20)
    turtle.right(60)
    turtle.forward(180)
    turtle.right(60)
    turtle.forward(20)
    #reposition the head to look up
    turtle.right(30)

def draw_fleet():
    """
    Function that draws fleet of ships
    :return: None
    """
    turtle.left(90)
    draw_ship()
    #moving to location of second ship
    turtle.penup()
    turtle.left(90)
    turtle.forward(300)
    turtle.pendown()
    #drawing second ship
    turtle.right(90)
    draw_ship()
    turtle.penup()
    turtle.right(90)
    turtle.forward(300)




if __name__ == "__main__" :
    draw_fleet()
    turtle.done()

















