#################################################################
# FILE : image_editor.py
# WRITER : your_name , your_login , your_id
# EXERCISE : intro2cs ex5 2022-2023
# DESCRIPTION: A simple program that...
# STUDENTS I DISCUSSED THE EXERCISE WITH: Bugs Bunny, b_bunny.
# Daffy Duck, duck_daffy.
# WEB PAGES I USED: www.looneytunes.com/lola_bunny
# NOTES: ...
#################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
from typing import Optional
import copy
import math
import pytest
import sys

##############################################################################
#                                  Functions                                 #
##############################################################################


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    """
    A function that on input (row,col,ch) return same list (ch,row,col)
    """
    image = copy.deepcopy(image)
    channels, cols, rows = len(image[0][0]), len(image[0]), len(image)
    separated_img = [[[image[row][col][channel] for col in range(
        cols)] for row in range(rows)] for channel in range(channels)]
    return separated_img


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    """
    A function that on input (ch,row,col) return same list (row,col,ch)
    """
    channels_image = copy.deepcopy(channels)
    channels, rows, cols = len(channels_image), len(
        channels_image[0]), len(channels_image[0][0])
    reconstructed_image = [[[channels_image[channel][row][col] for channel in range(
        channels)] for col in range(cols)] for row in range(rows)]
    # TODO: Review the above !
    return reconstructed_image


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    """
    A function that turns RGB images into GRAYSCALE following: RED*0.299 + GREEN*0.587 + BLUE*0.114
    """
    colored_image = copy.deepcopy(colored_image)

    channels, cols, rows = len(colored_image[0][0]), len(
        colored_image[0]), len(colored_image)

    grey_image = [[round(colored_image[row][col][0] * 0.299 + colored_image[row][col][1] *
                         0.587 + colored_image[row][col][2] * 0.114) for col in range(cols)] for row in range(rows)]
    return grey_image


def blur_kernel(size: int) -> Kernel:
    """
    Function that initiate a Uniform kernel of size (size*size)
    """
    val = 1/size**2
    kernel = [[val for col in range(size)] for row in range(size)]
    return kernel


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    """
    Function that applies a given kernel on a given image
    changes image (inplace) --> NOTE: WRONG need to appy kernel on original image !
    """
    image = copy.deepcopy(image)
    # allows to pass kernel on image without being affected by changed values
    image_copy = copy.deepcopy(image)
    num_rows = len(image)
    num_cols = len(image[0])  # assume image is symmetric
    for i in range(num_rows):
        for j in range(num_cols):
            image[i][j] = apply_kernel_on_pixel(image_copy, kernel, [i, j])
    return image


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    """
    Function which performs a billiniear interpolation given "source" representation coordinates
    return the pixel value after interpolation
    note x,y are not necesserally whole
    TODO: chekc if function can change original image
    TODO: I odnt get examples here
    """

    # identify 4 nearest pixels
    # NOTE: I dont get how works on exampls (image(x,y) or image(y,x))
    a = [math.floor(y), math.floor(x)]
    b = [math.ceil(y), math.floor(x)]  # TODO: check doesnt go out of bounds
    c = [math.floor(y), math.ceil(x)]
    d = [math.ceil(y), math.ceil(x)]

    a_val = image[a[0]][a[1]]
    b_val = image[b[0]][b[1]]
    c_val = image[c[0]][c[1]]
    d_val = image[d[0]][d[1]]

    # we will perform linear interpolation according to ratios of point a
    change_x = x - a[1]
    change_y = y - a[0]
    new_val = a_val*(1-change_x)*(1-change_y) + b_val*change_y * \
        (1-change_x) + c_val*change_x*(1-change_y) + d_val*change_x*change_y

    new_val = round(new_val)
    return new_val


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    ...
    """
    Resize image according to new_hight, new_width
    """
    image = copy.deepcopy(image)  # copies to avoid changes

    old_height = len(image)
    old_width = len(image[0])

    resized_image = [[0 for col in range(new_width)] for row in range(
        new_height)]  # empty image of target size
    left_up_pixel = image[0][0]
    right_up_pixel = image[0][old_width-1]
    left_down_pixel = image[old_height-1][0]
    right_down_pixel = image[old_height-1][old_width-1]
    set_corners(resized_image, new_height, new_width,
                left_up_pixel, right_up_pixel, left_down_pixel, right_down_pixel)

    corners = {(0, 0), (0, new_width - 1), (new_height - 1, 0),
               (new_height - 1, new_width - 1)}
    for i in range(new_height):
        for j in range(new_width):
            if (i, j) in corners:  # skip corners
                continue
            y, x = get_source_coordinates(  # changed here to y,x =
                [i, j], [old_height, old_width], [new_height, new_width])
            pixel_val = bilinear_interpolation(image, y, x)
            resized_image[i][j] = pixel_val

    return resized_image


