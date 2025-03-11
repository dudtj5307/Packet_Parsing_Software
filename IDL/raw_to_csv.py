import os
import sys
import time
from shutil import rmtree

import threading
from PyQt6.QtCore import QObject, QThread, pyqtSignal

from GUI.gui_progress import ProgressWindow
from IDL.generate_function import IDL_FUNC_GENERATOR

COMPLETE, STOPPED = True, False

class ProgressRawToCSV:
    def __init__(self, parent, raw_file_paths):
        # Inherited Variables
        self.parent = parent            # parent            (gui_main.py)
        # self.p_parent = p_parent        # parent of parent  (PPS.py)
        self.raw_file_paths = raw_file_paths
        self.csv_file_paths = []

        # Progress BackEnd & GUI
        self.progress_backend = ProgressBackend(raw_file_paths)
        self.progress_window = ProgressWindow(self.parent)          # Progress GUI (Modal)-'MainWindow'
        # Signal : (Backend) ---> (GUI)
        self.progress_backend.progress_update.connect(self.progress_window.update_progress)
        self.progress_backend.progress_finish.connect(self.progress_window.finish_progress)
        # Signal :   (GUI) ---> (Backend)
        self.progress_window.progress_stopped.connect(self.progress_backend.stop_progress)

    def run(self):
        self.progress_backend.start()
        self.progress_window.exec()

        self.csv_file_paths = self.progress_backend.csv_file_paths
        return not self.progress_backend.stopped


def raw_to_csv_path(raw_file_paths):
    csv_folder_path = os.path.join(os.getcwd(), 'CSV')
    return list(map(lambda x: os.path.join(csv_folder_path, os.path.split(x)[1].split('.pcap')[0]), raw_file_paths))


class ProgressBackend(QThread):
    progress_update = pyqtSignal(list, name="progress_update")
    progress_finish = pyqtSignal(name="finished")

    def __init__(self, raw_file_paths):
        super().__init__(None)
        self.raw_file_paths = raw_file_paths
        self.csv_file_paths = raw_to_csv_path(raw_file_paths)

        # Flag for stopping
        self.stopped = False

    def run_code_generation(self):
        code_generator = IDL_FUNC_GENERATOR(self)
        # idl_file_paths = get_idl_file_paths()
        idl_file_paths = ["IDL/EIE_Msg.idl", "IDL/TIE_Msg.idl"]
        for idl_file_path in idl_file_paths:
            if code_generator.run(idl_file_path) == STOPPED:
                return STOPPED
        return code_generator.results

    def run_packet_parse(self, raw_file_path):
        # print("run_packet_parse")
        pass

    def run_csv_create(self):
        pass

    def run(self):
        # Default IDL Folder Path
        idl_folder_path = os.path.join(os.getcwd(), 'IDL')
        os.makedirs(idl_folder_path, exist_ok=True)

        ## Step 1. Generate Parsing Function ##
        self.run_code_generation()

        # Default CSV Folder Path
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        for raw_file_path, csv_file_path in zip(self.raw_file_paths, self.csv_file_paths):

            if os.path.exists(csv_file_path):
                rmtree(csv_file_path)
            os.makedirs(csv_file_path, exist_ok=True)

            ## Step 2. Parse Packet Data ##
            self.run_packet_parse(raw_file_path)

            ## Step 3. Create CSV Files ##
            self.run_csv_create()

        self.progress_finish.emit()

    def stop_progress(self):
        self.stopped = True

######
        # progresses = [0, 0, 0]
        # file_num = len(self.parent.raw_file_paths)
        # for raw_file_path, new_folder_path in zip(self.parent.raw_file_paths, self.parent.csv_file_paths):
        #     # Make CSV folder
        #     if os.path.exists(new_folder_path):
        #         rmtree(new_folder_path)
        #     os.makedirs(new_folder_path, exist_ok=True)
        #     # Parse Msg TODO
        #     # result = parse_msg.raw_to_csv(self.parent, raw_file_path)
        #     # print("result", result)
#####



