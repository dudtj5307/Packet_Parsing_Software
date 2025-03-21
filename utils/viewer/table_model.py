from PyQt6.QtCore import QAbstractTableModel, pyqtSignal, Qt

class CSVTableModel(QAbstractTableModel):
    load_fail = pyqtSignal(str)  # (csv_path)
    def __init__(self, data, csv_path):
        super().__init__()
        self.csv_path = csv_path

        self.headers = data[0]
        self.data = data[1:]
        # Valid Flag
        self.valid = True

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.data[0]) if self.data else 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not self.valid:
            return None
        try:
            if role == Qt.ItemDataRole.DisplayRole:
                return self.data[index.row()][index.column()]
            return None
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            self.valid = False
            self.load_fail.emit(self.csv_path)
            return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if not self.valid:
            return None
        try:
            if role == Qt.ItemDataRole.DisplayRole:
                if orientation == Qt.Orientation.Horizontal:
                    return self.headers[section]
                elif orientation == Qt.Orientation.Vertical:
                    return str(section + 1)
        except Exception as e:
            print(f"Error loading CSV header: {e}")
            self.valid = False
            self.load_fail.emit(self.csv_path)
            return None