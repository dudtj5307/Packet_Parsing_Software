import sys
from PyQt6.QtWidgets import QApplication, QDialog
from GUI.dialog_settings import Ui_SettingsWindow

DEFAULT_CONFIG_DATA = {'interface': [" No", "Interface", "Selected"],
                       'IP_local': {'adoc_ip1':  "2", 'adoc_ip2':  "3", 'adoc_ip3':  "",
                                    'wcc_ip1' :  "8", 'wcc_ip2' : "10", 'wcc_ip3' : "11", 'wcc_ip4': "13",
                                    'dlu_ip1' : "27", 'dlu_ip2' : "28", 'dlu_ip3' : "30"},
                       'IP_near' : {'mdil_ip1' : "110", 'mdil_ip2' : "116", 'mdil_ip3' : "6"},
                       'IP_ext'  : {'kicc_ip1' : "", 'kicc_ip2' : "", 'kicc_ip3' : "", 'kicc_ip4' : "",
                                    'kamd_ip1' : "", 'kamd_ip2' : "", 'kamd_ip3' : "", 'kamd_ip4' : "",
                                    'picc_ip1' : "", 'picc_ip2' : "", 'picc_ip3' : "", 'picc_ip4' : ""},
                       'raw_file_paths': [""], 'csv_file_paths' : [""]}

class SettingsWindow(QDialog, Ui_SettingsWindow):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setupUi(self)
        # self.setModal(True)  # Set Modal

        self.parent = parent
        # if parent is not None:
        #     self.center_to_parent()

    def center_to_parent(self):
        parent_geometry, child_geometry = self.parent.geometry(), self.geometry()
        # Calculate Coordinate
        x = parent_geometry.x() + (parent_geometry.width()  - child_geometry.width()) // 2
        y = parent_geometry.y() + (parent_geometry.height() - child_geometry.height()) // 2
        self.move(x, y)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings = SettingsWindow()
    settings.show()
    app.exec()