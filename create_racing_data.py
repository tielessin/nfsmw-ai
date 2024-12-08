import numpy as np
import d3dshot
import cv2
import time
import datetime
from get_keys import key_check_with_nitro
import os
import keyboard
import pydirectinput

import tensorflow as tf
from tensorflow.train import Example, Features, Feature
from tensorflow.train import BytesList, FloatList



def create_example(X_inst, y_inst):
  X_tens = tf.convert_to_tensor(X_inst)
  y_tens = tf.convert_to_tensor(y_inst, dtype=tf.float32)
  img_shape = X_tens.shape

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

    training_data = []
    saved_files_counter = 0
    instances_per_file = 5000
    recorded_region = (100, 100, 740, 580)

    d = d3dshot.create(capture_output="numpy")
    
    countdown(5)
    print('recording...')

    paused = False
    while(True):

        filename = f"training_data/nfsmw_chase_{time.strftime('%Y_%m_%d-%H_%M_%S')}.tfrecord"

        with tf.io.TFRecordWriter(filename) as writer:
          for _ in range(instances_per_file):
            screen = d.screenshot(region=recorded_region)
            keys = key_check_with_nitro()
            print(keys)
            tf_example = create_example(screen, keys)
            writer.write(tf_example.SerializeToString())
            if keyboard.is_pressed('u'):
              break
        if keyboard.is_pressed('u'):
              print("Recoring stopped")
              break
        print(f"{instances_per_file} instances have been saved!")

    print("END OF SCRIPT")

main()
