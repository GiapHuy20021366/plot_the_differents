import pygame
import numpy as np
from utils.region import Region


def get_click_pos_origin(pos_click, img_width, padding):
    x_pos = pos_click[0]
    y_pos = pos_click[1]
    is_click_padding = False
    if x_pos >= img_width and x_pos < img_width + padding:
        is_click_padding = True

    if x_pos >= img_width + padding:
        x_pos -= img_width + padding

    return (x_pos, y_pos), is_click_padding


def get_trans_pos(pos_origin, img_width, padding):
    x, y = pos_origin
    # print(x, y, pos_origin, img_width, padding)
    return x + img_width + padding, y


def is_clicked(range, pos_click):
    x, y, w, h = range
    is_in_range_x = pos_click[0] >= x and pos_click[0] <= x + w
    is_in_range_y = pos_click[1] >= y and pos_click[1] <= y + h

    return is_in_range_x and is_in_range_y


def get_clicked_range(ranges, pos_clicked):
    for range in ranges:
        if is_clicked(range, pos_clicked):
            return range
    return None


def get_clicked_regions(regions, pos_clicked, strict_mode=True):
    for region in regions:
        if strict_mode and region.is_inside(pos_clicked[::-1]):
            return region
        if not strict_mode and Region.point_in_rect(pos_clicked[::-1], region.get_rect()):
            return region
    return None


def get_transform_range(range, width, padding):
    x, y, w, h = range
    return x + width + padding, y, w, h


def covert_opencv_img_to_pygame(opencv_img):
    # Since OpenCV is BGR and pygame is RGB, it is necessary to convert it.
    opencv_img = opencv_img[:, :, ::-1]
    # OpenCV(height,width,Number of colors), Pygame(width, height)So this is also converted.
    shape = opencv_img.shape[1::-1]
    pygame_image = pygame.image.frombuffer(
        opencv_img.tostring(), shape, 'RGB')

    return pygame_image


def is_choosed_range(choosed_ranges, pos_click):
    return get_clicked_range(choosed_ranges, pos_click) is not None


def convert_candy(candy_img):
    rows, cols = candy_img.shape
    img = np.zeros((rows, cols, 3), dtype=np.uint8)
    img = 0*img
    for row in range(rows):
        for col in range(cols):
            if candy_img[row][col] == 255:
                img[row][col] = (255, 255, 255)
    return img
