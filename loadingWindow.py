import sys
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
import numpy as np
from ui_loadingWindow import *
from application import *

# Author: Philip
# Reviewed by:
# Date: 2020-11-24

counter = 0

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

        #timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(20)

        self.show()

    def progress(self):
        global counter

        self.ui.progressBar.setValue(counter)

        if counter > 100:
            self.timer.stop()
            self.main = MainWindow("Object Detector")
            self.main.show()
            self.close()
        
        counter += 1


# this is the "main function" that makes an instance of the mainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = LoadingWindow()
    mainWindow.show()

    sys.exit(app.exec_())