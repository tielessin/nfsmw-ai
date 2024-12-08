from tensorflow import keras
import numpy as np
import d3dshot
import keyboard
import cv2
import time
import os

from vjoy import vj
from vjoy import nfsmw_speed_direction_input

print("\n\n##################################\n\n")

models_dir = "models 2"
model_file_name = "11thModel2_unfreezed_steeringWheel_pretrainedSixth_2021_01_23-02_16_53"
model_path = os.path.join(models_dir, model_file_name)
print(f'loading model "{model_file_name}"')
model = keras.models.load_model(model_path)
##recorded_region = (100, 100, 740, 580) # small window mode
##recorded_region = (320, 0, 2240, 1440) # fullscreen mode (doesn't work)
recorded_region = (100, 100, 1700, 1300) # big window mode
inp_size = (448, 224)
up_height = 450
left_width = 240
down_height = 1010
right_width = 1360

print(f'Starting {model_file_name} in...')

# Countdown
for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

fps = 0
start_time = time.time()
paused = False

d = d3dshot.create(capture_output="numpy")

while True:
    if not paused:
        screen = d.screenshot(region=recorded_region)
        screen = screen[up_height:down_height, left_width:right_width]
        screen = cv2.resize(screen, inp_size)
        screen = np.array([screen]) # for tenth model
        screen = (screen / 127.5) - 1
##        t_before_prediction = time.time()
        predicted_keys = model.predict(screen)
##        t_after_prediction = time.time()
##        t_delta = t_after_prediction - t_before_prediction
##        print(f"Time for prediction: {round(t_delta, 3)}")
        predicted_keys = [round(key, 3) for key in predicted_keys[0]]
        nfsmw_speed_direction_input(predicted_keys, full_speed=True)
        print(predicted_keys)

    # Quit with "u"
    if keyboard.is_pressed('u'):
        nfsmw_speed_direction_input([0, 0])
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
            nfsmw_speed_direction_input([0, 0])
            time.sleep(1)

    # Print FPS
    if not paused:
        if start_time + 1 > time.time():
            fps += 1
        else:
            print(f"FPS: {fps}")
            start_time = time.time()
            fps = 0
    

print("Model prediction script has been stopped...")
print("END OF SCRIPT\n")
