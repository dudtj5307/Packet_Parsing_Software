import os, sys
import time
from shutil import rmtree
import threading

import tkinter as tk
from tkinter import ttk, Frame, messagebox, PhotoImage, font, filedialog

from IDL import parse_msg
from GUI import gui_settings

def create_widgets(self):
    # Window Size
    self.root.geometry("770x350")
    self.root.resizable(False, False)

    frame_bg = '#203864'
    button_bg = '#dae3f3'
    label_bg = '#f7f7f5'
    self.root.configure(bg=frame_bg)

    frame_bg = [frame_bg] * 30
    # frame_bg = ['red', 'orange', 'green', 'skyblue', 'purple'] * 5

    # Icon directory
    self.icon_folder_path = os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else os.getcwd(), 'GUI', 'res')


    title_icon_path = os.path.join(self.icon_folder_path, 'PPS.ico')
    self.root.iconbitmap(title_icon_path)
    '''https://www.flaticon.com/kr/free-icons/ /"파싱 아이콘" > 파싱 아이콘 / zero_wing - Flaticon '''\

    # Font Change
    # self.root.option_add("*Font", ("Arial", 9))

    # ------------------------------------  Frame 1  ------------------------------------- #
    frame1 = Frame(self.root, bg=frame_bg[0])
    frame1.grid(row=0, column=0, padx=15, pady=0, sticky='w')
    # ------------------------------------ Frame 1-1 ------------------------------------- #
    frame1_1 = Frame(frame1, bg=frame_bg[1], highlightthickness=2, highlightbackground='skyblue')
    frame1_1.grid(row=0, column=0, padx=0, pady=5, ipadx=4, sticky='w')

    # Setting Button
    self.settings_img_on = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_settings.png'))
    self.settings_img_off = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_settings_off.png'))
    self.settings_button = tk.Button(frame1_1, borderwidth=0, bg='black', relief="raised", highlightthickness=0,
                                     image=self.settings_img_on, command=lambda: gui_settings.open_settings(self))
    self.settings_button.grid(row=0, column=0, padx=11, pady=10, sticky='w')

    # Start Button
    self.start_img_on = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_start.png'))
    self.start_img_off = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_start_off.png'))
    self.start_button = tk.Button(frame1_1, borderwidth=0, bg='black', relief="raised", highlightthickness=0,
                                  image=self.start_img_on, command=self.start_sniffing)
    self.start_button.grid(row=0, column=1, padx=11, pady=10, sticky='w')

    # Stop Button
    self.stop_img_on = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_stop.png'))
    self.stop_img_off = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_stop_off.png'))
    self.stop_button = tk.Button(frame1_1, borderwidth=0, bg='black', relief="raised", highlightthickness=0,
                                 image=self.stop_img_off, command=self.stop_sniffing, state=tk.DISABLED)
    self.stop_button.grid(row=0, column=2, padx=3, pady=10, sticky='w')

    # ------------------------------------ Frame 1-2 ------------------------------------- #
    frame1_2 = Frame(frame1, bg=frame_bg[2])
    frame1_2.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    # Raw Path Entry
    self.raw_path_entry = tk.Entry(frame1_2, width=40, font=('맑은 고딕',10,''), state='readonly', textvariable=self.raw_file_var)
    self.raw_path_entry.grid(row=0, column=1, padx=0, pady=5, sticky='n')
    # Raw Path Button
    self.raw_path_button = tk.Button(frame1_2, text="RAW", font=('맑은 고딕',9,'bold'), bg='#4bbcbc', width=7, height=1, command=lambda: open_raw_file(self))
    self.raw_path_button.grid(row=0, column=0, padx=5, pady=3, sticky='s')
    # CSV Path Entry
    self.csv_path_entry = tk.Entry(frame1_2, width=40, font=('맑은 고딕',10,''), state='readonly', textvariable=self.csv_file_var)
    self.csv_path_entry.grid(row=1, column=1, padx=2, pady=1, sticky='')
    # CSV Path Button
    self.csv_path_button = tk.Button(frame1_2, text="CSV", font=('맑은 고딕',9,'bold'), bg='#57a73d', width=7, height=1, command=lambda: open_csv_file(self))
    self.csv_path_button.grid(row=1, column=0, padx=5, pady=0, sticky='s')

    # ------------------------------------ Frame 1-3 ------------------------------------- #
    frame1_3 = Frame(frame1, bg=frame_bg[3])
    frame1_3.grid(row=0, column=2, padx=0, pady=5, sticky='w')

    # CSV Create Button
    self.csv_create_img_on = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_csv_create.png'))
    self.csv_create_img_off = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_csv_create_off.png'))
    self.csv_create_button = tk.Button(frame1_3, borderwidth=0, bg='black', relief="raised", highlightthickness=0,
                                 image=self.csv_create_img_off, command=lambda: csv_create_file(self), state=tk.DISABLED)
    self.csv_create_button.grid(row=0, column=0, padx=7, pady=10, sticky='w')

    # CSV View Button
    self.csv_view_img_on = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_csv_view.png'))
    self.csv_view_img_off = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_csv_view_off.png'))
    self.csv_view_button = tk.Button(frame1_3, borderwidth=0, bg='black', relief="raised", highlightthickness=0,
                                 image=self.csv_view_img_off, command=lambda: csv_view_file(self), state=tk.DISABLED)
    self.csv_view_button.grid(row=0, column=1, padx=5, pady=10, sticky='w')

    # CSV Folder Open Button
    self.csv_folder_img_on = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_csv_folder.png'))
    self.csv_folder_img_off = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_csv_folder_off.png'))
    self.csv_folder_button = tk.Button(frame1_3, borderwidth=0, bg='black', relief="raised", highlightthickness=0,
                                 image=self.csv_folder_img_on, command=lambda: csv_open_folder(self))
    self.csv_folder_button.grid(row=0, column=2, padx=5, pady=10, sticky='w')

    # ------------------------------------  Frame 2  ------------------------------------- #
    frame2 = Frame(self.root, bg=frame_bg[4], highlightthickness=2, highlightbackground='skyblue')       # purple
    frame2.grid(row=1, column=0, padx=15, pady=0, sticky='w')
    # ------------------------------------ Frame 2-1 ------------------------------------- #
    frame2_1 = Frame(frame2, bg=frame_bg[5])
    frame2_1.grid(row=0, column=0, padx=0, pady=0, sticky='')

    # Duration Timer
    self.timer_label = tk.Label(frame2_1, width=10, height=1, fg='black', bg=label_bg,font=('맑은 고딕', 17, 'bold'),
                                justify='center', textvariable=self.timer_var, state='normal')
    self.timer_label.grid(row=1, column=0, padx=10, ipadx=12, pady=2, columnspan=2, sticky='')
    self.timer_var.set("00 : 00 : 00")

    # File Name Entry
    self.file_name_entry = tk.Entry(frame2_1, width=23, fg='gray', font=('맑은 고딕', 10, 'italic'), justify='center', state=tk.NORMAL)
    self.file_name_entry.grid(row=0, column=0, padx=8, pady=5, ipadx=3, columnspan=2, sticky='')
    set_entry_hint(self.file_name_entry, "Raw File Name")

    # ------------------------------------  Frame 2-2 ------------------------------------- #
    frame2_2 = Frame(frame2, bg=frame_bg[6])
    frame2_2.grid(row=1, column=0, padx=0, pady=0, sticky='')
    # ------------------------------------ Frame 2-2-1 ------------------------------------ #
    frame2_2_1 = Frame(frame2_2, bg=frame_bg[7])
    frame2_2_1.grid(row=0, column=0, padx=0, pady=0, sticky='e')

    # TCP Labels
    self.tcp_label = tk.Label(frame2_2_1, width=6, height=1, fg='black', bg=label_bg, font=('맑은 고딕', 12, 'bold'),
                              text="TCP",justify='center', state='normal')
    self.tcp_label.grid(row=2, column=0, padx=3, pady=4, sticky='e')

    # UDP Labels
    self.udp_label = tk.Label(frame2_2_1, width=6, height=1, fg='black', bg=label_bg, font=('맑은 고딕', 12, 'bold'),
                              text="UDP",justify='center', state='normal')
    self.udp_label.grid(row=3, column=0, padx=3, pady=3, sticky='e')

    # ------------------------------------ Frame 2-2-2 ------------------------------------ #
    frame2_2_2 = Frame(frame2_2, bg=frame_bg[8])
    frame2_2_2.grid(row=0, column=1, padx=4, pady=0, sticky='e')

    # TCP Num
    self.tcp_num_label = tk.Label(frame2_2_2, width=10, height=1, fg='black', bg=label_bg, font=('맑은 고딕', 11),
                                  justify='center', textvariable=self.pkt_tcp_var, state='normal')
    self.tcp_num_label.grid(row=2, column=1, padx=0, pady=5, sticky='e')

    # UDP Num
    self.udp_num_label = tk.Label(frame2_2_2, width=10, height=1, fg='black', bg=label_bg, font=('맑은 고딕', 11),
                                  justify='center', textvariable=self.pkt_udp_var, state='normal')
    self.udp_num_label.grid(row=3, column=1, padx=0, pady=3, sticky='e')

    # ------------------------------------  Frame 2-3 ------------------------------------- #
    frame2_3 = Frame(frame2, bg=frame_bg[10])
    frame2_3.grid(row=2, column=0, padx=8, pady=0, sticky='w')

    # Restart
    self.restart_label = tk.Label(frame2_3, width=6, height=1, fg='black', bg=label_bg, font=('맑은 고딕', 11, 'bold'),
                                  text="Restart",justify='center', state='normal')
    self.restart_label.grid(row=0, column=0, padx=3, pady=4, ipadx=3, sticky='w')
    # Restart hour Entry
    self.hour_entry = tk.Entry(frame2_3, width=5, fg='gray', font=('맑은 고딕', 10, 'italic'), justify='center', state=tk.NORMAL)
    self.hour_entry.grid(row=0, column=1, padx=7, pady=5, sticky='e')
    set_entry_hint(self.hour_entry, "hour")

    # Restart min Entry
    self.min_entry = tk.Entry(frame2_3, width=5, fg='gray', font=('맑은 고딕', 10, 'italic'), justify='center', state=tk.NORMAL)
    self.min_entry.grid(row=0, column=2, padx=6, pady=5, sticky='e')
    set_entry_hint(self.min_entry, "min")


