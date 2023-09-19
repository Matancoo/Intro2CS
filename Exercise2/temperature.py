#################################################################
# WRITER : matan cohen , matatan , 208346320
# EXERCISE : intro2cs1 ex2
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED: None
# NOTES: ...
#################################################################

def is_vormir_safe(temp_thr, temp1, temp2, temp3):
    """
    Fucntion that calculates if two number out of three surpass a certain threshold.
    :param temp_thr: threshold temperature
    :param temp1: tumperature of day 1
    :param temp2: temperature of day 2
    :param temp3: temperature of day 3
    :return: Bool value if two days out of three satisfy condition
    """
    if temp_thr < temp1 and temp_thr < temp2:
        return True
    if temp_thr < temp1 and temp_thr < temp3:
        return True
    if temp_thr < temp2 and temp_thr < temp3:
        return True

