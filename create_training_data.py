import numpy as np
from capture_screen_pyautogui import take_screenshot
import d3dshot
import cv2
import time
import datetime
from get_keys import key_check
import os
import keyboard
import pydirectinput


def save_file(train_data):
    t = str(datetime.datetime.now())
    t = t.split('.')[0]
    t = t.replace(':', '')
    file_name = f"training_data\{t}.npy"
    np.save(file_name, train_data)

def countdown(start_num):
    for i in list(range(start_num))[::-1]:
        print(i+1)
        time.sleep(1)

def main():

    training_data = []
    saved_files_counter = 0
    instances_per_file = 1000
    
    countdown(5)
    print('recording...')

    paused = False
    while(True):

        if not paused:
            screen = take_screenshot(show_screenshot=True)
            last_time = time.time()
            keys = key_check()
            print(keys)
            training_data.append([screen, keys])
            
            if len(training_data) % instances_per_file == 0:
                saved_files_counter += 1
                print(f"saving {len(training_data)} instances to a file...")
                save_file(np.array(training_data))
                print(f"{saved_files_counter * instances_per_file} instances have been saved in total...")
                training_data = [] 

        # Pause recoring with "p"
        if keyboard.is_pressed('p'):
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                pydirectinput.keyDown("b")
                print('Pausing!')
                paused = True
                time.sleep(1)
                pydirectinput.keyUp("b")

        # Short pause and delete crash with "l"
        if keyboard.is_pressed('l'):
            training_data = training_data[:-100]
            pydirectinput.keyDown("r")
            pydirectinput.keyDown("x")
            print('deleted last 100 instances')
            print('returning to recording in:')
            countdown(8)
            pydirectinput.keyUp("r")
            pydirectinput.keyUp("x")
            print('recording...')

        # Stop training with "u"
        if keyboard.is_pressed('u'):
            print("Recoring stopped")
            break

    print("END OF SCRIPT")

main()
