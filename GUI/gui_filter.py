import sys
from collections import defaultdict

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QSizePolicy, QHeaderView, QMenu, QPushButton, QFrame, QWidgetAction, QSizeGrip, QScrollArea
from PyQt6.QtCore import Qt

from GUI.ui.dialog_filter import Ui_FilterForm


class CheckboxLabelFrame(QWidget, Ui_FilterForm):
    def __init__(self, data_set, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Create a QScrollArea for the checkboxes
        self.scroll_area = QScrollArea(self.frame)
        self.scroll_area.setWidgetResizable(True)  # Allow scroll area to resize its widget
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Create a widget to hold the checkboxes inside the scroll area
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        self.scroll_area.setWidget(self.scroll_content)

        # Main layout for the frame now holds the scroll area
        self.main_layout = QVBoxLayout(self.frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(3)
        self.main_layout.addWidget(self.scroll_area)

        # Create the checkbox items in the scroll area's layout
        self.create_items(data_set)
        self.button_close.clicked.connect(self.close)

    def create_items(self, data_set):
        for item in data_set:
            checkbox = QCheckBox(self.scroll_content)
            checkbox.setChecked(True)
            checkbox.setText(item)
            checkbox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            checkbox.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
            checkbox.setStyleSheet("text-overflow: ellipsis; white-space: nowrap;")
            self.scroll_layout.addWidget(checkbox)

class FilterHeaderView(QHeaderView):
    def __init__(self, orientation, table_view, parent=None):
        super().__init__(orientation, parent)
        self.table_view = table_view
        self.setSectionsClickable(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_filter_popup)
        self.current_col = None
        self.filter_popup = None
        self.setAutoFillBackground(True)
        self.setStyleSheet("QHeaderView::section { background-color: rgb(240, 240, 240); }")
        # For saving unique values
        self.unique_values = defaultdict(lambda: False)

    # def contextMenuEvent(self, event):
    #     pos = self.mapToGlobal(event.pos())
    #     self.filter_menu.move(pos)
    #     self.filter_menu.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            logical_index = self.logicalIndexAt(event.pos())
            self.table_view.selectColumn(logical_index)

        super().mousePressEvent(event)

    def show_filter_popup(self, pos):
        self.current_col = self.logicalIndexAt(pos)
        model = self.table_view.model()

        # Build unique values from the model for the selected column
        self.unique_values = defaultdict(lambda: False)
        for row in range(model.rowCount()):
            index = model.index(row, self.current_col)
            value = model.data(index, Qt.ItemDataRole.DisplayRole)
            self.unique_values[value] = True

        # Create a standalone popup instance of CheckboxLabelFrame (no QMenu used)
        self.filter_popup = CheckboxLabelFrame(self.unique_values)
        # Set the window flag to Popup so it behaves like a popup window
        self.filter_popup.setWindowFlags(Qt.WindowType.Popup)

        # Connect signals for the apply and close buttons
        self.filter_popup.button_apply.clicked.connect(self.apply_filter)
        self.filter_popup.button_close.clicked.connect(self.filter_popup.close)

        # Calculate the global position for the popup (displaying it below the header)
        header_pos = self.mapToGlobal(pos)
        self.filter_popup.move(header_pos.x(), header_pos.y())
        self.filter_popup.show()

    def apply_filter(self):
        # Find all QCheckBox widgets within the popup and get their texts if checked
        selected_values = {cb.text() for cb in self.filter_popup.findChildren(QCheckBox) if cb.isChecked()}
        model = self.table_view.model()

        # Hide rows that do not match the selected values
        for row in range(model.rowCount()):
            index = model.index(row, self.current_col)
            value = model.data(index, Qt.ItemDataRole.DisplayRole)
            self.table_view.setRowHidden(row, value not in selected_values)

        # Close the popup after applying the filter
        # self.filter_popup.close()     # TODO: How to deal with after apply


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    sample_data = {"EIE_0x4001", "EIE_0x4002", "EIE_0x4003", "EIE_0x4004"}
    frame = CheckboxLabelFrame(sample_data)
    frame.show()
    sys.exit(app.exec())