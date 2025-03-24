from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import pyqtSignal, Qt, QObject, QItemSelectionModel


class SearchModel(QObject):
    search_widget_update = pyqtSignal(int, int)

    def __init__(self, table_view: QTableView):
        super().__init__()

        self.table_view = table_view
        self.model = None

        self.matches = []           # (row, col) 튜플 리스트
        self.current_index = -1     # 현재 선택된 결과 인덱스

        self.is_running = False

    def search(self, search_text: str):
        # Return if already searching
        if self.is_running:
            print("Already Searching")
            return
        # Connect to model
        self.model = self.table_view.model()

        self.matches.clear()
        self.current_index = -1
        if not search_text or not self.model or not self.model.valid:
            return

        self.is_running = True

        # Find in Row header
        for col in range(self.model.columnCount()):
            header_text = self.model.headerData(col, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
            if header_text and search_text.lower() in str(header_text).lower():
                self.matches.append((-1, col))

        # Find in data cells
        for row in range(self.model.rowCount()):
            for col in range(self.model.columnCount()):
                cell_value = self.model.data(self.model.index(row, col), Qt.ItemDataRole.DisplayRole)
                if cell_value and search_text.lower() in str(cell_value).lower():
                    self.matches.append((row, col))

        # 전체 탐색 후, 결과가 있으면 첫번째 결과 선택
        if self.matches:
            self.current_index = 0
            self.select_current()

        self.send_result_to_gui()
        self.is_running = False

    def next_match(self):
        if not self.matches:
            return
        self.current_index = (self.current_index + 1) % len(self.matches)
        self.select_current()
        self.send_result_to_gui()

    def previous_match(self):
        if not self.matches:
            return
        self.current_index = (self.current_index - 1 + len(self.matches)) % len(self.matches)
        self.select_current()
        self.send_result_to_gui()

    def select_current(self):
        if self.current_index >= 0 and self.matches:
            row, col = self.matches[self.current_index]
            self.table_view.clearSelection()
            # If in Row Header
            if row == -1:
                self.table_view.scrollTo(self.model.index(0, col))
                self.table_view.selectColumn(col)
            # If in data
            else:
                idx = self.model.index(row, col)
                self.table_view.scrollTo(idx)
                self.table_view.setCurrentIndex(idx)
                self.table_view.setFocus()


    def send_result_to_gui(self):
        # 현재 선택된 검색 결과 번호와 전체 결과 개수를 전달합니다.
        self.search_widget_update.emit(self.current_index + 1, len(self.matches))