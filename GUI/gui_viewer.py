import os
import time
from collections import defaultdict

from PyQt6.QtWidgets import QAbstractItemView, QMainWindow, QListWidgetItem, QWidget
from PyQt6.QtGui import QIcon, QBrush, QColor
from PyQt6.QtCore import Qt, QTimer

from utils.viewer.table_model import CSVTableModel
from utils.viewer.filter_model import CSVFilterProxyModel
from utils.viewer.csv_loader import CSVLoaderThread
from utils.viewer.search_model import SearchModel

from GUI.ui.dialog_viewer import Ui_ViewerWindow
from GUI.ui.widget_esc import Ui_WidgetESC

from GUI.gui_filter import FilterHeaderView


class ViewerWindow(QMainWindow, Ui_ViewerWindow):
    def __init__(self, parent=None, csv_folder_path=None):
        super(ViewerWindow, self).__init__(None)
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowType.Window)

        self.setWindowIcon(QIcon(os.path.join(parent.icon_path, "button_csv_view.png")))
        self.csv_folder_path = csv_folder_path[0]
        self.setWindowTitle(f"CSV Viewer - {os.path.basename(self.csv_folder_path)}")
        self.table_csv.setStyleSheet("QTableView { background-color: white; }")
        self.table_csv.verticalHeader().setStyleSheet("QHeaderView::section:vertical { background-color: rgb(240, 240, 240); }")

        # Load csv list
        self.loader_thread = None
        self.get_csv_path = defaultdict(str)
        self.get_csv_name = defaultdict(str)
        self.load_csv_list()

        # CSV List
        self.current_csv_path = None
        self.list_csv_names.currentItemChanged.connect(self.clicked_csv_list)

        # Internal cache data
        self.cache = defaultdict(lambda: {'table_model': None, 'table_data': None, 'filter_setting':{},
                                          'search_model': None, 'search_setting':[], })
        # ESC widget for closing this window
        self.last_esc_time = 0
        self.widget_esc = QWidget(self)
        self.ui_esc = Ui_WidgetESC()
        self.ui_esc.setupUi(self.widget_esc)
        self.widget_esc.hide()

        # Search Widget
        self.search_model = SearchModel(self.table_csv)
        self.search_model.search_widget_update.connect(self.search_widget_update)
        self.button_forward.clicked.connect(self.search_model.previous_match)
        self.button_backward.clicked.connect(self.search_model.next_match)
        self.button_close.clicked.connect(self.search_widget_hide)
        self.frame_search.setVisible(False)

        # Custom horizontal header with filtering
        self.table_csv.setHorizontalHeader(FilterHeaderView(Qt.Orientation.Horizontal, self))

        # CSV table headers - size
        self.table_csv.horizontalHeader().setDefaultSectionSize(80)     # cell width
        self.table_csv.verticalHeader().setDefaultSectionSize(20)       # cell height
        self.table_csv.verticalHeader().setFixedWidth(48)
        # CSV table headers - alignment
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
            if time.time() - self.last_esc_time < 1:  # ESC pressed interval time < 1sec
                self.close()
            self.last_esc_time = time.time()    # Update last esc pressed time
            self.show_esc_message()

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

    def show_esc_message(self):
        pos_x = (self.width() - self.widget_esc.width()) // 2
        pos_y = (self.height() - self.widget_esc.height()) // 2
        self.widget_esc.setGeometry(pos_x, pos_y, self.widget_esc.width(), self.widget_esc.height(),)
        self.widget_esc.show()
        QTimer.singleShot(1000, self.widget_esc.hide)  # 1000 (ms)

    def add_item(self, csv_name, csv_path):
        self.get_csv_path[csv_name] = csv_path
        self.get_csv_name[csv_path] = csv_name
        self.list_csv_names.addItem(csv_name)

        # TODO: 구분선 표시...
        # item = QListWidgetItem(csv_name)
        # item.setData(Qt.ItemDataRole.UserRole, "border-bottom: 1px solid rgb(225, 225, 225); padding-left: 2px;")
        # self.list_csv_names.addItem(item)


    def paint_list_csv(self, csv_path, color):
        csv_name = self.get_csv_name[csv_path]
        for item in self.list_csv_names.findItems(csv_name, Qt.MatchFlag.MatchExactly):
            item.setBackground(QBrush(QColor(color[0], color[1], color[2])))  # Green

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
        # Close Search Widget
        self.search_widget_hide()
        # Close Filter Widget
        header = self.table_csv.horizontalHeader()
        if hasattr(header, "filter_popup") and header.filter_popup:
            header.filter_popup.close()

        csv_name = self.list_csv_names.currentItem().text()
        csv_path = self.get_csv_path[csv_name]
        self.current_csv_path = csv_path

        # Check if already in cache
        if csv_path in self.cache:
            self.update_table(csv_path)
        else:
            self.paint_list_csv(csv_path, (220, 220, 220))  # Gray
            self.loader_thread = CSVLoaderThread(csv_path)
            self.loader_thread.load_complete.connect(self.csv_load_complete)
            self.loader_thread.load_failed.connect(self.csv_load_failed)
            self.loader_thread.start()

    def csv_load_complete(self, csv_path, data):
        # Save in cache
        self.cache[csv_path]['table_data'] = data
        self.update_table(csv_path)
        self.paint_list_csv(csv_path, (230, 255, 230))  # Green

    def csv_load_failed(self, csv_path):
        # Save in cache
        self.cache[csv_path]['table_data'] = None
        self.update_table(csv_path)
        self.paint_list_csv(csv_path, (255, 230, 230))  # Red

    def update_table(self, csv_path=""):
        # Return if not currently selected
        csv_name = self.get_csv_name[csv_path]
        if self.list_csv_names.currentItem().text() != csv_name:
            return
        # Return if No data to load
        if not self.cache[csv_path]['table_data']:
            self.table_csv.setModel(None)
            return

        # Look if there is model already created
        if self.cache[csv_path]['table_model']:
            self.table_csv.setModel(self.cache[csv_path]['table_model'])
        else:
            model = CSVTableModel(self.cache[csv_path]['table_data'], csv_path)
            model.load_fail.connect(self.csv_load_failed)
            proxy_model = CSVFilterProxyModel()
            proxy_model.setSourceModel(model)

            self.cache[csv_path]['table_model'] = proxy_model
            self.table_csv.setModel(proxy_model)

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

    def closeEvent(self, event):
        self.deleteLater()  # 창이 닫힐 때 객체를 완전히 삭제
        super().closeEvent(event)

