import sys
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

from ui_mainWindow import *

# TIPS: convert from ui to py, use this in terminal: pyuic5 -x ui_application.ui -o ui_application.py
# Author: Philip
# Version: 1.0
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

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)

        self.setActions()

        # instantiate event filter
        self.installEventFilter(self)

        # the pixMap used to set the image on a QLabel
        self.pix = None
        # the width and height of the QLabel 
        self.w = 0
        self.h = 0
        
        self.cameraFrameIsActive = True
        self.sidePanelIsActive = True
        self.ui.frameSplitter.setSizes([16777215,300])

        self.imageColor = "RGB"
        

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
    
    def setActions(self):
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)

        # 
        self.ui.actionCamera.triggered.connect(self.showCameraFrame)
        self.ui.actionSidePanel.triggered.connect(self.showSidePanel)

        self.ui.radioButton_RGB.toggled.connect(self.radioButton_RGB_clicked)
        self.ui.radioButton_Grayscale.toggled.connect(self.radioButton_Grayscale_clicked)
        self.ui.radioButton_Edged.toggled.connect(self.radioButton_Edged_clicked)
    
    def radioButton_RGB_clicked(self, enabled):
        if enabled:
            print("RGB!!!")
            self.imageColor = "RGB"
            
    def radioButton_Grayscale_clicked(self, enabled):
        if enabled:
            print("GRAYSCALE!!!")
            self.imageColor = "Grayscale"

    def radioButton_Edged_clicked(self, enabled):
        if enabled:
            print("Edged!!!")
            self.imageColor = "Edged"
          

    def showCameraFrame(self):
        if self.cameraFrameIsActive is True:
            self.ui.frameSplitter.setSizes([0,16777215])
            self.ui.cameraFrame.setVisible(False)
            self.cameraFrameIsActive = False
        else:
            self.ui.frameSplitter.setSizes([16777215,300])
            self.ui.cameraFrame.setVisible(True)
            self.cameraFrameIsActive = True
         
        
    def showSidePanel(self):
        if self.sidePanelIsActive is True:
            self.ui.frameSplitter.setSizes([16777215,0])
            self.ui.sidePanel.setVisible(False)
            self.sidePanelIsActive = False
        else:
            self.ui.frameSplitter.setSizes([16777215,300])
            self.ui.sidePanel.setVisible(True)
            self.sidePanelIsActive = True
    
   

    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()

        # convert image to RGB format
        if self.imageColor is "RGB":
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image.shape
            qiFormat = QImage.Format_RGB888
        elif self.imageColor is "Grayscale":
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            height, width = image.shape
            channel = 1
            qiFormat = QImage.Format_Grayscale8
        elif self.imageColor is "Edged":
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
       
        # create QImage from image
        qImg = QImage(image.data, width, height, step, qiFormat)
        self.pix = QPixmap.fromImage(qImg)
        self.resize_camFrame()

    
        
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
            # update control_bt text
            self.ui.control_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")
    
    
    

# this is the "main function" that makes an instance of the mainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow("Application")
    mainWindow.show()

    sys.exit(app.exec_())