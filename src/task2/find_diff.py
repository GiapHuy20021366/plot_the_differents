'''
This task finds all different regions between two picture
'''

import numpy
import queue
from utils.region import *
from utils.Direct import *

COLOR_BLACK = (0, 0, 0)


def is_range(point, max_dims):
    max_row, max_col = max_dims
    row, col = point
    return row >= 0 and row < max_row and col >= 0 and col < max_col


def get_kernel_by_direct(region, kernel_size, kernel_direct):
    top_left, top_right, bottom_left, bottom_right = region.get_rect_extremes()
    match kernel_direct:
        case Direct.UP_LEFT:
            x, y = bottom_right
            return [x - kernel_size, y - kernel_size, kernel_size, kernel_size]
        case Direct.UP_RIGHT:
            x, y = bottom_left
            return [x - kernel_size, y, kernel_size, kernel_size]
        case Direct.DOWN_LEFT:
            x, y = top_right
            return [x, y - kernel_size, kernel_size, kernel_size]
        case Direct.DOWN_RIGHT:
            x, y = top_left
            return [x, y, kernel_size, kernel_size]

# This filter will merge all region by kernels


def merge_regions_by_kernel(regions, kernel_size=50, kernel_direct=Direct.DOWN_RIGHT):
    if len(regions) <= 1:
        return regions
    merges = numpy.full(len(regions), False)
    regions_queue = queue.Queue()
    [regions_queue.put((i, r)) for i, r in enumerate(regions)]
    new_regions = []
    while True:
        if regions_queue.empty():
            break
        idx, region = regions_queue.get()
        if merges[idx]:
            continue
        merges[idx] = True

        kernel_rect = get_kernel_by_direct(region, kernel_size, kernel_direct)
        regions_in_kernel = [(i, r)
                             for i, r in enumerate(regions) if r.is_inside_rect(kernel_rect) and not merges[i]]
        merge_region = Region()
        merge_region.add_region(region)
        merge_region.add_regions([r for _, r in regions_in_kernel])
        for i, _ in regions_in_kernel:
            merges[i] = True
        new_regions.append(merge_region)

    return new_regions


def growth_forest(point, max_dims, sub_img, marks, mark_val=False):
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

        if (sub_img[row][col] == COLOR_BLACK).all():
            continue

        # Check this point have tree or not
        if marks[row][col] == mark_val:
            continue

        marks[row][col] = mark_val

        # Add this point to region
        region.add_point((row, col))

        # Add neighbor point to queue if it doesn't have tree
        if not (sub_img[row][col] == COLOR_BLACK).all():
            if is_range((row, col - 1), max_dims) and marks[row, col - 1] != mark_val:
                temp_queue.put((row, col - 1))
            if is_range((row, col + 1), max_dims) and marks[row, col + 1] != mark_val:
                temp_queue.put((row, col + 1))
            if is_range((row - 1, col), max_dims) and marks[row - 1, col] != mark_val:
                temp_queue.put((row - 1, col))
            if is_range((row + 1, col), max_dims) and marks[row + 1, col] != mark_val:
                temp_queue.put((row + 1, col))
    return region


def detect_differences(img1, img2):
    sub_img = img1 - img2
    rows, cols = sub_img.shape[:2]
    max_dims = (rows, cols)
    empty_area = numpy.full(max_dims, True)

    regions = []
    for row in range(rows):
        for col in range(cols):
            if not empty_area[row][col]:
                continue
            region = growth_forest(
                (row, col), (rows, cols), sub_img, empty_area)
            if not region.empty():
                regions.append(region)
    print(len(regions))

    # Filter regions
    regions = merge_regions_by_kernel(regions, kernel_direct=Direct.DOWN_LEFT)
    regions = merge_regions_by_kernel(regions, kernel_direct=Direct.DOWN_RIGHT)
    regions = merge_regions_by_kernel(regions, kernel_direct=Direct.UP_LEFT)
    regions = merge_regions_by_kernel(regions, kernel_direct=Direct.UP_RIGHT)
    # Normalize regions
    for region in regions:
        region.normalize()

    return sub_img, regions
