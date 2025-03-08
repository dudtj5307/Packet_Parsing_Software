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
    def __init__(self, parent=None, p_parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowTitle("Settings")
        self.setupUi(self)
        # Parent Objects
        self.parent = parent            # parent            (gui_main.py)
        self.p_parent = p_parent        # parent of parent  (PPS.py)
        if parent is not None:
            self.center_to_parent()

        # Set Signal Functions
        # self.combo_iface.focusInEvent = self.update_combobox_iface
        self.combo_iface.activated.connect(self.update_combobox_iface)
        self.combo_iface.currentIndexChanged.connect(self.select_combobox_iface)
        # self.combo_iface.popup

        self.set_config_data()
        # self.save_config_data()


    def center_to_parent(self):
        parent, child = self.parent.geometry(), self.geometry()
        # Calculate Coordinate
        x = parent.x() + (parent.width() - child.width()) // 2
        y = parent.y() + (parent.height() - child.height()) // 2
        self.move(x, y)

    def set_config_data(self):
        config = self.p_parent.config_data

        # IP Settings
        config_ips = list(config['IP_local'].items()) + list(config['IP_near'].items()) + list(config['IP_ext'].items())
        for key, val in config_ips:
            edit_widget = getattr(self, f'edit_{key}', None)
            if edit_widget:
                edit_widget.setText(val)

    def save_config_data(self):
        config_origin = self.p_parent.config_data

        # IP Settings
        for config_dict in [config_origin['IP_local'], config_origin['IP_near'], config_origin['IP_ext']]:
            for key in config_dict.keys():
                edit_widget = getattr(self, f'edit_{key}', None)
                if edit_widget:
                    config_dict[key] = edit_widget.text()
        # Save to 'settings.conf'
        self.p_parent.save_config_data()

    def update_combobox_iface(self, event):
        # super().dropEvent(event)
        print("update")

    def select_combobox_iface(self):
        print('Selected')
        pass




if __name__ == "__main__":
    pass
    # app = QApplication(sys.argv)
    # settings = SettingsWindow()
    # settings.show()
    # app.exec()