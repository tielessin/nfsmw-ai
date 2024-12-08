import cv2
import numpy as np
import pyautogui
import time

# whole window
##padding_width = 100
##padding_height = 100
##width = 640
##height = 480

# recorded_region = (padding_width, paddding_height, width, height)
rec_region = (170, 280, 460, 200)


def take_screenshot(show_screenshot=False, recorded_region=rec_region):
    img = pyautogui.screenshot(region=rec_region)
    # convert these pixels to a proper numpy array to work with OpenCV
    screen = np.array(img)
    # convert colors from BGR to RGB
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    # Resize
    screen =  cv2.resize(screen, (240, 100))
    
    if show_screenshot:
        # write the frame
        #out.write(screen)
        # show the frame

        cv2.imshow("screenshot", screen)
        # if the user clicks q, it exits
        #if cv2.waitKey(1) == ord("q"):
            #break

    return screen
    


