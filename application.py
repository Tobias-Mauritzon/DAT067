import sys
import cv2

from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
import numpy as np
from ui_mainWindow import *
from dialogMenu import *
import tensorflow as tf

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

        #self.setWindowIcon(QtGui.QIcon('frame_icon.png'))
        # set window name
        self.setWindowTitle(windowName)
        self.resize(1200,800)
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
        self.settingsIsActive = True
        self.outputIsActive = True
        self.ui.Splitter_frame.setSizes([1000,300])
        self.ui.Splitter_sidePanel.setSizes([1,1])
        self.imageColor = "RGB"

        # Start values:
        self.start_brightness = 0
        self.start_contrast = 10

        # Laddar in den tidigare tränade modellen.
        #self.my_model = tf.keras.models.load_model('saved_model/car_model')

        # If the calibrationfile does not exist, show calibration dialog menu 
        if not Path("CALIBRATIONFILE").is_file():
            self.calibrate_popUp()
        
        
    
    def calibrate_popUp(self):
        dialogMenu = DialogMenu()
        dialogMenu.setTitle("<strong>Calibration</strong> is needed!")
        dialogMenu.setInformationText("In order to use the distance calculation feature of the application, you need to calibrate your camera.")
        dialogMenu.setTopButtonText("Calibrate camera")
        dialogMenu.setBottomButtonText("Skip")
        dialogMenu.ui.PushButton_top.clicked.connect(self.openCalibrationPage)
        dialogMenu.ui.PushButton_top.clicked.connect(dialogMenu.close)
        dialogMenu.ui.PushButton_bottom.clicked.connect(dialogMenu.close)

        dialogMenu.exec_()
        

    # resizes the cam frame
    def resize_camFrame(self):
        if self.pix is not None:
            self.w = self.ui.image_label.width()
            self.h = self.ui.image_label.height()
            self.ui.image_label.setPixmap(self.pix.scaled(self.w, self.h,QtCore.Qt.KeepAspectRatio))

    def openCalibrationPage(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    
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
        self.ui.action_Camera.triggered.connect(self.showCameraFrame)
        self.ui.action_SidePanel.triggered.connect(self.showSidePanel)

        # Set action for sidePanel menus
        self.ui.action_Settings.triggered.connect(self.showSettings)
        self.ui.action_Output.triggered.connect(self.showOutput)

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

    # Sets all ui-objects to default values
    def resetSettingValues(self):
        self.ui.Slider_brightness.setValue(self.start_brightness)
        self.ui.Label_brightnessValue.setNum(self.start_brightness)
        self.ui.Slider_contrast.setValue(self.start_contrast)
        self.ui.Label_contrastValue.setNum(self.start_contrast)
        self.ui.radioButton_RGB.toggle()
    
    # Function for RGB-radiobutton, change the image color to edged
    def changeImageAppearance(self, appearance):
            self.imageColor = appearance

    # Function that enables/disables the camera frame
    def showCameraFrame(self):
        if self.cameraFrameIsActive is True:
            self.ui.Splitter_frame.setSizes([0,16777215])
            self.ui.cameraFrame.setVisible(False)
            self.cameraFrameIsActive = False
        else:
            self.ui.Splitter_frame.setSizes([16777215,300])
            self.ui.cameraFrame.setVisible(True)
            self.cameraFrameIsActive = True
         
    # Function that enables/disables the side panel
    def showSidePanel(self):
        if self.sidePanelIsActive is True:
            self.ui.Splitter_frame.setSizes([16777215,0])
            self.ui.sidePanel.setVisible(False)
            self.sidePanelIsActive = False
            self.ui.action_SidePanel.setChecked(False)

            self.ui.settingsFrame.setVisible(False)
            self.settingsIsActive = False
            self.ui.action_Settings.setChecked(False)

            self.ui.outputFrame.setVisible(False)
            self.outputIsActive = False
            self.ui.action_Output.setChecked(False)
        else:
            self.ui.Splitter_frame.setSizes([16777215,300])
            self.ui.sidePanel.setVisible(True)
            self.sidePanelIsActive = True
            self.ui.action_SidePanel.setChecked(True)

            self.ui.settingsFrame.setVisible(True)
            self.settingsIsActive = True
            self.ui.action_Settings.setChecked(True)

            self.ui.outputFrame.setVisible(True)
            self.outputIsActive = True
            self.ui.action_Output.setChecked(True)
            self.ui.Splitter_sidePanel.setSizes([1,1])
            

    def showSettings(self):
        if self.settingsIsActive is True and self.outputIsActive is True:
            self.ui.Splitter_sidePanel.setSizes([0,16777215])
            self.ui.settingsFrame.setVisible(False)
            self.settingsIsActive = False
        elif self.settingsIsActive is True and self.outputIsActive is False:
            self.ui.settingsFrame.setVisible(False)
            self.settingsIsActive = False
            self.showSidePanel()
        else:
            self.ui.Splitter_sidePanel.setSizes([1,1])
            self.ui.settingsFrame.setVisible(True)
            self.settingsIsActive = True
            if self.sidePanelIsActive is False:
                self.ui.Splitter_frame.setSizes([16777215,300])
                self.ui.sidePanel.setVisible(True)
                self.sidePanelIsActive = True
                self.ui.action_SidePanel.setChecked(True)
        
    

    def showOutput(self):
        if self.outputIsActive is True and self.settingsIsActive is True:
            self.ui.Splitter_sidePanel.setSizes([16777215,0])
            self.ui.outputFrame.setVisible(False)
            self.outputIsActive = False
        elif self.outputIsActive is True and self.settingsIsActive is False:
            self.ui.outputFrame.setVisible(False)
            self.outputIsActive = False
            self.showSidePanel()
        else:
            self.ui.Splitter_sidePanel.setSizes([1,1])
            self.ui.outputFrame.setVisible(True)
            self.outputIsActive = True
            if self.sidePanelIsActive is False:
                self.ui.Splitter_frame.setSizes([16777215,300])
                self.ui.sidePanel.setVisible(True)
                self.sidePanelIsActive = True
                self.ui.action_SidePanel.setChecked(True)

    # Function that sets the resolution of the webcam
    def setResolution(self,width,height):
        self.cap.set(3,width)
        self.cap.set(4,height)

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

        # Testar modellen på en bild av en bil
        """
        self.check_categeori(self.my_model.predict([self.prepare(image)]))
"""

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
    
"""
    # Funktion för att ladda in bilder så det går att testa.
    def prepare(self,filepath):
        IMG_SIZE = 100
        img_array = cv2.imread("image-0.jpg", cv2.IMREAD_GRAYSCALE)
        new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

    def check_categeori(self,pred):
        if (int(pred[0][0]) == 1):
            print("Car")
            self.ui.Label_object.setText("Car")
        elif (int(pred[0][1]) == 1):
            print("Dog")
            self.ui.Label_object.setText("Dog")
        elif (int(pred[0][2]) == 1):
            print("Cat")
            self.ui.Label_object.setText("Cat")
        else:
            print("Not a Car, Cat or a Dog")
            self.ui.Label_object.setText("Not a Car, Cat or a Dog")
        return
    """

# Use this if you want to start without loading window

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow("Application")
    mainWindow.show()
    sys.exit(app.exec_())
