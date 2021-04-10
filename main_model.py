import tensorflow as tf

import matplotlib.pyplot as plt 

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

import collections
import random
import re
import numpy as np
import os
import time
import json
from glob import glob
from PIL import Image
import pickle

import h5py
import cv2

def imgpath_load(file_name):
    with open(file_name) as file:
        result = [[x for x in line.split(' ')] for line in file.read().split('\n')]
    # last element of list 'result' = '' so popping 'em out
    result.pop()
    # split list into 2 sperate list 
    image_path = [items[0] for items in result]
    # list -> idx "I could use enumerate instead but don't want any mismatching!"
    idx = [int(item[-1]) for item in result]
    # map list into dict
    mapping = dict(zip(image_path, idx))
    return mapping, image_path

filename = 'train.matching.txt' 
mapping, image_path = imgpath_load(filename)

img_dir = 'images_train/'
rand_ = np.random.randint(0, len(image_path))
img_str = img_dir + image_path[rand_]

img = cv2.imread(img_str)
plt.imshow(img)
plt.show()
