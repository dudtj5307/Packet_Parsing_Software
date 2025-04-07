import sys
from collections import defaultdict

from PyQt6.QtWidgets import QWidget, QCheckBox, QSizePolicy, QHeaderView, QSpacerItem, QApplication
from PyQt6.QtCore import Qt, QEvent, QTimer, QSize

from GUI.ui.dialog_filter import Ui_FilterForm


class FilterWidget(QWidget, Ui_FilterForm):
    def __init__(self, data_set, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.parent = parent
        if parent: self.parent.destroyed.connect(self.close)

        # Global EventFilter for noticing clicked outside this widget -> this widget closing
        QApplication.instance().installEventFilter(self)

        # Set Focus to this widget
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        # Create the checkbox items in the scroll area's layout
        self.create_items(data_set)

    def keyPressEvent(self, event):
        # Key 'ESC' - Close widget
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            # Check if the click was outside this widget
            if not self.rect().contains(event.pos()):
                self.close()
        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        # Remove the event filter when the widget is closed
        QApplication.instance().removeEventFilter(self)
        super().closeEvent(event)

    def create_items(self, data_set):
        self.checkboxes = []
        for item, status in sorted(data_set.items(), key=lambda x:x[0]):
            checkbox = QCheckBox()
            checkbox.setText(item)
            checkbox.setChecked(status)
            checkbox.stateChanged.connect(self.checkboxes_to_master)
            self.verticalLayout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        # Connecting to the master check button
        self.master_checkbox.stateChanged.connect(self.master_to_checkboxes)

        spacerItem = QSpacerItem(20, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        # Update widget size based on its content
        scrollbox_height = min(self.widget.sizeHint().height() + 20, 160)
        self.scrollArea.setMinimumHeight(scrollbox_height)

        self.setMaximumSize(QSize(400, 400))

    # Check all checkboxes -> update master checkbox
    def checkboxes_to_master(self, state):
        state_master = all(cb.isChecked() for cb in self.checkboxes)
        self.master_checkbox.blockSignals(True)
        self.master_checkbox.setChecked(state_master)
        self.master_checkbox.blockSignals(False)

        state_apply = any(cb.isChecked() for cb in self.checkboxes)
        self.button_apply.setEnabled(state_apply)

    # Apply master checkbox state to all checkboxes
    def master_to_checkboxes(self, state):
        if   state == Qt.CheckState.Checked.value:   checked = True
        elif state == Qt.CheckState.Unchecked.value: checked = False
        else: return
        for cb in self.checkboxes:
            cb.setChecked(checked)


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
            unique_values[value] = False
        for row in range(model.rowCount()):
            index = model.index(row, self.current_col)
            value = model.data(index, Qt.ItemDataRole.DisplayRole)
            unique_values[value] = True

        # Pop up Filter UI as Dialog
        self.filter_popup = FilterWidget(unique_values, self.parent)
        self.filter_popup.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint)

        # Connect signals for the apply and close buttons
        self.filter_popup.button_apply.clicked.connect(self.apply_filter)
        self.filter_popup.button_close.clicked.connect(self.filter_popup.close)

        # Display popup by mouse click position
        popup_x = event.globalPos().x()  # Mouse click global x-coordinate
        popup_y = event.globalPos().y()  # Mouse click global y-coordinate
        self.filter_popup.move(popup_x, popup_y)
        self.filter_popup.show()


    def apply_filter(self):
        # Find all unchecked boxes (to be filtered)
        col_filters = [cb.text() for cb in self.filter_popup.checkboxes if not cb.isChecked()]

        proxy_model = self.table_view.model()
        proxy_model.setFilterForColumn(self.current_col, col_filters)

        # TODO: After applying - add "color"? or indicator
        # Close the popup after applying the filter
        # self.filter_popup.close()

        # Update Search model if visible
        if self.parent.frame_search.isVisible():
            self.parent.search_model.search(self.parent.edit_text_input.text())


if __name__ == "__main__":
    # from PyQt6.QtWidgets import QApplication
    # app = QApplication(sys.argv)
    # sample_data = {"EIE_0x4001111111111111":True, "EIE_0x4002":True, "EIE_0x4003":True, "EIE_0x4004":True}
    # frame = FilterWidget(sample_data)
    # frame.show()
    # sys.exit(app.exec())
    from collections import defaultdict

    d = defaultdict(lambda: True)
    print(d[None])
