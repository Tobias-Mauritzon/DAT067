import sys
import cv2
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from dialogMenu import *
from GUI.ui_mainPage import *
from sys import platform

#Models:
from TensorFlow_Custom_Model import *
from HaarCascade_Model import *
from Yolov3_Model import *


# Author: Philip
# Reviewed by: Andreas
# Date: 2020-12-01

# Author: Joachim, William
# Reviewed by: Tobias Mauritzon
# Date: 2020-12-04

"""
MainPage inherits QWidget and creates the main page with the ui(ui_mainPage.py) made with Qt designer.
The class creates a page with all the object detection functions.
OBS! IF YOU ARE ON A RASPBERRY PI, YOU NEED TO REMOVE cv2.CAP_DSHOW in mainPage row 85!
OBS! IF YOU WANT TO START WITH THE LOADING SCREEN CHANGE timer start time TO 100 in loadingwindow row 42.
"""
class MainPage(QtWidgets.QWidget):
	def __init__(self,mainWindow):
		super().__init__() # call QWidget constructor
		self.mainWindow = mainWindow # the main window of the application
		self.ui = Ui_MainPage() # create ui
		self.ui.setupUi(self) # call setup funktion in ui
		self.installEventFilter(self) # used for event when window is resized
		self.__setActions() # set actions
		self.__initPage() # sets start sizes for widgets in page
		self.cap = None # the captured image
		self.timer = QTimer() # create a timer
		self.timer.timeout.connect(self.__update) # set timer timeout callback function
		self.pix = None # the pixMap used to set the image on a QLabel
		self.w = 0 # set the width of the QLabel
		self.h = 0 # set the height of the QLabel
		self.cameraFrameIsActive = True
		self.sidePanelIsActive = True
		self.settingsIsActive = True
		self.outputIsActive = True
		self.imageColor = "RGB" # start color of image
		self.frameRateIsShown = False
		self.prev_frame_time = 0
		# Start values:
		self.START_BRIGHTNESS = 0
		self.START_CONTRAST = 10
		self.capSize = (640,480)

		self.fps = 0
		self.fpsInc = 0
		self.fps_color = (0, 255, 127)

		#Models:
		self.customTensorFlowModel = None
		#Models activation booleans:
		self.usingHaarCascade_Cars = False # boolean to activate/deactivate Haar Cascade Cars
		self.YoloIsActive = False # boolean to activate/deactivate Yolo
		self.customModelIsActive = False # boolean to activate/deactivate custom model

	# Sets start sizes for widgets in page
	def __initPage(self):
		self.ui.Splitter_frame.setSizes([1000,300])
		self.ui.Splitter_sidePanel.setSizes([1,1])
		self.ui.label_HC_Cars_ScaleFactor.setNum(self.ui.horizontalSlider_HC_Cars_ScaleFactor.value()/100)
		self.ui.label_HC_Cars_MinNeighbors.setNum(self.ui.horizontalSlider_HC_Cars_MinNeighbors.value())
		self.ui.label_HC_LicencePlates_ScaleFactor.setNum(self.ui.horizontalSlider_HC_LicencePlates_ScaleFactor.value()/100)
		self.ui.label_HC_LicencePlates_MinNeighbors.setNum(self.ui.horizontalSlider_HC_LicencePlates_MinNeighbors.value())

	# Load this page
	def loadPage(self):
		if platform == "win32":
			self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) # create video fast with windows
		else:
			self.cap = cv2.VideoCapture(0) # create video capture for Raspberry and other OS:s
		self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 3) # set buffer size
		self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
		self.cap.set(cv2.CAP_PROP_FPS, 30) # set fps
		self.timer.start(20) # start timer
		self.ui.Button_startCam.setText("Stop") # update Button_startCam text
		self.cap.set(3,self.capSize[0])
		self.cap.set(4,self.capSize[1])

	# Close this page
	def closePage(self):
		if self.timer.isActive:
			print("close p0")
			# stop timer
			self.timer.stop()
			if self.cap is not None:
				# release video capture
				self.cap.release()
				self.ui.Button_startCam.setText("Start") # update Button_startCam text

	# Event for when the window is resized
	def eventFilter(self, obj, event):
		if (event.type() == QtCore.QEvent.Resize):
			self.__resize_camFrame()
		return super().eventFilter(obj, event)

	# Set actions for QWidgets
	def __setActions(self):
		# Set action for start button
		self.ui.Button_startCam.clicked.connect(self.__controlTimer)
		# Set action for radioButtons
		self.ui.radioButton_RGB.toggled.connect(lambda: self.__changeImageAppearance("RGB"))
		self.ui.radioButton_Grayscale.toggled.connect(lambda: self.__changeImageAppearance("Grayscale"))
		self.ui.radioButton_Edged.toggled.connect(lambda: self.__changeImageAppearance("Edged"))
		# Set actions for radioButtons
		self.ui.radioButton_showFrameRate.toggled.connect(self.__setFrameRateVisibility)
		self.ui.radioButton_res_0.toggled.connect(lambda: self.__setResolution(160,120))
		self.ui.radioButton_res_1.toggled.connect(lambda: self.__setResolution(320,240))
		self.ui.radioButton_res_2.toggled.connect(lambda: self.__setResolution(640,480))
		self.ui.radioButton_res_3.toggled.connect(lambda: self.__setResolution(800,600))
		self.ui.radioButton_res_4.toggled.connect(lambda: self.__setResolution(1280,720))
		# Set action for reset button
		self.ui.Button_reset.clicked.connect(self.__resetSettingValues)
		self.ui.Button_HC_Cars_Reset.clicked.connect(lambda: self.__reset_HC_Values(0))
		self.ui.Button_HC_LicencePlates_Reset.clicked.connect(lambda: self.__reset_HC_Values(1))

		#MODELS SETTINGS
		# Cars
		self.ui.horizontalSlider_HC_Cars_ScaleFactor.valueChanged.connect(lambda: self.HaarCascade_Cars_Model.setScaleFactor(self.ui.horizontalSlider_HC_Cars_ScaleFactor.value()/100,0))
		self.ui.horizontalSlider_HC_Cars_ScaleFactor.valueChanged.connect(lambda: self.ui.label_HC_Cars_ScaleFactor.setNum(self.ui.horizontalSlider_HC_Cars_ScaleFactor.value()/100))
		self.ui.horizontalSlider_HC_Cars_MinNeighbors.valueChanged.connect(lambda: self.HaarCascade_Cars_Model.setMinNeighbors(self.ui.horizontalSlider_HC_Cars_MinNeighbors.value(),0))
		self.ui.horizontalSlider_HC_Cars_MinNeighbors.valueChanged.connect(lambda: self.ui.label_HC_Cars_MinNeighbors.setNum(self.ui.horizontalSlider_HC_Cars_MinNeighbors.value()))
		self.ui.horizontalSlider_HC_Cars_MinSize.valueChanged.connect(lambda: self.HaarCascade_Cars_Model.setMinsize(self.ui.horizontalSlider_HC_Cars_MinSize.value(),0))
		self.ui.horizontalSlider_HC_Cars_MinSize.valueChanged.connect(lambda: self.ui.label_HC_Cars_MinSize.setNum(self.ui.horizontalSlider_HC_Cars_MinSize.value()))
		# Licence Plates
		self.ui.horizontalSlider_HC_LicencePlates_ScaleFactor.valueChanged.connect(lambda: self.HaarCascade_Cars_Model.setScaleFactor(self.ui.horizontalSlider_HC_LicencePlates_ScaleFactor.value()/100,1))
		self.ui.horizontalSlider_HC_LicencePlates_ScaleFactor.valueChanged.connect(lambda: self.ui.label_HC_LicencePlates_ScaleFactor.setNum(self.ui.horizontalSlider_HC_LicencePlates_ScaleFactor.value()/100))
		self.ui.horizontalSlider_HC_LicencePlates_MinNeighbors.valueChanged.connect(lambda: self.HaarCascade_Cars_Model.setMinNeighbors(self.ui.horizontalSlider_HC_LicencePlates_MinNeighbors.value(),1))
		self.ui.horizontalSlider_HC_LicencePlates_MinNeighbors.valueChanged.connect(lambda: self.ui.label_HC_LicencePlates_MinNeighbors.setNum(self.ui.horizontalSlider_HC_LicencePlates_MinNeighbors.value()))
		self.ui.horizontalSlider_HC_LicencePlates_MinSize.valueChanged.connect(lambda: self.HaarCascade_Cars_Model.setMinsize(self.ui.horizontalSlider_HC_LicencePlates_MinSize.value(),1))
		self.ui.horizontalSlider_HC_LicencePlates_MinSize.valueChanged.connect(lambda: self.ui.label_HC_LicencePlates_MinSize.setNum(self.ui.horizontalSlider_HC_LicencePlates_MinSize.value()))
		self.ui.groupBox_HC_LicencePlates.toggled.connect(lambda: self.HaarCascade_Cars_Model.setDetectPlates())

	# Resizes the cam frame
	def __resize_camFrame(self):
		if self.pix is not None:
			self.w = self.ui.image_label.width()
			self.h = self.ui.image_label.height()

	# Sets all ui-objects to default values
	def __resetSettingValues(self):
		self.ui.Slider_brightness.setValue(self.START_BRIGHTNESS)
		self.ui.Label_brightnessValue.setNum(self.START_CONTRAST)
		self.ui.Slider_contrast.setValue(self.START_CONTRAST)
		self.ui.Label_contrastValue.setNum(self.START_CONTRAST)
		self.ui.radioButton_RGB.toggle()

	# Sets the resolution of the webcam
	def __setResolution(self,width,height):
		self.capSize = (width,height)
		if self.cap is not None:
			self.cap.set(3,width)
			self.cap.set(4,height)

	# Start/stop timer
	def __controlTimer(self):
		# if timer is stopped
		if not self.timer.isActive():
			self.loadPage()
		# if timer is started
		else:
			self.closePage()

	""" Main camera loop START"""
	# View camera (loop)
	def __update(self):
		# read image in BGR format
		success, self.image = self.cap.read()

		# if no image was received, show popup
		if not success:
			self.__no_camera_available_popUp()
			return

		self.__setImageManipulation() # sets the chosen image manipulation
		self.__setContrastAndBrightness() # sets the chosen contrast and brightness
		self.__setObjectDetectionType() # sets the chosen object detection type

		self.__convertToQImage() # convert to QImage that can be used on the QLabel
		self.__resize_camFrame() # resize the image
		self.ui.image_label.setPixmap(self.pix.scaled(self.w, self.h,QtCore.Qt.KeepAspectRatio)) # set image to image label

	# Sets the chosen image manipulation
	def __setImageManipulation(self):
		# convert image to RGB format
		if self.imageColor == "RGB":
			self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
			self.height, self.width, self.channel = self.image.shape
			self.qiFormat = QImage.Format_RGB888
		# convert image to Grayscale format
		elif self.imageColor == "Grayscale":
			self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
			self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
			self.height, self.width = self.image.shape
			self.channel = 1
			self.qiFormat = QImage.Format_Grayscale8
		# convert image to Edged format
		elif self.imageColor == "Edged":
			self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
			gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
			blur = cv2.GaussianBlur(gray,(5,5),0)
			edged = cv2.Canny(blur,35,125)
			self.image = edged
			self.height, self.width = self.image.shape
			self.channel = 1
			self.qiFormat = QImage.Format_Grayscale8

	# Sets the chosen contrast and brightness on the image
	def __setContrastAndBrightness(self):
		# set contrast
		contrast = self.ui.Slider_contrast.value()/10
		self.ui.Label_contrastValue.setNum(contrast)
		# set brightness
		brightness = self.ui.Slider_brightness.value()
		self.ui.Label_brightnessValue.setNum(brightness)
		self.image = cv2.addWeighted(self.image,contrast,np.zeros(self.image.shape, self.image.dtype),0,brightness)

	# Sets the chosen object detection type
	def __setObjectDetectionType(self):
		if self.usingHaarCascade_Cars:
			self.HaarCascade_Cars_Model.findCars(self.image)
		if self.YoloIsActive:
			self.Yolo_model.findObjects(self.image)
		if self.customModelIsActive:
			self.customTensorFlowModel.findObject(self.image)
		if self.frameRateIsShown:
			self.__showFrameRate()

	# Converts the image to a QImage that is used to set the image on the QLabel
	def __convertToQImage(self):
		# calculate step
		step = self.channel * self.width
		# create QImage from image
		qImg = QImage(self.image.data, self.width, self.height, step, self.qiFormat)
		self.pix = QPixmap.fromImage(qImg)

	""" Main camera loop END"""

	# Saves images
	def __saveImages(self, img, amount):
		for i in range(amount):
			cv2.imwrite("image-" + str(i) + ".jpg", img)

	# Function to change the image appearance
	def __changeImageAppearance(self, appearance):
			self.imageColor = appearance

	# Function that displays the frame rate
	def __showFrameRate(self):
		position = (5, 25) # position of the text
		font = cv2.FONT_HERSHEY_SIMPLEX # font that is used for the fps output
		fontScale = 0.8	# the fontscale of the text
		thickness = 1 # the thickness of the text
		new_frame_time = time.time() # time when we finish processing for this frame

		TIME = new_frame_time - self.prev_frame_time # calculate the difference between current time and previous time
		self.fpsInc += 1 # increase the fpsInc variable
		if TIME > 0.2: # fps will update each 0.2 seconds
			self.fps = self.fpsInc/(TIME)
			self.prev_frame_time = new_frame_time
			self.fpsInc = 0
		fps = int(self.fps) # converting the fps into integer
		fps = str(fps) # converting the fps into string
		cv2.putText(self.image, "FPS: " + fps, position, font, fontScale, self.fps_color, thickness, cv2.LINE_AA) # puting the FPS count on the frame

	# Sets the framrate visiblity
	def __setFrameRateVisibility(self):
		if self.frameRateIsShown:
			self.frameRateIsShown = False
		else:
			self.prev_frame_time = time.time()
			self.frameRateIsShown = True

	# Sets camera frame visibility
	def setCameraFrame(self, wantToOpen):
		if wantToOpen:
			self.ui.Splitter_frame.setSizes([16777215,300])
			self.ui.cameraFrame.setVisible(True)
		else:
			self.ui.Splitter_frame.setSizes([0,16777215])
			self.ui.cameraFrame.setVisible(False)

	# Sets side panel visibility
	def setSidePanel(self, wantToOpen):
		if wantToOpen:
			self.ui.Splitter_frame.setSizes([16777215,300])
			self.ui.Splitter_sidePanel.setSizes([16777215,16777215])
			self.ui.Splitter_sidePanel.setSizes([16777215,16777215])
			self.ui.settingsFrame.setVisible(True)
			self.ui.outputFrame.setVisible(True)
			self.ui.sidePanel.setVisible(True)
		else:
			self.ui.Splitter_frame.setSizes([16777215,0])
			self.ui.sidePanel.setVisible(False)

	# Sets settings panel visibility
	def setSettingsPanel(self, wantToOpen, sidePanelIsOpen, outPutPanelIsOpen):
		if wantToOpen and sidePanelIsOpen:
			self.ui.Splitter_sidePanel.setSizes([16777215,16777215])
			self.ui.settingsFrame.setVisible(True)
		elif wantToOpen and not sidePanelIsOpen:
			self.ui.Splitter_frame.setSizes([16777215,300])
			self.ui.sidePanel.setVisible(True)
			self.ui.Splitter_sidePanel.setSizes([16777215,0])
			self.ui.settingsFrame.setVisible(True)
		elif not wantToOpen and sidePanelIsOpen and outPutPanelIsOpen:
			self.ui.Splitter_sidePanel.setSizes([0,16777215])
			self.ui.settingsFrame.setVisible(False)
		elif not wantToOpen and sidePanelIsOpen and not outPutPanelIsOpen:
			self.ui.Splitter_frame.setSizes([16777215,0])
			self.ui.sidePanel.setVisible(False)
			self.ui.settingsFrame.setVisible(False)

	# Sets output panel visibility
	def setOutPutPanel(self, wantToOpen, sidePanelIsOpen, settingsPanelIsOpen):
		if wantToOpen and sidePanelIsOpen:
			self.ui.Splitter_sidePanel.setSizes([16777215,16777215])
			self.ui.outputFrame.setVisible(True)
		elif wantToOpen and not sidePanelIsOpen:
			self.ui.Splitter_frame.setSizes([16777215,300])
			self.ui.sidePanel.setVisible(True)
			self.ui.Splitter_sidePanel.setSizes([0,16777215])
			self.ui.outputFrame.setVisible(True)
		elif not wantToOpen and sidePanelIsOpen and settingsPanelIsOpen:
			self.ui.Splitter_sidePanel.setSizes([16777215,0])
			self.ui.outputFrame.setVisible(False)
		elif not wantToOpen and sidePanelIsOpen and not settingsPanelIsOpen:
			self.ui.Splitter_frame.setSizes([16777215,0])
			self.ui.sidePanel.setVisible(False)
			self.ui.outputFrame.setVisible(False)

	# Shows no camera available pop
	def __no_camera_available_popUp(self):
		dialogMenu = DialogMenu(self.mainWindow)
		dialogMenu.setTitle("<strong>No available camera!</strong>")
		dialogMenu.setInformationText("Cannot find an available camera, make sure it's plugged in.")
		dialogMenu.setTopButtonText("Retry")
		dialogMenu.setBottomButtonText("Skip")
		dialogMenu.setFixedHeight(320)
		dialogMenu.centerOnWindow()
		dialogMenu.ui.PushButton_top.clicked.connect(lambda: self.closePage())
		dialogMenu.ui.PushButton_top.clicked.connect(lambda: self.loadPage())
		dialogMenu.ui.PushButton_top.clicked.connect(dialogMenu.close)
		dialogMenu.ui.PushButton_bottom.clicked.connect(lambda: self.closePage())
		dialogMenu.ui.PushButton_bottom.clicked.connect(dialogMenu.close)
		dialogMenu.exec_()

	""" Haar Cascade detection START"""
	# Activates the Haar cascade object detection and enables haaar cascade settings
	def activateHaarCascade(self, objectName):
		if objectName == "Car":
			if self.usingHaarCascade_Cars:
				self.usingHaarCascade_Cars = False
				self.ui.groupBox_HC_Cars.setEnabled(False)
			else:
				self.HaarCascade_Cars_Model = HaarCascade_Model("Car")
				self.ui.groupBox_HC_Cars.setEnabled(True)
				self.usingHaarCascade_Cars = True

	# Sets the haar cascade values, labels and sliders to default values
	def __reset_HC_Values(self, index):
		if index == 0:
			self.HaarCascade_Cars_Model.resetValues(0)
			self.ui.horizontalSlider_HC_Cars_ScaleFactor.setValue(self.HaarCascade_Cars_Model.scaleFactor_def)
			self.ui.label_HC_Cars_ScaleFactor.setNum(self.HaarCascade_Cars_Model.scaleFactor_def)
			self.ui.horizontalSlider_HC_Cars_MinNeighbors.setValue(self.HaarCascade_Cars_Model.minNeighbors_def)
			self.ui.label_HC_Cars_MinNeighbors.setNum(self.HaarCascade_Cars_Model.minNeighbors_def)
			self.ui.horizontalSlider_HC_Cars_MinSize.setValue(self.HaarCascade_Cars_Model.minSize_def)
			self.ui.label_HC_Cars_MinSize.setNum(self.HaarCascade_Cars_Model.minSize_def)
		elif index == 1:
			self.HaarCascade_Cars_Model.resetValues(1)
			self.ui.horizontalSlider_HC_LicencePlates_ScaleFactor.setValue(self.HaarCascade_Cars_Model.scaleFactor_def)
			self.ui.label_HC_LicencePlates_ScaleFactor.setNum(self.HaarCascade_Cars_Model.scaleFactor_def)
			self.ui.horizontalSlider_HC_LicencePlates_MinNeighbors.setValue(self.HaarCascade_Cars_Model.minNeighbors_def)
			self.ui.label_HC_LicencePlates_MinNeighbors.setNum(self.HaarCascade_Cars_Model.minNeighbors_def)
			self.ui.horizontalSlider_HC_LicencePlates_MinSize.setValue(self.HaarCascade_Cars_Model.minSize_def)
			self.ui.label_HC_LicencePlates_MinSize.setNum(self.HaarCascade_Cars_Model.minSize_def)

	"""Haar Cascade detection END"""

	"""YOLO detection START"""
	def activateYOLO(self):
		if self.YoloIsActive:
			self.YoloIsActive = False
		else:
			self.Yolo_model = Yolo_Model()
			self.YoloIsActive = True

	"""YOLO detection END"""

	""" Custom TensorFlow Model START"""
	# Activates the custom tensorFlow model
	def activateCustomModel(self):
		# Loads the custom trained model.
		print("LOADING CUSTOM TENSORFLOW MODEL")
		#self.my_model = tf.keras.models.load_model("pretrained_car_localization")
		self.customTensorFlowModel = TensorFlow_Custom_Model(0)
		if self.customModelIsActive:
			self.customModelIsActive = False
		else:
			self.customModelIsActive = True
