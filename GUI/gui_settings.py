import os
from scapy.arch import get_windows_if_list

from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIcon
from GUI.ui.dialog_settings import Ui_SettingsWindow

from utils.ip_config import IP_Config


class SettingsWindow(QDialog, Ui_SettingsWindow):
    def __init__(self, parent=None, p_parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowTitle("Settings")
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(parent.icon_path, "button_settings.png")))

        # ip_config data
        self.ip_config = IP_Config()

        # Parent Objects
        self.parent = parent            # parent            (gui_main.py)

        # Set Signal Functions
        self.combo_iface.mousePressEvent = self.update_combobox_iface
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel.clicked.connect(self.btn_cancel_clicked)
        self.btn_apply.clicked.connect(self.btn_apply_clicked)

        # Setup UI with ip_config data
        self.set_gui_from_config()

    def center_to_parent(self):
        parent, child = self.parent.geometry(), self.geometry()
        # Calculate Coordinate
        x = parent.x() + (parent.width() - child.width()) // 2
        y = parent.y() + (parent.height() - child.height()) // 2
        self.move(x, y)

    def set_gui_from_config(self):
        config = self.ip_config.get()
        # Interface combobox setting
        self.combo_iface.addItem(" ".join(config['interface']), config['interface'])
        # IP Settings
        config_ips = list(config['IP_local'].items()) + list(config['IP_near'].items()) + list(config['IP_ext'].items())
        for key, val in config_ips:
            edit_widget = getattr(self, f'edit_{key}', None)
            if edit_widget:
                edit_widget.setText(val)

    def save_config_data(self):
        config_data = self.ip_config.get()
        # Interface combobox setting
        config_data['interface'] = self.combo_iface.currentData()
        # IP Settings
        for config_dict in [config_data['IP_local'], config_data['IP_near'], config_data['IP_ext']]:
            for key in config_dict.keys():
                edit_widget = getattr(self, f'edit_{key}', None)
                if edit_widget:
                    config_dict[key] = edit_widget.text()
        self.ip_config.update(config_data)

    def update_combobox_iface(self, event):
        # current text backup before reset
        current_text = self.combo_iface.currentText()
        self.combo_iface.clear()
        # Update Network Interface
        for iface in get_windows_if_list():
            if len(iface['ips']) == 0 or "loopback" in iface['name'].lower():
                continue
            name = f"{iface['name']}"
            description = f"{iface['description']}"
            for ip in iface['ips']:
                if all(map(lambda x: x.isdecimal(), ip.split('.'))):
                    self.combo_iface.addItem(" ".join([ip, name, description]), [ip, name, description])
        # find combobox idx by text
        current_combobox_idx = self.combo_iface.findText(current_text)
        self.combo_iface.setCurrentIndex(current_combobox_idx)

        super().mousePressEvent(event)
        self.combo_iface.showPopup()

    def btn_ok_clicked(self):
        self.save_config_data()
        self.close()

    def btn_cancel_clicked(self):
        self.close()

    def btn_apply_clicked(self):
        self.save_config_data()



if __name__ == "__main__":
    pass
    # app = QApplication(sys.argv)
    # settings = SettingsWindow()
    # settings.show()
    # app.exec()