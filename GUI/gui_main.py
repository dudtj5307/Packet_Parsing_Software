import os
import threading

from tkinter import filedialog, messagebox

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon, QIntValidator, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

from GUI.ui.dialog_main import Ui_MainWindow

from GUI.gui_settings import SettingsWindow
from GUI.gui_viewer import ViewerWindow

from utils.stopwatch import StopWatch

from utils.raw_to_csv_converter import RawToCSVConverter

COMPLETE, STOPPED = True, False
SUCCESS, ERROR = True, False

class MainWindow(QMainWindow, Ui_MainWindow) :
    def __init__(self, parent) :
        super().__init__()
        self.setupUi(self)
        # Object variables
        self.parent = parent
        # Imported Modules
        self.settings_window = None
        self.restart_thread = None
        self.clock = StopWatch(self)
        # Button icons path
        self.icon_path = ""
        # Created CSV file paths
        self.raw_file_paths = []
        self.csv_file_paths = []
        # CSV Viewers - prevent garbage collection
        self.csv_viewers = []

        # Set Signal Functions
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_start.clicked.connect(self.start_recording)
        self.btn_stop.clicked.connect(self.stop_recording)
        self.btn_raw_open.clicked.connect(self.open_raw_file)
        self.btn_csv_open.clicked.connect(self.open_csv_file)
        self.btn_csv_create.clicked.connect(self.csv_create_file)
        self.btn_csv_view.clicked.connect(self.csv_view_file)
        self.btn_csv_folder.clicked.connect(self.csv_open_folder)

        self.clock.set_clock_time.connect(self.set_clock_time)

        # Enable/Disable Buttons
        self.lock_ui_controls(False)
        self.btn_csv_create.setEnabled(False)

        # Input Validator
        regex_pattern = r'^(?!^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?$)[^<>:"/\\|?*\x00-\x1F]{1,255}$'
        self.edit_file_name.setValidator(QRegularExpressionValidator(QRegularExpression(regex_pattern)))
        self.edit_reset_hour.setValidator(QIntValidator(0, 99, self.edit_reset_hour))
        self.edit_reset_min.setValidator(QIntValidator(0, 99, self.edit_reset_min))

    def tcp_num_set(self, val_str):
        self.edit_tcp_num.setText(val_str)

    def udp_num_set(self, val_str):
        self.edit_udp_num.setText(val_str)

    def set_clock_time(self, time_str):
        self.edit_clock.setText(time_str)

    def raw_path_set(self, raw_file_path):
        self.edit_raw_path.setText(os.path.split(raw_file_path)[1])
        self.raw_file_paths = [raw_file_path]

    def set_button_img(self, widget, image):
        img_normal = os.path.join(self.icon_path, image).replace('\\', '/')
        img_pressed = os.path.join(self.icon_path, image).replace('\\', '/').replace(".png", "_pressed.png")
        img_disabled = os.path.join(self.icon_path, image).replace('\\', '/').replace(".png", "_disabled.png")
        widget.setStyleSheet(f"""QPushButton {{border: none; border-image: url("{img_normal}");}}
                                 QPushButton:pressed  {{border-image: url({img_pressed});}}
                                 QPushButton:disabled {{border-image: url({img_disabled});}}""")

    def set_icon_path(self, icon_path):
        self.icon_path = icon_path
        self.setWindowIcon(QIcon(os.path.join(icon_path, "PPS.ico")))
        self.set_button_img(self.btn_settings,   "button_settings.png")
        self.set_button_img(self.btn_start,      "button_start.png")
        self.set_button_img(self.btn_stop,       "button_stop.png")
        self.set_button_img(self.btn_csv_create, "button_csv_create.png")
        self.set_button_img(self.btn_csv_view,   "button_csv_view.png")
        self.set_button_img(self.btn_csv_folder, "button_csv_folder.png")

    def lock_ui_controls(self, lock):
        self.btn_settings.setDisabled(lock)
        self.btn_start.setDisabled(lock)
        self.btn_stop.setEnabled(lock)
        self.btn_raw_open.setDisabled(lock)
        self.btn_csv_open.setDisabled(lock)
        self.edit_raw_path.setDisabled(lock)
        self.edit_csv_path.setDisabled(lock)
        self.btn_csv_create.setDisabled(lock)
        self.btn_csv_view.setDisabled(True)       # TODO: View CSV
        # self.btn_csv_view.setDisabled(lock)
        self.edit_reset_min.setDisabled(lock)
        self.edit_reset_hour.setDisabled(lock)
        if lock:
            self.parent.pkt_tcp_num = 0
            self.parent.pkt_udp_num = 0
            self.edit_tcp_num.setText("0")
            self.edit_udp_num.setText("0")
            self.edit_csv_path.setText("")

    def open_settings(self):
        self.settings_window = SettingsWindow(self, self.parent)
        self.settings_window.show()

    def start_recording(self):
        if self.parent.start_sniffing() == ERROR: return
        if self.clock.start()       == ERROR: return

        self.lock_ui_controls(True)

        # Recursive Restart
        reset_hour, reset_min = int(self.edit_reset_hour.text() or "0"), int(self.edit_reset_min.text() or "0")
        if reset_hour + reset_min > 0:
            delay_sec = 3600 * reset_hour + 60 * reset_min
            # Set restart Timer
            self.restart_thread = threading.Timer(delay_sec, self.restart_recording)
            self.restart_thread.start()

    def stop_recording(self):
        self.parent.stop_sniffing()

        self.clock.stop()
        self.lock_ui_controls(False)

        if self.restart_thread and self.restart_thread.is_alive():
            self.restart_thread.cancel()

    def restart_recording(self):
        if self.parent.is_sniffing:
            self.stop_recording()
            self.start_recording()

    def open_raw_file(self):
        # Select pcap file
        raw_folder_path = os.path.join(os.getcwd(), 'RAW')
        os.makedirs(raw_folder_path, exist_ok=True)
        file_paths = filedialog.askopenfilenames(title='Select PCAP file', filetypes=[("PCAP Files", "*.pcap")],
                                                    initialdir=raw_folder_path)
        file_num = len(file_paths)
        if file_num == 1:   self.edit_raw_path.setText(os.path.split(file_paths[0])[-1])
        elif file_num >= 2: self.edit_raw_path.setText(f"Selected {file_num} Raw Files")
        else: return
        self.raw_file_paths = file_paths
        self.edit_csv_path.setText("")

        self.btn_csv_create.setEnabled(True)
        self.btn_csv_view.setEnabled(False)       # TODO: View CSV

    def open_csv_file(self):
        # Select csv file
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        file_path = filedialog.askdirectory(title='Select CSV folder', initialdir=csv_folder_path)
        if file_path:
            self.csv_file_paths = [file_path]

            self.edit_raw_path.setText("")
            self.edit_csv_path.setText(os.path.split(file_path)[-1])

            self.btn_csv_create.setEnabled(False)
            self.btn_csv_view.setEnabled(True)       # TODO: View CSV

    def csv_create_file(self):
        os.makedirs(os.path.join(os.getcwd(), 'IDL'), exist_ok=True)
        idl_folder_path = os.path.join(os.getcwd(), 'IDL')
        if not os.path.isdir(idl_folder_path) or not [f for f in os.listdir(idl_folder_path)]:
            messagebox.showerror("File Error", "Please insert IDL files")
            os.startfile(idl_folder_path)
            return

        csv_converter = RawToCSVConverter(self, self.raw_file_paths)
        csv_converter.run()
        if csv_converter.progress_backend.stopped:
            return

        # Display to edit_csv_path
        self.csv_file_paths = csv_converter.progress_backend.csv_file_paths
        file_num = len(self.csv_file_paths)
        if file_num == 1:
            self.edit_csv_path.setText(os.path.split(self.csv_file_paths[0])[-1])
            self.btn_csv_view.setEnabled(True)       # TODO: View CSV
        if file_num >= 2:
            self.edit_csv_path.setText(f"Created {file_num} CSV Files")
            self.btn_csv_view.setEnabled(False)  # TODO: View CSV

    # TODO: View CSV
    def csv_view_file(self):
        csv_viewer = ViewerWindow(self, self.csv_file_paths)
        csv_viewer.show()
        self.csv_viewers.append(csv_viewer)


    def csv_open_folder(self):
        # Just open CSV folder
        csv_root_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_root_folder_path, exist_ok=True)
        os.startfile(csv_root_folder_path)

    def closeEvent(self, event):
        # Close child viewers
        for viewer in self.csv_viewers:
            try: viewer.close()
            except: pass
        # Override super
        super().closeEvent(event)

if __name__ == "__main__" :
    pass