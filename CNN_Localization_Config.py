"""""
A config script to prepare the how to handle both the output and input of a simple model that can estimate bounding boxes
Author: Greppe
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
"""""
#Define output paths
B_OUTPUT = "output"
MODEL_PATH = os.path.sep.join([B_OUTPUT, "detector.h5"])
LB_PATH = os.path.sep.join([B_OUTPUT, "lb.pickle"])
PLOTS_PATH = os.path.sep.join([B_OUTPUT, "plots"])
TEST_PATHS = os.path.sep.join([B_OUTPUT, "test_paths.txt"])

#INIT values for training
INIT_LR = 1e-4
EPOCHS = 20
BATCH = 16
"""""
# Init array for training
data = []
labels = []
bboxes = []
imagePaths = []

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
        imagePath = os.path.sep.join( [IMG_PATH, labels_temp[i], filename])
        img = cv2.imread(imagePath)
        print( os.path.join( IMG_PATH, labels_temp[i], filename))
        print(img)
        h, w = img.shape[:2]
        x1[i] = float(x1[i]) / w
        y1[i] = float(y1[i]) / h
        x2[i] = float(x2[i]) / w
        y2[i] = float(y2[i]) / h
        img = load_img(imagePath, target_size=(128, 128))
        img = img_to_array(img)

        data.append(img)
        labels.append(labels_temp[i])
        bboxes.append((x1[i], y1[i], x2[i], y2[i]))
        imagePaths.append(imagePath)
        i = i + 1

#imgPaths = os.path.sep.join([IMG_PATH, label, filename])


#Gör om till numpy arrayer.
data = np.array(data, dtype="float32") / 255.0
labels = np.array(labels)
bboxes = np.array(bboxes, dtype="float32")
imagePaths = np.array(imagePaths)

print(data)
print(labels)
print(bboxes)
print(imagePaths)

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