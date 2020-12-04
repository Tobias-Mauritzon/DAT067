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
DATADIR = "Car_Localization"
IMAGE_SIZE = 224
IMG_PATH = os.path.join(DATADIR, "cars_train")
ANNO_PATH = os.path.join(DATADIR, "BoundingBoxes.csv")
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
#labels = []
bboxes = []
imagePaths = []

# Read the csv and images and place them into the data arrays.
annot_file = pd.read_csv(ANNO_PATH)


#Reads the second collum, x1
x1 = annot_file.iloc[:, 0].values

#Reads the third collum, y1
y1 = annot_file.iloc[:, 1].values

#Reads the forth collum, x2
x2 = annot_file.iloc[:, 2].values

#Reads the fifth collum, y2
y2 = annot_file.iloc[:, 3].values

#Reads the first collum, file names
filenames = annot_file.iloc[:, 4].values

#Reads the sixth collum, label
#labels_temp = annot_file.iloc[:, 5].values
i = 0
while( i <10):
        print(filenames[i])
        print(x1[i])
        print(y1[i])
        print(x2[i])
        print(y2[i])
        i = i + 1
#Loops through all the filenames and appends it's data to the arrays.
i = 0
for filename in filenames:
        filename = filename.translate(str.maketrans({"'":None}))
        imagePath = os.path.sep.join( [IMG_PATH,  filename])
        img = cv2.imread(imagePath)
        #print( os.path.join( IMG_PATH, filename))
        #print(img)
        h, w = img.shape[:2]
        x_start = float(x1[i]) / w
        y_start = float(y1[i]) / h
        x_end = float(x2[i]) / w
        y_end = float(y2[i]) / h
   
        if(i < 10):
                print(imagePath)
                print(x_start)
                print(y_start)
                print(x_end)
                print(y_end)
        img = load_img(imagePath, target_size=(IMAGE_SIZE, IMAGE_SIZE))
        img = img_to_array(img)

        data.append(img)
        bboxes.append((x_start, y_start , x_end, y_end))
        imagePaths.append(imagePath)
        i = i + 1

#imgPaths = os.path.sep.join([IMG_PATH, label, filename])


#Gör om till numpy arrayer.
data = np.array(data, dtype="float32") / 255.0
bboxes = np.array(bboxes, dtype="float32")
imagePaths = np.array(imagePaths)

print(data)
print(bboxes)
print(imagePaths)

pickle_out = open("data.pickle","wb")
pickle.dump(data, pickle_out)
pickle_out.close()

pickle_out = open("bboxes.pickle","wb")
pickle.dump(bboxes, pickle_out)
pickle_out.close()

pickle_out = open("imagePaths.pickle","wb")
pickle.dump(imagePaths, pickle_out)
pickle_out.close()

pickle_in = open("data.pickle","rb")
data = pickle.load(pickle_in)