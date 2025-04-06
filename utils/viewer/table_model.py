from collections import defaultdict

from PyQt6.QtCore import QAbstractTableModel, pyqtSignal, Qt
from PyQt6.QtGui import QColor, QBrush

class CSVTableModel(QAbstractTableModel):
    load_fail = pyqtSignal(str)  # (csv_path)
    def __init__(self, data, csv_path):
        super().__init__()
        self.csv_path = csv_path

        # CSV Header & Data
        self.headers = data[0]
        self.csv_data_map = {row_idx: row for row_idx, row in enumerate(data[1:])}

        # Highlight cells
        self.highlight_cells = {}
        self.highlight_color = {'button_white': QColor("white"),
                                'button_red': QColor(255, 100, 100),
                                'button_yellow': QColor("yellow"),
                                'button_green': QColor(185, 255, 163),
                                'button_blue': QColor(121, 220, 255)}

        # Valid Flag
        self.valid = True

    def rowCount(self, parent=None):
        return len(self.csv_data_map)

    def columnCount(self, parent=None):
        return len(self.headers) if self.headers else 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not self.valid:
            return None
        row, col = index.row(), index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            return self.csv_data_map.get(row)[col]
        elif role == Qt.ItemDataRole.BackgroundRole:
            if (row, col) in self.highlight_cells:
                return QBrush(self.highlight_cells[(row, col)])
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
            print(f"[Model] Error loading CSV header: {e}")
            self.valid = False
            self.load_fail.emit(self.csv_path)
            return None

    def highlight_cell(self, button_name, cell_indexes):
        self.beginResetModel()
        # Initialization
        if button_name == "button_none":
            self.highlight_cells = {}
            self.layoutChanged.emit()
            self.endResetModel()
            return
        # Color selected cells
        color = self.highlight_color.get(button_name, None)
        for index in cell_indexes:
            row, col = index.row(), index.column()
            self.highlight_cells[(row, col)] = color
        self.endResetModel()



