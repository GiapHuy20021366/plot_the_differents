'''
    This level simple change color of a rect or rotate it
'''

import random
from setup.constants import *
from utils.task1_tools import *
import cv2


# Simple replace color a rect by random color
def change_rect_color(opencv_img, num_range):
    shape = opencv_img.shape
    width, height = shape[1], shape[0]
    points = generate_rally(100, width - 50, height - 50, num_range)
    g_img = opencv_img.copy()
    # diff_rects = []
    for i in range(num_range):
        x, y = points[i]
        range_width = random.randint(20, 50)
        range_height = random.randint(20, 50)
        # rect = g_img[y:y+range_height, x:x+range_width]
        # rect = similar_color_change(opencv_img, rect, (y, x))
        # g_img = replace_range(g_img, rect, (y, x))
        g_img[y:y+range_height, x:x+range_width] = rand_color()
    return g_img


# This filter calculate SSIM score between two opencv img and
# check does it in range of MIN_SSIM and MAX_SSIM
def filter(img1, img2):
    score, _ = calc_ssim(img1, img2, (0, 0, img1.shape[1], img1.shape[0]))
    # print(score)
    return score >= MIN_SSIM and score <= MAX_SSIM


# Flip some rect in opencv img
def flip_rect(opencv_img, num_range):
    shape = opencv_img.shape
    width, height = shape[1], shape[0]
    points = generate_rally(100, width - 50, height - 50, num_range)
    g_img = opencv_img.copy()
    # diff_rects = []
    for i in range(num_range):
        x, y = points[i]
        range_width = random.randint(40, 50)
        range_height = random.randint(40, 50)
        range_img = g_img[y:y+range_height, x:x+range_width]
        direct = random.randint(0, 2)
        flip_range = cv2.flip(range_img, direct)
        if filter(range_img, flip_range):
            # diff_rects.append((x, y, range_width, range_height))
            g_img = replace_range(g_img, flip_range, (y, x))
    return g_img


if __name__ == "__main__":
    print(generate_rally(100, 600, 399, 8))
