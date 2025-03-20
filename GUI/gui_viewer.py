import os
import csv
from collections import defaultdict

from PyQt6.QtWidgets import QDialog, QAbstractItemView
from PyQt6.QtGui import QIcon, QBrush, QColor
from PyQt6.QtCore import QAbstractTableModel, QThread, pyqtSignal, Qt

from GUI.ui.dialog_viewer import Ui_ViewerWindow

class ViewerWindow(QDialog, Ui_ViewerWindow):
    def __init__(self, parent=None, csv_folder_path=None):
        super(ViewerWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(parent.icon_path, "button_csv_view.png")))

        # CSV Folder to View
        self.csv_folder_path = csv_folder_path[0]

        print(self.csv_folder_path.split())

        self.setWindowTitle(f"CSV Viewer - {os.path.basename(self.csv_folder_path)}")

        self.table_csv.horizontalHeader().setDefaultSectionSize(80)     # cell width
        self.table_csv.verticalHeader().setDefaultSectionSize(20)       # cell height
        self.table_csv.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.table_csv.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        # Load csv list
        self.loader_thread = None
        self.get_path = defaultdict(str)
        self.get_name = defaultdict(str)
        self.load_csv_list()

        # CSV Table Cache
        self.cache = {}

        # Signal set
        self.list_csv_names.clicked.connect(self.clicked_csv_list)

    def add_item(self, csv_name, csv_path):
        self.get_path[csv_name] = csv_path
        self.get_name[csv_path] = csv_name
        self.list_csv_names.addItem(csv_name)

    def load_csv_list(self):
        csv_file_names = os.listdir(self.csv_folder_path)
        if len(csv_file_names) == 0:
            return
        for file_name in os.listdir(self.csv_folder_path):
            if file_name.lower().endswith('.csv'):
                csv_name = file_name.split('.csv')[0]
                csv_path = os.path.join(self.csv_folder_path, file_name)
                self.add_item(csv_name, csv_path)

    def clicked_csv_list(self):
        csv_name = self.list_csv_names.currentItem().text()
        csv_path = self.get_path[csv_name]
        # Check if already in cache
        if csv_path in self.cache:
            self.update_table(self.cache[csv_path])
        else:
            for item in self.list_csv_names.findItems(csv_name, Qt.MatchFlag.MatchExactly):
                item.setBackground(QBrush(QColor(220, 220, 220)))
            self.loader_thread = CSVLoaderThread(csv_path)
            self.loader_thread.load_complete.connect(self.on_csv_loaded)
            self.loader_thread.start()

    def on_csv_loaded(self, csv_path, data):
        # Save in cache
        self.update_table(data)
        self.cache[csv_path] = data

        csv_name = self.get_name[csv_path]
        for item in self.list_csv_names.findItems(csv_name, Qt.MatchFlag.MatchExactly):
            item.setBackground(QBrush(QColor(245, 255, 245)))

    def update_table(self, data):
        model = CSVTableModel(data)
        self.table_csv.setModel(model)

        self.table_csv.horizontalHeader().setDefaultSectionSize(80)     # cell width
        self.table_csv.verticalHeader().setDefaultSectionSize(20)       # cell height
        self.table_csv.scrollTo(self.table_csv.model().index(0, 0), QAbstractItemView.ScrollHint.PositionAtTop)


class CSVLoaderThread(QThread):
    load_complete = pyqtSignal(str, list)  # (파일경로, 데이터)

    def __init__(self, csv_path):
        super().__init__()
        self.csv_path = csv_path

    def run(self):
        try:
            with open(self.csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
            self.load_complete.emit(self.csv_path, data)
        except Exception as e:
            print(f"Error loading {self.csv_path}: {e}")
            import chardet
            with open(self.csv_path, 'rb') as f:
                raw_data = f.read()
                encoding_info = chardet.detect(raw_data)
                print(f"Detected encoding: {encoding_info['encoding']}")


class CSVTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.headers = data[0]
        self.data = data[1:]

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.data[0]) if self.data else 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1)  # 수직 헤더에서 행 번호 반환
        return None

