import cv2
import numpy as np

class TensorFlow_Custom_Model():
    def __init__(self):
        self.ObjectsFile = 'Yolo_v3/coco.names'
        self.ObjectNames = [] 
        self.openFiles()

    def loadObjectNames(self):
        with open(self.ObjectsFile,'rt') as f:
            self.ObjectNames = f.read().rstrip('\n').split('\n')
        #print(self.ObjectNames)
        #print(len(self.ObjectNames))


    # Finds where the object is and draws a rectangle
    #def findObject(self, image):
        
"""THIS "main" IS ONLY USED FOR TESTING PURPOSES"""
# Use this if you want to start without the loading window.
if __name__ == '__main__':
    test =  TensorFlow_Custom_Model()
        