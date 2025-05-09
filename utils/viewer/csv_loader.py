import csv
from PyQt6.QtCore import QThread, pyqtSignal

class CSVLoaderThread(QThread):
    load_complete = pyqtSignal(str, list)  # (파일경로, 데이터)
    load_failed   = pyqtSignal(str)

    def __init__(self, csv_path):
        super().__init__()
        self.csv_path = csv_path

    def run(self):
        for encode_type in ['utf-8', 'cp949', 'euc-kr']:
            try:
                with open(self.csv_path, newline='', encoding=encode_type) as csvfile:      # TODO: Check if 'cp949' or 'euc-kr'
                    reader = csv.reader(csvfile)
                    # Convert to str
                    data = [[str(cell) for cell in row] for row in reader]
                # Data Validation
                if self.is_valid(data):
                    header_count, data_count =  len(data[0]), len(data[1])
                    # If header is shorter
                    if header_count < data_count:
                        data[0] += [""] * (data_count-header_count)
                    self.load_complete.emit(self.csv_path, data)
                    print(f"[Loader] Success opening '{self.csv_path}' with {encode_type}")
                    return
                else:
                    self.load_failed.emit(self.csv_path)
                    raise TypeError("Invalid CSV data ! (no match in row and data)")

            except Exception as e:
                print(f"[Loader] Failed opening '{self.csv_path}' with {encode_type} / {e}")

        print(f"[Loader] Error: Cannot load '{self.csv_path}' with available encodings.\n")

    def is_valid(self, data):
        return all(len(row) == len(data[1]) for row in data)