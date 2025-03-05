import os, sys

from scapy.arch import get_windows_if_list

import tkinter as tk
from tkinter import ttk, Frame, messagebox, PhotoImage, font

DEFAULT_CONFIG_DATA = {'interface': ["No", "Interface", "Selected"],
                       'IP_local': {'adoc_ip1':  "2", 'adoc_ip2':  "3", 'adoc_ip3':  "",
                                    'wcc_ip1' :  "8", 'wcc_ip2' : "10", 'wcc_ip3' : "13",
                                    'dlu_ip1' : "27", 'dlu_ip2' : "28", 'dlu_ip3' : "30"},
                       'IP_near' : {},
                       'IP_ext'  : {},
                       'raw_file_paths': [""], 'csv_file_paths' : [""]}

def open_settings(self):
    window_width, window_height = 650, 455
    p = self.root # p : parent window
    p.update_idletasks()  # Update Window Info
    x = p.winfo_x() + (p.winfo_width() - window_width) // 2
    y = p.winfo_y() + (p.winfo_height() - window_height) // 2

    # Set to middle of parent window
    settings_window = tk.Toplevel(self.root)  # 새로운 창 생성
    settings_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    settings_window.resizable(False, False)
    settings_window.title("Settings")

    # Do-Modal
    settings_window.transient(self.root)  # 부모 창(root)과 연결
    settings_window.grab_set()            # 설정 창이 닫히기 전까지 다른 창 클릭 불가

    # Settings Title Icon
    settings_icon = PhotoImage(file=os.path.join(self.icon_folder_path, 'button_settings.png'))
    settings_window.iconphoto(True, settings_icon)

    # Initialize every open
    self.iface_selected_idx = -1

    # ------------------------------------ Frame 1 ------------------------------------- #
    frame1 = Frame(settings_window)
    frame1.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    # Network Interface 1
    self.iface_label = tk.Label(frame1, text=">  Network Interface")
    self.iface_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    self.iface_combobox1 = ttk.Combobox(frame1, textvariable=self.iface_selected_var, width=65, state="readonly")
    self.iface_combobox1.grid(row=0, column=1, padx=5, pady=10)
    self.iface_combobox1.set(self.iface_selected)

    self.iface_selected_var.set(self.iface_selected)

    # Function Binding
    self.iface_combobox1.bind("<Button-1>", lambda event: update_iface_combobox(self, self.iface_combobox1))
    self.iface_combobox1.bind("<<ComboboxSelected>>", lambda event: select_iface_combobox(self, event))

    # IP Setting Text
    self.iface_label = tk.Label(frame1, text=">  IP Setting")
    self.iface_label.grid(row=1, column=0, padx=10, pady=0, sticky='wn')

    # ------------------------------------ Frame 2 ------------------------------------- #
    frame2 = Frame(settings_window)
    frame2.grid(row=1, column=0, padx=20, pady=0)

    # ----------------------------------- Frame 2-1 ------------------------------------ #
    frame2_1 = Frame(frame2, bd=1, relief='ridge', width=280, height=150)
    frame2_1.grid(row=0, column=0, padx=20, pady=2)
    frame2_1.grid_propagate(False)

    internal_label = tk.Label(frame2_1, text=" ▶  Internal IP - 192. 168. 0. X")
    internal_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='wn')

    frame2_1_body = Frame(frame2_1)
    frame2_1_body.grid(row=1, column=0, padx=0, pady=2)

    adoc_label = tk.Label(frame2_1_body, text="ADOC")
    adoc_label.grid(    row=1, column=0, padx=30, pady=6, sticky='nw')
    self.adoc_ip_entry1 = tk.Entry(frame2_1_body, justify="center", width=5)
    self.adoc_ip_entry2 = tk.Entry(frame2_1_body, justify="center", width=5)
    self.adoc_ip_entry3 = tk.Entry(frame2_1_body, justify="center", width=5)
    self.adoc_ip_entry1.grid(row=1, column=1, padx=5,  pady=6, sticky='nw')
    self.adoc_ip_entry2.grid(row=1, column=2, padx=10, pady=6, sticky='nw')
    self.adoc_ip_entry3.grid(row=1, column=3, padx=10, pady=6, sticky='nw')

    wcc_label = tk.Label(frame2_1_body, text="WCC")
    wcc_label.grid(    row=2, column=0, padx=30, pady=6, sticky='nw')
    self.wcc_ip_entry1 = tk.Entry(frame2_1_body, justify="center", width=5)
    self.wcc_ip_entry2 = tk.Entry(frame2_1_body, justify="center", width=5)
    self.wcc_ip_entry3 = tk.Entry(frame2_1_body, justify="center", width=5)
    self.wcc_ip_entry1.grid(row=2, column=1, padx=5,  pady=6, sticky='nw')
    self.wcc_ip_entry2.grid(row=2, column=2, padx=10, pady=6, sticky='nw')
    self.wcc_ip_entry3.grid(row=2, column=3, padx=10, pady=6, sticky='nw')

    dlu_label = tk.Label(frame2_1_body, text="DLU")
    dlu_label.grid(    row=3, column=0, padx=30, pady=6, sticky='nw')
    self.dlu_ip_entry1 = tk.Entry(frame2_1_body, justify="center", width=5)
    self.dlu_ip_entry2 = tk.Entry(frame2_1_body, justify="center", width=5)
    self.dlu_ip_entry3 = tk.Entry(frame2_1_body, justify="center", width=5)
    self.dlu_ip_entry1.grid(row=3, column=1, padx=5,  pady=6, sticky='nw')
    self.dlu_ip_entry2.grid(row=3, column=2, padx=10, pady=6, sticky='nw')
    self.dlu_ip_entry3.grid(row=3, column=3, padx=10, pady=6, sticky='nw')

    try:
        self.adoc_ip_entry1.insert(0, self.config_data['IP_local']['adoc_ip1'])
        self.adoc_ip_entry2.insert(0, self.config_data['IP_local']['adoc_ip2'])
        self.adoc_ip_entry3.insert(0, self.config_data['IP_local']['adoc_ip3'])
        self.adoc_ip_entry3.configure(state='readonly')
        self.wcc_ip_entry1.insert(0, self.config_data['IP_local']['wcc_ip1'])
        self.wcc_ip_entry2.insert(0, self.config_data['IP_local']['wcc_ip2'])
        self.wcc_ip_entry3.insert(0, self.config_data['IP_local']['wcc_ip3'])
        self.dlu_ip_entry1.insert(0, self.config_data['IP_local']['dlu_ip1'])
        self.dlu_ip_entry2.insert(0, self.config_data['IP_local']['dlu_ip2'])
        self.dlu_ip_entry3.insert(0, self.config_data['IP_local']['dlu_ip3'])
    except:
        settings_window.destroy()
        messagebox.showerror("Error", f" Invalid File : \'setting.config\' \n Configuration Initialized ! ")
        if os.path.exists("settings.conf"):
            os.remove("settings.conf")
        self.save_config_data(changes=DEFAULT_CONFIG_DATA)

        return open_settings(self)

    # ----------------------------------- Frame 2-2 ------------------------------------ #
    frame2_2 = Frame(frame2, bd=1, relief='ridge', width=280, height=150)
    frame2_2.grid(row=0, column=1, padx=5, pady=2)
    frame2_2.grid_columnconfigure(0, minsize=300)
    frame2_2.grid_rowconfigure(0, minsize=150)
    frame2_2.grid_propagate(False)

    # ----------------------------------- Frame 2-3 ------------------------------------ #
    frame2_3 = Frame(frame2, bd=1, relief='ridge', width=280, height=150)
    frame2_3.grid(row=1, column=0, padx=5, pady=5)
    frame2_3.grid_columnconfigure(0, minsize=300)
    frame2_3.grid_rowconfigure(0, minsize=150)
    frame2_3.grid_propagate(False)


    # ------------------------------------ Frame 3 ------------------------------------- #
    frame3 = Frame(settings_window)
    frame3.grid(row=2, column=0, padx=15, pady=20, sticky='es')

    # OK Button
    self.ok_button = tk.Button(frame3, text="OK", width=6, height=1, command= lambda: (self.save_config_data(get_config_data(self)), settings_window.destroy()))
    self.ok_button.grid(row=0, column=0, padx=5, pady=10, sticky='se')
    # Close Button
    self.close_button = tk.Button(frame3, text="Close", width=6, height=1, command=lambda: settings_window.destroy())
    self.close_button.grid(row=0, column=1, padx=5, pady=10, sticky='se')
    # Apply Button
    self.apply_button = tk.Button(frame3, text="Apply", width=6, height=1, command= lambda: self.save_config_data(get_config_data(self)))
    self.apply_button.grid(row=0, column=2, padx=5, pady=10, sticky='se')

