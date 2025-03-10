import threading

from GUI.gui_progress import ProgressWindow


class RawToCSV:
    def __init__(self, parent, p_parent, raw_file_paths):
        # Inherited Variables
        self.parent = parent            # parent            (gui_main.py)
        self.p_parent = p_parent        # parent of parent  (PPS.py)
        self.raw_file_paths = raw_file_paths




    def run(self):
        backend_thread = threading.Thread(target=self.run_backend_progress)
        backend_thread.start()
        self.run_gui_progress()
        pass

    def run_gui_progress(self):
        # self.parent.progress_window = ProgressWindow(self, self.parent)
        self.parent.progress_window = ProgressWindow()
        self.parent.progress_window.exec()

    def run_backend_progress(self):
        self.run_code_generation()
        self.run_packet_parse()
        self.run_csv_create()

    def run_code_generation(self):
        print("run_code_generation")

    def run_packet_parse(self):
        print("run_packet_parse")

    def run_csv_create(self):
        print("run_csv_create")
