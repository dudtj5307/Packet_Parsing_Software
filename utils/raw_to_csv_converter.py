import os
from shutil import rmtree

from PyQt6.QtCore import QThread, pyqtSignal

from GUI.gui_progress import ProgressWindow
from utils.config import Config
from utils.monitor import ProgressMonitor
from utils.function_generator import ParsingFunctionGenerator
from utils.packet_parser import RAW_PACKET_PARSER

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


class ProgressBackend(QThread):
    progress_update = pyqtSignal(list, name="progress_update")
    progress_finish = pyqtSignal(name="finished")

    def __init__(self, raw_file_paths):
        super().__init__(None)
        self.config = Config()
        self.raw_file_paths = raw_file_paths
        self.csv_file_paths = raw_to_csv_paths(raw_file_paths)
        # Is stopped from GUI
        self.stopped = False
        self.monitor = ProgressMonitor(backend=self)

    def run(self):
        """ Step 1. Generate Parsing Functions """
        # Default IDL Folder
        os.makedirs(os.path.join(os.getcwd(), 'IDL'), exist_ok=True)

        # idl_file_paths = get_idl_file_paths()
        idl_file_paths = ["IDL/EIE_Msg.idl", "IDL/TIE_Msg.idl"] * 500  # TODO: For Testing

        generator = ParsingFunctionGenerator()
        self.monitor.update_and_check_stop('idl', work_total=len(idl_file_paths))
        for idx, idl_file_path in enumerate(idl_file_paths):
            # Update monitoring and Check if Stopped
            if self.monitor.update_and_check_stop('idl', work_idx=idx): return
            generator.run(idl_file_path)
        function_files = generator.outputs

        if self.stopped: return

        """ Step 2. Parse Packets """
        """ Step 3. Create CSV    """
        os.makedirs(os.path.join(os.getcwd(), 'CSV'), exist_ok=True)

        parser = RAW_PACKET_PARSER()
        parser.import_functions(function_files)

        self.monitor.update_and_check_stop('parse', work_total=len(self.raw_file_paths))
        for idx, (raw_file_path, csv_file_path) in enumerate(zip(self.raw_file_paths, self.csv_file_paths)):
            # Update monitoring and Check if Stopped
            if self.monitor.update_and_check_stop('parse', work_idx=idx): return

            # Renew CSV file path
            if os.path.exists(csv_file_path):
                rmtree(csv_file_path)
            os.makedirs(csv_file_path, exist_ok=True)

            ## Step 2. Parse Packet Data ##
            parser.run(raw_file_path)

            if self.stopped:  # TODO: [Monitoring] Check if Backend is stopped from GUI
                self.progress_finish.emit()
                return

            ## Step 3. Create CSV Files ##
            self.run_csv_create()

            if self.stopped:  # TODO: [Monitoring] Check if Backend is stopped from GUI
                self.progress_finish.emit()
                # return STOPPED
        self.progress_finish.emit()


    def stop_progress(self):
        self.stopped = True


    def run_csv_create(self):
        pass