# ComboBox List Expanded
def update_iface_combobox(self, self_combox, event=None):
    # Update Network Interface
    self.iface_list = []
    for iface in get_windows_if_list():
        if len(iface['ips']) == 0 or "loopback" in iface['name'].lower():
            continue
        iface_name = f"{iface['name']}"
        iface_description = f"{iface['description']}"
        for ip in iface['ips']:
            if all(map(lambda x: x.isdecimal(), ip.split('.'))):
                iface_ip = ip
                self.iface_list.append([iface_ip, iface_name, iface_description])

    # Update ComboBox List
    self_combox['values'] = self.iface_list

# ComboBox Item Selected
def select_iface_combobox(self, event):
    self.iface_selected_idx = self.iface_combobox1.current()

    # # Inserting this computer IP info
    self.adoc_ip_entry3.configure(state=tk.NORMAL)
    self.adoc_ip_entry3.delete(0, tk.END)
    self.adoc_ip_entry3.insert(0, self.iface_combobox1['values'][self.iface_selected_idx][0].split('.')[-1])
    self.adoc_ip_entry3.configure(state='readonly')

    print(f"Interface Selected :", self.iface_selected_var.get())

def get_config_data(self):
    if self.iface_selected_idx != -1: self.iface_selected = self.iface_combobox1['values'][self.iface_selected_idx]
    # Default Configuration of GUI data
    config_data = {'interface': self.iface_selected,
                   'IP_local': {'adoc_ip1': self.adoc_ip_entry1.get(), 'adoc_ip2': self.adoc_ip_entry2.get(), 'adoc_ip3': self.adoc_ip_entry3.get(),
                                'wcc_ip1' : self.wcc_ip_entry1.get(),  'wcc_ip2' : self.wcc_ip_entry2.get(),  'wcc_ip3' : self.wcc_ip_entry3.get(),
                                'dlu_ip1' : self.dlu_ip_entry1.get(),  'dlu_ip2' : self.dlu_ip_entry2.get(),  'dlu_ip3' : self.dlu_ip_entry3.get()},
                    'IP_near': {},
                    'IP_ext': {},
                    'raw_file_paths': [""], 'csv_file_paths': [""]}
    return config_data