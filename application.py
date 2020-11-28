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

"""
MainWindow inherits QMainWindow and creates a window with the ui(ui_mainWindow.py) made with Qt designer
Notice that a "page" is reffered to as a QWidget that is used on the MainWindow's stack widget.
"""
class MainWindow(QtWidgets.QMainWindow):
    # class constructor
    def __init__(self,windowName):
        super().__init__() # call QMainWindow constructor
        self.ui = Ui_MainWindow() # create ui
        self.ui.setupUi(self) # set ui
        self.setWindowTitle(windowName) # set window title
        self.resize(1200,800) # set start size of window
        self.page_0 = MainPage() # create page 0
        self.ui.stackedWidget.addWidget(self.page_0) # add page 0
        self.page_1 = CalibrationPage() # create page 1
        self.ui.stackedWidget.addWidget(self.page_1) # add page 1
        self.currentPage = 0 # current page
        self.__setMenuActions() # set actions on menubar buttons

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
        """View"""
        self.ui.action_Camera.triggered.connect(lambda: self.page_0.setCameraFrame(self.ui.action_Camera.isChecked()))
        self.ui.action_SidePanel.triggered.connect(lambda: self.page_0.setSidePanel(self.ui.action_SidePanel.isChecked()))
        self.ui.action_SidePanel.triggered.connect(lambda: self.__checkSidePanelActions(self.ui.action_SidePanel.isChecked()))
        self.ui.action_Settings.triggered.connect(lambda: self.page_0.setSettingsPanel(self.ui.action_Settings.isChecked(),self.ui.action_SidePanel.isChecked(),self.ui.action_Output.isChecked()))
        self.ui.action_Settings.triggered.connect(lambda: self.__setSidePanelAction(self.ui.action_Settings.isChecked(),self.ui.action_Output.isChecked()))
        self.ui.action_Output.triggered.connect(lambda: self.page_0.setOutPutPanel(self.ui.action_Output.isChecked(),self.ui.action_SidePanel.isChecked(),self.ui.action_Settings.isChecked()))
        self.ui.action_Output.triggered.connect(lambda: self.__setSidePanelAction(self.ui.action_Settings.isChecked(),self.ui.action_Output.isChecked()))
        """Navigation"""
        self.ui.action_MainScreen.triggered.connect(lambda: self.openPage(0))
        self.ui.action_Calibration.triggered.connect(lambda: self.openPage(1))
        """Object Detection"""
        self.ui.action_FaceDetection.triggered.connect(self.page_0.activateFaceDetection)
        """Help"""
        self.ui.action_HowToUse.triggered.connect(self.__showHowToUse)
        self.ui.action_About.triggered.connect(self.__showAbout)

    # Help-function that is used to check/uncheck the settings and output buttons on the menubar when the sidepanel button is pressed
    def __checkSidePanelActions(self, wantToCheck):
        self.ui.action_Settings.setChecked(wantToCheck)
        self.ui.action_Output.setChecked(wantToCheck)
    
    # Help-function that is used to check/uncheck the action_SidePanel
    def __setSidePanelAction(self, settinsIsChecked, outputIsChecked):
        if settinsIsChecked or outputIsChecked:
            self.ui.action_SidePanel.setChecked(True)
        elif not settinsIsChecked and not outputIsChecked:
            self.ui.action_SidePanel.setChecked(False)

    def __showHowToUse(self):
        dialogMenu = DialogMenu()
        dialogMenu.setTitle("<strong>How To Use</strong>")
        dialogMenu.setFixedHeight(500)
        dialogMenu.setFixedWidth(500)
        dialogMenu.centerOnScreen()
        f = open("How_to_use.txt","r")
        dialogMenu.setInformationText(f.read())
        dialogMenu.setTopButtonText("Ok")
        dialogMenu.ui.PushButton_bottom.setVisible(False)
        dialogMenu.ui.PushButton_top.clicked.connect(dialogMenu.close)
        dialogMenu.exec_()
    
    def __showAbout(self):
        dialogMenu = DialogMenu()
        dialogMenu.setTitle("<strong>Written By:</strong>")
        dialogMenu.setFixedHeight(360)
        dialogMenu.centerOnScreen()
        dialogMenu.centerText()
        f = open("About.txt","r")
        dialogMenu.setInformationText(f.read())
        dialogMenu.setTopButtonText("Ok")
        dialogMenu.ui.PushButton_bottom.setVisible(False)
        dialogMenu.ui.PushButton_top.clicked.connect(dialogMenu.close)
        dialogMenu.exec_()

# Use this if you want to start without the loading window
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow("test")
    mainWindow.show()
    sys.exit(app.exec_())