from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import pyqtSignal, Qt, QObject


class SearchModel(QObject):
    search_idx_count = pyqtSignal(int, int)

    def __init__(self, table_view: QTableView):
        super().__init__()

        self.table_view = table_view
        self.model = table_view.model()
        self.matches = []           # (row, col) 튜플 리스트
        self.current_index = -1     # 현재 선택된 결과 인덱스

        self.is_running = False

    def search(self, search_text: str):
        # 이미 검색 중이면 리턴
        if self.is_running:
            print("Already Searching")
            return

        self.matches.clear()
        self.current_index = -1
        if not search_text or not self.model.valid:
            return

        self.is_running = True
        # 전체 셀을 탐색
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
            row, col = self.matches[self.current_index]
            idx = self.model.index(row, col)  # (row, col) 튜플을 QModelIndex로 변환
            self.table_view.setCurrentIndex(idx)
            self.table_view.scrollTo(idx)

    def send_result_to_gui(self):
        # 현재 선택된 검색 결과 번호와 전체 결과 개수를 전달합니다.
        self.search_idx_count.emit(self.current_index + 1, len(self.matches))