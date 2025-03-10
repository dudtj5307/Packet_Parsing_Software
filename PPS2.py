import os
import sys
import time
from unittest.mock import DEFAULT

import psutil
import datetime
import json
import threading

import tkinter as tk
from tkinter import messagebox

import scapy.all as scapy
from scapy.arch import get_windows_if_list
from scapy.utils import PcapWriter


from GUI.gui_main2 import *
from GUI.gui_settings2 import *

from GUI.gui_settings import DEFAULT_CONFIG_DATA
from IDL.auto_generate import IDL_FUNC_GENERATOR


LAST_UPDATE, VERSION = "2025.03.03", "v0.0"

Ether, IP, TCP, UDP, ICMP, ARP = scapy.Ether, scapy.IP, scapy.TCP, scapy.UDP, scapy.ICMP, scapy.ARP


class PacketParser:
    def __init__(self):

        # Sniff Packets
        scapy.conf.verb = 0
        self.sniff_thread = None
        self.is_sniffing = False

        # File paths
        self.raw_file_paths = [""]
        self.csv_file_paths = [""]

        # default configuration data
        self.config_data = DEFAULT_CONFIG_DATA

        # selected interface from settings combobox
        self.iface_selected = ["No", "Interface", "Selected"]

        self.load_config_data()

        # For File Opener
        self.root = tk.Tk()
        self.root.withdraw()

        self.main_window = MainWindow(self)

        # Invalid configuration
        if self.config_data.keys() != DEFAULT_CONFIG_DATA.keys():
            messagebox.showerror("Error", f" Invalid File : \'setting.config\' \n Configuration Initialized ! ")
            if os.path.exists("../Project_PPS/GUI/settings.conf"):
                os.remove("../Project_PPS/GUI/settings.conf")
            self.config_data = DEFAULT_CONFIG_DATA
            self.save_config_data()
            self.main_window.open_settings()

    def load_config_data(self):
        try:
            with open("../Project_PPS/GUI/settings.conf", "r") as file:
                self.config_data = json.load(file)

            self.iface_selected = self.config_data['interface']
            self.iface_selected_var.set("".join(self.iface_selected))
        # except FileNotFoundError:
        except :
            # make file, if no config file
            self.config_data = DEFAULT_CONFIG_DATA
            self.save_config_data()

    def save_config_data(self, changes={}):
        self.config_data.update(changes)
        with open("../Project_PPS/GUI/settings.conf", "w") as file:
            json.dump(self.config_data, file, indent=4)
        print("Saved Configuration as 'setting.conf'")

    def packet_callback(self, packet):
        if not packet.haslayer(IP):
            return

        if packet.haslayer(TCP): self.pkt_tcp_var.set(self.pkt_tcp_var.get() + 1)
        else:                    self.pkt_udp_var.set(self.pkt_udp_var.get() + 1)

        self.pcap_writer.write(packet)

    def sniff_packets(self, interface=None, date_time=""):

        self.raw_file_var.set(" "+os.path.split(self.raw_file_paths[0])[1])

        self.pcap_writer = PcapWriter(self.raw_file_paths[0], append=True, sync=True)

        # Sniffing and processing packets
        bpf_filter = "ip and (tcp or udp)"
        scapy.sniff(iface=interface, prn=self.packet_callback, store=False, promisc=True,
                    filter=bpf_filter, stop_filter=lambda p: not self.is_sniffing)

    def start_sniffing(self):
        if self.is_sniffing:
            return
        if self.iface_selected[1] not in [iface['name'] for iface in get_windows_if_list()]:
            messagebox.showerror("Network Error", "Select a new Network Interface")
            self.main_window.open_settings()
            return

        # For pcap file name
        os.makedirs('../Project_PPS/GUI/RAW', exist_ok=True)
        date_time = datetime.datetime.now().strftime('%y%m%d_%H%M%S')

        file_name = self.file_name_entry.get()
        file_header = "packet" if file_name=="Raw File Name" or file_name=="" else file_name
        self.raw_file_paths = [os.path.join(os.getcwd(), 'RAW', f'{file_header}_{date_time}.pcap')]

        self.csv_file_var.set("")

        # Start Sniff Thread
        self.is_sniffing = True
        self.sniff_thread = threading.Thread(target=self.sniff_packets, daemon=True, args=(self.iface_selected[1], date_time,))
        self.sniff_thread.start()

        gui_main.start_button_pressed(self)
        print("Start Sniffing Packets")

        # Recursive Restart
        h, m = self.hour_entry.get(), self.min_entry.get()
        if h == "hour": h = "0"
        if m == "min":  m = "0"
        if h.isdigit() and m.isdigit() and (int(h)>=1 or int(m)>=1):
            delay = 3600 * int(h) + 60 * int(m)
            timer = threading.Timer(delay, self.restart_sniffing)
            timer.start()

    def stop_sniffing(self):
        # Stop Sniff Thread
        self.is_sniffing = False
        self.timer_thread.join()
        gui_main.stop_button_pressed(self)
        print("Stop Sniffing Packets")

    def restart_sniffing(self):
        if self.is_sniffing:
            self.stop_sniffing()
            print("Restarting!!")
            self.start_sniffing()


if __name__ == "__main__":
    # Check if scapy is available
    if not scapy.conf.use_pcap:
        messagebox.showerror("Error", "\"Npcap\" is not installed."
                                      "\nPlease install \"Npcap\" with 'Winpcap API-compatible mode'")
        exit(1)

    # Process Priority Elevation
    main_pid = psutil.Process(os.getpid())
    main_pid.nice(psutil.HIGH_PRIORITY_CLASS)

    app = QApplication(sys.argv)

    pss = PacketParser()
    pss.main_window.show()
    app.exec()
