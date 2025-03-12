import os
import sys
import time
from shutil import rmtree

import threading
from PyQt6.QtCore import QObject, QThread, pyqtSignal

from GUI.gui_progress import ProgressWindow
from IDL.function_generator import IDL_FUNC_GENERATOR
from IDL.packet_parser import RAW_PACKET_PARSER

COMPLETE, STOPPED = True, False

class ProgressRawToCSV:
    def __init__(self, parent, raw_file_paths):
        # Inherited Variables
        self.parent = parent                    # parent            (gui_main.py)
        self.p_parent = self.parent.parent      # parent of parent  (PPS.py)
        self.raw_file_paths = raw_file_paths
        self.csv_file_paths = []

        # Progress BackEnd & GUI
        self.progress_backend = ProgressBackend(self.p_parent, raw_file_paths)
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

class ProgressMonitor():
    def __init__(self, backend):
        self.backend = backend

        # Progress of each stage (int: 0~100)
        self.progress = {'idl': 0, 'parse': 0, 'csv': 0}

        self.total_idl_file = 0
        self.total_pkt_num = 0
        self.total_csv_num = 0

    def update(self, key, value):
        self.progress[key] = min(int(value + 0.5), 100)
        self.backend.progress_update([self.progress['idl'], self.progress['parse'], self.progress['csv']]).emit()

def raw_to_csv_path(raw_file_paths):
    csv_folder_path = os.path.join(os.getcwd(), 'CSV')
    return list(map(lambda x: os.path.join(csv_folder_path, os.path.split(x)[1].split('.pcap')[0]), raw_file_paths))

class ProgressBackend(QThread):
    progress_update = pyqtSignal(list, name="progress_update")
    progress_finish = pyqtSignal(name="finished")

    def __init__(self, p_pps, raw_file_paths):
        super().__init__(None)
        self.p_pps = p_pps
        self.raw_file_paths = raw_file_paths
        self.csv_file_paths = raw_to_csv_path(raw_file_paths)
        # Flag for stopping
        self.stopped = False

        self.monitor = ProgressMonitor(self)

    def run_code_generation(self):
        code_generator = IDL_FUNC_GENERATOR(backend=self)
        # idl_file_paths = get_idl_file_paths()
        idl_file_paths = ["IDL/EIE_Msg.idl", "IDL/TIE_Msg.idl", "IDL/EIE_Msg.idl", "IDL/TIE_Msg.idl", "IDL/EIE_Msg.idl", "IDL/TIE_Msg.idl"]
        for idx, idl_file_path in enumerate(idl_file_paths):

            if code_generator.run(idl_file_path) == STOPPED:
                return STOPPED
        return code_generator.results

    def run_packet_parse(self, raw_file_path, parsing_codes):

        pass

    def run_csv_create(self):
        pass

    def run(self):
        # Default IDL Folder Path
        idl_folder_path = os.path.join(os.getcwd(), 'IDL')
        os.makedirs(idl_folder_path, exist_ok=True)

        ## Step 1. Generate Parsing Function ##
        generated_code_paths = self.run_code_generation()

        if self.stopped:  # TODO: [Monitoring] Check if Backend is stopped from GUI
            self.progress_finish.emit()
            return STOPPED

        packet_parser = RAW_PACKET_PARSER(generated_code_paths, backend=self)

        # CSV Folder Path
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        for raw_file_path, csv_file_path in zip(self.raw_file_paths, self.csv_file_paths):

            # Renew CSV file path
            if os.path.exists(csv_file_path):
                rmtree(csv_file_path)
            os.makedirs(csv_file_path, exist_ok=True)

            ## Step 2. Parse Packet Data ##
            packet_parser.run(raw_file_path)

            if self.stopped:  # TODO: [Monitoring] Check if Backend is stopped from GUI
                self.progress_finish.emit()
                return STOPPED

            ## Step 3. Create CSV Files ##
            self.run_csv_create()

            if self.stopped:  # TODO: [Monitoring] Check if Backend is stopped from GUI
                self.progress_finish.emit()
                return STOPPED

        self.progress_finish.emit()

    def stop_progress(self):
        self.stopped = True



