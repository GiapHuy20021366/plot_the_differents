import pygame
from setup.constrants import *
from untils.diff_rects import *
from untils.translate import *
from generate.lv1 import *
from generate.lv2 import *
import cv2

# Images
IMG1 = "src/images/camels1.jpg"
IMG2 = "src/images/city2.jpg"

# Load images
img1 = cv2.imread(IMG1)
img1 = cv2.resize(img1, get_new_size(600, 400, img1.shape[1], img1.shape[0]))
# img2 = cv2.imread(IMG2)
img2 = lv2_generate(img1, 9)

# Init detecter
detecter = SubtractDetecter(img1, img2)
differents = detecter.differents
SSIMs = detecter.get_SSIM()
print(SSIMs)

size = detecter.get_size()
IMAGE_WIDTH = size[0]
IMAGE_HEIGHT = size[1]
SCREEN_WIDTH = IMAGE_WIDTH * 2 + PADDING
SCREEN_HEIGHT = IMAGE_HEIGHT


pygame.init()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


img1_screen = covert_opencv_img_to_pygame(detecter.img1)
img2_screen = covert_opencv_img_to_pygame(detecter.img2)


def print_all_differents():
    for dif in differents:
        pygame.draw.rect(screen, COLOR_RED,
                         pygame.Rect(dif),  2)
    pygame.display.flip()


def draw_images():
    screen.blit(img1_screen, (0, 0))
    screen.blit(img2_screen, (IMAGE_WIDTH + PADDING, 0))
    pygame.display.flip()


def draw_true(range1, range2):
    pygame.draw.rect(screen, COLOR_RED,
                     pygame.Rect(range1),  2)
    pygame.draw.rect(screen, COLOR_RED,
                     pygame.Rect(range2),  2)
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
    for range in true_ranges:
        trans_range = get_transform_range(
            range, IMAGE_WIDTH, PADDING)
        draw_true(range, trans_range)


#
true_ranges = []
fail_ranges = []


draw_images()
# print_all_differents()


# Timer for redraw scene
timer = pygame.time.set_timer(pygame.USEREVENT, 1000)
clock = pygame.time.Clock()

# Game status
status = {
    "Total Different": len(differents),
    "Total Fail": 0,
    "Total True": 0,
    "IsChanged": False,
    "IsPrintDifferent": False,
    "Logs": True
}


# Game loop
running = True
while running:
    if status["IsChanged"]:
        draw_images()
        draw_fail_ranges(fail_ranges)
        draw_true_ranges(true_ranges)
        status["IsChanged"] = False
        if status["IsPrintDifferent"]:
            print_all_differents()
        if status["Logs"]:
            print(status)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
            origin_pos, _ = get_click_pos_origin(pos, IMAGE_WIDTH, PADDING)
            trans_pos = get_trans_pos(origin_pos, IMAGE_WIDTH, PADDING)
            range_clicked = get_clicked_range(differents, origin_pos)
            if range_clicked is not None:
                if not is_choosed_range(true_ranges, origin_pos):
                    true_ranges.append(range_clicked)
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
