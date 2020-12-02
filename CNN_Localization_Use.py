
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
    
CATEGORIES = ["Car", "Dog", "Cat"]

# Funktion för att ladda in bilder så det går att testa.
def prepare(filepath):
    IMG_SIZE = 128
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)

model = tf.keras.models.load_model("saved_model/localization_model")

prediction = model.predict(prepare("dog7.jpg"))
print(prediction)
(boxPreds, labelPreds) = prediction
print(boxPreds)
print(labelPreds)
# loop over the images that we'll be testing using our bounding box
# regression model

def predictNprepare_image(filepath):
    IMG_SIZE = 128
    image = load_img(imagePath, target_size=(IMG_SIZE, IMG_SIZE))
    image = img_to_array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    (boxPreds, labelPreds) = prediction
    X1 = boxPreds[0]
    Y1 = boxPreds[1]
    X2 = boxPreds[2]
    Y2 = boxPreds[3]

    # determine the class label with the largest predicted
    # probability
    i = np.argmax(labelPreds, axis=1)
    label = CATEGORIES[i][0]
    print(label)
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    (h, w) = new_array.shape[:2]
    # scale the predicted bounding box coordinates based on the image
    # dimensions
    X1 = int(X1 * w)
    Y1 = int(Y1 * h)
    X2 = int(X2 * w)
    Y2 = int(Y2 * h)
    # draw the predicted bounding box and class label on the image
    y = startY - 10 if startY - 10 > 10 else startY + 10
    cv2.putText(new_array, label, (X1, y), cv2.FONT_HERSHEY_SIMPLEX,
    0.65, (0, 255, 0), 2)
    cv2.rectangle(new_array, (X1, Y1), (X2, Y2),
    (0, 255, 0), 2)
    # show the output image
    cv2.imshow("Output", new_array)
    cv2.waitKey(0)

def predict_image(filepath):
    # load the input image (in Keras format) from disk and preprocess
    # it, scaling the pixel intensities to the range [0, 1]
    image = load_img(filepath, target_size=(128, 128))
    image = img_to_array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    # predict the bounding box of the object along with the class
    # label
    (boxPreds, labelPreds) = model.predict(image)
    (startX, startY, endX, endY) = boxPreds[0]
    # determine the class label with the largest predicted
    # probability
    i = np.argmax(labelPreds, axis=1)
    label = CATEGORIES[i][0]
    print(label)
    image = cv2.imread(filepath)
    (h, w) = image.shape[:2]
    # scale the predicted bounding box coordinates based on the image
    # dimensions
    startX = int(startX * w)
    startY = int(startY * h)
    endX = int(endX * w)
    endY = int(endY * h)
    # draw the predicted bounding box and class label on the image
    y = startY - 10 if startY - 10 > 10 else startY + 10
    cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX,
    0.65, (0, 255, 0), 2)
    cv2.rectangle(image, (startX, startY), (endX, endY),
    (0, 255, 0), 2)
    # show the output image
    cv2.imshow("Output", image)
    cv2.waitKey(0)



predictNprepare_image("dog8.jpg")