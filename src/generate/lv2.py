from generate.untils import *
from setup.constrants import *
import cv2


def filter(img1, img2):
    score, _ = calc_ssim(img1, img2, (0, 0, img1.shape[1], img1.shape[0]))
    print(score)
    return score >= MIN_SSIM and score <= MAX_SSIM


# Flip range to make it difficult to detect different
def lv2_generate(opencv_img, num_range):
    shape = opencv_img.shape
    width, height = shape[1], shape[0]
    points = generate_rally(100, width - 50, height - 50, num_range)
    g_img = opencv_img.copy()
    diff_rects = []
    for i in range(num_range):
        x, y = points[i]
        range_width = random.randint(40, 50)
        range_height = random.randint(40, 50)
        range_img = g_img[y:y+range_height, x:x+range_width]
        direct = random.randint(0, 2)
        flip_range = cv2.flip(range_img, direct)
        if filter(range_img, flip_range):
            diff_rects.append((x, y, range_width, range_height))
            g_img = replace_range(g_img, flip_range, (y, x))
    return g_img, diff_rects
