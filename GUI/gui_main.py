import os
import time
import threading
from shutil import rmtree

import tkinter as tk
from tkinter import filedialog

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon, QIntValidator
from PyQt6.QtCore import pyqtSignal, QTimer

from GUI.ui.dialog_main import Ui_MainWindow

from GUI.gui_settings import SettingsWindow
from GUI.gui_progress import ProgressWindow
from GUI.gui_main_timer import GUI_Timer

from GUI.raw_to_csv import RawToCSV

class MainWindow(QMainWindow, Ui_MainWindow) :
    def __init__(self, parent) :
        super().__init__()
        self.setupUi(self)
        # Object variables
        self.parent = parent
        self.settings_window = None
        # GUI_Timer Object
        self.gui_timer = GUI_Timer(self)

        self.restart_thread = None
        # Set Signal Functions
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_start.clicked.connect(self.start_recording)
        self.btn_stop.clicked.connect(self.stop_recording)
        self.btn_raw_open.clicked.connect(self.open_raw_file)
        self.btn_csv_open.clicked.connect(self.open_csv_file)
        self.btn_csv_create.clicked.connect(self.csv_create_file)
        self.btn_csv_view.clicked.connect(self.csv_view_file)
        self.btn_csv_folder.clicked.connect(self.csv_open_folder)

        # Enable/Disable Buttons
        self.lock_ui_controls(False)
        self.btn_csv_create.setEnabled(False)
        # Input Validator
        self.edit_reset_hour.setValidator(QIntValidator(0, 99))
        self.edit_reset_min.setValidator(QIntValidator(0, 999))
        # Settings window

    def set_icon_path(self, icon_path):
        self.btn_settings.setIcon(QIcon(os.path.join(icon_path, "button_settings.png")))
        self.btn_start.setIcon(QIcon(os.path.join(icon_path, "button_start.png")))
        self.btn_stop.setIcon(QIcon(os.path.join(icon_path, "button_stop.png")))
        self.btn_csv_create.setIcon(QIcon(os.path.join(icon_path, "button_csv_create.png")))
        self.btn_csv_view.setIcon(QIcon(os.path.join(icon_path, "button_csv_view.png")))
        self.btn_csv_folder.setIcon(QIcon(os.path.join(icon_path, "button_csv_folder.png")))

    def lock_ui_controls(self, lock):
        self.btn_settings.setDisabled(lock)
        self.btn_start.setDisabled(lock)
        self.btn_stop.setEnabled(lock)
        self.btn_raw_open.setDisabled(lock)
        self.btn_csv_open.setDisabled(lock)
        self.edit_raw_path.setDisabled(lock)
        self.edit_csv_path.setDisabled(lock)
        self.btn_csv_create.setDisabled(lock)
        self.btn_csv_view.setDisabled(True)
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
        if not self.parent.start_sniffing(): return
        if not self.gui_timer.start(): return

        self.lock_ui_controls(True)

        # Recursive Restart Recording
        hour, min_ = self.edit_reset_hour.text(), self.edit_reset_min.text()
        if not hour: hour = "0"
        if not min_: min_ = "0"
        if hour.isdigit() and min_.isdigit() and (int(hour)>=1 or int(min_)>=1):
            delay = 3600 * int(hour) + 60 * int(min_)
            # Set restart Timer
            self.restart_thread = threading.Timer(delay, self.restart_recording)
            self.restart_thread.start()

    def stop_recording(self):
        self.parent.stop_sniffing()

        self.gui_timer.stop()
        self.lock_ui_controls(False)

        if self.restart_thread and self.restart_thread.is_alive():
            self.restart_thread.cancel()

    def restart_recording(self):
        if self.parent.is_sniffing:
            self.stop_recording()
            print("Restarting!!")
            self.start_recording()

    def open_raw_file(self):
        # Select pcap file
        raw_folder_path = os.path.join(os.getcwd(), 'RAW')
        os.makedirs(raw_folder_path, exist_ok=True)
        file_paths = tk.filedialog.askopenfilenames(title='Select PCAP file', filetypes=[("PCAP Files", "*.pcap")],
                                                    initialdir=raw_folder_path)
        file_num = len(file_paths)
        if file_num == 1:   self.edit_raw_path.setText(os.path.split(file_paths[0])[-1])
        elif file_num >= 2: self.edit_raw_path.setText(f"Selected {file_num} Raw Files")
        else: return
        self.parent.raw_file_paths = file_paths
        self.edit_csv_path.setText("")

        self.btn_csv_create.setEnabled(True)
        self.btn_csv_view.setEnabled(False)

    def open_csv_file(self):
        # Select csv file
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        file_path = tk.filedialog.askdirectory(title='Select CSV folder', initialdir=csv_folder_path)
        if file_path:
            self.parent.csv_file_paths = [file_path]

            self.edit_raw_path.setText("")
            self.edit_csv_path.setText(os.path.split(file_path)[-1])

            self.btn_csv_create.setEnabled(False)
            self.btn_csv_view.setEnabled(True)

    def csv_create_file(self):
        raw_to_csv = RawToCSV(self, self.parent, self.parent.csv_file_paths)
        raw_to_csv.run()

        # print("rest going on")
        # if self.is_csv_creating:
        #     csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        #     os.makedirs(csv_folder_path, exist_ok=True)
        #     self.parent.csv_file_paths = list(map(lambda x: os.path.join(csv_folder_path, os.path.split(x)[1].split('.pcap')[0]),
        #                                    self.parent.raw_file_paths))
        #     progresses = [0, 0, 0]
        #     file_num = len(self.parent.raw_file_paths)
        #     for raw_file_path, new_folder_path in zip(self.parent.raw_file_paths, self.parent.csv_file_paths):
        #         # Make CSV folder
        #         if os.path.exists(new_folder_path):
        #             rmtree(new_folder_path)
        #         os.makedirs(new_folder_path, exist_ok=True)
        #         # Parse Msg TODO
        #         # result = parse_msg.raw_to_csv(self.parent, raw_file_path)
        #         # print("result", result)
        #
        #     if file_num == 1:
        #         self.edit_csv_path.setText(os.path.split(self.parent.csv_file_paths[0])[-1])
        #         self.btn_csv_view.setEnabled(True)
        #     if file_num >= 2:
        #         self.edit_csv_path.setText(f"Created {file_num} CSV Files")
        #
        # print("CSV parse finished")

    # View CSV TODO
    def csv_view_file(self):
        print("csv_view_file: Not implemented")

    def csv_open_folder(self):
        # Just open CSV folder
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        os.startfile(csv_folder_path)


if __name__ == "__main__" :
    pass