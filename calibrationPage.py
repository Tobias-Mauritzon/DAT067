import cv2
import time
import numpy as np
import PyQt5
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIntValidator
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QTimer
from pathlib import Path
from GUI.ui_calibrationPage import * 
from dialogMenu import *
from sys import platform

# Author: Philip
# Author: William
# Reviewed by: Andreas
# Date: 2020-12-01

"""
CalibrationPage inherits QWidget and creates a calibration page with the ui(ui_calibrationPage.py) made with Qt designer.
The class creates a page with all the functions for the calibraiton.
"""
class CalibrationPage(QtWidgets.QWidget):
	def __init__(self, mainWindow):
		super().__init__()
		self.mainWindow = mainWindow # the main window of the application
		self.ui = Ui_CalibrationPage() # create ui
		self.ui.setupUi(self) # call setup function in ui
		self.timer = QTimer() # create a timer
		self.timer.timeout.connect(self.__update) # set timer timeout callback function
		self.__initLineEdits() # initialize the line edits
		self.ui.stackedWidget.setCurrentIndex(0) # start with page 0 (insert values page)
		self.ui.splitter.setSizes([1000,300]) # set start position for sidepanel
		self.__setActions() # set actions
		# checkerboard values
		self.objectWidth = 0
		self.objectHeight = 0
		self.squareWidth = 0
		self.objectDistance = 0.0

		self.calibrating = False # boolean that is true while calibrating
		self.cap = None # the captured image

	# Load this page
	def loadPage(self):
		if platform == "win32":
			self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) # create video fast with windows
		else:
			self.cap = cv2.VideoCapture(0) # create video capture for Raspberry and other OS:s
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
		self.calibrating = False
		self.ui.stackedWidget.setCurrentIndex(0)
		self.ui.Label_TakenCaptures.setNum(0)
		self.ui.Label_Information.clear()
		self.ui.lineEdit_Width.clear()
		self.ui.lineEdit_Height.clear()
		self.ui.lineEdit_Distance.clear()
		self.ui.lineEdit_SquareWidth.clear()

	"""Main camera loop START"""      
	# Update function for the camera, this function runs in a loop
	def __update(self):
		# read image in BGR format
		success, self.image = self.cap.read()

		# if no image was received, show popup
		if not success:
			self.__no_camera_available_popUp()
			return

		self.__convert2Grayscale() # convert the image to grayscale format
		if self.calibrating:
			self.__calibrate() # calibrate if calibration is active
		self.__convertToQImage() # convert to QImage that can be used on the QLabel
		self.__resize_camFrame() # resize the image

		self.ui.image_label.setPixmap(self.pix.scaled(self.w, self.h,QtCore.Qt.KeepAspectRatio)) # set image to image label

	# Converts the image to grayscale format
	def __convert2Grayscale(self):
		self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
		self.height, self.width = self.image.shape
		self.channel = 1
		self.qiFormat = QImage.Format_Grayscale8

	def __calibrate(self):
		# convert to rgb in order to get the colored lines
		self.image = cv2.cvtColor(self.image,cv2.COLOR_GRAY2RGB)
		self.height, self.width, self.channel = self.image.shape
		self.qiFormat = QImage.Format_RGB888
	
		self.foundChessboardCorners, self.corners = cv2.findChessboardCorners(self.image, (7,6),None) # find the chess board corners
		cv2.drawChessboardCorners(self.image, (7,6), self.corners,self.foundChessboardCorners) # draw and display the corners

	# Converts the image to a QImage that is used to set the image on the QLabel              
	def __convertToQImage(self):
		# calculate step
		step = self.channel * self.width
		# create QImage from image
		qImg = QImage(self.image.data, self.width, self.height, step, self.qiFormat)
		self.pix = QPixmap.fromImage(qImg)

	""" Main camera loop END"""
	
	# Resizes the cam frame
	def __resize_camFrame(self):
		if self.pix is not None:
			self.w = self.ui.image_label.width()
			self.h = self.ui.image_label.height()

	# Sets validators on the line edits
	def __initLineEdits(self):
		self.ui.lineEdit_Width.setValidator(QDoubleValidator(0,1000,3,self)) # mm double
		self.ui.lineEdit_Height.setValidator(QDoubleValidator(0,1000,3,self)) # mm double
		self.ui.lineEdit_SquareWidth.setValidator(QIntValidator(0,1000,self)) # mm int
		self.ui.lineEdit_Distance.setValidator(QDoubleValidator(0,100,3,self)) # m double
	
	# Sets actions on the buttons
	def __setActions(self):
		self.ui.Button_Calibrate.clicked.connect(self.__startCalibration)
		self.ui.Button_Capture.clicked.connect(self.__captureAction)
		self.ui.Button_calibration_help.clicked.connect(self.__calibrationHelp)

	# This function is called each time the user press the calirate button.
	# If the program has found chessboard corners, information is stored.
	# When the user has captured enough images, the calibration stops and the calibration information is stored in a file.
	def __captureAction(self):
		if self.foundChessboardCorners:
			self.imageCounter += 1 # add one to the captured image counter
			self.ui.Label_TakenCaptures.setNum(self.imageCounter) # show the amount of captured images
			self.objpoints.append(self.objp) # store object points
			gray = cv2.cvtColor(self.image,cv2.COLOR_RGB2GRAY) # convert to grayscale
			cv2.cornerSubPix(gray,self.corners,(11,11),(-1,-1),self.criteria)
			self.imgpoints.append(self.corners)
			
			# when the user has captured enough images, stop calibration and save the calibration info in a file
			if self.imageCounter >= self.REQUIRED_IMAGE_AMOUNT:
				self.calibrating = False
				ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, gray.shape[::-1],None,None)
				self.cameraMatrix = cameraMatrix
				self.__saveFile()
				self.__openFinnishedpopup()
				
	
	# Checks and sets the inputvalues, all values must be numbers
	def __checkValues(self):
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
	def __startCalibration(self):
		if self.__checkValues():
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
			self.ui.stackedWidget.setCurrentIndex(1)
			self.calibrating = True

	# Saves the values needed to the camera_info.ini file, if it already exists the function overwrites, else it creates a new file and writes the information to that file
	def __saveFile(self):
		fx = self.cameraMatrix[0][0]
		fy = self.cameraMatrix[1][1]
		if Path("camera_info.ini").is_file():
			try:
				myFile = open("camera_info.ini","w") # overwrite to existing file
				myFile.write("fx:" + str(fx) + "\nfy:" + str(fy))
			except Exception:
				raise Exception("Could not write to file!")
			finally:
				myFile.close()
		else:
			try:
				myFile = open("camera_info.ini","x") # create file and write to it
				myFile.write("fx:" + str(fx) + "\nfy:" + str(fy))
			except Exception:
				raise Exception("Could not write to file!")
			finally:
				myFile.close()
	
	# Show no camera available popup
	def __no_camera_available_popUp(self):
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
	
	def __calibrationHelp(self):
		dialogMenu = DialogMenu(self.mainWindow)
		dialogMenu.setTitle("<strong>Help</strong>")
		dialogMenu.setImage('CalibrationHelp.PNG')
		dialogMenu.setTopButtonText("Ok")
		dialogMenu.ui.PushButton_bottom.setVisible(False)
		dialogMenu.setFixedHeight(600)
		dialogMenu.setFixedWidth(700)
		dialogMenu.centerOnWindow()
		dialogMenu.ui.PushButton_top.clicked.connect(dialogMenu.close)
		dialogMenu.exec_()

	
	# Show finnished calibration popup
	def __openFinnishedpopup(self):
		dialogMenu = DialogMenu(self.mainWindow)
		dialogMenu.setTitle("<strong>Calibration was successful!</strong>")
		dialogMenu.disableInformationText()
		dialogMenu.setTopButtonText("Return")
		dialogMenu.ui.PushButton_bottom.setVisible(False)
		dialogMenu.setFixedHeight(200)
		dialogMenu.centerOnWindow()
		dialogMenu.ui.PushButton_top.clicked.connect(lambda: self.mainWindow.openPage(0))
		dialogMenu.ui.PushButton_top.clicked.connect(dialogMenu.close)
		dialogMenu.exec_()
