import tensorflow as tf
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
model_file_name = "12thModel3_unfreezed_UNcensoredMap_povMapSpd__2021_01_24-21_04_11"
model_path = os.path.join(models_dir, model_file_name)
print(f'loading model "{model_file_name}"')
model = keras.models.load_model(model_path)
##recorded_region = (100, 100, 740, 580) # small window mode
##recorded_region = (320, 0, 2240, 1440) # fullscreen mode (doesn't work)
recorded_region = (100, 100, 1700, 1300) # big window mode
pov_region = (96, 196, 544, 420)
map_region = (26, 307, 172, 453)
resized_screen = (640, 480)
resized_nav = (112, 112)


def detect_speed(img, detection_threshold=10, debugging=False):  
#     # For keyboard data
#     relative_pixel_positions = [((0, 2),(0, 7)),
#                             ((2, 0),(5, 0)),
#                             ((2, 10),(5, 10)),
#                             ((7, 2),(8, 6)),
#                             ((10, 0),(14, 0)),
#                             ((10, 10),(14, 10)),
#                             ((16, 2),(16, 7)),
#                            ]
    # For Steering-Wheel data
    relative_pixel_positions = [((-1, 2),(-1, 7)),
                            ((2, 0),(5, 0)),
                            ((2, 9),(5, 9)),
                            ((7, 2),(7, 7)),
                            ((10, 0),(13, 0)),
                            ((10, 9),(13, 9)),
                            ((16, 2),(16, 7)),
                           ]

    pos_ref_1 = (2, 7)
    pos_ref_2 = (14, 2)
    
    offset_num1 = (399, 520)
    offset_num2 = (399, 537)
    offset_num3 = (399, 554)

    offsets = [offset_num1, offset_num2, offset_num3]
    
    nothing = [0, 0, 0, 0, 0, 0, 0]
    zero = [1, 1, 1, 0, 1, 1, 1]
    one = [0, 0, 1, 0, 0, 1, 0] 
    two = [1, 0, 1, 1, 1, 0, 1]
    three = [1, 0, 1, 1, 0, 1, 1]
    four = [0, 1, 1, 1, 0, 1, 0]
    five = [1, 1, 0, 1, 0, 1, 1]
    six = [1, 1, 0, 1, 1, 1, 1]
    seven = [1, 0, 1, 0, 0, 1, 0]
    eight = [1, 1, 1, 1, 1, 1, 1]
    nine = [1, 1, 1, 1, 0, 1, 1]
    
    pixel_mean_threshold = tf.cast(detection_threshold, tf.float32)
    
    speed = ""

    for offset in offsets:
        tacho_code = []
        # Reference Pixels
        h_ref1 = offset[0] + pos_ref_1[0]
        w_ref1 = offset[1] + pos_ref_1[1]
        h_ref2 = offset[0] + pos_ref_2[0]
        w_ref2 = offset[1] + pos_ref_2[1]
        ref1 = tf.math.reduce_mean(img[h_ref1, w_ref1])
        ref2 = tf.math.reduce_mean(img[h_ref2, w_ref2])
        reference = tf.cast(tf.math.reduce_mean([ref1, ref2]), tf.float32)
        
        for positions in relative_pixel_positions:
            values = []
            for position in positions:
                h_index = position[0]+offset[0]
                w_index = position[1]+offset[1]
                values.append(img[h_index, w_index].numpy())
            mean = tf.cast(tf.math.reduce_mean(values), tf.float32)
            if mean < pixel_mean_threshold or mean*4 < reference:
                tacho_code.append(1)
            else:
                tacho_code.append(0)

        if tacho_code == nothing or tacho_code == zero:
            speed += "0"
        elif tacho_code == one:
            speed += "1"
        elif tacho_code == two:
            speed += "2"
        elif tacho_code == three:
            speed += "3"
        elif tacho_code == four:
            speed += "4"
        elif tacho_code == five:
            speed += "5"
        elif tacho_code == six:
            speed += "6"
        elif tacho_code == seven:
            speed += "7"
        elif tacho_code == eight:
            speed += "8"
        elif tacho_code == nine:
            speed += "9"
        
        elif len(speed) >= 2:
            speed += "5"
            break
            
        elif len(speed) == 1:
            speed += "50"
            break
            
        elif len(speed) == 0:
            if debugging:
                print(f"SPEED-O-METER DETECTION ERROR")
                print(f"The first digit couldn't be detected. Setting speed to 220")
                print("Tacho_code =", tacho_code)
                raise Exception()
            speed += "220"
            break
            
        else:
            if debugging:
                print(f"SPEED-O-METER DETECTION ERROR")
                print("Tacho code is invalid.")
                print("Reference ==", reference)
                print("Tacho_code =", tacho_code)
                raise Exception()
            speed += "220"
            break

    speed = int(speed)
    
    if speed > 420:
        if debugging:
            print(f"SPEED-O-METER DETECTION ERROR")
            print(f'The detected speed of {speed} km/h seems to be a detection error. Setting speed to 220')
            raise Exception()
        speed = 220
        
    return speed


def countdown(duration, end_message="0"):
    for i in range(duration, 0, -1):
        print(i)
        time.sleep(1)
    print(end_message)


print(f'Starting {model_file_name} in...')

countdown(3)

fps = 0
start_time = time.time()
paused = False

d = d3dshot.create(capture_output="numpy")

while True:
    if not paused:
        screen = d.screenshot(region=recorded_region)
        screen = cv2.resize(screen, resized_screen)
        pov = screen[pov_region[1]:pov_region[3], pov_region[0]:pov_region[2]]
        nav = screen[map_region[1]:map_region[3], map_region[0]:map_region[2]]
        nav = cv2.resize(nav, resized_nav)
        spd = detect_speed(tf.constant(screen))
##        screen = np.array([screen]) # for tenth model

##        from PIL import Image
##        Image.fromarray(pov).save("pov.png")
##        Image.fromarray(nav).save("nav.png")
##        Image.fromarray(screen).save("screen.png")
##        pov = ((pov / 127.5) - 1)
##        nav = ((nav / 127.5) - 1)
##        spd = ((spd / 200) - 1)
        pov = ((2 * pov / tf.math.reduce_max(pov).numpy()) - 1)
        nav = ((2 * nav / tf.math.reduce_max(nav).numpy()) - 1)
        spd = ((spd / 200) - 1)

        pov = tf.constant([pov], tf.float32)
        nav = tf.constant([nav], tf.float32)
        spd = tf.constant([[spd]], tf.float32)
##        print("pov:", tf.math.reduce_mean(nav).numpy(),
##              "| nav:", tf.math.reduce_mean(nav).numpy(),
##              "| spd:", spd.numpy(),)
##
##        print(pov.shape)
##        print(nav.shape)
##        print(spd.shape)
##        print(spd)
        
####        t_before_prediction = time.time()
        predicted_keys = model.predict([pov, nav, spd])
####        t_after_prediction = time.time()
####        t_delta = t_after_prediction - t_before_prediction
####        print(f"Time for prediction: {round(t_delta, 3)}")
        predicted_keys = [round(key, 3) for key in predicted_keys[0]]
##        nfsmw_speed_direction_input(predicted_keys)
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
##            print(f"FPS: {fps}")
            start_time = time.time()
            fps = 0
    

print("Model prediction script has been stopped...")
print("END OF SCRIPT\n")
