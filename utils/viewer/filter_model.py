from collections import defaultdict

from PyQt6.QtCore import QSortFilterProxyModel, Qt

class CSVFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.col_filters = defaultdict(lambda: True)
        self.filter_conditions = {}  # {col: [filter texts]}
        self.filter_column = 0
        self.filtered_texts = set()

    def setFilterForColumn(self, column, texts):
        # Set filtering column
        self.filter_column = column
        # Set filtered text to False
        # self.col_filters = defaultdict(lambda: True)
        # self.col_filters.update({text.lower(): False for text in texts})

        self.filtered_texts = frozenset(text.lower() for text in texts)

        print(self.filtered_texts)

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

        source_model = self.sourceModel()
        index = source_model.index(source_row, self.filter_column, source_parent)
        data_text = str(source_model.data(index)).lower()

        return data_text not in self.filtered_texts