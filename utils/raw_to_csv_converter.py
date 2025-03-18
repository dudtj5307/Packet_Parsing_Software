import os
from shutil import rmtree

from PyQt6.QtCore import QThread, pyqtSignal

from GUI.gui_progress import ProgressWindow
from utils.config import Config
from utils.monitor import ProgressMonitor
from utils.function_generator import ParsingFunctionGenerator
from utils.packet_parser import PacketParser
from utils.csv_creator import CsvCreator

COMPLETE, STOPPED = True, False


def raw_to_csv_paths(raw_file_paths):
    csv_folder_path = os.path.join(os.getcwd(), 'CSV')
    return list(map(lambda x: os.path.join(csv_folder_path, os.path.split(x)[1].split('.pcap')[0]), raw_file_paths))


class RawToCSVConverter:
    def __init__(self, parent, raw_file_paths):
        # Inherited Variables
        self.raw_file_paths = raw_file_paths
        self.csv_file_paths = []

        # Progress GUI & Backend
        self.progress_window = ProgressWindow(parent)  # Progress GUI (Modal)-'MainWindow'
        self.progress_backend = ProgressBackend(raw_file_paths)

        # Signal :   (GUI) ---> (Backend)
        self.progress_window.progress_stopped.connect(self.progress_backend.stop_progress)
        # Signal : (Backend) ---> (GUI)
        self.progress_backend.progress_update.connect(self.progress_window.update_progress)
        self.progress_backend.progress_finish.connect(self.progress_window.finish_progress)

    def run(self):
        self.progress_backend.start()
        self.progress_window.exec()


def get_idl_files():
    return [file for file in os.listdir(os.path.join(os.getcwd(), 'IDL')) if file.endswith(('.idl', '.h'))]


class ProgressBackend(QThread):
    progress_update = pyqtSignal(list, name="progress_update")
    progress_finish = pyqtSignal(name="finished")

    def __init__(self, raw_file_paths):
        super().__init__(None)
        self.config = Config()
        self.raw_file_paths = raw_file_paths
        self.csv_file_paths = raw_to_csv_paths(raw_file_paths)
        # Stopped from GUI
        self.stopped = False
        self.monitor = ProgressMonitor(backend=self)

    def run(self):
        self.run_backend()
        self.progress_finish.emit()

    def run_backend(self):
        """ Step 1. Generate Parsing Functions """
        # Default IDL Folder
        os.makedirs(os.path.join(os.getcwd(), 'IDL'), exist_ok=True)
        # idl_file_paths = get_idl_files()
        idl_file_paths = ["IDL/EIE_Msg.idl", "IDL/TIE_Msg.idl"] * 1  # TODO: For Testing

        generator = ParsingFunctionGenerator()
        for idx, idl_file_path in enumerate(idl_file_paths):
            # Update monitoring and Check if Stopped
            if self.monitor.update_check_stop('idl', work_idx=idx, work_total=len(idl_file_paths),
                                                         task_idx=0, task_total=float('inf')): return
            generator.run(idl_file_path)
        function_files = generator.outputs

        if self.stopped: return

        """ Step 2. Parse Packets """
        """ Step 3. Create CSV    """
        os.makedirs(os.path.join(os.getcwd(), 'CSV'), exist_ok=True)

        parser = PacketParser()
        parser.import_functions(function_files)

        creator = CsvCreator()

        for idx, (raw_file_path, csv_file_path) in enumerate(zip(self.raw_file_paths, self.csv_file_paths)):
            # Update monitoring and Check if Stopped
            if self.monitor.update_check_stop('parse', work_idx=idx, work_total=len(self.raw_file_paths),
                                                           task_idx=0, task_total=float('inf')): return

            # Reset CSV file path
            if os.path.exists(csv_file_path):
                rmtree(csv_file_path)
            os.makedirs(csv_file_path, exist_ok=True)

            ## Step 2. Parse Packet Data ##
            packet_infos = parser.run(raw_file_path)
            print(packet_infos)
            if self.stopped: return

            ## Step 3. Create CSV Files ##
            creator.run(packet_infos, csv_file_path)


    def stop_progress(self):
        self.stopped = True


    def run_csv_create(self):
        pass

