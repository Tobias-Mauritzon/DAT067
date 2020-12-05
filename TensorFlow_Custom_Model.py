import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
import cv2
import numpy as np

# Author: Philip
# Reviewed by: 
# Date: 2020-12-05

"""This class loads a specific pretrained model and uses it to find an object with the function findObject"""
class TensorFlow_Custom_Model():
    def __init__(self, modelType):
        self.modelType = modelType
        if self.modelType == 0:
            self.my_model = tf.keras.models.load_model("pretrained_car_localization") # only box (will always show box)
        elif self.modelType == 1:
            self.my_model = tf.keras.models.load_model("pretrained_localization_model") # with label and box

    # Finds where the object is and draws a rectangle
    def findObject(self, image):
        IMG_SIZE = 224
        resizedImage = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
        resizedImage = img_to_array(resizedImage) / 255.0
        resizedImage = np.expand_dims(resizedImage, axis=0)

        if self.modelType == 0:
            prediction = self.my_model.predict(resizedImage)[0]
            (x1, y1, x2, y2) = prediction
            X1 = prediction[0]
            Y1 = prediction[1]
            X2 = prediction[2]
            Y2 = prediction[3]

            # determine the class label with the largest predicted
            # probability

            (h, w) = image.shape[:2]
            # scale the predicted bounding box coordinates based on the image
            # dimensions
            X1 = int(X1 * w)
            Y1 = int(Y1 * h)
            X2 = int(X2 * w)
            Y2 = int(Y2 * h)
            # draw the predicted bounding box and class label on the image
            y = Y1 - 10 if Y1 - 10 > 10 else Y1 + 10
            cv2.putText(image, "Car", (X1, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
            cv2.rectangle(image, (X1, Y1), (X2, Y2), (0, 255, 0), 2)
            
        elif self.modelType == 1:
            prediction = self.my_model.predict(resizedImage)
            (boxPreds, labelPreds) = prediction    
            X1 = boxPreds[0][0]
            Y1 = boxPreds[0][1]
            X2 = boxPreds[0][2]
            Y2 = boxPreds[0][3]

            CATEGORIES = ["Car", "Dog", "Cat"]
            # determine the class label with the largest predicted
            # probability
            i = np.argmax(labelPreds[0], axis=0)
            label = CATEGORIES[i]

            (h, w) = image.shape[:2]
            # scale the predicted bounding box coordinates based on the image
            # dimensions
            X1 = int(X1 * w)
            Y1 = int(Y1 * h)
            X2 = int(X2 * w)
            Y2 = int(Y2 * h)
            # draw the predicted bounding box and class label on the image
            y = Y1 - 10 if Y1 - 10 > 10 else Y1 + 10

            if label == "Car":
                cv2.rectangle(image, (X1, Y1), (X2, Y2), (0, 255, 0), 2)
                cv2.putText(image, label, (X1, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)