def start_button_pressed(self):
    self.settings_button.config(state=tk.DISABLED, image=self.settings_img_off)
    self.start_button.configure(state=tk.DISABLED, image=self.start_img_off)
    self.stop_button.configure(state=tk.NORMAL, image=self.stop_img_on)
    self.csv_create_button.configure(state=tk.DISABLED, image=self.csv_create_img_off)
    self.csv_view_button.configure(state=tk.DISABLED, image=self.csv_view_img_off)
    self.raw_path_button.configure(state=tk.DISABLED)
    self.csv_path_button.configure(state=tk.DISABLED)

    start_timer(self)

def stop_button_pressed(self):
    self.settings_button.configure(state=tk.NORMAL, image=self.settings_img_on)
    self.start_button.configure(state=tk.NORMAL, image=self.start_img_on)
    self.stop_button.configure(state=tk.DISABLED, image=self.stop_img_off)
    self.csv_create_button.configure(state=tk.NORMAL, image=self.csv_create_img_on)
    self.raw_path_button.configure(state=tk.NORMAL)
    self.csv_path_button.configure(state=tk.NORMAL)

def open_raw_file(self):
    # Select pcap file
    raw_folder_path = os.path.join(os.getcwd(),'RAW')
    os.makedirs(raw_folder_path, exist_ok=True)
    file_paths = tk.filedialog.askopenfilenames(title='Select PCAP file', filetypes=[("PCAP Files", "*.pcap")],
                                              initialdir=raw_folder_path)
    file_num = len(file_paths)
    if file_num == 1:
        self.raw_file_var.set(" "+os.path.split(file_paths[0])[-1])
        self.csv_file_var.set("")
    elif file_num >= 2:
        self.raw_file_var.set(f" Selected {file_num} Raw Files")
        self.csv_file_var.set("")
    else:
        return
    self.raw_file_paths = file_paths
    self.csv_create_button.configure(state=tk.NORMAL, image=self.csv_create_img_on)
    self.csv_view_button.configure(state=tk.DISABLED, image=self.csv_view_img_off)

