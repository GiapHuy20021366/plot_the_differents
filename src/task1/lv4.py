'''
    This level erase or move regions in opencv img
'''
import numpy
import cv2
import queue
from utils.task1_tools import *
from utils.region import *
import numpy as np

SINGLE_COLOR_WHITE = 255


def is_range(point, max_dims):
    max_row, max_col = max_dims
    row, col = point
    return row >= 0 and row < max_row and col >= 0 and col < max_col


def growth_forest(point, max_dims, edges_img, marks, mark_val=False):
    temp_queue = queue.Queue()
    region = Region()
    max_row, max_col = max_dims

    # Add first element
    temp_queue.put(point)
    while True:

        if temp_queue.empty():
            break
        # Get an point from queue
        row, col = temp_queue.get()

        # Check valid of this point
        if row < 0 or row >= max_row or col < 0 or col >= max_col:
            continue

        # Check this point have tree or not
        if marks[row][col] == mark_val:
            continue

        marks[row][col] = mark_val

        # Add this point to region
        region.add_point((row, col))

        # Add neighbor point to queue if it doesn't have tree
        if edges_img[row][col] != SINGLE_COLOR_WHITE:
            if is_range((row, col - 1), max_dims) and marks[row, col - 1] != mark_val:
                temp_queue.put((row, col - 1))
            if is_range((row, col + 1), max_dims) and marks[row, col + 1] != mark_val:
                temp_queue.put((row, col + 1))
            if is_range((row - 1, col), max_dims) and marks[row - 1, col] != mark_val:
                temp_queue.put((row - 1, col))
            if is_range((row + 1, col), max_dims) and marks[row + 1, col] != mark_val:
                temp_queue.put((row + 1, col))
    return region


def simple_filter_condition(region):
    point_rate = region.get_point_rate()
    acreage = region.get_acreage()
    rect_width, rect_height = region.get_rect_size()
    wh_rate = rect_width / rect_height
    if wh_rate > 1:
        wh_rate = 1 / wh_rate
    valid_point_rate = point_rate > 0.3
    valid_acreage = acreage > 300 and acreage < 20000
    valid_rect_size = rect_width > 4 and rect_height > 4 and rect_width < 100 and rect_height < 100
    valid_wh_rate = wh_rate > 0.3
    return valid_acreage and valid_point_rate and valid_rect_size and valid_wh_rate


def distance_to_regions(region, regions):
    distances = [r.center_distance(region) for r in regions]
    return min(distances)


def max_distance_to_regions(regions, chose_regions):
    distances = [distance_to_regions(region, chose_regions)
                 for region in regions]
    max_index = np.argmax(distances)
    region_max = regions[max_index]
    return region_max, distances[max_index], max_index


def choose_regions(regions, num_choose, start_index=0):
    if len(regions) <= num_choose:
        return regions
    chose_regions = [regions[start_index]]
    del regions[start_index]
    for _ in range(num_choose - 1):
        region, _, index = max_distance_to_regions(
            regions, chose_regions)
        # print(distance)
        chose_regions.append(region)
        del regions[index]
    return chose_regions


def create_mask(opencv_img, region):
    mask = opencv_img.copy()
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask = mask * 0
    for point in region.get_points():
        mask[point] = SINGLE_COLOR_WHITE
    return mask


def erase_regions(opencv_img, num_range=9):
    empty_area = numpy.full(opencv_img.shape[:2], True)
    edged_img = cv2.Canny(opencv_img, 100, 200)
    edged_img = transform_candy(edged_img)
    # cv2.imshow("sfdsf", edged_img)
    rows, cols = opencv_img.shape[:2]
    # print(rows, cols)
    regions = []
    # Loop
    for row in range(rows):
        for col in range(cols):
            if not empty_area[row][col]:
                continue
            region = growth_forest(
                (row, col), (rows, cols), edged_img, empty_area)
            if not region.empty():
                regions.append(region)

    regions = [region for region in regions if simple_filter_condition(region)]
    random.shuffle(regions)
    regions = choose_regions(regions, num_range)
    show_img = opencv_img.copy()

    merge_region = Region()
    merge_region.add_regions(regions)
    mask = create_mask(opencv_img, merge_region)
    dst = cv2.inpaint(show_img, mask, 3, cv2.INPAINT_TELEA)
    return dst
