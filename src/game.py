import pygame
from setup.constants import *
from utils.game_tools import *
from task1.lv1 import *
from task1.lv2 import *
from task1.lv3 import *
from task1.lv4 import *
from components.Button import *
from task2.find_diff import *
import cv2
from utils.task1_tools import *
from task1 import Levels

# setup levels
level_setups = {
    Levels.CHANGE_RECT_COLOR: {
        "diff_style": "rect",
        "strict_mode": False,
        "generator": change_rect_color
    },
    Levels.FLIP_RECT: {
        "diff_style": "rect",
        "strict_mode": False,
        "generator": flip_rect
    },
    Levels.CHANGE_EDGES_COLOR: {
        "diff_style": "rect",
        "strict_mode": False,
        "generator": change_edges_color
    },
    Levels.CHANGE_COLOR_REGIONS: {
        "diff_style": "edges",
        "strict_mode": True,
        "generator": change_color_regions
    },
    Levels.ERASE_REGIONS: {
        "diff_style": "edges",
        "strict_mode": True,
        "generator": erase_regions
    }
}

# Choose game level
GAME_LEVEL = Levels.CHANGE_COLOR_REGIONS

# Generator
image_generator = level_setups[GAME_LEVEL]["generator"]

# Image path
IMG1 = "src/images/1.png"

# Load image
img1 = cv2.imread(IMG1)
img1 = cv2.resize(img1, get_new_size(600, 400, img1.shape[1], img1.shape[0]))

# Generate second image
img2 = image_generator(img1, 9)


candy_img = cv2.Canny(img1, 100, 200)

trans_candy_img = transform_candy(candy_img)
# candy_img = transform_candy(candy_img)

# Detect all different regions
subtract_img, diff_regions = detect_differences(img1, img2)


# size = img1.shape[:2]
IMAGE_WIDTH = img1.shape[1]
IMAGE_HEIGHT = img1.shape[0]
SCREEN_WIDTH = IMAGE_WIDTH * 2 + PADDING
SCREEN_HEIGHT = IMAGE_HEIGHT


pygame.init()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


img1_screen = covert_opencv_img_to_pygame(img1)
img2_screen = covert_opencv_img_to_pygame(img2)
img_sub_screen = covert_opencv_img_to_pygame(subtract_img)

img_candy_screen = convert_candy(candy_img)
img_candy_screen = covert_opencv_img_to_pygame(img_candy_screen)
img_modify_candy_screen = covert_opencv_img_to_pygame(
    convert_candy(trans_candy_img))


def draw_true(range1, range2):
    pygame.draw.rect(screen, COLOR_RED,
                     pygame.Rect(range1),  2)
    pygame.draw.rect(screen, COLOR_RED,
                     pygame.Rect(range2),  2)
    pygame.display.flip()


def draw_pixels(pixels, color=COLOR_RED):
    square = pygame.Surface((1, 1))
    square.fill(color)
    for pixel in pixels:
        x, y = pixel
        screen.blit(square, pygame.Rect(x, y, 1, 1))
    pygame.display.flip()


def draw_subtract_images():
    screen.blit(img_candy_screen, (0, 0))
    screen.blit(img_modify_candy_screen, (IMAGE_WIDTH + PADDING, 0))
    pygame.display.flip()


def draw_images():
    screen.blit(img1_screen, (0, 0))
    screen.blit(img2_screen, (IMAGE_WIDTH + PADDING, 0))
    pygame.display.flip()


def draw_fail(pos1, pos2):
    # Draw fail circle
    pygame.draw.circle(screen, COLOR_RED, pos1, 25, 2)
    pygame.draw.circle(screen, COLOR_RED, pos2, 25, 2)
    pygame.display.flip()


def draw_fail_ranges(fail_ranges):
    for pos, _ in fail_ranges:
        trans_pos = get_trans_pos(
            pos, IMAGE_WIDTH, PADDING)
        draw_fail(pos, trans_pos)


def draw_true_ranges(true_ranges):
    style = level_setups[GAME_LEVEL]["diff_style"]
    for region in true_ranges:
        if style == "rect":
            opencv_rect = region.get_rect()
            y, x, height, width = opencv_rect
            pygame_rect = (x, y, width, height)
            trans_rect = get_transform_range(
                pygame_rect, IMAGE_WIDTH, PADDING)
            draw_true(pygame_rect, trans_rect)
        if style == "edges":
            points = region.get_edges()
            origin_pixels = [point[::-1] for point in points]
            trans_pixels = [get_trans_pos(
                point[::-1], IMAGE_WIDTH, PADDING) for point in points]
            draw_pixels(origin_pixels)
            draw_pixels(trans_pixels)


