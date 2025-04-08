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
        self.progress_bars = {'idl': self.progress_bar1, 'parse': self.progress_bar2, 'csv': self.progress_bar3}
        self.edit_checks   = {'idl': self.edit_check1, 'parse': self.edit_check2, 'csv': self.edit_check3}
        self.complete      = {'idl': False, 'parse': False, 'csv': False}

        self.backend_finished = False
        self.gui_stopped = False

    def update_progress(self, values):
        key, val = values
        self.progress_bars[key].setValue(val)
        # Set Check to green color when finished
        if not self.complete[key] and val >= 100:
            self.edit_checks[key].setStyleSheet("color: rgb(28, 221, 16);background-color: transparent;")
            self.complete[key] = False

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