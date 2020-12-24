# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dialogMenu.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 558)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(800, 800))
        Dialog.setStyleSheet("QFrame{\n"
"    background-color: rgb(51, 55, 61);\n"
"    border-radius: 10;\n"
"}\n"
"\n"
"/*Buttons*/\n"
"QPushButton{\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 10;\n"
"}\n"
"\n"
"QPushButton:pressed {    \n"
"    background-color: #bcbcbc;\n"
"}\n"
"\n"
"/* VERTICAL SCROLLBAR */\n"
"QScrollBar:vertical\n"
" {\n"
"     background-color: gray;\n"
"     width: 15px;\n"
"     margin: 15px 3px 15px 3px;\n"
"     border: 1px transparent #2A2929;\n"
"     border-radius: 4px;\n"
" }\n"
"\n"
"/*  HANDLE BAR VERTICAL */\n"
" QScrollBar::handle:vertical\n"
" {\n"
"    background-color: rgb(67, 67, 67);  /* Handle color */\n"
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
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
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
        self.image_label = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy)
        self.image_label.setText("")
        self.image_label.setScaledContents(True)
        self.image_label.setObjectName("image_label")
        self.verticalLayout_2.addWidget(self.image_label)
        self.frame_text = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_text.sizePolicy().hasHeightForWidth())
        self.frame_text.setSizePolicy(sizePolicy)
        self.frame_text.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_text.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_text.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_text.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_text.setObjectName("frame_text")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_text)
        self.verticalLayout_5.setContentsMargins(9, 40, -1, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scrollArea = QtWidgets.QScrollArea(self.frame_text)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea.setAutoFillBackground(False)
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 746, 148))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setStyleSheet("background-color: rgb(51, 55, 61);")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.textFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textFrame.sizePolicy().hasHeightForWidth())
        self.textFrame.setSizePolicy(sizePolicy)
        self.textFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.textFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.textFrame.setObjectName("textFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.textFrame)
        self.verticalLayout_4.setContentsMargins(25, 0, 25, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Label_informationText = QtWidgets.QLabel(self.textFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_informationText.sizePolicy().hasHeightForWidth())
        self.Label_informationText.setSizePolicy(sizePolicy)
        self.Label_informationText.setMinimumSize(QtCore.QSize(0, 0))
        self.Label_informationText.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.Label_informationText.setFont(font)
        self.Label_informationText.setStyleSheet("color: white;")
        self.Label_informationText.setText("")
        self.Label_informationText.setTextFormat(QtCore.Qt.AutoText)
        self.Label_informationText.setScaledContents(True)
        self.Label_informationText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Label_informationText.setWordWrap(True)
        self.Label_informationText.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.Label_informationText.setObjectName("Label_informationText")
        self.verticalLayout_4.addWidget(self.Label_informationText)
        self.verticalLayout_6.addWidget(self.textFrame, 0, QtCore.Qt.AlignVCenter)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_5.addWidget(self.scrollArea)
        self.verticalLayout_2.addWidget(self.frame_text)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.PushButton_top = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PushButton_bottom.sizePolicy().hasHeightForWidth())
        self.PushButton_bottom.setSizePolicy(sizePolicy)
        self.PushButton_bottom.setMinimumSize(QtCore.QSize(100, 30))
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
        self.Label_title.setText(_translate("Dialog", "<html><head/><body><p>TITLE</p></body></html>"))
        self.PushButton_top.setText(_translate("Dialog", "Top Button"))
        self.PushButton_bottom.setText(_translate("Dialog", "Bottom Button"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
