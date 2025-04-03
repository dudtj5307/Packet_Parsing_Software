from collections import defaultdict

from PyQt6.QtCore import QSortFilterProxyModel, Qt

class CSVFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.col_filters = defaultdict(lambda: True)
        self.filter_conditions = {}  # {col: [filter texts]}
        self.filter_column = 0
        self.filtered_texts = set()
        self.cached_data = {}

        self.setDynamicSortFilter(False)

        # Sorting disabled
        # self.setSortRole(Qt.ItemDataRole.UserRole)
        # self.sort(-1)

    def setSourceModel(self, model, QAbstractItemModel=None):
        super().setSourceModel(model)
        # Get data from source model
        self.cached_data = model.csv_data_map.copy()  # 얕은 복사

    def setFilterForColumn(self, column, hide_texts):

        # Set filtering column
        self.filter_column = column

        self.filtered_texts = frozenset(text for text in hide_texts)

        # Refresh Filter
        self.blockSignals(True)
        self.invalidateRowsFilter()
        self.blockSignals(False)
        # Update GUI
        self.layoutChanged.emit()

    def filterAcceptsRow(self, source_row, source_parent):
        return self.cached_data[source_row][self.filter_column] not in self.filtered_texts

    def sort(self, column, order=None):
        pass

    def lessThan(self, left, right):
        return False