import cv2
import numpy as np
from DistanceEstimator import DistanceEstimator
from pathlib import Path

# Author: Philip
# Reviewed by:
# Date: 2020-12-13

"""This class loads loads the yolo method for object detection and uses it to find 80 different objects with the function findObject"""
class Yolo_Model():
    def __init__(self):
        self.ObjectsFile = 'Yolo_v3_tiny/coco.names'
        self.objectNames = []
        self.CONFTRESHOLD_def = 0.5
        self.CONFTRESHOLD = self.CONFTRESHOLD_def
        self.nms_threshold = 0.2 # less means less boxes
        self.textColor = (0, 255, 0)
        self.boxColor = (0, 255, 0)
        self.distanceTextColor = (0,0,0)
        self.__loadObjectNames()
        self.carEstimator = None
        self.__distanceSetup()
        self.__readNet()

    # Check if camera info file is available
    def __distanceSetup(self):
        if Path("camera_info.ini").is_file():
            self.setDistanceEtimators()

    # Read file with object names
    def __loadObjectNames(self):
        with open(self.ObjectsFile,'rt') as f:
            self.objectNames = f.read().rstrip('\n').split('\n')
    
    # Read the network
    def __readNet(self):
        self.weights = 'Yolo_v3_tiny/yolov3-tiny.weights'
        self.configFile = 'Yolo_v3_tiny/yolov3-tiny.cfg'
        self.net = cv2.dnn.readNetFromDarknet(self.configFile,self.weights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    
    # Convert to blobformat since the network only knows that format
    def __prepare(self, image):
        self.blob = cv2.dnn.blobFromImage(image,1/255,(250,250),[0,0,0],1,crop=False)

    # This function is used in the findObjects function. It loops through each detection in each output and prints out text and bounding boxes for each object.
    def __find(self, outputs, image):
        imgHeight, imgWidth, imgChannels = image.shape
        boundingBox = []
        classIds = []
        confidenceValues = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.CONFTRESHOLD:
                    w,h = int(detection[2]*imgWidth), int(detection[3]*imgHeight)
                    x,y = int(detection[0]*imgWidth) - int(w/2), int(detection[1]*imgHeight) - int(h/2)
                    boundingBox.append([x,y,w,h])
                    classIds.append(classId)
                    confidenceValues.append(float(confidence))

        indices = cv2.dnn.NMSBoxes(boundingBox,confidenceValues,self.CONFTRESHOLD,self.nms_threshold) # Eliminates overlaping boxes

        for i in indices:
            i = i[0]
            box = boundingBox[i]
            x,y,w,h = box[0],box[1],box[2],box[3]
            if self.carEstimator is not None:
                distance = self.carEstimator.estimate_distance(w)
                cv2.putText(image, distance, (x + 10, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.textColor, 2)

            cv2.rectangle(image,(x,y),(x+w,y+h),self.boxColor,2)
            cv2.putText(image,f'{self.objectNames[classIds[i]].upper()} {int(confidenceValues[i]*100)}%', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.textColor, 2)
    
    def setConfidenceTreshhold(self,number):
        self.CONFTRESHOLD = number/100

    def setDistanceEtimators(self):
        # sets width of obejct to measure distance to. //1.8 for car //0.52 for num.plate //0.15 for face
        self.carEstimator = DistanceEstimator(1.8)
    
    def resetValues(self):
        self.CONFTRESHOLD = self.CONFTRESHOLD_def


    # Finds objects 
    def findObjects(self, image):
        self.__prepare(image)
        self.net.setInput(self.blob)
        layerNames = self.net.getLayerNames()
        outputNames = [layerNames[i[0]-1] for i in self.net.getUnconnectedOutLayers()]
        outPuts = self.net.forward(outputNames)
        self.__find(outPuts,image)
        