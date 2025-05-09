# Form implementation generated from reading ui file 'dialog_filter.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FilterForm(object):
    def setupUi(self, FilterForm):
        FilterForm.setObjectName("FilterForm")
        FilterForm.setWindowModality(QtCore.Qt.WindowModality.NonModal)
        FilterForm.resize(175, 67)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FilterForm.sizePolicy().hasHeightForWidth())
        FilterForm.setSizePolicy(sizePolicy)
        FilterForm.setMaximumSize(QtCore.QSize(600, 600))
        FilterForm.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        FilterForm.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        FilterForm.setStyleSheet("QWidget#FilterForm {\n"
"    border: 1px solid rgb(158, 158, 158);\n"
"}")
        self.formLayout = QtWidgets.QFormLayout(FilterForm)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.formLayout.setContentsMargins(3, 0, 3, 3)
        self.formLayout.setHorizontalSpacing(3)
        self.formLayout.setVerticalSpacing(2)
        self.formLayout.setObjectName("formLayout")
        self.scrollArea = QtWidgets.QScrollArea(parent=FilterForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 10))
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea.setStyleSheet("QScrollArea#scrollArea {\n"
"    border: 1px solid rgb(158, 158, 158);\n"
"    background-color: rgb(255, 255, 255);\n"
"}")
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 167, 36))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        self.gridLayout_2.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(parent=self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.verticalLayout.setContentsMargins(5, 2, -1, -1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.master_checkbox = QtWidgets.QCheckBox(parent=self.widget)
        self.master_checkbox.setChecked(True)
        self.master_checkbox.setObjectName("master_checkbox")
        self.verticalLayout.addWidget(self.master_checkbox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.scrollArea)
        self.button_apply = QtWidgets.QPushButton(parent=FilterForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_apply.sizePolicy().hasHeightForWidth())
        self.button_apply.setSizePolicy(sizePolicy)
        self.button_apply.setMinimumSize(QtCore.QSize(83, 0))
        self.button_apply.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.button_apply.setObjectName("button_apply")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.button_apply)
        self.button_close = QtWidgets.QPushButton(parent=FilterForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_close.sizePolicy().hasHeightForWidth())
        self.button_close.setSizePolicy(sizePolicy)
        self.button_close.setMinimumSize(QtCore.QSize(83, 0))
        self.button_close.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.button_close.setObjectName("button_close")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.button_close)

        self.retranslateUi(FilterForm)
        QtCore.QMetaObject.connectSlotsByName(FilterForm)

    def retranslateUi(self, FilterForm):
        _translate = QtCore.QCoreApplication.translate
        FilterForm.setWindowTitle(_translate("FilterForm", "Filter"))
        self.master_checkbox.setText(_translate("FilterForm", "(Select All)"))
        self.button_apply.setText(_translate("FilterForm", "Apply"))
        self.button_close.setText(_translate("FilterForm", "Close"))
