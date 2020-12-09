import cv2
import numpy as np

class Yolo_Model():
    def __init__(self):
        self.ObjectsFile = 'Yolo_v3_tiny/coco.names'
        self.objectNames = []
        self.CONFTRESHOLD = 0.5
        self.nms_threshold = 0.3
        self.__loadObjectNames()
        self.__readNet()

    def __loadObjectNames(self):
        with open(self.ObjectsFile,'rt') as f:
            self.objectNames = f.read().rstrip('\n').split('\n')
        #print(self.ObjectNames)
        #print(len(self.ObjectNames))
    
    #read the network
    def __readNet(self):
        self.weights = 'Yolo_v3_tiny/yolov3-tiny.weights'
        self.configFile = 'Yolo_v3_tiny/yolov3-tiny.cfg'
        self.net = cv2.dnn.readNetFromDarknet(self.configFile,self.weights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    
    # convert to blobformat since the network only knows that format
    def __prepare(self, image):
        self.blob = cv2.dnn.blobFromImage(image,1/255,(250,250),[0,0,0],1,crop=False)

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

        indices = cv2.dnn.NMSBoxes(boundingBox,confidenceValues,self.CONFTRESHOLD,self.nms_threshold)

        for i in indices:
            i = i[0]
            box = boundingBox[i]
            x,y,w,h = box[0],box[1],box[2],box[3]
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
            cv2.putText(image,f'{self.objectNames[classIds[i]].upper()} {int(confidenceValues[i]*100)}%', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255), 2)
    
    def findObjects(self, image):
        self.__prepare(image)
        self.net.setInput(self.blob)

        layerNames = self.net.getLayerNames()

        outputNames = [layerNames[i[0]-1] for i in self.net.getUnconnectedOutLayers()]

        outPuts = self.net.forward(outputNames)

        self.__find(outPuts,image)

        
"""THIS "main" IS ONLY USED FOR TESTING PURPOSES"""
# Use this if you want to start without the loading window.
if __name__ == '__main__':
    test =  TensorFlow_Custom_Model()
        