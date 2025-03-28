import sys
from collections import defaultdict

from PyQt6.QtWidgets import QWidget, QCheckBox, QSizePolicy, QHeaderView, QSpacerItem, QApplication
from PyQt6.QtCore import Qt, QEvent, QTimer

from GUI.ui.dialog_filter import Ui_FilterForm


class FilterWidget(QWidget, Ui_FilterForm):
    def __init__(self, data_set, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.parent = parent

        # Create the checkbox items in the scroll area's layout
        self.create_items(data_set)

        # Install Global EventFilter for closing
        QApplication.instance().installEventFilter(self)

        # Set Focus to this widget
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

    def keyPressEvent(self, event):
        # Key 'ESC' - Close widget
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            # Check if the click was outside the FilterWidget
            if not self.rect().contains(event.pos()):
                self.close()
        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        # Remove the event filter when the widget is closed
        QApplication.instance().removeEventFilter(self)
        super().closeEvent(event)

    def create_items(self, data_set):
        for item in data_set:
            checkbox = QCheckBox(parent=self.parent)
            checkbox.setChecked(True)
            checkbox.setText(item)
            self.verticalLayout.addWidget(checkbox)

        spacerItem = QSpacerItem(20, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        # Update widget size based on its content
        self.scrollArea.setMinimumHeight(self.widget.sizeHint().height() + 25)


class FilterHeaderView(QHeaderView):
    def __init__(self, orientation, table_view, parent=None):
        super().__init__(orientation, parent)
        self.table_view = table_view
        self.setSectionsClickable(True)
        self.current_col = None
        self.filter_popup = None
        self.setAutoFillBackground(True)
        self.setStyleSheet("QHeaderView::section { background-color: rgb(240, 240, 240); }")
        # For saving unique values
        self.unique_values = defaultdict(lambda: False)

    def contextMenuEvent(self, event):
        if self.filter_popup:
            self.filter_popup.close()

        # Get current column & table model
        self.current_col = self.logicalIndexAt(event.pos())
        model = self.table_view.model()

        # Unique values from selected column
        self.unique_values = defaultdict(lambda: False)
        for row in range(model.rowCount()):
            index = model.index(row, self.current_col)
            value = model.data(index, Qt.ItemDataRole.DisplayRole)
            self.unique_values[value] = True

        # Pop up Filter UI as Dialog
        self.filter_popup = FilterWidget(self.unique_values, self.table_view)
        self.filter_popup.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint)

        # Connect signals for the apply and close buttons
        self.filter_popup.button_apply.clicked.connect(self.apply_filter)
        self.filter_popup.button_close.clicked.connect(self.filter_popup.close)

        # Display with fixed position
        pos = self.table_view.mapToGlobal(event.pos())
        self.filter_popup.move(pos)
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

        # TODO: After applying - add "color"? or indicator
        # Close the popup after applying the filter
        # self.filter_popup.close()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    sample_data = {"EIE_0x4001", "EIE_0x4002", "EIE_0x4003", "EIE_0x4004"}
    frame = FilterWidget(sample_data)
    frame.show()
    sys.exit(app.exec())