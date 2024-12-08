import cv2
import numpy as np
import d3dshot
import time

# recorded_region = (padding_width, paddding_height, width, height)
##rec_region = (170, 280, 460, 200)
rec_region = (170, 280, 630, 480)
out_size = (240, 100)
d3d = d3dshot.create(capture_output="numpy")

def take_screenshot(show_screenshot=False, recorded_region=rec_region):
    screen = d3d.screenshot(region=recorded_region)
    # convert colors from BGR to RGB
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
    # resize
    screen =  cv2.resize(screen, out_size)

    if show_screenshot:
        cv2.imshow("screenshot", screen)

    return screen
    


