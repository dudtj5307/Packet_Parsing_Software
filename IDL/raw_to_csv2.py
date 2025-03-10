import sys
import time

import threading
from PyQt6.QtCore import QObject, QThread, pyqtSignal

from GUI.gui_progress import ProgressWindow

class ProgressBackend(QThread):
    progress_update = pyqtSignal(list, name="progress_update")
    progress_finish = pyqtSignal(name="finished")

    def run(self):
        self.is_running = True
        self.run_code_generation()
        self.run_packet_parse()
        self.run_csv_create()

        self.progress_finish.emit()

    def run_code_generation(self):
        print("[code_generation] started")
        a = [0, 0, 0]
        for i in range(1000):
            if not self.is_running:
                print("Stopped!!")
                return
            a = [min(a[0]+4,100), 0, 0]
            time.sleep(0.1)
            inta = list(map(lambda x: int(x+0.5), a))
            self.progress_update.emit(inta)
            if a[0] == 100:
                break
        print("[code_generation] Finished")

    def run_packet_parse(self):
        # print("run_packet_parse")
        pass

    def run_csv_create(self):
        print("[csv_create] Started")
        a = [100, 0, 0]
        for i in range(1000):
            if not self.is_running:
                print("Stopped!!")
                return
            a = [100, min(a[1]+0.2,100), min(a[2]+0.15,100)]
            time.sleep(0.01)
            inta = list(map(lambda x: int(x+0.5), a))
            self.progress_update.emit(inta)
            if a[2] == 100:
                break
        print("[csv_create] Finished")

    def stop_backend(self):
        self.is_running = False

class RawToCSV:
    def __init__(self, parent, p_parent, raw_file_paths):
        # Inherited Variables
        self.parent = parent            # parent            (gui_main.py)
        self.p_parent = p_parent        # parent of parent  (PPS.py)
        self.raw_file_paths = raw_file_paths

        # Progress GUI
        # self.progress_window = ProgressWindow(self.parent, self.p_parent)

        self.progress_window = ProgressWindow(self.parent, self.p_parent)

        # Backend thread
        self.progress_backend = ProgressBackend()
        self.progress_backend.progress_update.connect(self.progress_window.update_progress)
        self.progress_backend.progress_finish.connect(self.progress_window.finish_progress)
        self.progress_window.progress_stopped.connect(self.progress_backend.stop_backend)

    def run(self):
        self.progress_backend.start()
        self.progress_window.exec()

