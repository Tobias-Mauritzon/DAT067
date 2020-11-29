import sys
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from GUI.ui_dialogMenu import *
import numpy as np

# Author: Philip
# Reviewed by:
# Date: 2020-11-24

class DialogMenu(QtWidgets.QDialog):
    def __init__(self,window):
        # call QWidget constructor
        super().__init__()

        # create ui
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.window = window

        self.setFixedWidth(500)
        self.setFixedHeight(300)

        # Remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ## shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,0,0,60))
        self.ui.frame.setGraphicsEffect(self.shadow)  

        self.__setButtonActions()  

    def setTitle(self, title):
        self.ui.Label_title.setText(title)

    def setInformationText(self, text):
        self.ui.Label_informationText.setText(text)

    def setTopButtonText(self, text):
        self.ui.PushButton_top.setText(text)
    
    def setBottomButtonText(self, text):
        self.ui.PushButton_bottom.setText(text)
    
    def centerOnWindow(self):
        frameGm = self.frameGeometry()
        centerPoint = self.window.frameGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        blur_effect = QtWidgets.QGraphicsBlurEffect(blurRadius=5)
        self.window.setGraphicsEffect(blur_effect)

    def centerText(self):
        self.ui.Label_informationText.setAlignment(QtCore.Qt.AlignCenter)
    
    def __setButtonActions(self):
        self.ui.PushButton_top.clicked.connect(self.__removeBlur)
        self.ui.PushButton_bottom.clicked.connect(self.__removeBlur)
    
    def __removeBlur(self):
        self.window.setGraphicsEffect(None)
