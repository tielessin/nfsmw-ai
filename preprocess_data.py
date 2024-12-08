import tensorflow as tf
import numpy as np
import pandas as pd  
import matplotlib.pyplot as plt
import os
import random

print("\n")
print(tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None))
print("\n")
print(tf.__version__)

##basepath = "training_data/training_1"
##
##
##def plot_img(sample):
##    plt.imshow(sample[0], cmap="gray")
####    plt.title(f"index {index(sample)}: , input: {sample[1]}")
##    plt.title(f"input: {sample[1]}")
##    plt.axis("off")
##    plt.show()
##
##
##def import_all_data(basepath):
##    data = []
##    files = os.scandir(basepath)
##    file_names = [file.name for file in files]
##    file_paths = [f"{basepath}/{file_name}" for file_name in file_names]
##    
##    some_path = file_paths[20]
##    some_data = np.load(some_path, allow_pickle=True)
##    print(np.shape(data))
##    print(np.shape(some_data))
##
##
##    for file_path in file_paths:
##        file_data = np.load(file_path, allow_pickle=True)
##        if data == []:
##            data = file_data
##            print(f"Filedata after init: {np.shape(file_data)}")
##        else:
##            data = np.append(data, file_data)
##
##    #data = np.append(data, some_data)
##    print(np.shape(data))
##    return data
##
##print("\n\n")
##
##data = import_all_data(basepath)
##print(np.shape(data))
##print(np.shape(data[0]))
##print(np.shape(data[1]))
##
###plot_img(random.choice(data))
