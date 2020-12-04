"""""
A script for training object localization for cars only using the VGG16 network / modell
Author: Greppe
Reviewed by: William
Reviewed on: 2020-12-04
"""""

from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow import keras
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
import pickle
import cv2
import os

#Limits how much tensorflow can use of the GPU
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session =tf.compat.v1.InteractiveSession(config=config)


#INIT values for training
INIT_LR = 1e-4
EPOCHS = 10
BATCH = 8
PLOTS_PATH = "plots"

#Loads in the saved data that the config file created
pickle_in = open("data.pickle","rb")
data = pickle.load(pickle_in)

pickle_in = open("bboxes.pickle","rb")
bboxes = pickle.load(pickle_in)

pickle_in = open("imagePaths.pickle","rb")
imagePaths = pickle.load(pickle_in)

#Splits the data for training and testing
split = train_test_split(data, bboxes, imagePaths, test_size=0.20, random_state=42)

(trainImages, testImages) = split[:2]
(trainTargets, testTargets) = split[2:4]
(trainPaths, testPaths) = split[4:]

#Loads the VGG16 network
vgg = VGG16(weights="imagenet", include_top=False, input_tensor=Input(shape=(224, 224, 3)))
vgg.summary()
flatten_1 = vgg.output
flatten_1 = Flatten(name="flatten_1") (flatten_1)

#Estimation for bounding boxes
bboxHead = Dense(128, activation="relu")(flatten_1)
bboxHead = Dense(64, activation="relu")(bboxHead)
bboxHead = Dense(32, activation="relu")(bboxHead)
bboxHead = Dense(4, activation="sigmoid", name="bounding_box")(bboxHead)

loc_model = Model(inputs=vgg.input, outputs=bboxHead)
loc_model.summary()

#Defines the loss fucntion
losses = {'bounding_box': 'mean_squared_error'}

#Defines the weight of the loss function
lossWeights = {'bounding_box': 1.0}

#Defines the optimizer and the learning rate
opt = tf.keras.optimizers.Adam(learning_rate=INIT_LR)

#Complies the model with the defined optimizers, loss and loss weight
loc_model.compile(optimizer=keras.optimizers.Adam(learning_rate=INIT_LR), loss=losses, metrics=["accuracy"], loss_weights=lossWeights)
print(loc_model.summary())

#Trains the model and stores its output in a variable for plotning
history = loc_model.fit(trainImages, trainTargets,validation_data = (testImages, testTargets),batch_size=BATCH, epochs = EPOCHS,verbose=1, shuffle=True)

#Saves the model
loc_model.save('saved_model/pretrained_car_localization')

# plot the model training history
N = EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), history.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), history.history["val_loss"], label="val_loss")
plt.title("Bounding Box Regression Loss on Training Set")
plt.xlabel("Epoch #")
plt.ylabel("Loss")
plt.legend(loc="lower left")
plt.savefig(PLOT_PATH)