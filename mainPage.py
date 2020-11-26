import sys
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import numpy as np
import tensorflow as tf
from GUI.ui_mainPage import * 

# Author: Philip
# Reviewed by:
# Date: 2020-11-25

class MainPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__() # call QWidget constructor
        self.ui = Ui_MainPage()
        self.ui.setupUi(self)
        self.installEventFilter(self)
        self.setActions() #set actions for QWidgets
        self.initPage() # sets start sizes for widgets in page
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
        self.start_brightness = 0
        self.start_contrast = 10

    def initPage(self):
        self.ui.Splitter_frame.setSizes([1000,300])
        self.ui.Splitter_sidePanel.setSizes([1,1])
    
     # event for when the window is resized
    def eventFilter(self, obj, event):
        if (event.type() == QtCore.QEvent.Resize):
            self.resize_camFrame()
        return super().eventFilter(obj, event)

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
    
    # resizes the cam frame
    def resize_camFrame(self):
        if self.pix is not None:
            self.w = self.ui.image_label.width()
            self.h = self.ui.image_label.height()
    
     # Sets all ui-objects to default values
    def resetSettingValues(self):
        self.ui.Slider_brightness.setValue(self.start_brightness)
        self.ui.Label_brightnessValue.setNum(self.start_brightness)
        self.ui.Slider_contrast.setValue(self.start_contrast)
        self.ui.Label_contrastValue.setNum(self.start_contrast)
        self.ui.radioButton_RGB.toggle()

    # Function that sets the resolution of the webcam
    def setResolution(self,width,height):
        self.cap.set(3,width)
        self.cap.set(4,height)

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) # create video capture
            self.timer.start(20) # start timer
            self.ui.Button_startCam.setText("Stop") # update Button_startCam text
        # if timer is started
        else:
            self.timer.stop() # stop timer
            self.cap.release() # release video capture
            self.ui.Button_startCam.setText("Start") # update Button_startCam text

    # view camera (loop)
    def viewCam(self):
        # read image in BGR format
        ret, self.image = self.cap.read()

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
    
    def convertToQImage(self):
        # calculate step
        step = self.channel * self.width
        # create QImage from image
        qImg = QImage(self.image.data, self.width, self.height, step, self.qiFormat)
        self.pix = QPixmap.fromImage(qImg)
    
    # writes the image to _pycache_ folder
    def saveImages(self, img, amount):
        for i in range(amount):
            cv2.imwrite("image-" + str(i) + ".jpg", img)
    
    # Function to change the image appearance
    def changeImageAppearance(self, appearance):
            self.imageColor = appearance

    def setCameraFrame(self, wantToOpen):
        if wantToOpen:
            self.ui.Splitter_frame.setSizes([16777215,300])
            self.ui.cameraFrame.setVisible(True)
        else: 
            self.ui.Splitter_frame.setSizes([0,16777215])
            self.ui.cameraFrame.setVisible(False)
    
    def setSidePanel(self, wantToOpen):
        if wantToOpen:
            self.ui.Splitter_frame.setSizes([16777215,300])
            self.ui.Splitter_sidePanel.setSizes([16777215,16777215])
            self.ui.sidePanel.setVisible(True)
        else: 
            self.ui.Splitter_frame.setSizes([16777215,0])
            self.ui.sidePanel.setVisible(False)

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

    
        

    