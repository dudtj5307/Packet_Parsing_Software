import os
from shutil import rmtree

from PyQt6.QtCore import QThread, pyqtSignal

from GUI.gui_progress import ProgressWindow
from utils.config import Config
from utils.monitor import ProgressMonitor
from utils.function_generator import IDL_FUNC_GENERATOR
from utils.packet_parser import RAW_PACKET_PARSER

COMPLETE, STOPPED = True, False


def raw_to_csv_paths(raw_file_paths):
    csv_folder_path = os.path.join(os.getcwd(), 'CSV')
    return list(map(lambda x: os.path.join(csv_folder_path, os.path.split(x)[1].split('.pcap')[0]), raw_file_paths))


class CreateCSV:
    def __init__(self, parent, raw_file_paths):
        # Inherited Variables
        self.parent = parent                    # parent            (gui_main.py)
        self.p_parent = self.parent.parent      # parent of parent  (main.py)
        self.raw_file_paths = raw_file_paths
        self.csv_file_paths = []

        # Progress BackEnd & GUI
        self.progress_backend = ProgressBackend(self.p_parent, raw_file_paths)
        self.progress_window  = ProgressWindow(self.parent)          # Progress GUI (Modal)-'MainWindow'
        # Signal : (Backend) ---> (GUI)
        self.progress_backend.progress_update.connect(self.progress_window.update_progress)
        self.progress_backend.progress_finish.connect(self.progress_window.finish_progress)
        # Signal :   (GUI) ---> (Backend)
        self.progress_window.progress_stopped.connect(self.progress_backend.stop_progress)

    def run(self):
        self.progress_backend.start()
        self.progress_window.exec()

        if self.progress_backend.stopped:
            return STOPPED

        self.csv_file_paths = self.progress_backend.csv_file_paths

class ProgressBackend(QThread):
    progress_update = pyqtSignal(list, name="progress_update")
    progress_finish = pyqtSignal(name="finished")
    def __init__(self, p_pps, raw_file_paths):
        super().__init__(None)
        self.config = Config()
        self.p_pps = p_pps
        self.raw_file_paths = raw_file_paths
        self.csv_file_paths = raw_to_csv_paths(raw_file_paths)
        # Flag for stopping
        self.stopped = False
        self.monitor = ProgressMonitor(backend=self)

    def run_code_generation(self):
        code_generator = IDL_FUNC_GENERATOR()
        # idl_file_paths = get_idl_file_paths()
        idl_file_paths = ["IDL/EIE_Msg.idl", "IDL/TIE_Msg.idl"] * 500  # TODO: For Testing

        self.monitor.update('idl', work_num=len(idl_file_paths))
        for idx, idl_file_path in enumerate(idl_file_paths):
            # Update monitoring and Check if Stopped
            self.monitor.update('idl', work_idx=idx)
            if self.monitor.backend_stopped(): return

            code_generator.run(idl_file_path)

        return code_generator.results

    def run(self):
        # Default IDL Folder Path
        idl_folder_path = os.path.join(os.getcwd(), 'IDL')
        os.makedirs(idl_folder_path, exist_ok=True)

        ## Step 1. Generate 'Parsing Function' from IDL files ##
        generated_code_paths = self.run_code_generation()

        if self.monitor.backend_stopped():  # TODO: [Monitoring] Check if Backend is stopped from GUI
            self.progress_finish.emit()
            return

        ## Step 2. 'Parse Packets' with generated codes ##
        print(generated_code_paths)
        packet_parser = RAW_PACKET_PARSER(generated_code_paths)
        self.monitor.update('parse', work_num=len(self.raw_file_paths))

        # CSV Folder Path
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        for idx, (raw_file_path, csv_file_path) in enumerate(zip(self.raw_file_paths, self.csv_file_paths)):
            # Update monitoring and Check if Stopped
            self.monitor.update('parse', work_idx=idx)
            if self.monitor.backend_stopped(): return

            # Renew CSV file path
            if os.path.exists(csv_file_path):
                rmtree(csv_file_path)
            os.makedirs(csv_file_path, exist_ok=True)

            ## Step 2. Parse Packet Data ##
            packet_parser.run(raw_file_path)

            if self.stopped:  # TODO: [Monitoring] Check if Backend is stopped from GUI
                self.progress_finish.emit()
                return

            ## Step 3. Create CSV Files ##
            self.run_csv_create()

            if self.stopped:  # TODO: [Monitoring] Check if Backend is stopped from GUI
                self.progress_finish.emit()
                # return STOPPED
        self.progress_finish.emit()

    def run_packet_parse(self, raw_file_path, parsing_codes):

        pass

    def run_csv_create(self):
        pass

    def stop_progress(self):
        self.stopped = True



