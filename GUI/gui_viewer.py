import os
from collections import defaultdict

from PyQt6.QtWidgets import QAbstractItemView, QMainWindow
from PyQt6.QtGui import QIcon, QBrush, QColor
from PyQt6.QtCore import Qt

from utils.viewer.table_model import CSVTableModel
from utils.viewer.csv_loader import CSVLoaderThread
from utils.viewer.search_model import SearchModel

from GUI.ui.dialog_viewer import Ui_ViewerWindow
from GUI.gui_filter import FilterHeaderView


class ViewerWindow(QMainWindow, Ui_ViewerWindow):
    def __init__(self, parent=None, csv_folder_path=None):
        super(ViewerWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(parent.icon_path, "button_csv_view.png")))
        self.csv_folder_path = csv_folder_path[0]
        self.setWindowTitle(f"CSV Viewer - {os.path.basename(self.csv_folder_path)}")

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
        self.search_model = SearchModel(self.table_csv)
        self.search_model.search_widget_update.connect(self.search_widget_update)
        self.button_forward.clicked.connect(self.search_model.previous_match)
        self.button_backward.clicked.connect(self.search_model.next_match)
        self.button_close.clicked.connect(self.search_widget_hide)
        self.frame_search.setVisible(False)

        # Filter Widget
        self.table_csv.setHorizontalHeader(FilterHeaderView(Qt.Orientation.Horizontal, self.table_csv))

        # CSV Table default size
        self.table_csv.horizontalHeader().setDefaultSectionSize(80)     # cell width
        self.table_csv.verticalHeader().setDefaultSectionSize(20)       # cell height
        self.table_csv.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.table_csv.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

    def keyPressEvent(self, event):
        # Initial Ctrl+F Key Pressed
        if event.key() == Qt.Key.Key_F and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.search_widget_init()
            self.search_widget_show()

        # 'ESC' Key Pressed & Search Widget On
        elif event.key() == Qt.Key.Key_Escape and self.frame_search.isVisible():
            self.search_widget_hide()

        # 'ESC' Key Pressed & Search Widget Off
        elif event.key() == Qt.Key.Key_Escape and not self.frame_search.isVisible():
            self.close()

        # 'Enter' Key Pressed & Search Widget On
        elif ((event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter)
               and self.frame_search.isVisible() and self.edit_text_input.hasFocus()):
            self.search_model.search(self.edit_text_input.text())

        # 'F2' Key Pressed & 'Previous' Button Enabled
        elif event.key() == Qt.Key.Key_F2:
            self.search_model.previous_match()

        # 'F3' Key Pressed & 'Next' Button Enabled
        elif event.key() == Qt.Key.Key_F3:
            self.search_model.next_match()

        # 'Home' Key Pressed
        elif event.key() == Qt.Key.Key_Home:
            self.table_csv.scrollToTop()
        # 'End' Key Pressed
        elif event.key() == Qt.Key.Key_End:
            self.table_csv.scrollToBottom()
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
        self.search_widget_hide()
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
            self.loader_thread.load_failed.connect(self.csv_load_failed)
            self.loader_thread.start()

    def csv_load_complete(self, csv_path, data):
        # Save in cache
        self.cache[csv_path] = data

        # Paint Green to list_csv
        csv_name = self.get_csv_name[csv_path]
        for item in self.list_csv_names.findItems(csv_name, Qt.MatchFlag.MatchExactly):
            item.setBackground(QBrush(QColor(245, 255, 245)))   # Green

        # Update table if currently selected
        if self.list_csv_names.currentItem().text() == csv_name:
            self.update_table(data, csv_path)

    def csv_load_failed(self, csv_path):
        # Save in cache
        self.cache[csv_path] = None
        self.update_table(None, csv_path)

        csv_name = self.get_csv_name[csv_path]
        for item in self.list_csv_names.findItems(csv_name, Qt.MatchFlag.MatchExactly):
            item.setBackground(QBrush(QColor(255, 245, 245)))   # Red

    def update_table(self, data, csv_path=""):
        # CSV loading failed
        if not self.cache[csv_path]:
            self.table_csv.setModel(None)
            return

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

    def search_widget_init(self):
        self.edit_text_input.clear()
        self.label_idx_count.clear()
        self.button_backward.setDisabled(True)
        self.button_forward.setDisabled(True)

    def search_widget_update(self, current_idx, total_count):
        self.label_idx_count.setText(f"{current_idx}/{total_count}")
        if total_count <= 1:
            self.button_forward.setDisabled(True)
            self.button_backward.setDisabled(True)
        else:
            self.button_forward.setDisabled(False)
            self.button_backward.setDisabled(False)

    def get_selected_cells(self):
        indexes = self.table_csv.selectedIndexes()
        for ind in indexes:
            print(ind.row(), ind.column())



