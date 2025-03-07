import os
import sys
import time
import threading
from shutil import rmtree

import tkinter as tk
from tkinter import filedialog

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon
from PyQt6 import uic

from GUI import dialog_main
from GUI.gui_settings import SettingsWindow

from IDL import parse_msg


class MainWindow(QMainWindow, dialog_main.Ui_MainWindow) :
    def __init__(self, parent) :
        super().__init__()
        self.setupUi(self)
        # Set Images
        self.parent = parent
        # Set Events
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_start.clicked.connect(self.start_sniffing)
        self.btn_stop.clicked.connect(self.stop_sniffing)
        self.btn_raw_open.clicked.connect(self.open_raw_file)
        self.btn_csv_open.clicked.connect(self.open_csv_file)
        self.btn_csv_create.clicked.connect(self.csv_create_file)
        self.btn_csv_view.clicked.connect(self.csv_view_file)
        self.btn_csv_folder.clicked.connect(self.csv_open_folder)

        self.btn_stop.setEnabled(False)

    def set_icon_path(self, icon_path):
        print(os.path.join(icon_path, "button_settings.png"))
        print(os.path.exists(os.path.join(icon_path, "button_settings.png")))
        print(os.path.exists(os.path.join(icon_path, "button_settings1.png")))
        self.btn_settings.setIcon(QIcon(os.path.join(icon_path, "button_settings.png")))
        self.btn_start.setIcon(QIcon(os.path.join(icon_path, "button_start.png")))
        self.btn_stop.setIcon(QIcon(os.path.join(icon_path, "button_stop.png")))
        self.btn_csv_create.setIcon(QIcon(os.path.join(icon_path, "button_csv_create.png")))
        self.btn_csv_view.setIcon(QIcon(os.path.join(icon_path, "button_csv_view.png")))
        self.btn_csv_folder.setIcon(QIcon(os.path.join(icon_path, "button_csv_folder.png")))

    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.exec()
        print("open_settings")

    def buttons_control_running(self, val):
        self.btn_settings.setDisabled(val)
        self.btn_start.setDisabled(val)
        self.btn_stop.setEnabled(val)
        self.btn_raw_open.setDisabled(val)
        self.btn_csv_open.setDisabled(val)
        self.edit_raw_path.setDisabled(val)
        self.edit_csv_path.setDisabled(val)
        self.btn_csv_create.setDisabled(val)
        self.btn_csv_view.setDisabled(val)


    def start_sniffing(self):
        print("start_sniffing")
        # self.parent.start_sniffing()


        self.buttons_control_running(True)

    def stop_sniffing(self):
        print("stop_sniffing")
        # self.parent.stop_sniffing()

        self.buttons_control_running(False)

    def open_raw_file(self):
        # Select pcap file
        raw_folder_path = os.path.join(os.getcwd(), 'RAW')
        os.makedirs(raw_folder_path, exist_ok=True)
        file_paths = tk.filedialog.askopenfilenames(title='Select PCAP file', filetypes=[("PCAP Files", "*.pcap")],
                                                    initialdir=raw_folder_path)
        file_num = len(file_paths)
        if file_num == 1:   self.edit_raw_path.setText(" " + os.path.split(file_paths[0])[-1])
        elif file_num >= 2: self.edit_raw_path.setText(f" Selected {file_num} Raw Files")
        else: return
        self.raw_file_paths = file_paths
        self.edit_csv_path.setText("")

        # Button 설정하기 TODO
        # self.csv_create_button.configure(state=tk.NORMAL, image=self.csv_create_img_on)
        # self.csv_view_button.configure(state=tk.DISABLED, image=self.csv_view_img_off)

    def open_csv_file(self):
        # Select csv file
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        file_path = tk.filedialog.askdirectory(title='Select CSV folder', initialdir=csv_folder_path)
        if file_path:
            self.csv_file_paths = [file_path]

            self.edit_raw_path.setText(" ")
            self.edit_csv_path.setText(" " + os.path.split(file_path)[-1])
            # Button 설정하기 TODO
            # self.csv_create_button.configure(state=tk.DISABLED, image=self.csv_create_img_off)
            # self.csv_view_button.configure(state=tk.NORMAL, image=self.csv_view_img_on)

    def csv_create_file(self):
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        self.csv_file_paths = list(map(lambda x: os.path.join(csv_folder_path, os.path.split(x)[1].split('.pcap')[0]),
                                       self.raw_file_paths))

        for raw_file_path, new_folder_path in zip(self.raw_file_paths, self.csv_file_paths):
            # Make CSV folder
            print(raw_file_path, new_folder_path)
            if os.path.exists(new_folder_path):
                rmtree(new_folder_path)
            os.makedirs(new_folder_path, exist_ok=True)
            # Parse Msg
            result = parse_msg.raw_to_csv(self.parent, raw_file_path)
            print("result", result)

        file_num = len(self.raw_file_paths)
        if file_num == 1: self.edit_csv_path.setText(" " + os.path.split(self.csv_file_paths[0])[-1])
        if file_num >= 2: self.edit_csv_path.setText(f" Created {file_num} CSV Files")

        # Button 설정하기 TODO
        # self.csv_view_button.configure(state=tk.NORMAL, image=self.csv_view_img_on)

    # View CSV TODO
    def csv_view_file(self):
        print("csv_view_file: Not implemented")

    def csv_open_folder(self):
        # Just open CSV folder
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        os.startfile(csv_folder_path)


    def start_timer(self):
        self.timer_var.set("00 : 00 : 00")
        self.pkt_tcp_var.set(0)
        self.pkt_udp_var.set(0)
        self.timer_thread = threading.Thread(target=update_timer, daemon=True, args=(self, time.time(),))
        self.timer_thread.start()

    def update_timer(self, start_time):
        while self.is_sniffing:
            duration = int(time.time() - start_time)
            if duration >= 0:
                hour = duration // 3600
                minutes = (duration % 3600) // 60
                seconds = duration % 60
                self.timer_var.set(f"{hour:02} : {minutes:02} : {seconds:02}")
            time.sleep(0.2)




if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = MainWindow("3")
    myWindow.show()

    app.exec()