from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QObject, pyqtSignal

from GUI.ui.dialog_progress import Ui_ProgressWindow

class ProgressWindow(QDialog, Ui_ProgressWindow):
    # Static Attribute
    stop_create = pyqtSignal()

    def __init__(self, parent=None, p_parent=None):
        super(ProgressWindow, self).__init__(parent)
        self.setWindowTitle("Progress")
        self.setupUi(self)

        # Parent Objects
        self.parent = parent            # parent            (gui_main.py)
        self.p_parent = p_parent        # parent of parent  (PPS.py)

        # Group Objects
        self.progress_bars = [self.progress_bar1, self.progress_bar2, self.progress_bar3]
        for progress_bar in self.progress_bars:
            progress_bar.not_finished = True        # flag for changing 'edit_check' color
        self.edit_checks = [self.edit_check1, self.edit_check2, self.edit_check3]

        # Set Signal Functions
        self.btn_bottom.clicked.connect(self.button_clicked)




        self.mode_running = True  # True : Running (Stop Button) / False : Finished (OK Button)



    def button_clicked(self):
        if self.mode_running:           # Running (Stop Button)
            self.parent.stop_create.emit()
        else:                           # Finished (OK Button)
            self.close()

    def update_progress(self, progresses):
        for i in range(3):
            self.progress_bars[i].setValue(progresses[i])
            if self.progress_bars[i].not_finished and progresses[i] >= 100:
                print('checked!')
                # Set Check to green color
                self.edit_checks[i].setStyleSheet("color: rgb(28, 221, 16); background-color: transparent;")
                self.progress_bars[i].not_finished = False

    def set_finished(self):
        self.mode_running = False       # Finished (OK Button)
        self.btn_bottom.setText("OK")
