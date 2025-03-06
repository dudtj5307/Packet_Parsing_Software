import os
import sys
import subprocess

import tkinter as tk
from tkinter import filedialog

from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt6 import uic

from GUI import dialog_main
from GUI.gui_settings2 import SettingsWindow


class MainWindow(QMainWindow, dialog_main.Ui_MainWindow) :
    def __init__(self, parent) :
        super().__init__()
        self.setupUi(self)
        # Set Events
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_start.clicked.connect(self.start_sniffing)
        self.btn_stop.clicked.connect(self.stop_sniffing)
        self.btn_raw_open.clicked.connect(self.open_raw_file)
        self.btn_csv_open.clicked.connect(self.open_csv_file)
        self.btn_csv_create.clicked.connect(self.csv_create_file)
        self.btn_csv_view.clicked.connect(self.csv_view_file)
        self.btn_csv_folder.clicked.connect(self.csv_open_folder)

        self.parent = parent

    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.exec()
        print("open_settings")

    def start_sniffing(self):
        print("start_sniffing")
        self.parent.start_sniffing()

    def stop_sniffing(self):
        print("stop_sniffing")
        self.parent.stop_sniffing()

    def open_raw_file(self):
        # Select pcap file
        raw_folder_path = os.path.join(os.getcwd(), 'RAW')
        os.makedirs(raw_folder_path, exist_ok=True)
        file_paths = tk.filedialog.askopenfilenames(title='Select PCAP file', filetypes=[("PCAP Files", "*.pcap")],
                                                    initialdir=raw_folder_path)
        file_num = len(file_paths)
        # if file_num == 1:
        #     self.raw_file_var.set(" " + os.path.split(file_paths[0])[-1])
        #     self.csv_file_var.set("")
        # elif file_num >= 2:
        #     self.raw_file_var.set(f" Selected {file_num} Raw Files")
        #     self.csv_file_var.set("")
        # else:
        #     return
        self.raw_file_paths = file_paths
        # self.csv_create_button.configure(state=tk.NORMAL, image=self.csv_create_img_on)
        # self.csv_view_button.configure(state=tk.DISABLED, image=self.csv_view_img_off)

    def open_csv_file(self):
        # Select csv file
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        file_path = tk.filedialog.askdirectory(title='Select CSV folder', initialdir=csv_folder_path)
        if file_path:
            self.csv_file_paths = [file_path]
            # self.csv_file_var.set(" " + os.path.split(file_path)[-1])
            # self.raw_file_var.set("")
            #
            # self.csv_create_button.configure(state=tk.DISABLED, image=self.csv_create_img_off)
            # self.csv_view_button.configure(state=tk.NORMAL, image=self.csv_view_img_on)


    def csv_create_file(self):
        print("csv_create_file")

    def csv_view_file(self):
        print("csv_view_file")

    def csv_open_folder(self):
        # Just open CSV folder
        csv_folder_path = os.path.join(os.getcwd(), 'CSV')
        os.makedirs(csv_folder_path, exist_ok=True)
        os.startfile(csv_folder_path)







if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = MainWindow()
    myWindow.show()

    app.exec()