def rotate_90(image: Image, direction: str) -> Image:
    """
    Function that rotates a given image in a given direction
    TODO: debug
    """
    image = copy.deepcopy(image)
    # if image (row,col) --> (row,col,1) else return same image
    # adds dim only if image is 1channel (row,col) --> (row,col,1)
    image = add_dim(image)
    if is_img_RGB(image):
        image = separate_channels(image)

        new_red_im = single_channel_rotate_90(image[0], direction)
        new_green_im = single_channel_rotate_90(image[1], direction)
        new_blue_im = single_channel_rotate_90(image[2], direction)
        rotated_image = combine_channels(
            [new_red_im, new_green_im, new_blue_im])

    else:
        # here I didnt convert to list --> check 1D rotation in case not RGB
        rotated_image = single_channel_rotate_90(image, direction)
        rotated_image = reduce_dim(rotated_image)
        # check if need to up dim
    return rotated_image


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    """ 
    function that thresholds the values in th eimage to allow only black or white pixels
    Threshold calculated based on average + c
    """
    image = copy.deepcopy(image)
    # We will blur the image first:
    blurring_kernel = blur_kernel(blur_size)
    blurred_image = apply_kernel(image, blurring_kernel)

    edges_image = copy.deepcopy(blurred_image)

    kernel = [[1 for col in range(block_size)] for row in range(
        block_size)]  # kernel of only ones to calculate average

    for i in range(len(image)):
        for j in range(len(image[0])):
            threshold = apply_kernel_on_pixel(
                blurred_image, kernel, [i, j])/block_size**2
            threshold -= c
            if edges_image[i][j] < threshold:
                edges_image[i][j] = 0
            else:
                edges_image[i][j] = 255

    return edges_image


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    """
    Function that quantize a single channel image pixel values based on number of desired gray levels N 
    """
    quantize_image = copy.deepcopy(image)
    for i in range(len(quantize_image)):
        for j in range(len(quantize_image[0])):
            N = int(N)
            val1 = image[i][j]*N//256
            val2 = (255/(N-1))  # NOTE:
            quantize_image[i][j] = round(val1 * val2)
    return quantize_image


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    # TODO: test function
    """
    Function that quantize colored image pixel values based on number of desired gray levels N 
    """
    image = copy.deepcopy(image)
    separated_image = separate_channels(image)
    ans = []
    for channel in range(len(separated_image)):
        quant_channel = quantize(separated_image[channel], N)
        ans.append(quant_channel)
    return combine_channels(ans)


############################################## HELPER FUNCTIONS ##############################################################################################


def apply_kernel_on_pixel(image, kernel, coordinates: list) -> int:
    """
    helper function that calculates the value of applying the kernel on given image at given coordintes
    Assume kernel averages
    """
    image = copy.deepcopy(image)
    max_row = len(image) - 1
    max_col = len(image[0]) - 1
    kernel_size = len(kernel)   # Assume symmetric
    step = kernel_size//2  # (kernel_size-1)//2   switched
    lower_left_point = [coordinates[0] - step, coordinates[1] - step]
    new_pixel = 0
    for i in range(kernel_size):
        for j in range(kernel_size):
            row_position = lower_left_point[0] + i
            col_position = lower_left_point[1] + j
            # check if coordinates are valid
            if 0 > row_position or row_position > max_row or 0 > col_position or col_position > max_col:
                val = image[coordinates[0]][coordinates[1]]
            else:
                val = image[row_position][col_position]
            new_pixel += val * kernel[i][j]
    return round(new_pixel)


