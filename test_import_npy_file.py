import os
import numpy as np
import matplotlib.pyplot as plt
import random

some_file = "training_data/training_1/2020-10-30 200910.npy"
basepath = "training_data/training_1"
files = os.scandir(basepath)
file_names = [file.name for file in files]
print(file_names[7])
file7_path = f"{basepath}/{file_names[7]}"
print(file7_path)

data = np.load(file7_path, allow_pickle=True)

# print(np.shape(data))
##print(len(data[0]))
#print(np.shape(data[0][0]))
##first_img = data[0][0]
##print(np.shape(first_img))
##print(first_img[0][0])

def plot_img(sample):
    plt.imshow(sample[0], cmap="gray")
##    plt.title(f"index {index(sample)}: , input: {sample[1]}")
    plt.title(f"input: {sample[1]}")
    plt.axis("off")
    plt.show()

plot_img(random.choice(data))
