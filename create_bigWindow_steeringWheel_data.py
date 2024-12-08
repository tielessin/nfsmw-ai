import numpy as np
import d3dshot
import pygame

import datetime
import time
import os

import tensorflow as tf
from tensorflow.train import Example, Features, Feature
from tensorflow.train import BytesList, FloatList


def create_example(X_inst, y_inst):
  X_target_shape = (480, 640, 3)
  X_tens = tf.convert_to_tensor(X_inst)
  y_tens = tf.convert_to_tensor(y_inst, dtype=tf.float32)
  if X_tens.shape != X_target_shape:
    X_tens = tf.image.resize(X_tens, X_target_shape[:2])
    X_tens = tf.cast(X_tens, tf.uint8)

  features = {
            "image_raw": Feature(bytes_list=BytesList(value=[tf.io.serialize_tensor(X_tens).numpy()])),
            "label": Feature(bytes_list=BytesList(value=[tf.io.serialize_tensor(y_tens).numpy()])),
            }
  return Example(features=Features(feature=features))


def countdown(start_num):
    for i in list(range(start_num))[::-1]:
        print(i+1)
        time.sleep(1)

def main():

    pygame.display.init()
    pygame.joystick.init()
    pygame.joystick.Joystick(0).init()
    controller = pygame.joystick.Joystick(0)

    d = d3dshot.create(capture_output="numpy")

    saved_files_counter = 0
    instances_per_file = 5000
##    recorded_region = (100, 100, 740, 580) # small window mode
##    recorded_region = (320, 0, 2240, 1440) # fullscreen mode (doesn't work)
    recorded_region = (100, 100, 1700, 1300) # big window mode

    end_session = False


    countdown(5)
    print('recording...')

    
    while(True):

        filename = f"training_data\\train_1stP_High99_chaseH5_fastBMW_SteeringWheel_{time.strftime('%Y_%m_%d-%H_%M_%S')}.tfrecord"
        
        with tf.io.TFRecordWriter(filename) as writer:
          for _ in range(instances_per_file):
            # Get steering-wheel inputs and turn into wasd
            pygame.event.pump()
            steer = controller.get_axis(0)
            acc = controller.get_axis(1) / (-2) + 0.5
            stop = controller.get_axis(2) / (-2) + 0.5
            nitro = float(controller.get_button(9))
            wasdn = [acc, max(0.0, -steer), stop, max(0.0, steer), nitro]
            print([round(value, 3) for value in wasdn])
            
            screen = d.screenshot(region=recorded_region)
            
            tf_example = create_example(screen, wasdn)
            writer.write(tf_example.SerializeToString())

##            # PAUSE recoring session
##            # with bottom right wheel button
##            if controller.get_button(8):
##              print('Pausing!')
##              time.sleep(1)
##              while True:
##                time.sleep(0.1)
##                pygame.event.pump()
##                # unpause
##                if controller.get_button(8):
##                  print('unpaused!')
##                  time.sleep(1)
##                  break
##                # End File or Session
##                if controller.get_button(11) or controller.get_button(3):
##                  break

            # Start new file
            # with top right wheel button
            if controller.get_button(11):
                print('manually started a new file.')
                print('starting in:')
                countdown(3)
                print('recording...')
                break

            # STOP recording session
            # With "o" button
            if controller.get_button(3):
                print("manually stopped recording session.")
                end_session = True
                break

          else:
            print(f"{instances_per_file} instances have been saved!")

        if end_session:
          break



    print("END OF SCRIPT")


if __name__ == "__main__":
  main()
