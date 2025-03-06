import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog
from PyQt6 import uic
from GUI import dialog_settings

DEFAULT_CONFIG_DATA = {'interface': ["No", "Interface", "Selected"],
                       'IP_local': {'adoc_ip1':  "2", 'adoc_ip2':  "3", 'adoc_ip3':  "",
                                    'wcc_ip1' :  "8", 'wcc_ip2' : "10", 'wcc_ip3' : "13",
                                    'dlu_ip1' : "27", 'dlu_ip2' : "28", 'dlu_ip3' : "30"},
                       'IP_near' : {},
                       'IP_ext'  : {},
                       'raw_file_paths': [""], 'csv_file_paths' : [""]}

class SettingsWindow(QDialog, dialog_settings.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setModal(True)  # Set Modal

        self.parent = parent
        if parent is not None:
            self.center_to_parent()

    def center_to_parent(self):
        parent_geometry = self.parent.geometry()
        child_geometry  = self.geometry()
        # Calculate Coordinate
        x = parent_geometry.x() + (parent_geometry.width()  - child_geometry.width()) // 2
        y = parent_geometry.y() + (parent_geometry.height() - child_geometry.height()) // 2
        self.move(x, y)



if __name__ == "__main__":
    pass