def get_source_coordinates(resized_coordinates, source_image_size, resized_image_size):
    """
    Helper function that returns the source coordinates of a pixel in the resized image
    working based on : resized_coord = source_image_size/ resized_image_size
    """
    # NOTE why we set corners first and then apply ?
    resized_image_rows = resized_image_size[0] - 1
    resized_image_cols = resized_image_size[1] - 1
    source_image_rows = source_image_size[0] - 1
    source_image_cols = source_image_size[1] - 1

    ratio_rows = source_image_rows/resized_image_rows
    ratio_cols = source_image_cols/resized_image_cols
    return resized_coordinates[0]*ratio_rows, resized_coordinates[1]*ratio_cols


def set_corners(image, im_height, im_width, left_up, right_up, left_down, right_down):
    """
    helper function that sets image corners to be the inpute pixels
    inplace TODO: debug
    """
    # left_up_pixel
    image[0][0] = left_up
    image[0][im_width - 1] = right_up
    image[im_height - 1][0] = left_down
    image[im_height - 1][im_width - 1] = right_down


def is_img_RGB(image):
    """
    inpute: separated image of shape (channel, row,col)
    helper function to classify image as rgb or greyscale
    """
    if len(image[0][0]) == 3:
        return True
    return False


def single_channel_rotate_90(image, direction):
    """
    input image: (row,col,channel) (combined)
    Helper function for rotate 90.
    performes rotation on a one channel image
    Inplace
    output image: channel*row*col
    """
    combined_image = image
    # combined_image = image
    rows_num = len(combined_image)
    cols_num = len(combined_image[0])

    if direction == 'R':
        rotated_image = [[image[j][i] for j in range(rows_num)[::-1]]
                         for i in range(cols_num)]

    else:   # direction == 'L

        rotated_image = [[image[j][i]
                          for j in range(rows_num)] for i in range(cols_num)[::-1]]

    return rotated_image


def add_dim(image):
    """
    Helper function (used in rotate90)
    change shape of singleChannelImage  (row,col)--->(row,col,1)
    If image already of form (row,col,channel) --> return image
    Inplace
    TODO: how to implement this better
    """
    try:
        channel = image[0][0][0]
        return image
    except TypeError:
        reshaped_im = []
        for row in image:
            new_row = []
            for element in row:
                new_row.append([element])
            reshaped_im.append(new_row)
        return reshaped_im


def reduce_dim(image):
    """
    Helper function (used in rotate90)
    change shape of singleChannelImage  (row,col,1)--->(row,col)
    Inplace
    """

    reshaped_im = []
    for row in image:
        new_row = []
        for element in row:
            new_row.append(element[0])
        reshaped_im.append(new_row)
    return reshaped_im


def is_int(s):
    '''Checks if a string can be casted to an integer'''
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_whole(s):
    if math.floor(float(s)) == math.ceil(float(s)):
        return True
    return False


