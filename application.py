import sys
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
import numpy as np
from ui_mainWindow import *
from CameraCalibration import *
from mainPage import * 
from calibrationPage import *
import tensorflow as tf

# Author: Philip
# Reviewed by:
# Date: 2020-11-25

# MainWindow inherits QMainWindow and creates a window with the ui(ui_mainWindow.py) made with Qt designer
# Notice that a "page" is reffered to as a QWidget that is used on the MainWindow's stack widget.
class MainWindow(QtWidgets.QMainWindow):
 
    # class constructor
    def __init__(self,windowName):
        # call QWidget constructor
        super().__init__()

        # self.setWindowIcon(QtGui.QIcon('frame_icon.png'))
        # set window name and size
        self.setWindowTitle(windowName)
        self.resize(1200,800)

        # create mainwindow ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # initializes the pages
        self.initPages()
        # current page
        self.currentPage = 0

        # set actions for QWidgets
        self.setActions()

        # instantiate event filter, used for "window resize-event"
        self.installEventFilter(self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)

        # the pixMap used to set the image on a QLabel
        self.pix = None
        # the width and height of the QLabel 
        self.w = 0
        self.h = 0
        
        # Booleans for page 0:
        self.cameraFrameIsActive = True
        self.sidePanelIsActive = True
        self.settingsIsActive = True
        self.outputIsActive = True

        # start color of image
        self.imageColor = "RGB"

        # Start values:
        self.start_brightness = 0
        self.start_contrast = 10

        # Set start page
        self.ui.stackedWidget.setCurrentIndex(0)

        # If the calibrationfile does not exist, show calibration dialog menu 
        #if not Path("camera_info.ini").is_file():
          #  self.calibrate_popUp()

    # Funktion that initiazies the pages
    def initPages(self):
        # PAGE 0:
        self.mainPage = Ui_MainPage()
        self.mainPage.setupUi(self.mainPage)
        self.ui.stackedWidget.addWidget(self.mainPage)
        self.mainPage.Splitter_frame.setSizes([1000,300])
        self.mainPage.Splitter_sidePanel.setSizes([1,1])

        # PAGE 1:
        self.calibrationPage = Ui_CalibrationPage()
        self.calibrationPage.setupUi(self.calibrationPage)
        self.ui.stackedWidget.addWidget(self.calibrationPage)

    # Funktion that opens a specific page
    def openPage(self,pageIndex):
        if pageIndex == 0:
            self.ui.menuView.menuAction().setVisible(True)
            self.ui.menuCalibrate.menuAction().setVisible(True)
            self.ui.stackedWidget.setCurrentIndex(0)
            self.currentPage = 0
        elif pageIndex == 1:
            self.ui.menuView.menuAction().setVisible(False)
            self.ui.menuCalibrate.menuAction().setVisible(False)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.controlTimer() #start videocap
            self.currentPage = 1

    # resizes the cam frame
    def resize_camFrame(self):
        if self.pix is not None and self.currentPage == 0:
            self.w = self.mainPage.image_label.width()
            self.h = self.mainPage.image_label.height()
            self.mainPage.image_label.setPixmap(self.pix.scaled(self.w, self.h,QtCore.Qt.KeepAspectRatio))
        elif self.pix is not None and self.currentPage == 1:
            self.w = self.calibrationPage.image_label.width()
            self.h = self.calibrationPage.image_label.height()
            self.calibrationPage.image_label.setPixmap(self.pix.scaled(self.w, self.h,QtCore.Qt.KeepAspectRatio))

    # event for when the window is resized
    def eventFilter(self, obj, event):
        if (event.type() == QtCore.QEvent.Resize):
            self.resize_camFrame()
        return super().eventFilter(obj, event)
    
    # Sets actions for GUI-objects
    def setActions(self):
        # Set action for topBar menu actions
        self.ui.action_Camera.triggered.connect(self.showCameraFrame)
        self.ui.action_SidePanel.triggered.connect(self.showSidePanel)
        # Set action for sidePanel menus
        self.ui.action_Settings.triggered.connect(self.showSettings)
        self.ui.action_Output.triggered.connect(self.showOutput)

        # Set action for start button
        self.mainPage.Button_startCam.clicked.connect(self.controlTimer)
        # Set action for radioButtons
        self.mainPage.radioButton_RGB.toggled.connect(lambda: self.changeImageAppearance("RGB"))
        self.mainPage.radioButton_Grayscale.toggled.connect(lambda: self.changeImageAppearance("Grayscale"))
        self.mainPage.radioButton_Edged.toggled.connect(lambda: self.changeImageAppearance("Edged"))
        # Set actions for radioButtons
        self.mainPage.radioButton_res_0.toggled.connect(lambda: self.setResolution(160,120))
        self.mainPage.radioButton_res_1.toggled.connect(lambda: self.setResolution(320,240))
        self.mainPage.radioButton_res_2.toggled.connect(lambda: self.setResolution(640,480))
        self.mainPage.radioButton_res_3.toggled.connect(lambda: self.setResolution(800,600))
        self.mainPage.radioButton_res_4.toggled.connect(lambda: self.setResolution(1280,720))
        # Set action for reset button
        self.mainPage.Button_reset.clicked.connect(self.resetSettingValues)

    # Sets all ui-objects to default values
    def resetSettingValues(self):
        self.mainPage.Slider_brightness.setValue(self.start_brightness)
        self.mainPage.Label_brightnessValue.setNum(self.start_brightness)
        self.mainPage.Slider_contrast.setValue(self.start_contrast)
        self.mainPage.Label_contrastValue.setNum(self.start_contrast)
        self.mainPage.radioButton_RGB.toggle()
    
    # Function to change the image appearance
    def changeImageAppearance(self, appearance):
            self.imageColor = appearance

    # Function that enables/disables the camera frame
    def showCameraFrame(self):
        if self.cameraFrameIsActive is True:
            self.mainPage.Splitter_frame.setSizes([0,16777215])
            self.mainPage.cameraFrame.setVisible(False)
            self.cameraFrameIsActive = False
        else:
            self.mainPage.Splitter_frame.setSizes([16777215,300])
            self.mainPage.cameraFrame.setVisible(True)
            self.cameraFrameIsActive = True
         
    # Function that enables/disables the side panel
    def showSidePanel(self):
        if self.sidePanelIsActive is True:
            self.mainPage.Splitter_frame.setSizes([16777215,0])
            self.mainPage.sidePanel.setVisible(False)
            self.sidePanelIsActive = False
            self.ui.action_SidePanel.setChecked(False)

            self.mainPage.settingsFrame.setVisible(False)
            self.settingsIsActive = False
            self.ui.action_Settings.setChecked(False)

            self.mainPage.outputFrame.setVisible(False)
            self.outputIsActive = False
            self.ui.action_Output.setChecked(False)
        else:
            self.mainPage.Splitter_frame.setSizes([16777215,300])
            self.mainPage.sidePanel.setVisible(True)
            self.sidePanelIsActive = True
            self.ui.action_SidePanel.setChecked(True)

            self.mainPage.settingsFrame.setVisible(True)
            self.settingsIsActive = True
            self.ui.action_Settings.setChecked(True)

            self.mainPage.outputFrame.setVisible(True)
            self.outputIsActive = True
            self.ui.action_Output.setChecked(True)
            self.mainPage.Splitter_sidePanel.setSizes([1,1])
            

    def showSettings(self):
        if self.settingsIsActive is True and self.outputIsActive is True:
            self.mainPage.Splitter_sidePanel.setSizes([0,16777215])
            self.mainPage.settingsFrame.setVisible(False)
            self.settingsIsActive = False
        elif self.settingsIsActive is True and self.outputIsActive is False:
            self.mainPage.settingsFrame.setVisible(False)
            self.settingsIsActive = False
            self.showSidePanel()
        else:
            self.mainPage.Splitter_sidePanel.setSizes([1,1])
            self.mainPage.settingsFrame.setVisible(True)
            self.settingsIsActive = True
            if self.sidePanelIsActive is False:
                self.mainPage.Splitter_frame.setSizes([16777215,300])
                self.mainPage.sidePanel.setVisible(True)
                self.sidePanelIsActive = True
                self.ui.action_SidePanel.setChecked(True)
        
    

    def showOutput(self):
        if self.outputIsActive is True and self.settingsIsActive is True:
            self.mainPage.Splitter_sidePanel.setSizes([16777215,0])
            self.mainPage.outputFrame.setVisible(False)
            self.outputIsActive = False
        elif self.outputIsActive is True and self.settingsIsActive is False:
            self.mainPage.outputFrame.setVisible(False)
            self.outputIsActive = False
            self.showSidePanel()
        else:
            self.mainPage.Splitter_sidePanel.setSizes([1,1])
            self.mainPage.outputFrame.setVisible(True)
            self.outputIsActive = True
            if self.sidePanelIsActive is False:
                self.mainPage.Splitter_frame.setSizes([16777215,300])
                self.mainPage.sidePanel.setVisible(True)
                self.sidePanelIsActive = True
                self.ui.action_SidePanel.setChecked(True)

    # Function that sets the resolution of the webcam
    def setResolution(self,width,height):
        self.cap.set(3,width)
        self.cap.set(4,height)

    # view camera
    def viewCam(self):
        if self.currentPage == 0:
            # read image in BGR format
            ret, image = self.cap.read()

            # convert image to RGB format
            if self.imageColor == "RGB":
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                height, width, channel = image.shape
                qiFormat = QImage.Format_RGB888
            # convert image to Grayscale format
            elif self.imageColor == "Grayscale":
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                height, width = image.shape
                channel = 1
                qiFormat = QImage.Format_Grayscale8
            # convert image to Edged format
            elif self.imageColor == "Edged":
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray,(5,5),0)
                edged = cv2.Canny(blur,35,125)
                image = edged
                height, width = image.shape
                channel = 1
                qiFormat = QImage.Format_Grayscale8

            # calculate step
            step = channel * width

            # set contrast
            contrast = self.mainPage.Slider_contrast.value()/10
            self.mainPage.Label_contrastValue.setNum(contrast)
            # set brightness
            brightness = self.mainPage.Slider_brightness.value()
            self.mainPage.Label_brightnessValue.setNum(brightness)

            image = cv2.addWeighted(image,contrast,np.zeros(image.shape, image.dtype),0,brightness)
            # create QImage from image
            qImg = QImage(image.data, width, height, step, qiFormat)
            self.pix = QPixmap.fromImage(qImg)
            self.resize_camFrame()

            # save images
            self.saveImages(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),5)
        elif self.currentPage == 1:
             # read image in BGR format
            ret, image = self.cap.read()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image.shape
            qiFormat = QImage.Format_RGB888
        
            # calculate step
            step = channel * width

            # create QImage from image
            qImg = QImage(image.data, width, height, step, qiFormat)
            self.pix = QPixmap.fromImage(qImg)
            self.resize_camFrame()
        

    # writes the image to _pycache_ folder
    def saveImages(self, img, amount):
        for i in range(amount):
            cv2.imwrite("image-" + str(i) + ".jpg", img)
        
    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

            #focus = 25  # min: 0, max: 255, increment:5
            
            #self.cap.set(cv2.CAP_PROP_FOCUS,focus)
            
            # start timer
            self.timer.start(20)
            # update Button_startCam text
            self.mainPage.Button_startCam.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update Button_startCam text
            self.mainPage.Button_startCam.setText("Start")
    
# Use this if you want to start without loading window
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow("Application")
    mainWindow.show()
    sys.exit(app.exec_())
