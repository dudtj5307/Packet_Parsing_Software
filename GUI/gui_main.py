import os, sys
import tkinter as tk
from tkinter import ttk, Frame, messagebox, PhotoImage, font

import json

from GUI import gui_settings

def create_widgets(self):
    # Window Size
    self.root.geometry("1200x600")
    self.root.resizable(False, False)
    # Icon directory
    icon_folder_path = os.path.join(self.current_path, 'GUI', 'res')
    title_icon_path = os.path.join(icon_folder_path, 'PPS.ico')
    self.root.iconbitmap(title_icon_path)
    '''https://www.flaticon.com/kr/free-icons/ /"파싱 아이콘" > 파싱 아이콘 / zero_wing - Flaticon '''\

    # Font Change
    # self.root.option_add("*Font", ("Arial", 9))

    # ------------------------------------ Frame 1 ------------------------------------- #
    frame1 = Frame(self.root)
    frame1.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    # Setting Button
    self.settings_img = PhotoImage(file=icon_folder_path+"/button_settings.png")
    self.settings_button = tk.Button(frame1, image=self.settings_img, borderwidth=3,
                                     command=lambda: gui_settings.open_settings(self))
    self.settings_button.grid(row=0, column=0, padx=20, pady=10, sticky='w')

    # Start Button
    self.start_img = PhotoImage(file=icon_folder_path+"/button_start.png")
    self.start_button = tk.Button(frame1, image=self.start_img, borderwidth=3,
                                  command=self.start_sniffing)
    self.start_button.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    # Stop Button
    self.stop_img = PhotoImage(file=icon_folder_path+"/button_stop.png")
    self.stop_button = tk.Button(frame1, image=self.stop_img, borderwidth=3,
                                 command=self.stop_sniffing)
    self.stop_button.grid(row=0, column=2, padx=0, pady=10, sticky='w')


def start_button_pressed(self):
    self.settings_button.config(state=tk.DISABLED)
    self.start_button.config(state=tk.DISABLED)
    self.stop_button.config(state=tk.NORMAL)

def stop_button_pressed(self):
    self.settings_button.config(state=tk.NORMAL)
    self.start_button.config(state=tk.NORMAL)
    self.stop_button.config(state=tk.DISABLED)


