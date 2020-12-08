import threading
import sys
from PyQt5.QtWidgets import QApplication
from GUI.ui_loadingWindow import *
from dialogMenu import *
from pathlib import Path

# Author: Philip
# Reviewed by: Andreas
# Date: 2020-12-01

# Global values
counter = 0.0
increments = 1.0
applicationWindow = None

"""
LoadingWindow is class that handles the loading window that opens the program. 
It starts the loading window, imports modules used by the application, checks if calibration is needed and boots up the main application.
OBS! IF YOU ARE ON A RASPBERRY PI, YOU NEED TO REMOVE cv2.CAP_DSHOW in mainPage row 85! 
OBS! IF YOU WANT TO START WITH THE LOADING SCREEN CHANGE timer start time TO 100 in loadingwindow row 42.
"""
class LoadingWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # call QWidget constructor
        self.ui = Ui_LoadingWindow() # create ui
        self.ui.setupUi(self) # ui setup 
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint) # remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # remove title bar
        # shadow effect
        self.shadow = QGraphicsDropShadowEffect(self) 
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,0,0,60))
        self.ui.frame_dropShadow.setGraphicsEffect(self.shadow)
        # starting thread for imports
        thread = threading.Thread(target=self.__importModules)
        thread.setDaemon(True)
        thread.start()
        # timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__progress)
        self.timer.start(30)

        self.calibrationIsNeeded = False # boolean for checking if calibration is needed
        self.show()
    
    # Funktion that loops and shows the progress of the imports
    def __progress(self):
        global counter,increments
        self.ui.progressBar.setValue(int(counter))
        if counter > 100.0:
            self.timer.stop()
            try:
                self.main = applicationWindow("Object Detector")
                self.main.show()
                self.close()
                if self.calibrationIsNeeded:
                    self.__calibrate_popUp()
            except:
                self.ui.Label_information.setText("<strong>Error:</strong> could not load modules")
        counter += increments

    # Imorts the modules used in the main application
    def __importModules(self):
        global applicationWindow,increments
        self.ui.Label_information.setText("Importing modules...")
        increments = 0.5
        from application import MainWindow as applicationWindow
        increments = 3.5
        self.ui.Label_information.setText("Checking if calibration is needed...")
        if not Path("camera_info.ini").is_file():
            self.calibrationIsNeeded = True
        else: 
            self.calibrationIsNeeded = False

    # Function that instantiates a dialog menu that informs the user to calibrate
    def __calibrate_popUp(self):
        dialogMenu = DialogMenu(self.main)
        dialogMenu.setTitle("<strong>Calibration</strong> is needed!")
        dialogMenu.setInformationText("In order to use the distance-calculation feature of the application, you need to calibrate your camera.")
        dialogMenu.setTopButtonText("Calibrate camera")
        dialogMenu.setBottomButtonText("Skip")
        dialogMenu.setFixedHeight(340)
        dialogMenu.centerOnScreen()
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