if __name__ == "__main__":

    val = True
    image_path = sys.argv[1]
    if len(sys.argv) != 2:
        print('wrong inpute : need only one argument <image_path>')
        val = False
    else:
        image = load_image(image_path)

    while True:
        operation = input(
            "chose one of the following operation to perfrom on the image\n 1.RGB-->Gray\n 2.Blurr image\n 3.resize\n 4.Rotate90\n 5.Get_edges\n 6.Quantize\n 7.Show_image\n 8.Exit ")

        if len(operation) != 1:
            print('wrong operation format chose again')
            continue
        if not is_int(operation):
            print('wrong operation format chose again')
            continue
        if not is_whole(operation):
            print('wrong operation not whole format chose again')
            continue
        if int(operation) < 1 or int(operation) > 8:
            print('wrong operation wout of range format chose again')
            continue

        if operation == '1':  # Turn to GRAYSCALE
            if not is_img_RGB(image):
                print('How do you see colors where there are nones?1 chose again ')
                continue
            image = RGB2grayscale(image)

        if operation == '2':  # Blurr image
            inpute_str = input(
                "please enter a number for the size of the blurring kernel ")
            if len(inpute_str) != 1:
                print('wrong inpute length chose again')
                continue
            if not is_int(inpute_str):
                print('wrong inpute isnt an intiger. chose again')
                continue
            if not is_whole(inpute_str):
                print('wrong inpute isnt whole. chose again')
                continue

            kernel_size = int(inpute_str)
            if kernel_size % 2 == 0 or kernel_size <= 0:
                print(
                    'inpute is not odd or not positive. only enter odd positive numbers. chose again')
                continue
            blurring_kernel = blur_kernel(kernel_size)

            # blurr RGB image
            if is_img_RGB(image):
                separated_image = separate_channels(image)
                ans = []
                for channel in range(len(separated_image)):
                    kernalized_im = apply_kernel(
                        image[channel], blurring_kernel)
                    ans.append(kernalized_im)
                image = combine_channels(ans)

            else:
                image = apply_kernel(image, blurring_kernel)

        if operation == '3':  # Resize image
            inpute_str = input(
                'please enter the new dimentions for the image.  inpute-form: (hight,width) ')
            if ',' not in inpute_str:
                print('wrong inpute please chose again which operation to perform')
                continue
            inpute_str = inpute_str.split(',')
            if len(inpute_str) != 2:
                print('wrong inpute please chose again which operation to perform')
                continue
            y, x = inpute_str[0], inpute_str[1]
            if not is_int(x) or not is_int(y):
                print('wrong inpute please chose again. see specified form')
                continue
            if not is_whole(y) or not is_whole(x):
                print(
                    'wrong inpute please chose again. numbers not whole ! see specified form')
                continue
            y, x = int(y), int(x)
            if x <= 1 or y <= 1:
                print('impossible size please chose again')
                continue

            if is_img_RGB(image):
                separated_image = separate_channels(image)
                image = combine_channels(
                    [resize(image[channel], y, x) for channel in range(len(image))])
            else:
                image = resize(image, y, x)

        if operation == '4':  # Rotate 90  R or L
            inpute_str = input(
                'Please enter L for rotating left or R for rotating right ')
            if len(inpute_str) != 1:
                print('wrong inpute please enter either L or R')
                continue
            if ord(inpute_str) != ord('L') and ord(inpute_str) != ord('R'):
                print('wrong inpute please enter either L or R')
                continue
            direction = inpute_str
            image = rotate_90(image, direction)

        if operation == '5':  # Edges
            inpute_str = input(
                'please enter a blur_size for kernel and block_size for avg.  inpute-form: (blur_size,block_size) ')

            if ',' not in inpute_str:
                print('wrong inpute please chose again which operation to perform')
                continue
            inpute_str = inpute_str.split(',')
            if len(inpute_str) != 3:
                print('wrong inpute please chose again which operation to perform')
                continue
            blur_size, block_size, c = inpute_str[0], inpute_str[1], inpute_str[2]
            if not is_int(blur_size) or not is_int(block_size) or not is_int(c):
                print('wrong inpute please chose again. see spceified form')
                continue
            if not is_whole(blur_size) or not is_whole(block_size):
                print('wrong inpute please chose again. see spceified form')
                continue

            blur_size, block_size, c = int(
                blur_size), int(block_size), float(c)
            if blur_size <= 0 or block_size <= 0 or c < 0 or blur_size % 2 == 0 or block_size % 2 == 0:
                print(
                    'wrong inpute please chose a whole, positive, odd number for sizes and non-negative number for c ')
                continue
            if is_img_RGB(image):
                image = RGB2grayscale(image)

            image = get_edges(image)

        if operation == '6':  # Quatization
            inpute_str = input(
                'please enter the number of graylevels to quatize accordingly: inpute form (int) ')

            if not is_int(inpute_str):
                print("wrong input, enter an intiger. please try again. ")
                continue
            if not is_whole(inpute_str):
                print("wrong input, enter a whole number. please try again. ")
                continue

            graylevels = int(inpute_str)
            if graylevels <= 1:
                print('wrong inpute try greylevels greater than 1')
                continue

            if is_img_RGB(image):
                image = quantize_colored_image(image, graylevels)
            else:
                image = quantize(image, graylevels)

        if operation == '7':  # Show image
            show_image(image)

        if operation == '8':  # Exit
            path = input('please enter a path to save the image')
            save_image(image, path)
            break
