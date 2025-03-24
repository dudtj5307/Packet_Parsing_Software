from PyQt6.QtWidgets import QHeaderView, QMenu, QVBoxLayout, QCheckBox, QPushButton, QFrame, QWidgetAction
from PyQt6.QtCore import Qt

class FilterHeaderView(QHeaderView):
    def __init__(self, orientation, table_view, parent=None):
        super().__init__(orientation, parent)
        self.table_view = table_view
        self.setSectionsClickable(True)  # 클릭 가능 설정
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_filter_menu)
        self.current_col = None
        self.filter_menu = None
        self.setAutoFillBackground(True)
        self.setStyleSheet("QHeaderView::section { background-color: rgb(240, 240, 240); }")    # TODO : change button style

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 좌클릭 시 열 전체 선택
            logical_index = self.logicalIndexAt(event.pos())
            self.table_view.selectColumn(logical_index)
        super().mousePressEvent(event)

    def show_filter_menu(self, pos):
        # 우클릭한 열 인덱스 확인
        self.current_col = self.logicalIndexAt(pos)
        model = self.table_view.model()

        # 고유 데이터 수집
        unique_values = set()
        for row in range(model.rowCount()):
            index = model.index(row, self.current_col)
            value = model.data(index, Qt.ItemDataRole.DisplayRole)
            unique_values.add(value)

        # 기존 필터 메뉴 제거
        if self.filter_menu:
            self.filter_menu.close()

        # 컨텍스트 메뉴 생성
        self.filter_menu = QMenu(self)

        # QFrame으로 컨텍스트 메뉴처럼 보이게 설정
        frame = QFrame(self.filter_menu)
        frame.setStyleSheet("background-color: white; border: 1px solid gray;")
        frame.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(frame)

        self.checkboxes = []
        for value in unique_values:
            checkbox = QCheckBox(str(value))
            checkbox.setChecked(True)  # 기본적으로 체크됨
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

        action = QWidgetAction(self.filter_menu)
        action.setDefaultWidget(frame)
        self.filter_menu.addAction(action)

        # 메뉴를 열 헤더 아래에 표시
        header_pos = self.mapToGlobal(pos)
        self.filter_menu.setGeometry(header_pos.x(), header_pos.y() + self.height(), 200, 200)
        self.filter_menu.show()

    def apply_filter(self):
        selected_values = {cb.text() for cb in self.checkboxes if cb.isChecked()}
        model = self.table_view.model()

        for row in range(model.rowCount()):
            index = model.index(row, self.current_col)
            value = model.data(index, Qt.ItemDataRole.DisplayRole)

            # Hide datas not selected
            self.table_view.setRowHidden(row, value not in selected_values)

            # TODO : Filtering Effect to display

        # 필터 메뉴 닫기
        if self.filter_menu:
            self.filter_menu.close()
