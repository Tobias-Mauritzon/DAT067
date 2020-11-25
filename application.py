import sys
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import numpy as np
from ui_mainWindow import *
from CameraCalibration import *
from ui_mainPage import * 
from mainPage import *
from calibrationPage import *

# Author: Philip
# Reviewed by:
# Date: 2020-11-25

# MainWindow inherits QMainWindow and creates a window with the ui(ui_mainWindow.py) made with Qt designer
# Notice that a "page" is reffered to as a QWidget that is used on the MainWindow's stack widget.
class MainWindow(QtWidgets.QMainWindow):
 
    # class constructor
    def __init__(self,windowName):
        # call QMainWindow constructor
        super().__init__()

        # set window name and size
        self.setWindowTitle(windowName)
        self.resize(1200,800)

        # create mainwindow ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # add page 0
        self.page_0 = mainPage()
        self.ui.stackedWidget.addWidget(self.page_0)
        
        # current page
        self.currentPage = 0

        self.setMenuActions()

        # Set start page
        self.openPage(0)

        # If the calibrationfile does not exist, show calibration dialog menu 
        #if not Path("camera_info.ini").is_file():
          #  self.calibrate_popUp()

        """
        # Funktion that initiazies the pages
        def addPage(self, page):
    
        # PAGE 1:
        self.calibrationPage = Ui_CalibrationPage()
        self.calibrationPage.setupUi(self.calibrationPage)
        self.ui.stackedWidget.addWidget(self.calibrationPage)
        """
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
    """
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
        """
    # event for when the window is resized
    def eventFilter(self, obj, event):
        if (event.type() == QtCore.QEvent.Resize):
            if(self.page == 0):
                self.mainPage.resize_camFrame()
        return super().eventFilter(obj, event)
    
    # Sets actions for top menus
    def setMenuActions(self):

        self.ui.action_Camera.triggered.connect(lambda: self.page_0.setCameraFrame(self.ui.action_Camera.isChecked()))
        
        
        self.ui.action_SidePanel.triggered.connect(lambda: self.page_0.setSidePanel(self.ui.action_SidePanel.isChecked()))
        self.ui.action_SidePanel.triggered.connect(lambda: self.checkSidePanelActions(self.ui.action_SidePanel.isChecked()))
        
        self.ui.action_Settings.triggered.connect(lambda: self.page_0.setSettingsPanel(self.ui.action_Settings.isChecked(),self.ui.action_SidePanel.isChecked(),self.ui.action_Output.isChecked()))
        self.ui.action_Settings.triggered.connect(lambda: self.setSidePanelAction(self.ui.action_Settings.isChecked(),self.ui.action_Output.isChecked()))

        self.ui.action_Output.triggered.connect(lambda: self.page_0.setOutPutPanel(self.ui.action_Output.isChecked(),self.ui.action_SidePanel.isChecked(),self.ui.action_Settings.isChecked()))
        self.ui.action_Output.triggered.connect(lambda: self.setSidePanelAction(self.ui.action_Settings.isChecked(),self.ui.action_Output.isChecked()))

     
    def checkSidePanelActions(self, wantToCheck):
        self.ui.action_Settings.setChecked(wantToCheck)
        self.ui.action_Output.setChecked(wantToCheck)
    
    def setSidePanelAction(self, s, o):
        if s or o:
            self.ui.action_SidePanel.setChecked(True)
        elif not s and not o:
            self.ui.action_SidePanel.setChecked(False)


    
# Use this if you want to start without loading window
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow("Application")
    mainWindow.show()
    sys.exit(app.exec_())
