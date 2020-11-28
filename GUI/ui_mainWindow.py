# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(399, 280)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("*\n"
"{\n"
"    background-color: rgb(35, 35, 38);\n"
"}\n"
"\n"
"QMenuBar{\n"
"    background-color: rgb(35, 35, 38);\n"
"    color: white;\n"
"}\n"
"\n"
"QMenuBar::item::selected {\n"
"    background-color: rgb(51, 55, 61);\n"
"}\n"
"\n"
"/*QMenu*/\n"
"QMenu{\n"
"    background-color: rgb(51, 55, 61);\n"
"    color: white;\n"
"    selection-color: black;\n"
"    selection-background-color: #E4E4E5;\n"
"}\n"
"\n"
"\n"
"/* VERTICAL SCROLLBAR */\n"
"QScrollBar:vertical\n"
" {\n"
"     background-color: red;\n"
"     width: 15px;\n"
"     margin: 15px 3px 15px 3px;\n"
"     border: 1px transparent #2A2929;\n"
"     border-radius: 4px;\n"
" }\n"
"\n"
"/*  HANDLE BAR VERTICAL */\n"
" QScrollBar::handle:vertical\n"
" {\n"
"     background-color: rgb(35, 35, 38);         /* Handle color */\n"
"     min-height: 5px;\n"
"     border-radius: 4px;\n"
" }\n"
"\n"
"QScrollBar::handle:vertical:hover{    \n"
"    background-color: #0D0D0D;\n"
"}\n"
"QScrollBar::handle:vertical:pressed {    \n"
"    background-color: #0D0D0D;\n"
"}\n"
"\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
" {\n"
"     background: none;\n"
" }\n"
"\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
" {\n"
"     background: none;\n"
" }\n"
"\n"
"/* Disable top and bottom arrows*/\n"
"QScrollBar::add-line:vertical {\n"
"      border: none;\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"      border: none;\n"
"      background: none;\n"
"}\n"
"\n"
"\n"
"/*Slider*/\n"
"\n"
"\n"
"/*\n"
"QSlider::groove:horizontal { \n"
"    background-color: black;\n"
"    border: 0px solid; \n"
"    height: 5px; \n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal { \n"
"    background-color: white; \n"
"    border: 2px solid; \n"
"    width: 10px; \n"
"    height: 20px; \n"
"    line-height: 20px; \n"
"    margin-top: -5px; \n"
"    margin-bottom: -5px; \n"
"    border-radius: 7px; \n"
"}\n"
"*/\n"
"\n"
"QSlider::groove:horizontal {\n"
"    background: white;\n"
"    height: 5px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #49BF88, stop: 1 #7289DA);\n"
"border: 0px solid #777;\n"
"height: 10px;\n"
"border-radius: 7px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"background: #fff;\n"
"border: 1px solid #777;\n"
"height: 10px;\n"
"border-radius: 7px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #eee, stop:1 #ccc);\n"
"border: 1px solid #777;\n"
"width: 13px;\n"
"margin-top: -5px;\n"
"margin-bottom: -5px;\n"
"border-radius: 7px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #fff, stop:1 #ddd);\n"
"border: 1px solid #444;\n"
"border-radius: 7px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 7px;\n"
"}\n"
"\n"
"\n"
"/*Buttons*/\n"
"\n"
"QPushButton{\n"
"    background-color: white;\n"
"    border-radius: 10;\n"
"}\n"
"\n"
"QPushButton:pressed {    \n"
"    background-color: #bcbcbc;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.gridLayout_2.addWidget(self.stackedWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 399, 22))
        self.menubar.setStyleSheet("")
        self.menubar.setObjectName("menubar")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setAutoFillBackground(False)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuObject_detection = QtWidgets.QMenu(self.menubar)
        self.menuObject_detection.setObjectName("menuObject_detection")
        self.menuHaar_Cascade = QtWidgets.QMenu(self.menuObject_detection)
        self.menuHaar_Cascade.setObjectName("menuHaar_Cascade")
        self.menuNavigation = QtWidgets.QMenu(self.menubar)
        self.menuNavigation.setTearOffEnabled(False)
        self.menuNavigation.setObjectName("menuNavigation")
        MainWindow.setMenuBar(self.menubar)
        self.actionView = QtWidgets.QAction(MainWindow)
        self.actionView.setObjectName("actionView")
        self.action_HowToUse = QtWidgets.QAction(MainWindow)
        self.action_HowToUse.setObjectName("action_HowToUse")
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.action_Camera = QtWidgets.QAction(MainWindow)
        self.action_Camera.setCheckable(True)
        self.action_Camera.setChecked(True)
        self.action_Camera.setObjectName("action_Camera")
        self.actionControls = QtWidgets.QAction(MainWindow)
        self.actionControls.setCheckable(True)
        self.actionControls.setChecked(True)
        self.actionControls.setObjectName("actionControls")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setCheckable(True)
        self.actionSettings.setChecked(True)
        self.actionSettings.setObjectName("actionSettings")
        self.actionOutput = QtWidgets.QAction(MainWindow)
        self.actionOutput.setCheckable(True)
        self.actionOutput.setChecked(True)
        self.actionOutput.setObjectName("actionOutput")
        self.actionSettings_2 = QtWidgets.QAction(MainWindow)
        self.actionSettings_2.setObjectName("actionSettings_2")
        self.actionOutput_2 = QtWidgets.QAction(MainWindow)
        self.actionOutput_2.setObjectName("actionOutput_2")
        self.action_SidePanel = QtWidgets.QAction(MainWindow)
        self.action_SidePanel.setCheckable(True)
        self.action_SidePanel.setChecked(True)
        self.action_SidePanel.setObjectName("action_SidePanel")
        self.actionCar_detection = QtWidgets.QAction(MainWindow)
        self.actionCar_detection.setObjectName("actionCar_detection")
        self.action_Settings = QtWidgets.QAction(MainWindow)
        self.action_Settings.setCheckable(True)
        self.action_Settings.setChecked(True)
        self.action_Settings.setObjectName("action_Settings")
        self.action_Output = QtWidgets.QAction(MainWindow)
        self.action_Output.setCheckable(True)
        self.action_Output.setChecked(True)
        self.action_Output.setObjectName("action_Output")
        self.action_MainScreen = QtWidgets.QAction(MainWindow)
        self.action_MainScreen.setObjectName("action_MainScreen")
        self.action_Calibration = QtWidgets.QAction(MainWindow)
        self.action_Calibration.setObjectName("action_Calibration")
        self.action_FaceDetection = QtWidgets.QAction(MainWindow)
        self.action_FaceDetection.setObjectName("action_FaceDetection")
        self.actionYOLO = QtWidgets.QAction(MainWindow)
        self.actionYOLO.setObjectName("actionYOLO")
        self.actionSSD = QtWidgets.QAction(MainWindow)
        self.actionSSD.setObjectName("actionSSD")
        self.menuView.addAction(self.action_Camera)
        self.menuView.addAction(self.action_SidePanel)
        self.menuView.addAction(self.action_Settings)
        self.menuView.addAction(self.action_Output)
        self.menuHelp.addAction(self.action_HowToUse)
        self.menuHelp.addAction(self.action_About)
        self.menuHelp.addSeparator()
        self.menuHaar_Cascade.addAction(self.action_FaceDetection)
        self.menuObject_detection.addAction(self.actionCar_detection)
        self.menuObject_detection.addAction(self.menuHaar_Cascade.menuAction())
        self.menuObject_detection.addAction(self.actionYOLO)
        self.menuObject_detection.addAction(self.actionSSD)
        self.menuNavigation.addAction(self.action_MainScreen)
        self.menuNavigation.addAction(self.action_Calibration)
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuNavigation.menuAction())
        self.menubar.addAction(self.menuObject_detection.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuObject_detection.setTitle(_translate("MainWindow", "Object Detection"))
        self.menuHaar_Cascade.setTitle(_translate("MainWindow", "Haar Cascade"))
        self.menuNavigation.setTitle(_translate("MainWindow", "Navigation"))
        self.actionView.setText(_translate("MainWindow", "View"))
        self.action_HowToUse.setText(_translate("MainWindow", "How to use"))
        self.action_About.setText(_translate("MainWindow", "About"))
        self.action_Camera.setText(_translate("MainWindow", "Camera"))
        self.actionControls.setText(_translate("MainWindow", "Controls"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionOutput.setText(_translate("MainWindow", "Output"))
        self.actionSettings_2.setText(_translate("MainWindow", "Settings"))
        self.actionOutput_2.setText(_translate("MainWindow", "Output"))
        self.action_SidePanel.setText(_translate("MainWindow", "Side panel"))
        self.actionCar_detection.setText(_translate("MainWindow", "CNN"))
        self.action_Settings.setText(_translate("MainWindow", "Settings"))
        self.action_Output.setText(_translate("MainWindow", "Output"))
        self.action_MainScreen.setText(_translate("MainWindow", "Main"))
        self.action_Calibration.setText(_translate("MainWindow", "Calibration"))
        self.action_FaceDetection.setText(_translate("MainWindow", "Face Detection"))
        self.actionYOLO.setText(_translate("MainWindow", "YOLO"))
        self.actionSSD.setText(_translate("MainWindow", "SSD"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
