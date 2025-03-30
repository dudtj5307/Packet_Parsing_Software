from PyQt6.QtCore import QSortFilterProxyModel, Qt

class CSVFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_conditions = {}  # {col: [filter texts]}

    def setFilterForColumn(self, column, texts):
        if texts:
            self.filter_conditions[column] = [text.lower() for text in texts]
        else:
            self.filter_conditions.pop(column, None)
        # Refresh Filter
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        for column, filter_list in self.filter_conditions.items():
            index = model.index(source_row, column, source_parent)
            data = str(model.data(index, role=Qt.ItemDataRole.DisplayRole)).lower()
            # Any match will be filtered(hidden)
            if any(filter_text in data for filter_text in filter_list):
                return False
        return True