def print_all_differences():
    draw_true_ranges(diff_regions)


#
true_ranges = []
fail_ranges = []


draw_images()
# print_all_differences()


# Timer for redraw scene
timer = pygame.time.set_timer(pygame.USEREVENT, 1000)
clock = pygame.time.Clock()

# Game status
status = {
    "Total Different": len(diff_regions),
    "Total Fail": 0,
    "Total True": 0,
    "IsChanged": False,
    "IsPrintDifferent": False,
    "Logs": False,
    "IsPrintSubtract": False
}

font = pygame.font.SysFont("Arial", 20)
btn_show = Button("Show", (IMAGE_WIDTH, 0), 20, feedback="Hide")
btn_clear = Button("Clear", (IMAGE_WIDTH, 50), 20, feedback="Clear")
btn_subtract = Button("Subtract", (IMAGE_WIDTH, 100), 20, feedback="Subtract")


def draw_text(text, pos):
    text = font.render(text, 1, COLOR_WHITE)
    text_rect = text.get_rect()
    text_rect.topleft = pos
    screen.blit(text, text_rect)
    pygame.display.flip()


def draw_mid():
    pygame.draw.rect(screen, COLOR_BLACK,
                     pygame.Rect(IMAGE_WIDTH, 0, PADDING, IMAGE_HEIGHT))
    btn_show.show(screen)
    btn_clear.show(screen)
    btn_subtract.show(screen)

    draw_text("Total: {}".format(
        status["Total Different"]), (IMAGE_WIDTH, 150))
    draw_text("True:  {}".format(
        status["Total True"]), (IMAGE_WIDTH, 200))
    draw_text("Fail:  {}".format(
        status["Total Fail"]), (IMAGE_WIDTH, 250))
    pygame.display.flip()


def btn_show_callback():
    status["IsPrintDifferent"] = not status["IsPrintDifferent"]
    status["IsChanged"] = True


def btn_clear_callback():
    status["Total True"] = 0
    status["Total Fail"] = 0
    true_ranges.clear()
    status["IsChanged"] = True


def btn_subtract_callback():
    status["IsPrintSubtract"] = not status["IsPrintSubtract"]
    status["IsChanged"] = True


draw_mid()

# Game loop
running = True
while running:
    if status["IsChanged"]:
        draw_images()
        if status["IsPrintSubtract"]:
            draw_subtract_images()
        draw_fail_ranges(fail_ranges)
        draw_true_ranges(true_ranges)
        status["IsChanged"] = False
        if status["IsPrintDifferent"]:
            print_all_differences()
        if status["Logs"]:
            print(status)
        draw_mid()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Btn event loader
        btn_show.click(event, btn_show_callback)
        btn_clear.click(event, btn_clear_callback)
        btn_subtract.click(event, btn_subtract_callback)

        # User event to draw fail click range
        if event.type == pygame.USEREVENT:
            new_fail_ranges = [
                pos for pos, tick_time in fail_ranges if pygame.time.get_ticks() - tick_time >= 1000]
            if (len(new_fail_ranges) != len(fail_ranges)):
                fail_ranges = new_fail_ranges
                status["IsChanged"] = True

        # Event handle click event
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            origin_pos, is_click_padding = get_click_pos_origin(
                pos, IMAGE_WIDTH, PADDING)
            # Click padding
            if is_click_padding:
                continue

            trans_pos = get_trans_pos(origin_pos, IMAGE_WIDTH, PADDING)
            region_clicked = get_clicked_regions(
                diff_regions, origin_pos, strict_mode=False)
            if region_clicked is not None:
                # ssim_score, _ = calc_ssim(
                #     img1, img2, range_clicked)
                # print(ssim_score)
                if region_clicked not in true_ranges:
                    true_ranges.append(region_clicked)
                    status["Total True"] += 1
                    status["IsChanged"] = True
            else:
                fail_ranges.append(
                    (origin_pos, pygame.time.get_ticks()))
                status["Total Fail"] += 1
                status["IsChanged"] = True

    clock.tick(60)

# Quit Pygame
pygame.quit()
