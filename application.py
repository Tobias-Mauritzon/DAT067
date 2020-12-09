from GUI.ui_mainWindow import *
from mainPage import *
from calibrationPage import *

# Author: Philip
# Reviewed by: Andreas
# Date: 2020-12-01

"""
MainWindow creates the main window for the application. It has a topbar and a stack widget where different "pages" can be shown.
This class inherits QMainWindow and creates a window with the ui(ui_mainWindow.py) made with Qt designer.
Notice that a "page" is reffered to as a QWidget that is used on the MainWindow's stack widget.
OBS! IF YOU ARE ON A RASPBERRY PI, YOU NEED TO REMOVE cv2.CAP_DSHOW in mainPage row 85! 
OBS! IF YOU WANT TO START WITH THE LOADING SCREEN CHANGE timer start time TO 100 in loadingwindow row 42.
"""
class MainWindow(QtWidgets.QMainWindow):
	# class constructor
	def __init__(self,windowName):
		super().__init__() # call QMainWindow constructor
		self.ui = Ui_MainWindow() # create ui
		self.ui.setupUi(self) # set ui
		self.setWindowTitle(windowName) # set window title
		self.resize(1200,800) # set start size of window
		self.page_0 = MainPage(self) # create page 0
		self.ui.stackedWidget.addWidget(self.page_0) # add page 0
		self.page_1 = CalibrationPage(self) # create page 1
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
	
	# enables/disables fullscreen
	def __setFullScreen(self):
		if self.isFullScreen():
			self.showNormal()
		else:
			self.showFullScreen()
	

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
		self.ui.action_Full_Screen.triggered.connect(self.__setFullScreen)
		"""Navigation"""
		self.ui.action_MainScreen.triggered.connect(lambda: self.openPage(0))
		self.ui.action_Calibration.triggered.connect(lambda: self.openPage(1))
		"""Object Detection"""
		self.ui.action_HaarCascade_Cars.triggered.connect(lambda: self.page_0.activateHaarCascade("Car"))
		self.ui.action_YOLO.triggered.connect(lambda: self.page_0.activateYOLO())
		self.ui.action_CustomModel.triggered.connect(self.page_0.activateCustomModel)
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

	# Shows a dialogmenu with text from the how_to_use.txt file
	def __showHowToUse(self):
		dialogMenu = DialogMenu(self)
		dialogMenu.setTitle("<strong>How To Use</strong>")
		dialogMenu.setFixedHeight(500)
		dialogMenu.setFixedWidth(500)
		dialogMenu.centerOnWindow()
		dialogMenu.setInformationTextFromFile("How_to_use.txt")
		dialogMenu.setTopButtonText("Ok")
		dialogMenu.ui.PushButton_bottom.setVisible(False)
		dialogMenu.ui.PushButton_top.clicked.connect(dialogMenu.close)
		dialogMenu.exec_()
	
	# Shows a dialogmenu with text from the About.txt file
	def __showAbout(self):
		dialogMenu = DialogMenu(self)
		dialogMenu.setTitle("<strong>Made By:</strong>")
		dialogMenu.setFixedHeight(400)
		dialogMenu.centerOnWindow()
		dialogMenu.centerText()
		dialogMenu.setInformationTextFromFile("About.txt")
		dialogMenu.setTopButtonText("Ok")
		dialogMenu.ui.PushButton_bottom.setVisible(False)
		dialogMenu.ui.PushButton_top.clicked.connect(dialogMenu.close)
		dialogMenu.exec_()

"""THIS "main" IS ONLY USED FOR TESTING PURPOSES"""
# Use this if you want to start without the loading window.
if __name__ == '__main__':
	app = QApplication(sys.argv)
	# create and show mainWindow
	mainWindow = MainWindow("TEST OF APPLICATION")
	mainWindow.show()
	sys.exit(app.exec_())