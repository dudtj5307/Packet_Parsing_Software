from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import pyqtSignal, Qt, QObject


class SearchModel(QObject):
    search_idx_count = pyqtSignal(int, int)

    def __init__(self, table_view : QTableView):
        super().__init__()

        self.table_view = table_view
        self.model = table_view.model()
        self.matches = []           # match list
        self.current_index = -1     # current index

    def search(self, search_text: str):
        self.matches.clear()
        self.current_index = -1
        if not search_text or not self.model.valid:
            return

        for row in range(self.model.rowCount()):
            for col in range(self.model.columnCount()):
                index = self.model.index(row, col)
                cell_value = index.data(Qt.ItemDataRole.DisplayRole)  # 수정된 부분
                if cell_value is not None and search_text.lower() in str(cell_value).lower():
                    self.matches.append(index)

            if self.matches:
                self.current_index = 0
                self.select_current()

        self.send_result_to_gui()

    def next_match(self):
        """다음 검색 결과로 이동합니다."""
        if not self.matches:
            return
        self.current_index = (self.current_index + 1) % len(self.matches)
        self.select_current()

        self.send_result_to_gui()

    def previous_match(self):
        """이전 검색 결과로 이동합니다."""
        if not self.matches:
            return
        self.current_index = (self.current_index - 1 + len(self.matches)) % len(self.matches)
        self.select_current()

        self.send_result_to_gui()

    def select_current(self):
        """현재 선택된 검색 결과를 테이블 뷰에 표시합니다."""
        if self.current_index >= 0 and self.matches:
            index = self.matches[self.current_index]
            self.table_view.setCurrentIndex(index)
            self.table_view.scrollTo(index)

    def send_result_to_gui(self):
        self.search_idx_count.emit(self.current_index + 1, len(self.matches))