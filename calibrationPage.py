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
from GUI.ui_calibrationPage import * 
from CameraCalibration import * 
from threading import Thread
from pathlib import Path
from dialogMenu import *

# Author: Philip
# Authot: William
# Reviewed by:
# Date: 2020-11-25

class CalibrationPage(QtWidgets.QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.ui = Ui_CalibrationPage()
        self.ui.setupUi(self)
        self.timer = QTimer() # create a timer
        self.timer.timeout.connect(self.viewCam) # set timer timeout callback function
        self.initLineEdits() # initialize the line edits
        self.ui.stackedWidget.setCurrentIndex(0) # start with page 0 (insert values page)
        self.setActions() # set actions
        # checkerboard values
        self.objectWidth = 0
        self.objectHeight = 0
        self.squareWidth = 0
        self.objectDistance = 0.0

        self.calibrating = False # boolean that is true while calibrating
        self.capture = False # boolean that is true when the button capture is pressed

        self.cap = None # the captured image

    # Load this page
    def loadPage(self):
        print("load p1")
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.timer.start(0)

    # Close this page
    def closePage(self):
        if self.timer.isActive:
            print("close p1")
            # stop timer
            self.timer.stop()
            if self.cap is not None:
                # release video capture
                self.cap.release()
            self.reset()
    
    # Reset page values
    def reset(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.Label_TakenCaptures.setNum(0)
        self.ui.Label_Information.clear()
        self.ui.lineEdit_Width.clear()
        self.ui.lineEdit_Height.clear()
        self.ui.lineEdit_Distance.clear()
        self.ui.lineEdit_SquareCorners.clear()
        self.ui.lineEdit_SquareWidth.clear()

    """ Main camera loop START"""
    def viewCam(self):
         # read image in BGR format
        ret, self.image = self.cap.read()
        if self.image is None:
            self.no_camera_available_popUp()
            return
        self.update()
        self.convertToQImage()
        self.resize_camFrame()
        # set image to image label
        self.ui.image_label.setPixmap(self.pix.scaled(self.w, self.h,QtCore.Qt.KeepAspectRatio))

    # Update funktion for the camera, this function runs in a loop
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
                    self.saveFile()
                    self.ui.Label_Information.setText("<strong>Calibration</strong> was successful, return to main screen by clicking on <strong>Navigation -> Main Screen</strong> in the menubar")
    
    # Converts the image to a QImage that is used to set the image on the QLabel              
    def convertToQImage(self):
        # calculate step
        step = self.channel * self.width
        # create QImage from image
        qImg = QImage(self.image.data, self.width, self.height, step, self.qiFormat)
        self.pix = QPixmap.fromImage(qImg)

    """ Main camera loop END"""
    
    # Resizes the cam frame
    def resize_camFrame(self):
        if self.pix is not None:
            self.w = self.ui.image_label.width()
            self.h = self.ui.image_label.height()

    # Sets validators on the line edits
    def initLineEdits(self):
        self.ui.lineEdit_Width.setValidator(QDoubleValidator(0,1000,3,self)) # mm double
        self.ui.lineEdit_Height.setValidator(QDoubleValidator(0,1000,3,self)) # mm double
        self.ui.lineEdit_SquareWidth.setValidator(QIntValidator(0,1000,self)) # mm int
        self.ui.lineEdit_Distance.setValidator(QDoubleValidator(0,100,3,self)) # m double
    
    # Sets actions on the buttons
    def setActions(self):
        self.ui.Button_Calibrate.clicked.connect(self.startCalibration)
        self.ui.Button_Capture.clicked.connect(self.captureAction)

    # Sets capture boolean to true
    def captureAction(self):
        self.capture = True
    
    # Checks and sets the inputvalues, all values must be numbers
    def checkValues(self):
        try:
            self.width = float(self.ui.lineEdit_Width.text().replace(',','.'))
            self.height = float(self.ui.lineEdit_Height.text().replace(',','.'))
            self.patternSquareSize = int(self.ui.lineEdit_SquareWidth.text())
            self.distance = float(self.ui.lineEdit_Distance.text().replace(',','.'))
            return True
        except:
            print("ERROR not a number somewhere")
            return False

    # Starts the calibration if all values are numbers
    def startCalibration(self):
        if self.checkValues():
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
            self.objp = self.objp * self.patternSquareSize

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

    # Saves the values needed to the camera_info.ini file, if it already exists the function overwrites, else it creates a new file and writes the information to that file
    def saveFile(self):
        fx = self.cameraMatrix[0][0]
        fy = self.cameraMatrix[1][1]
        if Path("camera_info.ini").is_file():
            print("FILEN FINNS!!")
            try:
                myFile = open("camera_info.ini","w")
                myFile.write("fx:" + str(fx) + "\nfy:" + str(fy))
            except Exception:
                raise Exception("Could not write to file!")
            finally:
                myFile.close()
        else:
            try:
                myFile = open("camera_info.ini","x")
                myFile.write("fx:" + str(fx) + "\nfy:" + str(fy))
            except Exception:
                raise Exception("Could not write to file!")
            finally:
                myFile.close()
    
    # Show no camera available popup
    def no_camera_available_popUp(self):
        dialogMenu = DialogMenu(self.mainWindow)
        dialogMenu.setTitle("<strong>No available camera!</strong>")
        dialogMenu.setInformationText("Cannot find an available camera, make sure it's plugged in.")
        dialogMenu.setTopButtonText("Retry calibration")
        dialogMenu.setBottomButtonText("Skip")
        dialogMenu.setFixedHeight(320)
        dialogMenu.centerOnWindow()
        dialogMenu.ui.PushButton_top.clicked.connect(lambda: self.closePage())
        dialogMenu.ui.PushButton_top.clicked.connect(lambda: self.loadPage())
        dialogMenu.ui.PushButton_top.clicked.connect(dialogMenu.close)
        dialogMenu.ui.PushButton_bottom.clicked.connect(lambda: self.closePage())
        dialogMenu.ui.PushButton_bottom.clicked.connect(dialogMenu.close)
        dialogMenu.exec_()
