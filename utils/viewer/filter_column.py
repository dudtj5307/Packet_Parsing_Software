from PyQt6.QtWidgets import QHeaderView, QMenu, QVBoxLayout, QCheckBox, QPushButton, QFrame, QWidgetAction
from PyQt6.QtCore import Qt

from GUI.gui_filter import CheckboxLabelFrame


class FilterHeaderView(QHeaderView):
    def __init__(self, orientation, table_view, parent=None):
        super().__init__(orientation, parent)
        self.table_view = table_view
        self.setSectionsClickable(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_filter_menu)
        self.current_col = None
        self.filter_menu = None
        self.setAutoFillBackground(True)
        self.setStyleSheet("QHeaderView::section { background-color: rgb(240, 240, 240); }")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            logical_index = self.logicalIndexAt(event.pos())
            self.table_view.selectColumn(logical_index)
        super().mousePressEvent(event)

    def show_filter_menu(self, pos):
        self.current_col = self.logicalIndexAt(pos)
        model = self.table_view.model()

        unique_values = set()
        for row in range(model.rowCount()):
            index = model.index(row, self.current_col)
            value = model.data(index, Qt.ItemDataRole.DisplayRole)
            unique_values.add(value)

        if self.filter_menu:
            self.filter_menu.close()

        self.filter_menu = QMenu(self)

        filter_frame = CheckboxLabelFrame(unique_values, parent=self.filter_menu)
        action = QWidgetAction(self.filter_menu)
        action.setDefaultWidget(filter_frame)
        self.filter_menu.addAction(action)

        filter_frame.button_apply.clicked.connect(self.apply_filter)

        header_pos = self.mapToGlobal(pos)
        self.filter_menu.setGeometry(header_pos.x(), header_pos.y() + self.height(), 200, 200)
        self.filter_menu.show()

    def apply_filter(self):
        selected_values = {cb.text() for cb in self.filter_menu.findChildren(QCheckBox) if cb.isChecked()}
        model = self.table_view.model()

        for row in range(model.rowCount()):
            index = model.index(row, self.current_col)
            value = model.data(index, Qt.ItemDataRole.DisplayRole)
            self.table_view.setRowHidden(row, value not in selected_values)

        if self.filter_menu:
            self.filter_menu.close()