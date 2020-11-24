# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_loadingWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoadingWindow(object):
    def setupUi(self, LoadingWindow):
        LoadingWindow.setObjectName("LoadingWindow")
        LoadingWindow.resize(680, 400)
        self.centralwidget = QtWidgets.QWidget(LoadingWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_dropShadow = QtWidgets.QFrame(self.centralwidget)
        self.frame_dropShadow.setStyleSheet("QFrame{\n"
"    background-color: rgb(35, 35, 38);\n"
"    border-radius: 10;\n"
"}")
        self.frame_dropShadow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_dropShadow.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_dropShadow.setObjectName("frame_dropShadow")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_dropShadow)
        self.verticalLayout_2.setContentsMargins(-1, 80, -1, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_dropShadow)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(40)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 255, 127);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.frame = QtWidgets.QFrame(self.frame_dropShadow)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(500, 0))
        self.progressBar.setStyleSheet("QProgressBar{\n"
"    background-color: #2F3136;\n"
"    color: white;\n"
"    border-style: none;\n"
"    border-radius: 10;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk{\n"
"     border-radius:10;\n"
"    \n"
"    \n"
"    \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.506, stop:0 rgba(114, 137, 218, 255), stop:1 rgba(0, 255, 127, 255));\n"
"}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_3 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: white;")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_2.addWidget(self.frame)
        self.verticalLayout.addWidget(self.frame_dropShadow)
        LoadingWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoadingWindow)
        QtCore.QMetaObject.connectSlotsByName(LoadingWindow)

    def retranslateUi(self, LoadingWindow):
        _translate = QtCore.QCoreApplication.translate
        LoadingWindow.setWindowTitle(_translate("LoadingWindow", "MainWindow"))
        self.label.setText(_translate("LoadingWindow", "<html><head/><body><p><span style=\" font-weight:600;\">OBJECT </span>DETECTOR</p></body></html>"))
        self.label_2.setText(_translate("LoadingWindow", "Loading..."))
        self.label_3.setText(_translate("LoadingWindow", "<strong>Version:</strong> 1.0"))


