import random
import numpy as np
from setup.constrants import *
from untils.diff_rects import *


def rand_poses(max_x, max_y, count):
    rands = []
    for i in range(count):
        x = random.randint(1, max_x)
        y = random.randint(1, max_y)
        rands.append((x, y))
    return rands


def replace_range(origin_img, range_r, start_pos):
    start_x, start_y = start_pos
    range_x = range_r.shape[0]
    range_y = range_r.shape[1]
    # print(start_x, start_y, range_x, range_y)
    for x in range(start_x, start_x + range_x):
        for y in range(start_y, start_y + range_y):
            origin_img[x][y] = range_r[x - start_x][y - start_y]
    return origin_img


def square_distance(point1, point2):
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2


def rally_distance(point, rally, dis_calc=square_distance):
    distances = [dis_calc(point, ral) for ral in rally]
    return min(distances)


def rally_max_distance(cur_rally, choose_rally):
    distances = [rally_distance(point, cur_rally) for point in choose_rally]
    max_index = np.argmax(distances)
    point_max = choose_rally[max_index]
    return point_max, distances[max_index], max_index

# Remove all range that much similar or different from origin


def generate_rally(max_random, max_x, max_y, num_choose, start_index=0):
    choose_rally = rand_poses(max_x, max_y, max_random)
    cur_rally = [choose_rally[start_index]]
    del choose_rally[start_index]
    for i in range(num_choose):
        point, distance, index = rally_max_distance(cur_rally, choose_rally)
        # print(distance)
        cur_rally.append(point)
        del choose_rally[index]
    return cur_rally


def rand_color():
    x1 = random.randint(0, 256)
    x2 = random.randint(0, 256)
    x3 = random.randint(0, 256)
    return x1, x2, x3
