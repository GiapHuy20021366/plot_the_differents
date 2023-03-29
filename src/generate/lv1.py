import random
from setup.constrants import *
from generate.untils import *


def lv1_generate(opencv_img, num_range):
    shape = opencv_img.shape
    width, height = shape[1], shape[0]
    points = generate_rally(100, width - 50, height - 50, num_range)
    g_img = opencv_img.copy()
    diff_rects = []
    for i in range(num_range):
        x, y = points[i]
        range_width = random.randint(20, 50)
        range_height = random.randint(20, 50)
        diff_rects.append((x, y, range_width, range_height))
        g_img[y:y+range_height, x:x+range_width] = rand_color()
    return g_img, diff_rects


if __name__ == "__main__":
    print(generate_rally(100, 600, 399, 8))
