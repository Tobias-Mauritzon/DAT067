import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
import cv2
import numpy as np
from DistanceEstimator import DistanceEstimator
from pathlib import Path

# Author: Philip
# Reviewed by: 
# Date: 2020-12-05

# Author: Joachim Antfolk
# Reviewed by:
# Date: 2020-12-15

"""This class loads a specific pretrained model and uses it to find an object with the function findObject"""
class TensorFlow_Custom_Model():
    def __init__(self, modelType):
        self.modelType = modelType
        if self.modelType == 0:
            self.my_model = tf.keras.models.load_model("pretrained_car_localization") # only box (will always show box)
        elif self.modelType == 1:
            self.my_model = tf.keras.models.load_model("pretrained_localization_model") # with label and box
        elif self.modelType == 2:
            print("TF_LITE TEST!")
            MODELPATH = "Cl_tflite"
            self.interpreter = tf.lite.Interpreter(model_path=MODELPATH)
            self.input_det = self.interpreter.get_input_details()
            self.output_det = self.interpreter.get_output_details()
            self.interpreter.resize_tensor_input(self.input_det[0]['index'],(1,224,224,3))
            self.interpreter.resize_tensor_input(self.output_det[0]['index'],(4,3))
            self.interpreter.allocate_tensors()
        elif self.modelType == 3: # Tensorflow Lite multiple 
            MODELPATH = "Cl_tflite_OI"
            self.interpreter = tf.lite.Interpreter(model_path=MODELPATH)
            self.input_det = self.interpreter.get_input_details()
            self.output_det = self.interpreter.get_output_details()
            self.interpreter.resize_tensor_input(self.input_det[0]['index'],(1,128,128,3))
            self.interpreter.resize_tensor_input(self.output_det[0]['index'],(4,3))
            self.interpreter.allocate_tensors()

    def __resizeImage(self,image):
        resizedImage = None
        if self.modelType == 0 or self.modelType == 1 or self.modelType == 2:
            IMG_SIZE = 224
            resizedImage = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
            resizedImage = img_to_array(resizedImage) / 255.0
            resizedImage = resizedImage.reshape([1, IMG_SIZE, IMG_SIZE, 3])
        elif self.modelType == 3:
            IMG_SIZE = 128
            resizedImage = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
            resizedImage = img_to_array(resizedImage) / 255.0
            resizedImage = resizedImage.reshape([1, IMG_SIZE, IMG_SIZE, 3])

        return resizedImage

        self.carEstimator = None
        if Path("camera_info.ini").is_file():
            self.setDistanceEtimators()

    # Finds where the object is and draws a rectangle
    def findObject(self, image):

        if self.modelType == 0: # TF car
            resizedImage = self.__resizeImage(image)
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

            if self.carEstimator is not None:
                distance = self.carEstimator.estimate_distance(X2)
                cv2.rectangle(image, (X1, Y2), (X2, Y2 + 40), (0, 255, 0), -1)
                cv2.putText(image, distance, (X1 + 10, Y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
            cv2.putText(image, "Car", (X1, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
            cv2.rectangle(image, (X1, Y1), (X2, Y2), (0, 255, 0), 2)
            
        elif self.modelType == 1: # TF Car and more
            resizedImage = self.__resizeImage(image)
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

            if label == "Car" or label == "Dog" or label == "Cat":
                cv2.rectangle(image, (X1, Y1), (X2, Y2), (0, 255, 0), 2)
                cv2.putText(image, label, (X1, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

        elif self.modelType == 2: # TF Lite Car
            resizedImage = self.__resizeImage(image)
            img_np = np.array(resizedImage, dtype=np.float32)
            self.interpreter.set_tensor(self.input_det[0]['index'], img_np)
            self.interpreter.invoke()
            predictions = self.interpreter.get_tensor(self.output_det[0]['index'])
            X1 = predictions[0][0]
            Y1 = predictions[0][1]
            X2 = predictions[0][2]
            Y2 = predictions[0][3]

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

        elif self.modelType == 3: # TF Lite Car and more
            CATEGORIES = ["Car", "Dog", "Cat"]
            resizedImage = self.__resizeImage(image)
            img_np = np.array(resizedImage, dtype=np.float32)
            self.interpreter.set_tensor(self.input_det[0]['index'], img_np)
            self.interpreter.invoke()
            labelPreds = self.interpreter.get_tensor(self.output_det[1]['index'])
            predictions = self.interpreter.get_tensor(self.output_det[0]['index'])
            i = np.argmax(labelPreds[0], axis=0)
            label = CATEGORIES[i]

            X1 = predictions[0][0]
            Y1 = predictions[0][1]
            X2 = predictions[0][2]
            Y2 = predictions[0][3]

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
            if label == "Car":
                if self.carEstimator is not None:
                    distance = self.carEstimator.estimate_distance(X2)
                    cv2.rectangle(image, (X1, Y2), (X2, Y2 + 40), (0, 255, 0), -1)
                    cv2.putText(image, distance, (X1 + 10, Y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
                cv2.putText(image, label, (X1, y), cv2.FONT_HERSHEY_SIMPLEX,0.65, (0, 255, 0), 2)
                cv2.rectangle(image, (X1, Y1), (X2, Y2),(0, 255, 0), 2)

    def setDistanceEtimators(self):
        # sets width of obejct to measure distance to. //1.8 for car //0.52 for num.plate //0.15 for face
        self.carEstimator = DistanceEstimator(1.8)
