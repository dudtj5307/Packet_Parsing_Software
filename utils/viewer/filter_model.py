from collections import defaultdict

from PyQt6.QtCore import QSortFilterProxyModel, Qt

class CSVFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.col_filters = defaultdict(lambda: True)
        self.filter_conditions = {}  # {col: [filter texts]}
        self.filter_column = 0

    def setFilterForColumn(self, column, texts):
        # Set
        self.filter_column = column
        # Set filtered text to False
        self.col_filters = defaultdict(lambda: True)
        self.col_filters.update({text.lower(): False for text in texts})
        print(self.col_filters)

        # Refresh Filter
        self.invalidateRowsFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        index = model.index(source_row, self.filter_column, source_parent)

        # Get the text from the model
        data_text = str(model.data(index)).lower()
        return self.col_filters[data_text]  # Will return True by default unless the text is in filtered texts

        # for column, filter_list in self.filter_conditions.items():
        #     index = model.index(source_row, column, source_parent)
        #     data = str(model.data(index, role=Qt.ItemDataRole.DisplayRole)).lower()
        #     # Any match will be filtered(hidden)
        #     if any(filter_text in data for filter_text in filter_list):
        #         return False
