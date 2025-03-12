import os

from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal

from GUI.ui.dialog_progress import Ui_ProgressWindow
'''
              signal        signal
     (parent) <----> (self) <----> (progress)
     
'''
class ProgressWindow(QDialog, Ui_ProgressWindow):
    progress_stopped = pyqtSignal()

    def __init__(self, parent=None):
        super(ProgressWindow, self).__init__(parent)
        # super().__init__()
        self.setWindowTitle("Progress")
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(parent.icon_path, "button_csv_create.png")))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)

        # Parent objects
        self.parent = parent            # parent            (gui_main.py)

        # Set signal functions
        self.btn_bottom.clicked.connect(self.button_clicked)

        # Group Objects
        self.progress_bars = [self.progress_bar1, self.progress_bar2, self.progress_bar3]
        self.edit_checks   = [self.edit_check1, self.edit_check2, self.edit_check3]
        self.complete      = [False, False, False]

        self.backend_finished = False
        self.gui_stopped = False

    def update_progress(self, values):
        for idx, val in enumerate(values):
            self.progress_bars[idx].setValue(val)
            # Set Check to green color when finished
            if not self.complete[idx] and val >= 100:
                self.edit_checks[idx].setStyleSheet("color: rgb(28, 221, 16);background-color: transparent;")
                self.complete[idx] = False

    def finish_progress(self):
        if self.gui_stopped:
            self.close()
        else:
            self.btn_bottom.setText("OK")
            self.backend_finished = True

    def button_clicked(self):
        if self.backend_finished:
            self.close()
        else:
            self.gui_stopped = True
            self.progress_stopped.emit()

    def keyPressEvent(self, event):
        # Ignore ESC Key during parsing
        if not self.backend_finished and event.key() == Qt.Key.Key_Escape:
            return
        else:
            super(ProgressWindow, self).keyPressEvent(event)