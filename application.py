import sys
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import numpy as np
from ui_mainWindow import *

# Author: Philip
# Reviewed by:
# Date: 2020-11-16

# MainWindow inherits QWidget and creates a window with the ui(ui_mainWindow.py) made with Qt designer
class MainWindow(QtWidgets.QMainWindow):
 
    # class constructor
    def __init__(self,windowName):
        # call QWidget constructor
        super().__init__()

        # create ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set window name
        self.setWindowTitle(windowName)

        self.setActions()

        # instantiate event filter
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
        
        self.cameraFrameIsActive = True
        self.sidePanelIsActive = True
        self.ui.Splitter_frame.setSizes([1000,500])
        self.ui.Splitter_sidePanel.setSizes([3,2])
        self.imageColor = "RGB"

        # Start values:
        self.start_brightness = 0
        self.start_contrast = 10

    # resizes the cam frame
    def resize_camFrame(self):
        if self.pix is not None:
            self.w = self.ui.image_label.width()
            self.h = self.ui.image_label.height()
            self.ui.image_label.setPixmap(self.pix.scaled(self.w, self.h,QtCore.Qt.KeepAspectRatio))
    
    # event for when the window is resized
    def eventFilter(self, obj, event):
        if (event.type() == QtCore.QEvent.Resize):
            self.resize_camFrame()
        return super().eventFilter(obj, event)
    
    # Sets actions for GUI-objects
    def setActions(self):
        # Set action for start button
        self.ui.Button_startCam.clicked.connect(self.controlTimer)
        # Set action for topBar menu actions
        self.ui.actionCamera.triggered.connect(self.showCameraFrame)
        self.ui.actionSidePanel.triggered.connect(self.showSidePanel)
        # Set action for radioButtons
        self.ui.radioButton_RGB.toggled.connect(self.radioButton_RGB_clicked)
        self.ui.radioButton_Grayscale.toggled.connect(self.radioButton_Grayscale_clicked)
        self.ui.radioButton_Edged.toggled.connect(self.radioButton_Edged_clicked)
        # Set action for reset button
        self.ui.Button_reset.clicked.connect(self.resetSettingValues)

    # Sets all ui-objects to default values
    def resetSettingValues(self):
        self.ui.Slider_brightness.setValue(self.start_brightness)
        self.ui.Label_brightnessValue.setNum(self.start_brightness)
        self.ui.Slider_contrast.setValue(self.start_contrast)
        self.ui.Label_contrastValue.setNum(self.start_contrast)
        self.ui.radioButton_RGB.toggle()
    
    # Function for RGB-radiobutton, change the image color to edged
    def radioButton_RGB_clicked(self, enabled):
        if enabled:
            self.imageColor = "RGB"
            
    # Function for Grayscale-radiobutton, change the image color to edged
    def radioButton_Grayscale_clicked(self, enabled):
        if enabled:
            self.imageColor = "Grayscale"

    # Function for Edged-radiobutton, change the image color to edged
    def radioButton_Edged_clicked(self, enabled):
        if enabled:
            self.imageColor = "Edged"

    # Funktion that enables/disables the camera frame
    def showCameraFrame(self):
        if self.cameraFrameIsActive is True:
            self.ui.Splitter_frame.setSizes([0,16777215])
            self.ui.cameraFrame.setVisible(False)
            self.cameraFrameIsActive = False
        else:
            self.ui.Splitter_frame.setSizes([1000,500])
            self.ui.cameraFrame.setVisible(True)
            self.cameraFrameIsActive = True
         
    # Funktion that enables/disables the side panel
    def showSidePanel(self):
        if self.sidePanelIsActive is True:
            self.ui.Splitter_frame.setSizes([16777215,0])
            self.ui.sidePanel.setVisible(False)
            self.sidePanelIsActive = False
        else:
            self.ui.Splitter_frame.setSizes([1000,500])
            self.ui.sidePanel.setVisible(True)
            self.sidePanelIsActive = True
    
    # view camera
    def viewCam(self):
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
        contrast = self.ui.Slider_contrast.value()/10
        self.ui.Label_contrastValue.setNum(contrast)
        # set brightness
        brightness = self.ui.Slider_brightness.value()
        self.ui.Label_brightnessValue.setNum(brightness)

        image = cv2.addWeighted(image,contrast,np.zeros(image.shape, image.dtype),0,brightness)
        # create QImage from image
        qImg = QImage(image.data, width, height, step, qiFormat)
        self.pix = QPixmap.fromImage(qImg)
        self.resize_camFrame()

        # save images
        self.saveImages(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),5)
    
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
            self.ui.Button_startCam.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update Button_startCam text
            self.ui.Button_startCam.setText("Start")
    

# this is the "main function" that makes an instance of the mainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow("Application")
    mainWindow.show()

    sys.exit(app.exec_())