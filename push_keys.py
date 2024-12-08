import numpy as np
import pyautogui
import pydirectinput
import time
import random

def input_demo():
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)

    for i in range(3):
        pydirectinput.keyDown('w')
        time.sleep(5)
        pydirectinput.keyUp('w')
        time.sleep(2)

    print("END OF SCRIPT")


def push_wasd(key_strokes):
    # 0 == w; 1 == a; 2 == s; 3 == d
    keys = ['w', 'a', 's', 'd']
    for index, key in enumerate(keys):
        if random.random() < key_strokes[index]:
            pydirectinput.keyDown(key)
        else:
            pydirectinput.keyUp(key)


def release_wasd():
    keys = ['w', 'a', 's', 'd']
    for key in keys:
        pydirectinput.keyUp(key)
