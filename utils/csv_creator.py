from utils.monitor import ProgressMonitor

class CsvCreator:
    def __init__(self):
        self.monitor = ProgressMonitor()

        self.packet_infos = []
        self.csv_file_path = ""
        self.output = []


    def run(self, packet_infos, csv_file_path):
        self.packet_infos = packet_infos
        self.csv_file_path = packet_infos
        print('CsvCreator run!')