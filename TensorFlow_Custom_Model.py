import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
import cv2
import numpy as np
from DistanceEstimator import DistanceEstimator
from pathlib import Path

# Author: Philip
# Reviewed by: 
# Date: 2020-12-18

# Author: Joachim Antfolk
# Date: 2020-12-15
# Reviewed by: William Jönsson
# Reviewed on: 2020-12-18

# Author: William Jönsson
# Date: 2020-12-18
# Reviewed by:
# Reviewed on:

"""This class loads a specific pretrained model and uses it to find an object with the function findObject"""
class TensorFlow_Custom_Model():
    def __init__(self, modelType):
        self.modelType = modelType
        self.__loadModel()
        self.carEstimator = None
        self.__distanceSetup()
        
    # Load custom model
    def __loadModel(self):
        if self.modelType == 0:
            self.imageSize = 224
            self.my_model = tf.keras.models.load_model("pretrained_car_localization") # Tensorflow Cars
        elif self.modelType == 1:
            self.imageSize = 224
            self.my_model = tf.keras.models.load_model("pretrained_localization_model") # Tensorflow Cars and other
        elif self.modelType == 2: # Tensorflow Lite Cars
            self.imageSize = 224
            self.__loadTensorFlowLite("Cl_tflite")        
        elif self.modelType == 3: # Tensorflow Lite Cars and other 
            self.imageSize = 128
            self.__loadTensorFlowLite("Cl_tflite_OI")

    # Load tensorflow lite model
    def __loadTensorFlowLite(self,modelPath):
        self.interpreter = tf.lite.Interpreter(model_path=modelPath)
        self.input_det = self.interpreter.get_input_details()
        self.output_det = self.interpreter.get_output_details()
        self.interpreter.resize_tensor_input(self.input_det[0]['index'],(1,self.imageSize,self.imageSize,3))
        #self.interpreter.resize_tensor_input(self.output_det[0]['index'],(4,3))
        self.interpreter.allocate_tensors()

    # Check if camera info file is available
    def __distanceSetup(self):
        if Path("camera_info.ini").is_file():
            self.setDistanceEtimators()

    # Resizes the image to suit the model 
    def __resizeImage(self,image):
        resizedImage = None
        resizedImage = cv2.resize(image, (self.imageSize, self.imageSize))
        resizedImage = img_to_array(resizedImage) / 255.0
        resizedImage = resizedImage.reshape([1, self.imageSize, self.imageSize, 3])
        return resizedImage

    # Finds where the object is and draws a rectangle
    def findObject(self, image):
        self.carFound = False
        resizedImage = self.__resizeImage(image)
        if self.modelType == 0: # TF car
            prediction = self.my_model.predict(resizedImage)[0]
            (x1, y1, x2, y2) = prediction
            x1 = prediction[0]
            y1 = prediction[1]
            x2 = prediction[2]
            y2 = prediction[3]
            # determine the class label with the largest predicted
            # probability
            self.__showOutput(image,x1,x2,y1,y2,"Car")
            
        elif self.modelType == 1: # TF Car and more
            CATEGORIES = ["Car", "Dog", "Cat"]
            predictions = self.my_model.predict(resizedImage)
            (boxPreds, labelPreds) = predictions    
            x1 = boxPreds[0][0]
            y1 = boxPreds[0][1]
            x2 = boxPreds[0][2]
            y2 = boxPreds[0][3]
            # determine the class label with the largest predicted
            # probability
            i = np.argmax(labelPreds[0], axis=0)
            label = CATEGORIES[i]
            self.__showOutput(image,x1,x2,y1,y2,label)

        elif self.modelType == 2: # TF Lite Car
            img_np = np.array(resizedImage, dtype=np.float32)
            self.interpreter.set_tensor(self.input_det[0]['index'], img_np)
            self.interpreter.invoke()
            prediction = self.interpreter.get_tensor(self.output_det[0]['index'])
            x1 = prediction[0][0]
            y1 = prediction[0][1]
            x2 = prediction[0][2]
            y2 = prediction[0][3]
            self.__showOutput(image,x1,x2,y1,y2,"Car")

        elif self.modelType == 3: # TF Lite Car and more
            CATEGORIES = ["Car", "Dog", "Cat"]
            img_np = np.array(resizedImage, dtype=np.float32)
            self.interpreter.set_tensor(self.input_det[0]['index'], img_np)
            self.interpreter.invoke()
            labelPreds = self.interpreter.get_tensor(self.output_det[1]['index'])
            predictions = self.interpreter.get_tensor(self.output_det[0]['index'])
            i = np.argmax(labelPreds[0], axis=0)
            label = CATEGORIES[i]

            x1 = predictions[0][0]
            y1 = predictions[0][1]
            x2 = predictions[0][2]
            y2 = predictions[0][3]

            self.__showOutput(image,x1,x2,y1,y2,label)
        
        
    # Shows label and bounding box
    def __showOutput(self,image,x1,x2,y1,y2,label):
        (h, w) = image.shape[:2]
        # scale the predicted bounding box coordinates based on the image
        # dimensions
        x1 = int(x1 * w)
        y1 = int(y1 * h)
        x2 = int(x2 * w)
        y2 = int(y2 * h)
        # draw the predicted bounding box and class label on the image
        y = y1 - 10 if y1 - 10 > 10 else y1 + 10
        # distance estimation with label
        if label == "Car":
            self.carFound = True
            cv2.putText(image, label, (x1, y), cv2.FONT_HERSHEY_SIMPLEX,0.65, (0, 255, 0), 2)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        else:
            cv2.putText(image, label, (x1, y), cv2.FONT_HERSHEY_SIMPLEX,0.65, (0, 255, 0), 2)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if self.carFound is True and self.carEstimator is not None:
            distance = self.carEstimator.estimate_distance(x2)
            cv2.rectangle(image, (x1, y2), (x2, y2 + 40), (0, 255, 0), -1)
            cv2.putText(image, distance, (x1 + 10, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
            
    def setDistanceEtimators(self):
        # sets width of obejct to measure distance to. //1.8 for car //0.52 for num.plate //0.15 for face
        self.carEstimator = DistanceEstimator(1.8)
