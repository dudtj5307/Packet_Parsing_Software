import os
import sys
import time

import threading
from PyQt6.QtCore import QObject, QThread, pyqtSignal

from GUI.gui_progress import ProgressWindow

class ProgressBackend(QThread):
    progress_update = pyqtSignal(list, name="progress_update")
    progress_finish = pyqtSignal(name="finished")

    def __init__(self, parent=None):
        super().__init__(parent)
        # Parent Objects
        self.parent = parent            # (gui_main.py)
        # Flag for running & stopping
        self.is_running = True

    def run(self):
        self.run_code_generation()
        # Default Folder Path
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        self.run_packet_parse()
        self.run_csv_create()

        self.progress_finish.emit()

    def run_code_generation(self):
        pass

    def run_packet_parse(self):
        # print("run_packet_parse")
        pass

    def run_csv_create(self):
        pass

    def stop_backend(self):
        self.is_running = False

######
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        self.parent.csv_file_paths = list(map(lambda x: os.path.join(csv_folder_path, os.path.split(x)[1].split('.pcap')[0]),
                                       self.parent.raw_file_paths))
        progresses = [0, 0, 0]
        file_num = len(self.parent.raw_file_paths)
        for raw_file_path, new_folder_path in zip(self.parent.raw_file_paths, self.parent.csv_file_paths):
            # Make CSV folder
            if os.path.exists(new_folder_path):
                rmtree(new_folder_path)
            os.makedirs(new_folder_path, exist_ok=True)
            # Parse Msg TODO
            # result = parse_msg.raw_to_csv(self.parent, raw_file_path)
            # print("result", result)
#####

class RawToCSV:
    def __init__(self, parent, raw_file_paths):
        # Inherited Variables
        self.parent = parent            # parent            (gui_main.py)
        # self.p_parent = p_parent        # parent of parent  (PPS.py)
        self.raw_file_paths = raw_file_paths

        # Progress GUI
        self.progress_window = ProgressWindow(self.parent)

        # Backend thread
        self.progress_backend = ProgressBackend()
        self.progress_backend.progress_update.connect(self.progress_window.update_progress)
        self.progress_backend.progress_finish.connect(self.progress_window.finish_progress)
        self.progress_window.progress_stopped.connect(self.progress_backend.stop_backend)

    def run(self):
        self.progress_backend.start()
        self.progress_window.exec()

