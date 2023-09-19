#################################################################
# WRITER : matan cohen , matatan , 208346320
# EXERCISE : intro2cs1 ex2
# STUDENTS I DISCUSSED THE EXERCISE WITH: None
# WEB PAGES I USED:
# NOTES: ...
################################ Imports ######################################

################################ Constants ####################################


################################ Main functions ###############################
def input_list() -> list:
    """
    Functions that returns a list of inputs with their sum at output[-1]
    :return: list of numbers where last number is sum.
    """
    answer_list = []
    sum_counter = 0
    while True:
        user_input_number = input()
        if user_input_number == "":
            break
        user_input_number = float(user_input_number)
        answer_list.append(user_input_number)
        sum_counter += user_input_number
    answer_list.append(sum_counter)
    return answer_list


def inner_product(vec_1, vec_2) -> int:
    """
    Functions that calculates the dot product between two vectors.
    :param vec_1: vector of type list
    :param vec_2: vector of type list
    :return: (int) dot product
    """
    dot = 0
    length_v1, length_v2 = len(vec_1), len(vec_2)
    if length_v1 != length_v2:
        return None
    elif not vec_1 or not vec_2:
        return dot
    for i in range(length_v1):
        dot += vec_1[i] * vec_2[i]
    return dot


def sequence_monotonicity(sequence) -> list:
    """
    Functions that return a boolean list expressing the monotonicity characteristic
    :param sequence: list of number
    :return: list of bool values (see helper functions)
    """
    answer = [False, False, False, False]
    answer[0] = is_mono_increasing(sequence)
    answer[1] = is_real_mono_increasing(sequence)
    answer[2] = is_mono_decreasing(sequence)
    answer[3] = is_real_mono_decreasing(sequence)
    if len(sequence) <= 1:
        answer = [1, 1, 1, 1]
    return answer


def monotonicity_inverse(def_bool) -> list:
    """
    given a boolean list the function returns a sequence example.
    """
    if def_bool[0] == 1 and def_bool[1] == 0 and def_bool[2] == 1 and def_bool[3] == 0:
        equal_sequence = [1, 1, 1, 1]
        return equal_sequence

    if def_bool[0] == 0 and def_bool[1] == 0 and def_bool[2] == 0 and def_bool[3] == 0:
        mono_increase = [1, 0,-1, 1]
        return mono_increase

    if def_bool[0] == 0 and def_bool[1] == 0 and def_bool[2] == 0 and def_bool[3] == 1:
        return

    if def_bool[0] == 1 and def_bool[1] == 0 and def_bool[2] == 0 and def_bool[3] == 0:
        mono_increase = [1, 2, 3, 3]
        return mono_increase
    if def_bool[0] == 1 and def_bool[1] == 1 and def_bool[2] == 0 and def_bool[3] == 0:
        equal_mono_increase = [1, 2, 3, 4]
        return equal_mono_increase
    if def_bool[0] == 0 and def_bool[1] == 0 and def_bool[2] == 1 and def_bool[3] == 0:
        mono_decrease = [4, 3, 3, 2, 1]
        return mono_decrease
    if def_bool[0] == 0 and def_bool[1] == 0 and def_bool[2] == 0 and def_bool[3] == 1:
        real_mono_decease = [4, 3, 2, 1]
        return real_mono_decease
    if def_bool[0] == 0 and def_bool[1] == 0 and def_bool[2] == 1 and def_bool[3] == 1:
        equal_mono_decrease = [4, 3, 2, 1]
        return equal_mono_decrease
    return None


def convolve(mat):
    """
    1D convolution operation on matrix
    """
    if not mat:  # check if list is empty
        return
    convoluted_matrix = []
    rows_num = 1 + len(mat) % 3
    columns_num = 1 + len(mat[0]) % 3
    for row in range(rows_num):
        convoluted_matrix.append([])
        for col in range(columns_num):
            convoluted_matrix[row].append(calculate_kernel_for_index(mat, (row, col)))
    return convoluted_matrix


def sum_of_vectors(vec_lst):
    """
    function that calculates the pointwise sum of two vectors
    """
    if not vec_lst:
        return
    elif not vec_lst[0]:  # checks that inner lists are not empty (assume all same length)
        return []
    current_list = len(vec_lst)
    sub_list_length = len(vec_lst[0])
    answer_list = list(range(sub_list_length))
    for i in range(sub_list_length):
        current_sum = 0
        for j in range(current_list):
            current_sum += vec_lst[j][i]
        answer_list[i] = current_sum
    return answer_list


def num_of_orthogonal(vectors):
    """
    return the number of pairs of vectors that are orthogonal to each other
    """
    answer_counter = 0
    lists_count = len(vectors)
    for i in range(lists_count):
        for j in range(i + 1, lists_count):
            if not inner_product(vectors[i], vectors[j]):
                answer_counter += 1
    return answer_counter


################################ Helpers ######################################
def is_mono_increasing(sequence):
    """
    sequence_monotonicity helper function
    """
    for i in range(len(sequence) - 1):
        if sequence[i] > sequence[i + 1]:
            return False
    return True


def is_real_mono_increasing(sequence):
    """
    sequence_monotonicity helper function
    """
    for i in range(len(sequence) - 1):
        if sequence[i] >= sequence[i + 1]:
            return False
    return True


def is_mono_decreasing(sequence):
    """
    sequence_monotonicity helper function
    """
    for i in range(len(sequence) - 1):
        if sequence[i] < sequence[i + 1]:
            return False
    return True


def is_real_mono_decreasing(sequence):
    """
    sequence_monotonicity helper function
    """
    for i in range(len(sequence) - 1):
        if sequence[i] <= sequence[i + 1]:
            return False
    return True


def calculate_kernel_for_index(mat, index: tuple):
    """
    helper function for convolution
    function that calculates the convolution operation with a 3*3 kernel.
    I consider the (i,j) index as the top left corner of the kernel.
    """
    final_sum = 0
    for i in range(index[0], index[0] + 3):
        for j in range(index[1], index[1] + 3):
            final_sum += mat[i][j]

    return final_sum

