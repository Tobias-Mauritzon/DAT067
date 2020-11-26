import sys
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import numpy as np

from mainPage import *
from calibrationPage import *
from GUI.ui_mainWindow import *


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

        # create mainwindow ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # set window name and size
        self.setWindowTitle(windowName)
        self.resize(1200,800)

        # add page 0
        self.page_0 = MainPage()
        self.ui.stackedWidget.addWidget(self.page_0)

        # add page 1
        self.page_1 = CalibrationPage()
        self.ui.stackedWidget.addWidget(self.page_1)
        
        # current page
        self.currentPage = 0

        self.__setMenuActions()

        # Set start page
        #self.openPage(0)

    # Function that opens a specific page
    def openPage(self,pageIndex):
        if pageIndex == 0:
            self.ui.menuObject_detection.menuAction().setVisible(True)
            self.ui.menuView.menuAction().setVisible(True)
            self.ui.stackedWidget.setCurrentIndex(0)
            self.page_1.closePage()
            self.page_0.loadPage()
            self.currentPage = 0
        elif pageIndex == 1:
            self.ui.menuObject_detection.menuAction().setVisible(False)
            self.ui.menuView.menuAction().setVisible(False)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.page_0.closePage()
            self.page_1.loadPage()
            self.currentPage = 1
    
    
    
    # Sets actions for top menus
    def __setMenuActions(self):
        self.ui.action_Camera.triggered.connect(lambda: self.page_0.setCameraFrame(self.ui.action_Camera.isChecked()))
        self.ui.action_SidePanel.triggered.connect(lambda: self.page_0.setSidePanel(self.ui.action_SidePanel.isChecked()))
        self.ui.action_SidePanel.triggered.connect(lambda: self.__checkSidePanelActions(self.ui.action_SidePanel.isChecked()))
        self.ui.action_Settings.triggered.connect(lambda: self.page_0.setSettingsPanel(self.ui.action_Settings.isChecked(),self.ui.action_SidePanel.isChecked(),self.ui.action_Output.isChecked()))
        self.ui.action_Settings.triggered.connect(lambda: self.__setSidePanelAction(self.ui.action_Settings.isChecked(),self.ui.action_Output.isChecked()))
        self.ui.action_Output.triggered.connect(lambda: self.page_0.setOutPutPanel(self.ui.action_Output.isChecked(),self.ui.action_SidePanel.isChecked(),self.ui.action_Settings.isChecked()))
        self.ui.action_Output.triggered.connect(lambda: self.__setSidePanelAction(self.ui.action_Settings.isChecked(),self.ui.action_Output.isChecked()))
        self.ui.action_MainScreen.triggered.connect(lambda: self.openPage(0))
        self.ui.action_Calibration.triggered.connect(lambda: self.openPage(1))

     
    def __checkSidePanelActions(self, wantToCheck):
        self.ui.action_Settings.setChecked(wantToCheck)
        self.ui.action_Output.setChecked(wantToCheck)
    
    def __setSidePanelAction(self, s, o):
        if s or o:
            self.ui.action_SidePanel.setChecked(True)
        elif not s and not o:
            self.ui.action_SidePanel.setChecked(False)

# Use this if you want to start without loading window
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow("test")
    mainWindow.show()
    sys.exit(app.exec_())
