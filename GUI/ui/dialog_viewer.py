# Form implementation generated from reading ui file 'dialog_viewer.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ViewerWindow(object):
    def setupUi(self, ViewerWindow):
        ViewerWindow.setObjectName("ViewerWindow")
        ViewerWindow.resize(1018, 641)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ViewerWindow.sizePolicy().hasHeightForWidth())
        ViewerWindow.setSizePolicy(sizePolicy)
        ViewerWindow.setStyleSheet("QMainWindow#ViewerWindow {\n"
"    background-color: rgb(89, 89, 89);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(parent=ViewerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setContentsMargins(-1, -1, -1, 9)
        self.gridLayout_3.setVerticalSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_3 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(10, 31))
        self.frame_3.setMaximumSize(QtCore.QSize(10, 31))
        self.frame_3.setStyleSheet("background-color: transparent;\n"
"border: 0px;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3.addWidget(self.frame_3, 0, 2, 1, 1)
        self.frame_search = QtWidgets.QFrame(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_search.sizePolicy().hasHeightForWidth())
        self.frame_search.setSizePolicy(sizePolicy)
        self.frame_search.setMinimumSize(QtCore.QSize(300, 31))
        self.frame_search.setMaximumSize(QtCore.QSize(300, 31))
        self.frame_search.setStyleSheet("QFrame {\n"
"    border: 1px solid gray;\n"
"    border-radius: 8px;\n"
"    background-color: rgb(255, 255, 255);\n"
"}")
        self.frame_search.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_search.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_search.setObjectName("frame_search")
        self.edit_text_input = QtWidgets.QLineEdit(parent=self.frame_search)
        self.edit_text_input.setGeometry(QtCore.QRect(10, 5, 101, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_text_input.sizePolicy().hasHeightForWidth())
        self.edit_text_input.setSizePolicy(sizePolicy)
        self.edit_text_input.setStyleSheet("border: 0px;\n"
"background-color: rgb(255, 255, 255);")
        self.edit_text_input.setText("")
        self.edit_text_input.setObjectName("edit_text_input")
        self.button_forward = QtWidgets.QPushButton(parent=self.frame_search)
        self.button_forward.setEnabled(False)
        self.button_forward.setGeometry(QtCore.QRect(215, 4, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.button_forward.setFont(font)
        self.button_forward.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.button_forward.setStyleSheet("QPushButton {\n"
"    color: rgb(50, 50, 100);\n"
"    background-color: white;\n"
"    border: 0px;    \n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: lightgray;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(200,200,200);\n"
"}")
        self.button_forward.setObjectName("button_forward")
        self.button_backward = QtWidgets.QPushButton(parent=self.frame_search)
        self.button_backward.setEnabled(False)
        self.button_backward.setGeometry(QtCore.QRect(240, 4, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.button_backward.setFont(font)
        self.button_backward.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.button_backward.setStyleSheet("QPushButton {\n"
"    color: rgb(50, 50, 100);\n"
"    background-color: white;\n"
"    border: 0px;    \n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: lightgray;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(200,200,200);\n"
"}")
        self.button_backward.setObjectName("button_backward")
        self.button_close = QtWidgets.QPushButton(parent=self.frame_search)
        self.button_close.setEnabled(True)
        self.button_close.setGeometry(QtCore.QRect(270, 4, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.button_close.setFont(font)
        self.button_close.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.button_close.setStyleSheet("QPushButton {\n"
"    color: rgb(100, 100, 100);\n"
"    background-color: white;\n"
"    border: 0px;    \n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: lightgray;\n"
"}")
        self.button_close.setObjectName("button_close")
        self.label_idx_count = QtWidgets.QLabel(parent=self.frame_search)
        self.label_idx_count.setGeometry(QtCore.QRect(115, 5, 91, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_idx_count.sizePolicy().hasHeightForWidth())
        self.label_idx_count.setSizePolicy(sizePolicy)
        self.label_idx_count.setMinimumSize(QtCore.QSize(31, 21))
        self.label_idx_count.setMaximumSize(QtCore.QSize(100, 21))
        self.label_idx_count.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_idx_count.setStyleSheet("color: rgb(50, 50, 50);\n"
"border: 0px;")
        self.label_idx_count.setText("")
        self.label_idx_count.setScaledContents(False)
        self.label_idx_count.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_idx_count.setObjectName("label_idx_count")
        self.edit_text_input.raise_()
        self.button_close.raise_()
        self.button_backward.raise_()
        self.button_forward.raise_()
        self.label_idx_count.raise_()
        self.gridLayout_3.addWidget(self.frame_search, 0, 1, 1, 1)
        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_2.setStyleSheet("QFrame#frame_2 {\n"
"    background-color: transparent;\n"
"    border: 0px\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.button_yellow = QtWidgets.QPushButton(parent=self.frame_2)
        self.button_yellow.setEnabled(True)
        self.button_yellow.setGeometry(QtCore.QRect(260, 20, 39, 19))
        self.button_yellow.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 247, 1);\n"
"    border: 1px solid black;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"   \n"
"    background-color: rgb(208, 208, 0);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(200,200,200);\n"
"}")
        self.button_yellow.setText("")
        self.button_yellow.setObjectName("button_yellow")
        self.button_green = QtWidgets.QPushButton(parent=self.frame_2)
        self.button_green.setEnabled(True)
        self.button_green.setGeometry(QtCore.QRect(300, 20, 39, 19))
        self.button_green.setStyleSheet("QPushButton {\n"
"    background-color: rgb(0, 255, 60);\n"
"    border: 1px solid black;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    \n"
"    background-color: rgb(55, 166, 0);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(200,200,200);\n"
"}")
        self.button_green.setText("")
        self.button_green.setObjectName("button_green")
        self.button_blue = QtWidgets.QPushButton(parent=self.frame_2)
        self.button_blue.setEnabled(True)
        self.button_blue.setGeometry(QtCore.QRect(340, 20, 39, 19))
        self.button_blue.setStyleSheet("QPushButton {\n"
"    background-color: rgb(0, 89, 255);\n"
"    border: 1px solid black;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 15, 149);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(200,200,200);\n"
"}")
        self.button_blue.setText("")
        self.button_blue.setObjectName("button_blue")
        self.button_white = QtWidgets.QPushButton(parent=self.frame_2)
        self.button_white.setEnabled(True)
        self.button_white.setGeometry(QtCore.QRect(180, 20, 39, 19))
        self.button_white.setStyleSheet("QPushButton {\n"
"    background-color: rgb(253, 253, 253);\n"
"    border: 1px solid black;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: lightgray;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(200,200,200);\n"
"}")
        self.button_white.setText("")
        self.button_white.setObjectName("button_white")
        self.button_red = QtWidgets.QPushButton(parent=self.frame_2)
        self.button_red.setEnabled(True)
        self.button_red.setGeometry(QtCore.QRect(220, 20, 39, 19))
        self.button_red.setStyleSheet("QPushButton {\n"
"    background-color: rgb(223, 20, 23);\n"
"    border: 1px solid black;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"   background-color: rgb(172, 2, 5);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(200,200,200);\n"
"}")
        self.button_red.setText("")
        self.button_red.setObjectName("button_red")
        self.button_none = QtWidgets.QPushButton(parent=self.frame_2)
        self.button_none.setEnabled(True)
        self.button_none.setGeometry(QtCore.QRect(160, 22, 16, 16))
        font = QtGui.QFont()
        font.setBold(True)
        self.button_none.setFont(font)
        self.button_none.setStyleSheet("QPushButton {\n"
"    background-color: rgb(200, 200, 200);\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: lightgray;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(200,200,200);\n"
"}")
        self.button_none.setObjectName("button_none")
        self.gridLayout_3.addWidget(self.frame_2, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setStyleSheet("border: 0px;")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.table_csv = QtWidgets.QTableView(parent=self.frame)
        self.table_csv.setStyleSheet("")
        self.table_csv.setObjectName("table_csv")
        self.gridLayout.addWidget(self.table_csv, 0, 1, 1, 1)
        self.list_csv_names = QtWidgets.QListWidget(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_csv_names.sizePolicy().hasHeightForWidth())
        self.list_csv_names.setSizePolicy(sizePolicy)
        self.list_csv_names.setMinimumSize(QtCore.QSize(140, 0))
        self.list_csv_names.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.list_csv_names.setFont(font)
        self.list_csv_names.setStyleSheet("QListView {\n"
"    background-color: rgb(253, 253, 253);\n"
"}\n"
"/*\n"
"QListView::item {\n"
"    border-bottom: 1px solid rgb(225, 225, 225);     // 아이템 사이 회색 구분선\n"
"    padding-left: 2px;         // 텍스트와 구분선 사이 여백\n"
"    background: none;\n"
"}\n"
"*/\n"
"\n"
"QListView::item:selected { \n"
"    background-color: rgb(100, 149, 237); \n"
"    color: white;\n"
"}\n"
"\n"
"QListView::item:hover { \n"
"    background-color: rgb(230, 230, 255); \n"
"    color: black;\n"
"}\n"
"")
        self.list_csv_names.setObjectName("list_csv_names")
        self.gridLayout.addWidget(self.list_csv_names, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame, 1, 0, 1, 3)
        ViewerWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ViewerWindow)
        QtCore.QMetaObject.connectSlotsByName(ViewerWindow)

    def retranslateUi(self, ViewerWindow):
        _translate = QtCore.QCoreApplication.translate
        ViewerWindow.setWindowTitle(_translate("ViewerWindow", "MainWindow"))
        self.edit_text_input.setToolTip(_translate("ViewerWindow", "Find Text (Enter)"))
        self.edit_text_input.setPlaceholderText(_translate("ViewerWindow", "Find Text (Enter)"))
        self.button_forward.setToolTip(_translate("ViewerWindow", "Previous (F2)"))
        self.button_forward.setText(_translate("ViewerWindow", "<"))
        self.button_backward.setToolTip(_translate("ViewerWindow", "Next (F3)"))
        self.button_backward.setText(_translate("ViewerWindow", ">"))
        self.button_close.setToolTip(_translate("ViewerWindow", "Close (ESC)"))
        self.button_close.setText(_translate("ViewerWindow", "×"))
        self.button_none.setText(_translate("ViewerWindow", "X"))
