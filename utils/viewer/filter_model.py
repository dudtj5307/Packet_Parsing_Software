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

    def setSourceModel(self, model):
        super().setSourceModel(model)
        # Get data from source model
        self.cached_data = model.csv_data_map.copy()  # 얕은 복사

    def setFilterForColumn(self, column, texts):
        # Set filtering column
        self.filter_column = column

        self.filtered_texts = frozenset(text for text in texts)

        # Refresh Filter
        import time
        start = time.time()
        self.invalidateRowsFilter()
        print("complete time:", time.time() - start)


    def filterAcceptsRow(self, source_row, source_parent):
        # if self.source_model is None:
        #     return True
        # index = self.source_model.index(source_row, self.filter_column, source_parent)
        #
        # # Get the text from the model
        # data_text = str(self.source_model.data(index)).lower()
        # return self.col_filters[data_text]  # Will return True by default unless the text is in filtered texts

        # source_model = self.sourceModel()
        # index = source_model.index(source_row, self.filter_column, source_parent)

        # data_text = self.cached_data[source_row][self.filter_column]

        # data_text = str(source_model.data(index)).lower()

        if source_row == 0:
            print(type(self.cached_data[source_row][self.filter_column]), self.filtered_texts)

        return self.cached_data[source_row][self.filter_column] not in self.filtered_texts