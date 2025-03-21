import os
import csv
from collections import defaultdict

from PyQt6.QtWidgets import QAbstractItemView, QMainWindow, QTableView
from PyQt6.QtGui import QIcon, QBrush, QColor, QFont
from PyQt6.QtCore import QAbstractTableModel, QThread, pyqtSignal, Qt

from utils.viewer.table_model import CSVTableModel
from utils.viewer.csv_loader import CSVLoaderThread
from utils.viewer.search_model import SearchModel

from GUI.ui.dialog_viewer import Ui_ViewerWindow


class ViewerWindow(QMainWindow, Ui_ViewerWindow):
    def __init__(self, parent=None, csv_folder_path=None):
        super(ViewerWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(parent.icon_path, "button_csv_view.png")))
        self.csv_folder_path = csv_folder_path[0]
        self.setWindowTitle(f"CSV Viewer - {os.path.basename(self.csv_folder_path)}")

        # CSV Table default size
        self.table_csv.horizontalHeader().setDefaultSectionSize(80)     # cell width
        self.table_csv.verticalHeader().setDefaultSectionSize(20)       # cell height
        self.table_csv.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.table_csv.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        # Load csv list
        self.loader_thread = None
        self.get_csv_path = defaultdict(str)
        self.get_csv_name = defaultdict(str)
        self.load_csv_list()

        # CSV Table Cache
        self.cache = {}

        # Signal set
        self.list_csv_names.clicked.connect(self.clicked_csv_list)

        # Search Widget
        self.search_model = None
        self.frame_search.setVisible(False)
        self.button_close.clicked.connect(self.search_widget_hide)


    def keyPressEvent(self, event):
        # Ctrl+F Key Pressed
        if event.key() == Qt.Key.Key_F and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.search_widget_show()
            self.search_model = SearchModel(self.table_csv)
            self.search_model.search_idx_count.connect(self.search_idx_count)
            self.button_forward.clicked.connect(self.search_model.previous_match)
            self.button_backward.clicked.connect(self.search_model.next_match)

        # ESC Key Pressed & Search Widget On
        elif event.key() == Qt.Key.Key_Escape and self.frame_search.isVisible():
            self.search_widget_hide()
        # ESC Key Pressed & Search Widget Off
        elif event.key() == Qt.Key.Key_Escape and not self.frame_search.isVisible():
            self.close()
        # Enter Key Pressed & Search Widget On
        # elif event.key() == Qt.Key.Key_Enter and self.frame_search.isVisible():
        elif ((event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter)
              and self.frame_search.isVisible() and self.edit_text_input.hasFocus()):
            print('Enter!!')
            self.search_model.search(self.edit_text_input.text())
        else:
            super().keyPressEvent(event)

    def add_item(self, csv_name, csv_path):
        self.get_csv_path[csv_name] = csv_path
        self.get_csv_name[csv_path] = csv_name
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
        csv_path = self.get_csv_path[csv_name]
        # Check if already in cache
        if csv_path in self.cache:
            self.update_table(self.cache[csv_path], csv_path)
        else:
            for item in self.list_csv_names.findItems(csv_name, Qt.MatchFlag.MatchExactly):
                item.setBackground(QBrush(QColor(220, 220, 220)))
            self.loader_thread = CSVLoaderThread(csv_path)
            self.loader_thread.load_complete.connect(self.csv_load_complete)
            self.loader_thread.start()

    def csv_load_complete(self, csv_path, data):
        # Save in cache
        self.update_table(data, csv_path)
        self.cache[csv_path] = data

        csv_name = self.get_csv_name[csv_path]
        for item in self.list_csv_names.findItems(csv_name, Qt.MatchFlag.MatchExactly):
            item.setBackground(QBrush(QColor(245, 255, 245)))
            # item.setFont(QFont("맑은 고딕", 10, QFont.Weight.Bold))

    def csv_load_failed(self, csv_path):
        csv_name = self.get_csv_name[csv_path]
        for item in self.list_csv_names.findItems(csv_name, Qt.MatchFlag.MatchExactly):
            item.setBackground(QBrush(QColor(255, 245, 245)))

    def update_table(self, data, csv_path=""):
        model = CSVTableModel(data, csv_path)
        model.load_fail.connect(self.csv_load_failed)

        self.table_csv.setModel(model)
        self.table_csv.horizontalHeader().setDefaultSectionSize(80)     # cell width
        self.table_csv.verticalHeader().setDefaultSectionSize(20)       # cell height
        self.table_csv.scrollTo(self.table_csv.model().index(0, 0), QAbstractItemView.ScrollHint.PositionAtTop)

    def search_widget_show(self):
        self.frame_search.setVisible(True)
        self.edit_text_input.setFocus()

    def search_widget_hide(self):
        self.frame_search.setVisible(False)

    def search_idx_count(self, current_idx, total_count):
        self.label_idx_count.setText(f"{current_idx}/{total_count}")
        if total_count <= 1:
            self.button_forward.setDisabled(True)
            self.button_backward.setDisabled(True)
        else:
            self.button_forward.setDisabled(False)
            self.button_backward.setDisabled(False)




