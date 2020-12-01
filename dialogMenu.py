
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from GUI.ui_dialogMenu import *
import numpy as np

# Author: Philip
# Reviewed by: Andreas
# Date: 2020-12-01

"""
DialogMenu inherits QDialog and creates a dialog menu with the ui(ui_dialogMenu.py) made with Qt designer.
The menu consists of a title, informationtext(label) and two buttons.
"""
class DialogMenu(QtWidgets.QDialog):
    def __init__(self, window):
        super().__init__() # call QWidget constructor
        self.ui = Ui_Dialog() # create ui
        self.ui.setupUi(self) # call setup funktion in ui
        self.window = window # the window that this dialog menu should be placed in
        self.setFixedWidth(500) # set default width
        self.setFixedHeight(300) # set default height
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ## shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,0,0,60))
        self.ui.frame.setGraphicsEffect(self.shadow)  
        # set button actions
        self.__setButtonActions()  

    # Sets the title of the dialog menu
    def setTitle(self, title):
        self.ui.Label_title.setText(title)

    # Sets the informationtext to be displayed in the dialog menu
    def setInformationText(self, text):
        self.ui.Label_informationText.setText(text)
    
    # Sets the informationtext from a file to be displayed in the dialog menu 
    def setInformationTextFromFile(self, fileName):
        try:
            f = open(fileName,"r")
            self.setInformationText(f.read())
        except Exception:
            raise Exception("Could not read file!")
        finally:
            f.close()
    
    # disables the informationTextLabel
    def disableInformationText(self):
        self.ui.Label_informationText.setVisible(False)
    # Sets the text to be displayed on the top button
    def setTopButtonText(self, text):
        self.ui.PushButton_top.setText(text)

    # Sets the text to be displayed on the bottom button
    def setBottomButtonText(self, text):
        self.ui.PushButton_bottom.setText(text)
    
    # Sets the informationtext to be center aligned
    def centerText(self):
        self.ui.Label_informationText.setAlignment(QtCore.Qt.AlignCenter)

    # Centers the dialog menu on the window
    def centerOnWindow(self):
        frameGm = self.frameGeometry()
        centerPoint = self.window.frameGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        blur_effect = QtWidgets.QGraphicsBlurEffect(blurRadius=5)
        self.window.setGraphicsEffect(blur_effect)

    # Sets actions for buttons
    def __setButtonActions(self):
        self.ui.PushButton_top.clicked.connect(self.__removeBlur)
        self.ui.PushButton_bottom.clicked.connect(self.__removeBlur)
    
    # Removes the blur effect
    def __removeBlur(self):
        self.window.setGraphicsEffect(None)

