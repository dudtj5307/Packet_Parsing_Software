import csv
from PyQt6.QtCore import QAbstractTableModel, QThread, pyqtSignal, Qt

class CSVLoaderThread(QThread):
    load_complete = pyqtSignal(str, list)  # (파일경로, 데이터)

    def __init__(self, csv_path):
        super().__init__()
        self.csv_path = csv_path

    def run(self):
        for encode_type in ['utf-8', 'cp949', 'euc-kr']:
            try:
                with open(self.csv_path, newline='', encoding=encode_type) as csvfile:      # TODO: Check if 'cp949' or 'euc-kr'
                    reader = csv.reader(csvfile)
                    data = list(reader)
                self.load_complete.emit(self.csv_path, data)
                print(f"Loading Success '{self.csv_path}' with {encode_type}")
                return
            except Exception as e:
                print(f"Error loading '{self.csv_path}': {e}")
        print(f"Error: Cannot load '{self.csv_path}' with available encodings.")