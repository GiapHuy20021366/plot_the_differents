from generate.untils import *
from setup.constrants import *
import cv2


def replace_range(origin_img, range_r, start_pos):
    start_x, start_y = start_pos
    range_x = range_r.shape[0]
    range_y = range_r.shape[1]
    # print(start_x, start_y, range_x, range_y)
    for x in range(start_x, start_x + range_x):
        for y in range(start_y, start_y + range_y):
            origin_img[x][y] = range_r[x - start_x][y - start_y]
    return origin_img


def lv2_generate(opencv_img, num_range):
    shape = opencv_img.shape
    width, height = shape[1], shape[0]
    points = generate_rally(100, width - 50, height - 50, num_range)
    g_img = opencv_img.copy()
    for i in range(num_range):
        x, y = points[i]
        range_width = random.randint(40, 50)
        range_height = random.randint(40, 50)
        range_img = g_img[y:y+range_height, x:x+range_width]
        direct = random.randint(0, 2)
        range_img = cv2.flip(range_img, direct)
        g_img = replace_range(g_img, range_img, (y, x))
    return g_img
