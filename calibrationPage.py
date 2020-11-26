import sys
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIntValidator
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QTimer
import numpy as np
import tensorflow as tf
from GUI.ui_calibrationPage import * 
from CameraCalibration import * 
from threading import Thread

# Author: Philip
# Reviewed by:
# Date: 2020-11-25

class CalibrationPage(QtWidgets.QWidget):
    def __init__(self):
        # call QWidget constructor
        super().__init__()

        self.ui = Ui_CalibrationPage()
        self.ui.setupUi(self)
        
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        # create a timer
        self.timer = QTimer()

        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)


        self.initLineEdits()
        self.ui.stackedWidget.setCurrentIndex(0) # start with page 0 (insert values page)

        self.setActions()

        self.objectWidth = 0
        self.objectHeight = 0
        self.squareWidth = 0
        self.objectDistance = 0.0
        
        self.calibrating = False
        self.capture = False

        #camCal = CameraCalibration(100,200,100)
        #camCal.calibrateCamera(200)

    def startCam(self):
        self.timer.start(0)

    def stopCam(self):
        # stop timer
        self.timer.stop()
        # release video capture
        self.cap.release()


    def viewCam(self):
       
         # read image in BGR format
        ret, self.image = self.cap.read()

        self.update()
        self.convertToQImage()
        self.resize_camFrame()
        # set image to image label
        self.ui.image_label.setPixmap(self.pix.scaled(self.w, self.h,QtCore.Qt.KeepAspectRatio))

    def update(self):
         # convert image to RGB format
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        self.height, self.width = self.image.shape
        self.channel = 1
        self.qiFormat = QImage.Format_Grayscale8

        if self.calibrating:
            self.image = cv2.cvtColor(self.image,cv2.COLOR_GRAY2RGB)
            self.height, self.width, self.channel = self.image.shape
            self.qiFormat = QImage.Format_RGB888
        
            ret, corners = cv2.findChessboardCorners(self.image, (7,6),None) # Find the chess board corners
            cv2.drawChessboardCorners(self.image, (7,6), corners,ret)# Draw and display the corners
            # Press space to use image for calibration
            if self.capture and ret:
                print("pressed")
                self.capture = False
                self.imageCounter += 1
                self.ui.Label_TakenCaptures.setNum(self.imageCounter)
                self.objpoints.append(self.objp)
                gray = cv2.cvtColor(self.image,cv2.COLOR_RGB2GRAY)
                cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),self.criteria)
                self.imgpoints.append(corners)
                
                if self.imageCounter >= self.REQUIRED_IMAGE_AMOUNT:
                    self.calibrating = False
                    print("Calculating camera matrix etc...")
                    ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, gray.shape[::-1],None,None)
                    print("...done calculating.")
                    self.cameraMatrix = cameraMatrix
                    self.ui.Label_Information.setText("<strong>Calibration</strong> was successful, return to main screen by clicking on <strong>Navigation -> Main Screen</strong> in the menubar")
                    
                    

    def convertToQImage(self):
        # calculate step
        step = self.channel * self.width
        # create QImage from image
        qImg = QImage(self.image.data, self.width, self.height, step, self.qiFormat)
        self.pix = QPixmap.fromImage(qImg)

    # resizes the cam frame
    def resize_camFrame(self):
        if self.pix is not None:
            self.w = self.ui.image_label.width()
            self.h = self.ui.image_label.height()

    def initLineEdits(self):
        self.ui.lineEdit_Width.setValidator(QDoubleValidator(0,1000,3,self)) # mm double
        self.ui.lineEdit_Height.setValidator(QDoubleValidator(0,1000,3,self)) # mm double
        self.ui.lineEdit_SquareWidth.setValidator(QIntValidator(0,1000,self)) # mm int
        self.ui.lineEdit_Distance.setValidator(QDoubleValidator(0,100,3,self)) # m double
    
    def setActions(self):
        self.ui.Button_Calibrate.clicked.connect(self.startCalibration)
        self.ui.Button_Capture.clicked.connect(self.captureAction)

    def captureAction(self):
        self.capture = True

    def startCalibration(self):
        try:
            width = float(self.ui.lineEdit_Width.text().replace(',','.'))
            height = float(self.ui.lineEdit_Height.text().replace(',','.'))
            patternSquareSize = int(self.ui.lineEdit_SquareWidth.text())
            distance = float(self.ui.lineEdit_Distance.text().replace(',','.'))
        except:
            print("ERROR not a number somewhere")

        """
        Calibrates camera using webcam feed with a checkerboard pattern.
        Parameters:
            patternSquareSize - checkerboard square size in mm
        """
        # termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((7*6,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        self.objp = self.objp * patternSquareSize

        # Arrays to store object points and image points from all the images.
        self.objpoints = [] # 3d point in real world space
        self.imgpoints = [] # 2d points in image plane.

        # Counter to keep track of calibration images taken - needs REQUIRED_IMAGE_AMOUNT to calibrate
        self.imageCounter = 0
        self.REQUIRED_IMAGE_AMOUNT = 5

        self.ui.Label_NeededCaptures.setNum(self.REQUIRED_IMAGE_AMOUNT)
        print("Press space to use current image to calibrate. Need ", self.REQUIRED_IMAGE_AMOUNT - self.imageCounter, " more images.")
        self.ui.stackedWidget.setCurrentIndex(1)
        self.calibrating = True

    def write_to_file(self, fx: int, fy: int):
        """
        Writes the integer parameters fx and fy to camera_info.ini  
        otherwise throws exception 
        """
        try:
            file = open("camera_info.ini", "w")
            file.write("fx:" + str(fx) + "\nfy:" + str(fy))
        except Exception:
            raise Exception("Could not write to file!")
        finally:
            file.close()
        
    def read_from_file(self) -> (int, int):
        """ 
        Reads the relevant camera inforamtion from camera_info.ini 
        returns a tuple in the format (fx, fy) 
        otherwise throws exception 
        """
        try:
            file = open("camera_info.ini", "r")
            fx = int(file.readline().split(":")[1])
            fy = int(file.readline().split(":")[1])
            retval = (fx, fy)
        except Exception:
            raise Exception("Could not read from file!")
        finally:
            file.close()
            return retval
        
    def calibrate(self, img_width: int, img_height: int) -> (int, int):
        """
        Takes the width and height of the recognised object in pixels 
        and calculates the focal length using the formula: 
        Focal length = (Size in image x Distance) / Real size
        """
        fx = (img_width * self.distance) / self.width
        fy = (img_height * self.distance) / self.height
        try:
            self.write_to_file(fx, fy)
        except Exception:
            raise Exception("Could not write to file!")
        return (fx, fy)


    


