import sys

from PyQt6 import QtCore, QtGui, QtWidgets

from GUI.ui.dialog_filter import Ui_FilterForm


class CheckboxLabelFrame(QtWidgets.QWidget, Ui_FilterForm):
    def __init__(self, data_set, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.frame)
        self.main_layout.setContentsMargins(10, 5, 5, 5)
        self.main_layout.setSpacing(3)

        self.create_items(data_set)
        self.button_apply.clicked.connect(self.on_apply)
        self.button_close.clicked.connect(self.close)

    def create_items(self, data_set):
        for item in data_set:
            h_layout = QtWidgets.QHBoxLayout()
            checkbox = QtWidgets.QCheckBox(self.frame)
            checkbox.setChecked(True)
            h_layout.addWidget(checkbox)

            label = QtWidgets.QLabel(str(item), self.frame)
            label.setFixedWidth(200)
            label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
            label.setWordWrap(False)
            label.setStyleSheet("text-overflow: ellipsis; white-space: nowrap;")
            h_layout.addWidget(label)

            self.main_layout.addLayout(h_layout)

    def on_apply(self):
        print("Apply 버튼 클릭됨!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    sample_data = {"항목 A", "항목 B", "항목 C", "항목 D"}
    frame = CheckboxLabelFrame(sample_data)
    frame.show()
    sys.exit(app.exec())