import sys
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import numpy as np
import tensorflow as tf
from dialogMenu import *
from GUI.ui_mainPage import * 

# Author: Philip
# Reviewed by:
# Date: 2020-11-25

"""
This class handles the ui for the main page
"""
class MainPage(QtWidgets.QWidget):
	def __init__(self):
		super().__init__() # call QWidget constructor
		self.ui = Ui_MainPage()
		self.ui.setupUi(self)
		self.installEventFilter(self) # used for event when window is resized
		self.setActions() 
		self.initPage() # sets start sizes for widgets in page
		self.cap = None # the captured image
		self.timer = QTimer() # create a timer
		self.timer.timeout.connect(self.viewCam) # set timer timeout callback function
		self.pix = None # the pixMap used to set the image on a QLabel
		self.w = 0 # set the width of the QLabel 
		self.h = 0 # set the height of the QLabel
		self.cameraFrameIsActive = True
		self.sidePanelIsActive = True
		self.settingsIsActive = True
		self.outputIsActive = True
		self.imageColor = "RGB" # start color of image
		# Start values:
		self.START_BRIGHTNESS = 0
		self.START_CONTRAST = 10

	# Sets start sizes for widgets in page
	def initPage(self):
		self.ui.Splitter_frame.setSizes([1000,300])
		self.ui.Splitter_sidePanel.setSizes([1,1])
	
	# Load this page
	def loadPage(self):
		print("load p0")
		self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) # create video capture
		self.timer.start(20) # start timer
		self.ui.Button_startCam.setText("Stop") # update Button_startCam text
	
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
			self.resize_camFrame()
		return super().eventFilter(obj, event)

	# Set actions for QWidgets
	def setActions(self):
		# Set action for start button
		self.ui.Button_startCam.clicked.connect(self.controlTimer)
		# Set action for radioButtons
		self.ui.radioButton_RGB.toggled.connect(lambda: self.changeImageAppearance("RGB"))
		self.ui.radioButton_Grayscale.toggled.connect(lambda: self.changeImageAppearance("Grayscale"))
		self.ui.radioButton_Edged.toggled.connect(lambda: self.changeImageAppearance("Edged"))
		# Set actions for radioButtons
		self.ui.radioButton_res_0.toggled.connect(lambda: self.setResolution(160,120))
		self.ui.radioButton_res_1.toggled.connect(lambda: self.setResolution(320,240))
		self.ui.radioButton_res_2.toggled.connect(lambda: self.setResolution(640,480))
		self.ui.radioButton_res_3.toggled.connect(lambda: self.setResolution(800,600))
		self.ui.radioButton_res_4.toggled.connect(lambda: self.setResolution(1280,720))
		# Set action for reset button
		self.ui.Button_reset.clicked.connect(self.resetSettingValues)
	
	# Resizes the cam frame
	def resize_camFrame(self):
		if self.pix is not None:
			self.w = self.ui.image_label.width()
			self.h = self.ui.image_label.height()
	
	# Sets all ui-objects to default values
	def resetSettingValues(self):
		self.ui.Slider_brightness.setValue(self.START_BRIGHTNESS)
		self.ui.Label_brightnessValue.setNum(self.START_CONTRAST)
		self.ui.Slider_contrast.setValue(self.start_contrast)
		self.ui.Label_contrastValue.setNum(self.start_contrast)
		self.ui.radioButton_RGB.toggle()

	# Sets the resolution of the webcam
	def setResolution(self,width,height):
		self.cap.set(3,width)
		self.cap.set(4,height)

	# Start/stop timer
	def controlTimer(self):
		# if timer is stopped
		if not self.timer.isActive():
			self.loadPage()
		# if timer is started
		else:
			self.closePage()

	""" Main camera loop START"""
	# View camera (loop)
	def viewCam(self):
		# read image in BGR format
		ret, self.image = self.cap.read()

		if self.image is None:
			self.no_camera_available_popUp()
			return
		
		self.update()

		# set contrast
		contrast = self.ui.Slider_contrast.value()/10
		self.ui.Label_contrastValue.setNum(contrast)
		# set brightness
		brightness = self.ui.Slider_brightness.value()
		self.ui.Label_brightnessValue.setNum(brightness)
		self.image = cv2.addWeighted(self.image,contrast,np.zeros(self.image.shape, self.image.dtype),0,brightness)

		self.convertToQImage()
		self.resize_camFrame()
		# set image to image label
		self.ui.image_label.setPixmap(self.pix.scaled(self.w, self.h,QtCore.Qt.KeepAspectRatio))
		# save images
		#self.saveImages(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),5)

	# Update funktion for the camera, this function runs in a loop
	def update(self):
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
	
	# Converts the image to a QImage that is used to set the image on the QLabel
	def convertToQImage(self):
		# calculate step
		step = self.channel * self.width
		# create QImage from image
		qImg = QImage(self.image.data, self.width, self.height, step, self.qiFormat)
		self.pix = QPixmap.fromImage(qImg)

	""" Main camera loop END"""

	# Saves images
	def saveImages(self, img, amount):
		for i in range(amount):
			cv2.imwrite("image-" + str(i) + ".jpg", img)
	
	# Function to change the image appearance
	def changeImageAppearance(self, appearance):
			self.imageColor = appearance

	# Set camera frame visibility
	def setCameraFrame(self, wantToOpen):
		if wantToOpen:
			self.ui.Splitter_frame.setSizes([16777215,300])
			self.ui.cameraFrame.setVisible(True)
		else: 
			self.ui.Splitter_frame.setSizes([0,16777215])
			self.ui.cameraFrame.setVisible(False)
	
	# Set side panel visibility
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

	# Set settings panel visibility
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
	
	# Set output panel visibility
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

	# Show no camera available pop
	def no_camera_available_popUp(self):
		dialogMenu = DialogMenu()
		dialogMenu.setTitle("No available camera!")
		dialogMenu.setInformationText("Cannot find an available camera, make sure it's plugged in.")
		dialogMenu.setTopButtonText("Retry")
		dialogMenu.setBottomButtonText("Skip")
		dialogMenu.ui.PushButton_top.clicked.connect(lambda: self.closePage())
		dialogMenu.ui.PushButton_top.clicked.connect(lambda: self.loadPage())
		dialogMenu.ui.PushButton_top.clicked.connect(dialogMenu.close)
		dialogMenu.ui.PushButton_bottom.clicked.connect(lambda: self.closePage())
		dialogMenu.ui.PushButton_bottom.clicked.connect(dialogMenu.close)
		dialogMenu.exec_()