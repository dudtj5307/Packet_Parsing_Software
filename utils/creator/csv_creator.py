import os
import csv
from utils.monitor import ProgressMonitor

class CsvCreator:
    def __init__(self):
        self.monitor = ProgressMonitor()

        self.packet_infos = []
        self.csv_file_path = ""
        self.outputs = []

    def run(self, packet_infos, csv_file_path):
        self.packet_infos = packet_infos
        self.csv_file_path = csv_file_path

        if self.monitor.update_check_stop('csv', task_idx=-1, task_total=1, prior_status=0.1): return

        # Create CSV - all.csv
        self.make_csv_all()

        if self.monitor.update_check_stop('csv', task_idx=-1, task_total=1, prior_status=0.5): return

        # Create CSV - each MSG_NAMES
        uniq_msg_names = self.get_unique_value("MSG_NAME")
        self.make_csv_separate(uniq_msg_names)

    def get_unique_value(self, colname):
        return set(map(lambda info: info[colname], self.packet_infos))

    # TODO: Add monitor update
    def make_csv_all(self):
        csv_save_path = os.path.join(self.csv_file_path, "all.csv")
        with open(csv_save_path, mode="w", encoding="utf-8", newline="") as file:
            fieldnames = self.packet_infos[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()            # Write Header
            writer.writerows(self.packet_infos)  # Write Data

    def make_csv_separate(self, uniq_names):
        for idx, name in enumerate(uniq_names):
            packet_filtered = [info['DATA'] for info in self.packet_infos if info["MSG_NAME"] == name]
            csv_save_path = os.path.join(self.csv_file_path, f"{name}.csv")
            with open(csv_save_path, mode="w", encoding="utf-8", newline="") as file:
                fieldnames = packet_filtered[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()  # Write Header
                writer.writerows(packet_filtered)  # Write Data
            if self.monitor.update_check_stop('csv', task_idx=idx, task_total=len(uniq_names), prior_status=0.5): return
