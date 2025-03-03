import os, sys

import tkinter as tk
from tkinter import ttk, Frame, messagebox, PhotoImage, font, filedialog

import json

from GUI import gui_settings

def create_widgets(self):
    # Window Size
    self.root.geometry("1200x600")
    self.root.resizable(False, False)

    frame_bg = '#203864'
    button_bg = '#dae3f3'
    # self.root.configure(bg=frame_bg)

    # Icon directory
    self.icon_folder_path = os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else os.getcwd(), 'GUI', 'res')


    title_icon_path = os.path.join(self.icon_folder_path, 'PPS.ico')
    self.root.iconbitmap(title_icon_path)
    '''https://www.flaticon.com/kr/free-icons/ /"파싱 아이콘" > 파싱 아이콘 / zero_wing - Flaticon '''\

    # Font Change
    # self.root.option_add("*Font", ("Arial", 9))

    # ------------------------------------ Frame 1 ------------------------------------- #
    frame1 = Frame(self.root)
    frame1.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    # Setting Button
    self.settings_img_on = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_settings.png'))
    self.settings_img_off = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_settings_off.png'))
    self.settings_button = tk.Button(frame1, borderwidth=0, bg='black', relief="raised", highlightthickness=0,
                                     image=self.settings_img_on, command=lambda: gui_settings.open_settings(self))
    self.settings_button.grid(row=0, column=0, padx=20, pady=10, sticky='w')

    # Start Button
    self.start_img_on = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_start.png'))
    self.start_img_off = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_start_off.png'))
    self.start_button = tk.Button(frame1, borderwidth=0, bg='black', relief="raised", highlightthickness=0,
                                  image=self.start_img_on, command=self.start_sniffing)
    self.start_button.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    # Stop Button
    self.stop_img_on = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_stop.png'))
    self.stop_img_off = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_stop_off.png'))
    self.stop_button = tk.Button(frame1, borderwidth=0, bg='black', relief="raised", highlightthickness=0,
                                 image=self.stop_img_off, command=self.stop_sniffing, state=tk.DISABLED)
    self.stop_button.grid(row=0, column=2, padx=0, pady=10, sticky='w')

    frame2 = Frame(self.root)
    frame2.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    self.raw_path_entry = tk.Entry(frame2, width=40, font=('맑은 고딕',11), state='readonly', textvariable=self.raw_file_var)
    self.raw_path_entry.grid(row=0, column=0, padx=0, pady=5, sticky='n')
    self.raw_path_button = tk.Button(frame2, text="RAW", width=7, height=1, command=lambda: open_raw_file(self))
    self.raw_path_button.grid(row=0, column=1, padx=0, pady=1, sticky='')

    self.csv_path_entry = tk.Entry(frame2, width=40, font=('맑은 고딕',11), state='readonly', textvariable=self.csv_file_var)
    self.csv_path_entry.grid(row=1, column=0, padx=2, pady=1, sticky='')
    self.csv_path_button = tk.Button(frame2, text="CSV", width=7, height=1, command=lambda: open_csv_file(self))
    self.csv_path_button.grid(row=1, column=1, padx=2, pady=1, sticky='')

def start_button_pressed(self):
    self.settings_button.config(state=tk.DISABLED, image=self.settings_img_off)
    self.start_button.configure(state=tk.DISABLED, image=self.start_img_off)
    self.stop_button.configure(state=tk.NORMAL, image=self.stop_img_on)

def stop_button_pressed(self):
    self.settings_button.configure(state=tk.NORMAL, image=self.settings_img_on)
    self.start_button.configure(state=tk.NORMAL, image=self.start_img_on)
    self.stop_button.configure(state=tk.DISABLED, image=self.stop_img_off)


def open_raw_file(self):
    # Select pcap file
    raw_folder_path = os.path.join(os.getcwd(),'RAW')
    os.makedirs(raw_folder_path, exist_ok=True)
    file_path = tk.filedialog.askopenfilenames(title='Select PCAP file', filetypes=[("PCAP Files", "*.pcap")],
                                              initialdir=raw_folder_path)
    file_num = len(file_path)
    if file_num == 1:
        self.raw_file_path = file_path[0]
        self.raw_file_var.set(" "+os.path.split(self.raw_file_path[0])[1])
    elif file_num >= 2:
        self.raw_file_path = file_path
        self.raw_file_var.set(f" Selected {file_num} Raw Files")


def open_csv_file(self):
    # Select csv file
    csv_folder_path = os.path.join(os.getcwd(), 'CSV')
    os.makedirs(csv_folder_path, exist_ok=True)
    file_path = tk.filedialog.askopenfilename(title='Select CSV file', filetypes=[("CSV Files", "*.csv")],
                                              initialdir=csv_folder_path)
    if file_path:
        self.csv_file_path = file_path
        self.csv_file_var.set(os.path.split(file_path)[1])

