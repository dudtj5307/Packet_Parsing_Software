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
        if parent: self.parent.destroyed.connect(self.close)

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
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            checkbox.setText(item)
            self.verticalLayout.addWidget(checkbox)

        spacerItem = QSpacerItem(20, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        # Update widget size based on its content
        scrollbox_height = min(self.widget.sizeHint().height() + 25, 130)
        self.scrollArea.setMinimumHeight(scrollbox_height)


class FilterHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.parent = parent
        self.table_view = parent.table_csv
        self.setSectionsClickable(True)
        self.current_col = None
        self.filter_popup = None
        self.setAutoFillBackground(True)
        self.setStyleSheet("QHeaderView::section { background-color: rgb(240, 240, 240); }")
        self.filter_setting = {}

    def contextMenuEvent(self, event):
        if self.filter_popup:
            self.filter_popup.close()

        # Get current column & table model
        self.current_col = self.logicalIndexAt(event.pos())

        model = self.table_view.model()
        # get data from origin model
        origin_model = model.sourceModel()

        # Unique values from selected column
        unique_values = defaultdict(lambda: False)
        for row in range(origin_model.rowCount()):
            index = origin_model.index(row, self.current_col)
            value = origin_model.data(index, Qt.ItemDataRole.DisplayRole)
            unique_values[value] = True

        # Pop up Filter UI as Dialog
        self.filter_popup = FilterWidget(unique_values, self.parent)
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
        filtered_values = [cb.text() for cb in self.filter_popup.findChildren(QCheckBox) if not cb.isChecked()]
        model = self.table_view.model()

        model.setFilterForColumn(self.current_col, filtered_values)
        # # Hide rows that do not match the selected values
        # for row in range(model.rowCount()):
        #     index = model.index(row, self.current_col)
        #     value = model.data(index, Qt.ItemDataRole.DisplayRole)
        #     self.table_view.setRowHidden(row, value in filtered_values)

        # TODO: After applying - add "color"? or indicator
        # Close the popup after applying the filter
        # self.filter_popup.close()
        self.save_filter_settings(self.filter_setting)

    def set_filter_setting(self, filter_setting):
        self.filter_setting = filter_setting

    def save_filter_settings(self, filter_setting):
        self.parent.cache[self.parent.current_csv_path]['filter_setting'] = filter_setting
        self.set_filter_setting(filter_setting)
        pass



if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    sample_data = {"EIE_0x4001", "EIE_0x4002", "EIE_0x4003", "EIE_0x4004"}
    frame = FilterWidget(sample_data)
    frame.show()
    sys.exit(app.exec())