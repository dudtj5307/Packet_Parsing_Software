import time
import threading

from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

from GUI.ui.dialog_progress import Ui_ProgressWindow

'''
              signal        signal
     (parent) <----> (self) <----> (progress)
     
'''

class ProgressWindow(QDialog, Ui_ProgressWindow):
    def __init__(self, parent=None, p_parent=None):
        super(ProgressWindow, self).__init__(parent)
        self.setWindowTitle("Progress")
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        # Parent objects
        self.parent = parent            # parent            (gui_main.py)
        self.p_parent = p_parent        # parent of parent  (PPS.py)

        # Set signal functions
        self.btn_bottom.clicked.connect(self.close_window)

        # Group Objects
        self.progress_bars = [self.progress_bar1, self.progress_bar2, self.progress_bar3]
        self.edit_checks   = [self.edit_check1, self.edit_check2, self.edit_check3]
        self.complete      = [False, False, False]

        # Flag for stopping Process
        self.is_running = True

        self.run()

    def update_progress(self, values):
        if not self.is_running:
            return
        if values == [100, 100, 100]:
            self.is_running = False
            self.finished()

        for idx, val in enumerate(values):
            if val == 100:
                self.progress_bars[idx].setValue(val)
            # Set Check to green color when finished
            # if self.edit_checks[idx][1] and val >= 100:
            #     self.edit_checks[idx][0].setStyleSheet("color: rgb(28, 221, 16);")
            #     self.edit_checks[idx][1] = False
        

        new_vals = [v + 10 for v in values]
        self.update_progress(new_vals)

    def finished(self):
        self.btn_bottom.setText("OK")

    def close_window(self):
        self.btn_bottom.setDisabled(True)
        self.close()
