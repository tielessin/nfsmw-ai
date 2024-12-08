from tensorflow import keras
import numpy as np
import keyboard
import cv2
import time
import os

from capture_screen_pyautogui import take_screenshot
from push_keys import push_wasd, release_wasd
from vjoy import vj
from vjoy import nfsmw_model1_continuous_input

print("\n\n##################################\n\n")

models_dir = "models 1"
model_file_name = "Full_Big_unbalanced_6to1_model_linear 11-11-2020 00-35-04"
model_path = os.path.join(models_dir, model_file_name)
print(f'loading model "{model_file_name}"')
model = keras.models.load_model(model_path)

def countdown(duration):
    for i in range(duration, 0, -1):
        print(i)
        time.sleep(1)
    print("GO!")

print(f'Loading model "{model_file_name}"')
countdown(3)

fps = 0
start_time = time.time()
paused = False

while True:
    if not paused:
        screen = take_screenshot(True)
        screen = [np.expand_dims(screen, -1)]
        screen = np.array(screen)
        screen = screen
        predicted_keys = model.predict(screen)
        predicted_keys = [round(key, 3) for key in predicted_keys[0]]
        nfsmw_model1_continuous_input(predicted_keys)
        print(predicted_keys)

    # Quit with "u"
    if cv2.waitKey(25) & 0xFF == ord('u'):
        cv2.destroyAllWindows()
        nfsmw_model1_continuous_input([-1000, -1000, -1000, -1000])
        #release_wasd()
        break

    # Pause with "p"
    if keyboard.is_pressed('p'):
        if paused:
            paused = False
            print('unpaused!')
            time.sleep(1)
        else:
            print('Pausing!')
            paused = True
            nfsmw_model1_continuous_input([-1000, -1000, -1000, -1000])
            #release_wasd()
            time.sleep(1)

    # Print FPS
    if start_time + 1 > time.time():
        fps += 1
    else:
        print(f"FPS: {fps}")
        start_time = time.time()
        fps = 0
    

print("Model prediction script has been stopped...")
print("END OF SCRIPT\n")
