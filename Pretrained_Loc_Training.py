"""""
A script for training object localization & classifcation for cars, cats and dogs using the VGG16 network / modell
Author: Greppe
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
BATCH = 32
PLOTS_PATH = "plots"

#Loads in the saved data that the config file created
pickle_in = open("data.pickle","rb")
data = pickle.load(pickle_in)

pickle_in = open("labels.pickle","rb")
labels = pickle.load(pickle_in)

pickle_in = open("bboxes.pickle","rb")
bboxes = pickle.load(pickle_in)

pickle_in = open("imagePaths.pickle","rb")
imagePaths = pickle.load(pickle_in)

#Converts the catogerisation labels to a readable format
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
# only there are only two labels in the dataset, then we need to use
# Keras/TensorFlow's utility function as well
if len(lb.classes_) == 2:
    labels = to_categorical(labels)

#Splits the data for training and testing
split = train_test_split(data, labels, bboxes, imagePaths, test_size=0.20, random_state=42)

(trainImages, testImages) = split[:2]
(trainLabels, testLabels) = split[2:4]
(trainBBoxes, testBBoxes) = split[4:6]
(trainPaths, testPaths) = split[6:]

#Loads the VGG16 network
vgg = VGG16(weights="imagenet", include_top=False, input_tensor=Input(shape=(224, 224, 3)))
vgg.summary()
flatten_1 = vgg.output
flatten_1 = Flatten(name="flatten_1") (flatten_1)

#Split for bounding boxes
bboxHead = Dense(128, activation="relu")(flatten_1)
bboxHead = Dense(64, activation="relu")(bboxHead)
bboxHead = Dense(32, activation="relu")(bboxHead)
bboxHead = Dense(4, activation="sigmoid", name="bounding_box")(bboxHead)

#Split for estimating category
softmaxHead = Dense(512, activation="relu")(flatten_1)
softmaxHead = Dropout(0.5)(softmaxHead)
softmaxHead = Dense(512, activation="relu")(softmaxHead)
softmaxHead = Dropout(0.5)(softmaxHead)
softmaxHead = Dense(3, activation="softmax", name="class_label")(softmaxHead)

#Defines the outputs and inputs
loc_model = Model(inputs=vgg.input, outputs=[bboxHead, softmaxHead])
loc_model.summary()

#Defines the loss functions to use for each split of the network
losses = {'class_label': 'categorical_crossentropy', 'bounding_box': 'mean_squared_error'}

#Defines the loss functions weight to use for each split of the network
lossWeights = { 'class_label': 1.0,'bounding_box': 1.0}

#Defines our optimizer and the learning rate of the model
opt = tf.keras.optimizers.Adam(learning_rate=INIT_LR)

#Compiles our network with the loss, losswieght and optimizers defined before
loc_model.compile(optimizer=keras.optimizers.Adam(learning_rate=INIT_LR), loss=losses, metrics=["accuracy"], loss_weights=lossWeights)
print(loc_model.summary())

#Defines what data ot use for traing and for testing
trainTargets = {"class_label": trainLabels, "bounding_box": trainBBoxes}
testTargets = {"class_label": testLabels , "bounding_box": testBBoxes}

#Runs the training and stories the outputs as history so we can plot the results
history = loc_model.fit(trainImages, trainTargets,validation_data = (testImages, testTargets),batch_size=BATCH, epochs = EPOCHS,verbose=1)

#Saves the model
loc_model.save('saved_model/pretrained_localization_model')

#Plots the data of the training

# plot the total loss, label loss, and bounding box loss
lossNames = ["loss", "class_label_loss", "bounding_box_loss"]
N = np.arange(0, EPOCHS)
plt.style.use("ggplot")
(fig, ax) = plt.subplots(3, 1, figsize=(13, 13))
# loop over the loss names
for (i, l) in enumerate(lossNames):
	# plot the loss for both the training and validation data
	title = "Loss for {}".format(l) if l != "loss" else "Total loss"
	ax[i].set_title(title)
	ax[i].set_xlabel("Epoch #")
	ax[i].set_ylabel("Loss")
	ax[i].plot(N, history.history[l], label=l)
	ax[i].plot(N, history.history["val_" + l], label="val_" + l)
	ax[i].legend()
# save the losses figure and create a new figure for the accuracies
plt.tight_layout()


plt.style.use("ggplot")
plt.figure()
plt.plot(N, history.history["class_label_accuracy"],
	label="class_label_train_acc")
plt.plot(N, history.history["val_class_label_accuracy"],
	label="val_class_label_acc")
plt.title("Class Label Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Accuracy")
plt.legend(loc="lower left")
plt.show()