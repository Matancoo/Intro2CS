#################################################################
# WRITER : matan cohen , matatan , 208346320
# EXERCISE : intro2cs1 ex2
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED:
# NOTES: ...
#################################################################
import math





def calculate_mathematical_expression(x: int, y: int, oper: str) -> float:
    """
    Calculates simple mathematical expression

    :param x: number
    :param y:number
    :param oper: operation to be performed
    :return: the output of the matematical operation or None
    """
    if oper == "+":
        return x + y
    elif oper == "-":
        return x - y
    elif oper == "*":
        return x * y
    elif oper == ":":
        return x/y
    return None


def calculate_from_string(equation: str) -> float:
    """
    Function that calculate the output of a string equation
    :param equation: Equation to be solved
    :return: the output of the matematical operation or None
    """
    equation_lst = equation.split()
    num1 = int(equation_lst[0])
    num2 = int(equation_lst[2])
    operation = equation_lst[1]
    return calculate_mathematical_expression(x = num1, y = num2, oper= operation)



if __name__ == "__main__":
    print(calculate_from_string('3 - 6'))