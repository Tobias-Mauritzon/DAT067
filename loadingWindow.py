import sys
import cv2
import time
import threading
import numpy as np

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from GUI.ui_loadingWindow import *
from dialogMenu import *
from pathlib import Path


# Author: Philip
# Reviewed by:
# Date: 2020-11-24

counter = 0.0
increments = 1.0
mw = None

class LoadingWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # call QWidget constructor
        super().__init__()

        # create ui
        self.ui = Ui_LoadingWindow()
        self.ui.setupUi(self)

        # Remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ## shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,0,0,60))
        self.ui.frame_dropShadow.setGraphicsEffect(self.shadow)

        # starting thread for imports
        thread = threading.Thread(target=self.importModules)
        thread.setDaemon(True)
        thread.start()

        #timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(30)

        # boolean for checking if calibration is needed
        self.calibrationIsNeeded = False
        
        self.show()

    def progress(self):
        global counter,increments
        self.ui.progressBar.setValue(int(counter))
        
        if counter > 100.0:
            self.timer.stop()
            try:
                self.main = mw("Object Detector")
                self.main.show()
                self.close()

                if self.calibrationIsNeeded:
                    self.calibrate_popUp()
            except:
                self.ui.Label_information.setText("<strong>Error:</strong> could not load modules")
        counter += increments

    def importModules(self):
        global mw,increments
        self.ui.Label_information.setText("Importing modules...")
        increments = 0.5
        from application import MainWindow as mw
        increments = 3.5
        self.ui.Label_information.setText("Checking if calibration is needed...")
        if not Path("camera_info.ini").is_file():
            self.calibrationIsNeeded = True
        else: 
            self.calibrationIsNeeded = False

    # Function that instantiates a dialog menu that informs the user to calibrate
    def calibrate_popUp(self):
        dialogMenu = DialogMenu()
        dialogMenu.setTitle("<strong>Calibration</strong> is needed!")
        dialogMenu.setInformationText("In order to use the distance-calculation feature of the application, you need to calibrate your camera.")
        dialogMenu.setTopButtonText("Calibrate camera")
        dialogMenu.setBottomButtonText("Skip")
        dialogMenu.ui.PushButton_top.clicked.connect(lambda: self.main.openPage(1))
        dialogMenu.ui.PushButton_top.clicked.connect(dialogMenu.close)
        dialogMenu.ui.PushButton_bottom.clicked.connect(dialogMenu.close)
        dialogMenu.exec_()

# this is the "main function"
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = LoadingWindow()
    mainWindow.show()
    sys.exit(app.exec_())