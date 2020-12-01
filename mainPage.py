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
from dialogMenu import *
from GUI.ui_mainPage import * 

# Author: Philip
# Reviewed by:
# Date: 2020-11-25

"""
This class handles the ui for the main page
"""
class MainPage(QtWidgets.QWidget):
	def __init__(self,mainWindow):
		super().__init__() # call QWidget constructor
		self.mainWindow = mainWindow
		self.ui = Ui_MainPage()
		self.ui.setupUi(self)
		self.installEventFilter(self) # used for event when window is resized
		self.__setActions() 
		self.__initPage() # sets start sizes for widgets in page
		self.cap = None # the captured image
		self.timer = QTimer() # create a timer
		self.timer.timeout.connect(self.__viewCam) # set timer timeout callback function
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

		self.faceDetection = False # boolean to activate/deactivate facedetection
		self.customModelIsActive = False # boolean to activate/deactivate custom model

	# Sets start sizes for widgets in page
	def __initPage(self):
		self.ui.Splitter_frame.setSizes([1000,300])
		self.ui.Splitter_sidePanel.setSizes([1,1])
	
	# Load this page
	def loadPage(self):
		print("load p0")
		self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) # create video capture
		self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 3) # set buffer size
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
	def __viewCam(self):
		# read image in BGR format
		ret, self.image = self.cap.read()

		if self.image is None:
			self.__no_camera_available_popUp()
			return
		
		self.__update()

		self.__convertToQImage()
		self.__resize_camFrame()
		# set image to image label
		self.ui.image_label.setPixmap(self.pix.scaled(self.w, self.h,QtCore.Qt.KeepAspectRatio))
		# save images
		#self.saveImages(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),5)

	# Update funktion for the camera, this function runs in a loop
	def __update(self):
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

		# set contrast
		contrast = self.ui.Slider_contrast.value()/10
		self.ui.Label_contrastValue.setNum(contrast)
		# set brightness
		brightness = self.ui.Slider_brightness.value()
		self.ui.Label_brightnessValue.setNum(brightness)
		self.image = cv2.addWeighted(self.image,contrast,np.zeros(self.image.shape, self.image.dtype),0,brightness)

		if self.faceDetection:
			self.__detectFaces()

		if self.customModelIsActive:
			self.__customModel()

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
		position = (5, 25)
		font = cv2.FONT_HERSHEY_SIMPLEX # font that is used for the fps output
		fontScale = 0.8
		color = (25, 25, 25)
		thickness = 1
		new_frame_time = time.time() # time when we finish processing for this frame
        # fps will be number of frame processed in given time frame 
        # since their will be most of time error of 0.001 second 
        # we will be subtracting it to get more accurate result
		fps = 1/(new_frame_time-self.prev_frame_time)
		self.prev_frame_time = new_frame_time
		fps = int(fps) # converting the fps into integer
		fps = str(fps) # converting the fps into string		
		cv2.putText(self.image, "FPS: " + fps, position, font, fontScale, color, thickness, cv2.LINE_AA) # puting the FPS count on the frame
	
	def __setFrameRateVisibility(self):
		if self.frameRateIsShown:
			self.frameRateIsShown = False
		else:
			self.frameRateIsShown = True

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

	""" Face detection START"""
	def __detectFaces(self):

		#Filters that are searching for different things, in this case 'the front of the face and the eyes'
		face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml')
		eye_cascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
		#Convert to gray
		gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		for(x, y, w, h) in faces:
			color = (255,0,0)
			stroke = 2
			end_cord_x = x + w
			end_cord_y = y + h
			#Draws the rectangle around the face
			face_rectangle = cv2.rectangle(self.image, (x, y), (end_cord_x, end_cord_y), color, stroke)

			font = cv2.FONT_HERSHEY_SIMPLEX
			#Display the text
			cv2.putText(face_rectangle,"FACE",(x, y-10), font, 0.5, (11,255,255), 2, cv2.LINE_AA)

			roi_gray = gray[y:y+h, x:x+w]
			roi_color = self.image[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi_gray)
			for(ex,ey,ew,eh) in eyes:
				#Draws a rectangle within the face and around the eyes
				cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh),(0,255,0), 2)
				#Draws a circle within the face and around the eyes
				#cv2.circle(self.image,(int(x+ex+ew/2),int(y+ey+eh/2)),int(ey/2),(0,255,0),1)
			#Saves a picture of the last face seen when the application is closed
			#img_item = "lastFace.png"
			#cv2.imwrite(img_item, roi_gray)

	def activateFaceDetection(self):
		if self.faceDetection:
			self.faceDetection = False
		else:
			self.faceDetection = True
			
	""" Face detection END """

	""" Custom Model START"""
	# Funktion för att ladda in bilder så det går att testa.
	def __prepare(self):
		IMG_SIZE = 100
		gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		new_array = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))
		return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

	def __customModel(self):
		prediction = self.my_model.predict([self.__prepare()])
		self.__check_categeori(prediction)
	
	def __check_categeori(self,prediction):
		if (int(prediction[0][0]) == 1):
			#print("Car")
			self.ui.Label_object.setText("CAR")
		elif (int(prediction[0][1]) == 1):
			#print("Dog")
			self.ui.Label_object.setText("DOG")
		elif (int(prediction[0][2]) == 1):
			#print("Cat")
			self.ui.Label_object.setText("CAT")
		else:
			#print("Not a Car, Cat or a Dog")
			self.ui.Label_object.setText("Not a Car, Cat or a Dog")
		return
	
	def activateCustomModel(self):
		# Laddar in den tidigare tränade modellen.
		self.my_model = tf.keras.models.load_model('saved_model/car_model')
		if self.customModelIsActive:
			self.customModelIsActive = False
		else:
			self.customModelIsActive = True