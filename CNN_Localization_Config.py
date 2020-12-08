"""""
Config scrip for loading in and handelning training data for a Localization model that estimates the bounding boxes of cars, cats and dogs.
Uses the pretrained our own pretrained CNN network.
Author: Greppe
Reviewed by: William
Reviewed on: 2020-12-04
"""""
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras import layers
import tensorflow as tf
import pandas as pd
import numpy as np
import pickle
import cv2
import os





#Define input paths
DATADIR = "BB_Dataset"
IMAGE_SIZE = 128
IMG_PATH = os.path.join(DATADIR, "images")
ANNO_PATH = os.path.join(DATADIR, "annotations\labels.csv")

# Init array for training
data = []
labels = []
bboxes = []
imagePaths = []

print("loading data")

# Read the csv and images and place them into the data arrays.
annot_file = pd.read_csv(ANNO_PATH)

#Reads the first collum, file names
filenames = annot_file.iloc[:, 0].values

#Reads the second collum, x1
x1 = annot_file.iloc[:, 1].values

#Reads the third collum, y1
y1 = annot_file.iloc[:, 2].values

#Reads the forth collum, x2
x2 = annot_file.iloc[:, 3].values

#Reads the fifth collum, y2
y2 = annot_file.iloc[:, 4].values

#Reads the sixth collum, label
labels_temp = annot_file.iloc[:, 5].values

#Loops through all the filenames and appends it's data to the arrays.
i = 0
for filename in filenames:
        #Gets the path for the images from the csv file
        imagePath = os.path.sep.join( [IMG_PATH, labels_temp[i], filename])
        img = cv2.imread(imagePath)
       
        #Convert the coordinates to a usable values for the model
        h, w = img.shape[:2]
        x_start = float(x1[i]) / w
        y_start = float(y1[i]) / h
        x_end = float(x2[i]) / w
        y_end = float(y2[i]) / h

        #Loads the actually image
        img = load_img(imagePath, target_size=(128, 128))
        img = img_to_array(img)

        #Adds processed / loaded data to it's respective array
        data.append(img)
        labels.append(labels_temp[i])
        bboxes.append((x_start, y_start, x_end, y_end))
        imagePaths.append(imagePath)
        i = i + 1

print("storing data")

#Gör om till numpy arrayer.
data = np.array(data, dtype="float32") / 255.0
labels = np.array(labels)
bboxes = np.array(bboxes, dtype="float32")
imagePaths = np.array(imagePaths)

#Saves all the data in pickle format, so it can be loaded in the trainign file
#This is to avoid reloading the data every time we train it.

pickle_out = open("data.pickle","wb")
pickle.dump(data, pickle_out)
pickle_out.close()


pickle_out = open("labels.pickle","wb")
pickle.dump(labels, pickle_out)
pickle_out.close()

pickle_out = open("bboxes.pickle","wb")
pickle.dump(bboxes, pickle_out)
pickle_out.close()

pickle_out = open("imagePaths.pickle","wb")
pickle.dump(imagePaths, pickle_out)
pickle_out.close()

pickle_in = open("data.pickle","rb")
data = pickle.load(pickle_in)

print("done")