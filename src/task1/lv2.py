'''
    This level detect edges by Candy algorithm and change color edges in a rect 
'''

import random
import cv2
from utils.task1_tools import *
import numpy


def count_color(img_2d, color_val):
    row, col = img_2d.shape
    count = 0
    for x in range(row):
        for y in range(col):
            if img_2d[x][y] == color_val:
                count += 1
    return count / row / col


def replace_color(edges, origin_img, start_pos):
    height,  width = edges.shape
    start_x, start_y = start_pos
    rect = origin_img[start_y:start_y+height, start_x:start_x+width]
    color = rand_color()
    # print(type(rect[0][0]))
    white = 255
    # print(start_x, start_y, range_x, range_y)
    for x in range(edges.shape[0]):
        for y in range(edges.shape[1]):
            if edges[x][y] == white:
                rect[x][y] = color
            else:
                rect[x][y] = origin_img[x + start_y][y+start_x]
    return rect

# This level contain edge detection algorithm


def change_edges_color(opencv_img, num_range):
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
        edges = cv2.Canny(range_img, 100, 200)
        score = count_color(edges, 255)
        # print(score)
        if (score < 0.04):
            continue

        edges = replace_color(edges, g_img, (x, y))
        g_img = replace_range(g_img, edges, (y, x))
        # diff_rects.append((x, y, range_width, range_height))
    return g_img
