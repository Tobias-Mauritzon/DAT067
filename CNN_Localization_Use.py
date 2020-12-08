
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
import numpy as np
import mimetypes
import argparse
import pickle
import cv2
import os
import tensorflow as tf
"""""
A simple script to use the model that is trained on object localization & classifcation on cars, cats and dogs using our own pretrained model / network
Author: Greppe
Reviewed by: William
Reviewed on: 2020-12-04
"""""
CATEGORIES = ["Car", "Dog", "Cat"]

model = tf.keras.models.load_model("saved_model/localization_model")

# loop over the images that we'll be testing using our bounding box
# regression model

"""""
Loads the images specifed by Filepath and predicts it bounding boxes and classifcation, will output the images with boundings drawn with the estimated class as title.
filepath - the file path for the image you want to load.
"""""
def predictNprepare_image(filepath):
    IMG_SIZE = 128
    image = load_img(filepath, target_size=(IMG_SIZE, IMG_SIZE))
    image = img_to_array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    (boxPreds, labelPreds) = prediction
    X1 = boxPreds[0][0]
    Y1 = boxPreds[0][1]
    X2 = boxPreds[0][2]
    Y2 = boxPreds[0][3]

    # determine the class label with the largest predicted
    # probability
    print(labelPreds)
    i = np.argmax(labelPreds[0], axis=0)
    label = CATEGORIES[i]
    print(label)
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    (h, w) = img_array.shape[:2]
    # scale the predicted bounding box coordinates based on the image
    # dimensions
    X1 = int(X1 * w)
    Y1 = int(Y1 * h)
    X2 = int(X2 * w)
    Y2 = int(Y2 * h)
    # draw the predicted bounding box and class label on the image
    y = Y1 - 10 if Y1 - 10 > 10 else Y1 + 10
    cv2.putText(img_array, label, (X1, y), cv2.FONT_HERSHEY_SIMPLEX,
    0.65, (0, 255, 0), 2)
    cv2.rectangle(img_array, (X1, Y1), (X2, Y2),
    (0, 255, 0), 2)
    # show the output image
    cv2.imshow("Output", img_array)
    cv2.waitKey(0)

predictNprepare_image("dog8.jpg")