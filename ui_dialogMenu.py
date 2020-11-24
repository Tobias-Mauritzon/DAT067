# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dialogMenu_calibration.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(473, 300)
        Dialog.setStyleSheet("/*Buttons*/\n"
"\n"
"QPushButton{\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 10;\n"
"}\n"
"\n"
"QPushButton:pressed {    \n"
"    background-color: #bcbcbc;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setStyleSheet("QFrame{\n"
"    background-color: #232326;\n"
"    border-radius: 10;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(20, 12, 20, 12)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Label_title = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_title.sizePolicy().hasHeightForWidth())
        self.Label_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.Label_title.setFont(font)
        self.Label_title.setStyleSheet("background-color: none; color: white;")
        self.Label_title.setObjectName("Label_title")
        self.verticalLayout_2.addWidget(self.Label_title, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.Label_informationText = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_informationText.sizePolicy().hasHeightForWidth())
        self.Label_informationText.setSizePolicy(sizePolicy)
        self.Label_informationText.setMinimumSize(QtCore.QSize(390, 0))
        self.Label_informationText.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.Label_informationText.setFont(font)
        self.Label_informationText.setStyleSheet("background-color: none; color: white;")
        self.Label_informationText.setTextFormat(QtCore.Qt.AutoText)
        self.Label_informationText.setScaledContents(False)
        self.Label_informationText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Label_informationText.setWordWrap(True)
        self.Label_informationText.setObjectName("Label_informationText")
        self.verticalLayout_2.addWidget(self.Label_informationText, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.PushButton_top = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PushButton_top.sizePolicy().hasHeightForWidth())
        self.PushButton_top.setSizePolicy(sizePolicy)
        self.PushButton_top.setMinimumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PushButton_top.setFont(font)
        self.PushButton_top.setObjectName("PushButton_top")
        self.verticalLayout_3.addWidget(self.PushButton_top, 0, QtCore.Qt.AlignHCenter)
        self.PushButton_bottom = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PushButton_bottom.sizePolicy().hasHeightForWidth())
        self.PushButton_bottom.setSizePolicy(sizePolicy)
        self.PushButton_bottom.setMinimumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.PushButton_bottom.setFont(font)
        self.PushButton_bottom.setObjectName("PushButton_bottom")
        self.verticalLayout_3.addWidget(self.PushButton_bottom, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Label_title.setText(_translate("Dialog", "<strong>Calibration</strong> is needed!"))
        self.Label_informationText.setText(_translate("Dialog", "In order to use the distance calculation feature of the application, you need to calibrate your camera."))
        self.PushButton_top.setText(_translate("Dialog", "Calibrate camera"))
        self.PushButton_bottom.setText(_translate("Dialog", "Skip"))

