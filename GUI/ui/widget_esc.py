# Form implementation generated from reading ui file 'widget_esc.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_WidgetESC(object):
    def setupUi(self, WidgetESC):
        WidgetESC.setObjectName("WidgetESC")
        WidgetESC.resize(335, 86)
        self.label_esc = QtWidgets.QLabel(parent=WidgetESC)
        self.label_esc.setGeometry(QtCore.QRect(0, 0, 331, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_esc.sizePolicy().hasHeightForWidth())
        self.label_esc.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label_esc.setFont(font)
        self.label_esc.setStyleSheet("color: rgb(98, 98, 98);\n"
"background-color: rgba(172, 172, 172, 150);\n"
"\n"
"border-radius: 4px;")
        self.label_esc.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_esc.setObjectName("label_esc")

        self.retranslateUi(WidgetESC)
        QtCore.QMetaObject.connectSlotsByName(WidgetESC)

    def retranslateUi(self, WidgetESC):
        _translate = QtCore.QCoreApplication.translate
        WidgetESC.setWindowTitle(_translate("WidgetESC", "Form"))
        self.label_esc.setText(_translate("WidgetESC", "Press ESC to Exit"))
