import os
import sys
import time
import psutil
import datetime
import json
import threading

import tkinter as tk
from tkinter import messagebox

import scapy.all as scapy
from scapy.arch import get_windows_if_list
from scapy.utils import PcapWriter

from GUI import gui_main, gui_settings
from IDL.auto_generate import IDL_CODE_GENERATION


LAST_UPDATE, VERSION = "2025.03.03", "v0.0"

Ether, IP, TCP, UDP, ICMP, ARP = scapy.Ether, scapy.IP, scapy.TCP, scapy.UDP, scapy.ICMP, scapy.ARP


class PacketParser:
    def __init__(self, root):
        self.root = root

        # Sniff Packets
        scapy.conf.verb = 0
        self.sniff_thread = None
        self.is_sniffing = False

        # Packet Monitoring
        self.timer_var = tk.StringVar()
        self.pkt_tcp_var = tk.IntVar(value=0)
        self.pkt_udp_var = tk.IntVar(value=0)

        # Flag for printing packets
        self.print_flag = tk.BooleanVar()
        self.print_flag.set(False)

        # File paths
        self.raw_file_var = tk.StringVar()
        self.csv_file_var = tk.StringVar()
        self.raw_file_paths = [""]
        self.csv_file_paths = [""]

        # default configuration data
        self.config_data = gui_settings.DEFAULT_CONFIG_DATA

        # selected interface from settings combobox
        self.iface_selected = ["No", "Interface", "Selected"]
        self.iface_selected_var = tk.StringVar()
        self.iface_selected_idx = -1

        self.load_config_data()

        # Auto-generator for IDL parsing-functions
        self.generator = IDL_CODE_GENERATION()

        gui_main.create_widgets(self)

    def load_config_data(self):
        try:
            with open("settings.conf", "r") as file:
                self.config_data = json.load(file)
        except FileNotFoundError:
            # make file, if no config file
            self.save_config_data()

        self.iface_selected = self.config_data['iface_selected']
        self.iface_selected_var.set("".join(self.iface_selected))

    def save_config_data(self, changes={}):
        self.config_data.update(changes)
        with open("settings.conf", "w") as file:
            json.dump(self.config_data, file, indent=4)
        print("Saved Configuration as 'setting.conf'")

    def packet_callback(self, packet):
        if not packet.haslayer(IP):
            return
        # Check IP Number
        src_ip, dst_ip = packet[IP].src, packet[IP].dst

        # Internal IPs (192.168.0.X)
        # if src_ip.startswith('192.168.0') and dst_ip.startswith('192.168.0'):
        #     src_ip_4th = int(src_ip.split('.')[3])
        #     dst_ip_4th = int(dst_ip.split('.')[3])
        #     if src_ip_4th not in self.config_data['IP'].values() or dst_ip_4th not in self.config_data['IP'].values():
        #         return
        # else:
        #     return

        if packet.haslayer(TCP): self.pkt_tcp_var.set(self.pkt_tcp_var.get() + 1)
        else:                    self.pkt_udp_var.set(self.pkt_udp_var.get() + 1)

        # scapy.wrpcap(self.raw_file_paths[0], packet, append=True)
        # if self.written:
        #     return
        self.pcap_writer.write(packet)
        # self.written = True

    def sniff_packets(self, interface=None, date_time=""):
        # Create PCAP file
        # if not os.path.exists(self.raw_file_paths[0]):
        #     with open(self.raw_file_paths[0], "wb") as f:
        #         f.write(b'\xd4\xc3\xb2\xa1')    # PCAP File Header
        self.raw_file_var.set(" "+os.path.split(self.raw_file_paths[0])[1])

        self.pcap_writer = PcapWriter(self.raw_file_paths[0], append=True, sync=True)
        # self.written = False

        # Sniffing and processing packets
        bpf_filter = "ip and (tcp or udp)"
        scapy.sniff(iface=interface, prn=self.packet_callback, store=False, promisc=True,
                    filter=bpf_filter, stop_filter=lambda p: not self.is_sniffing)

    def start_sniffing(self):
        if self.is_sniffing:
            return
        if self.iface_selected[1] not in [iface['name'] for iface in get_windows_if_list()]:
            messagebox.showerror("Network Error", "Select a new Network Interface")
            gui_settings.open_settings(self)
            return

        # For pcap file name
        os.makedirs('RAW', exist_ok=True)
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

    root = tk.Tk()
    pss = PacketParser(root)
    # GUI Title
    root.title(f"Packet Parsing Software {VERSION}")
    # Run GUI Application
    root.mainloop()