def open_csv_file(self):
    # Select csv file
    csv_folder_path = os.path.join(os.getcwd(), 'CSV')
    os.makedirs(csv_folder_path, exist_ok=True)
    file_path = tk.filedialog.askdirectory(title='Select CSV folder', initialdir=csv_folder_path)
    if file_path:
        self.csv_file_paths = [file_path]
        self.csv_file_var.set(" "+os.path.split(file_path)[-1])
        self.raw_file_var.set("")

        self.csv_create_button.configure(state=tk.DISABLED, image=self.csv_create_img_off)
        self.csv_view_button.configure(state=tk.NORMAL, image=self.csv_view_img_on)

def csv_create_file(self):
    csv_folder_path = os.path.join(os.getcwd(), 'CSV')
    os.makedirs(csv_folder_path, exist_ok=True)
    self.csv_file_paths = list(map(lambda x: os.path.join(csv_folder_path, os.path.split(x)[1].split('.pcap')[0]),
                                   self.raw_file_paths))

    for folder_path in self.csv_file_paths:
        if os.path.exists(folder_path):
            rmtree(folder_path)
        os.makedirs(folder_path, exist_ok=True)

    for raw_file_path in self.raw_file_paths:
        result = parse_msg.raw_to_csv(self, raw_file_path)
        print(result)

    file_num = len(self.raw_file_paths)
    if file_num == 1:
        self.csv_file_var.set(" " + os.path.split(self.csv_file_paths[0])[-1])
    if file_num >= 2:
        self.csv_file_var.set(f" Created {file_num} CSV Files")

    self.csv_view_button.configure(state=tk.NORMAL, image=self.csv_view_img_on)

def csv_view_file(self):
    pass

def csv_open_folder(self):
    # Select csv file
    csv_folder_path = os.path.join(os.getcwd(), 'CSV')
    os.makedirs(csv_folder_path, exist_ok=True)
    os.startfile(csv_folder_path)

# Entry hint message
def set_entry_hint(entry, hint):
    entry.bind('<FocusIn>', lambda e: entry_focus_in(entry,  hint, e))
    entry.bind('<FocusOut>',lambda e: entry_focus_out(entry, hint, e))
    entry.insert(0, hint)

def entry_focus_in(entry, hint_string, event=None):
    if entry.get() == hint_string:
        entry.delete(0, tk.END)
        entry.config(fg='black', font=('맑은 고딕', 10, 'normal'))  # Text : back to Black
def entry_focus_out(entry, hint_string, event):
    if not entry.get():
        entry.insert(0, hint_string)
        entry.config(fg='gray', font=('맑은 고딕', 10, 'italic'))  # Text : Gray

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