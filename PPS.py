import os
import sys
import time
import datetime
import json
import threading

import tkinter as tk
from tkinter import messagebox
import scapy.all as scapy

from GUI import gui_main, gui_settings
from IDL.auto_generate import IDL_CODE_GENERATION


LAST_UPDATE, VERSION = "2025.03.03", "v0.0"


Ether, IP, TCP, UDP, ICMP, ARP = scapy.Ether, scapy.IP, scapy.TCP, scapy.UDP, scapy.ICMP, scapy.ARP

DEFAULT_CONFIG_DATA = {'iface_selected': "",
                       'IP': {'adoc_ip1':  2, 'adoc_ip2':  3, 'adoc_ip3': "",
                              'wcc_ip1' :  8, 'wcc_ip2' : 10, 'wcc_ip3' : 13,
                              'dlu_ip1' : 27, 'dlu_ip2' : 28, 'dlu_ip3' : 30},
                       'raw_file_path': "", 'csv_file_path' : "",}

class PacketParser:
    def __init__(self, root):
        self.root = root

        # Sniff Packets
        scapy.conf.verb = 0
        self.sniff_thread = None
        self.is_sniffing = False

        # Packet Monitoring
        self.pkt_tcp_var, self.pkt_tcp_num = tk.StringVar(), 0
        self.pkt_udp_var, self.pkt_udp_num = tk.StringVar(), 0

        self.pkt_tcp_var.set(str(self.pkt_tcp_num))
        self.pkt_udp_var.set(str(self.pkt_udp_num))

        # Flag for printing packets
        self.print_flag = tk.BooleanVar()
        self.print_flag.set(False)

        # File paths
        self.raw_file_var = tk.StringVar()
        self.csv_file_var = tk.StringVar()
        self.raw_file_path = ""
        self.csv_file_path = ""

        # default configuration data
        self.config_data = DEFAULT_CONFIG_DATA

        # selected interface from settings combobox
        self.iface_selected = ""

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

    def save_config_data(self, changes={}):
        self.config_data.update(changes)
        with open("settings.conf", "w") as file:
            json.dump(self.config_data, file, indent=4)

    def packet_callback(self, packet):
        if not packet.haslayer(IP):
            return
        # Check IP Number
        src_ip, dst_ip = packet[IP].src, packet[IP].dst

        # Internal IPs (192.168.0.X)
        if src_ip.startswith('192.168.0') and dst_ip.startswith('192.168.0'):
            src_ip_4th = int(src_ip.split('.')[3])
            dst_ip_4th = int(dst_ip.split('.')[3])
            if src_ip_4th not in self.config_data['IP'].values() or dst_ip_4th not in self.config_data['IP'].values():
                return
        else:
            return

        if packet.haslayer(TCP): self.pkt_tcp_num += 1
        else:                    self.pkt_udp_num += 1

        scapy.wrpcap(self.raw_file_path, packet, append=True)


    def sniff_packets(self, interface=None, date_time=""):
        # Create PCAP file
        if not os.path.exists(self.raw_file_path):
            with open(self.raw_file_path, "wb") as f:
                f.write(b'\xd4\xc3\xb2\xa1')    # PCAP File Header
        self.raw_file_var.set(os.path.split(self.raw_file_path)[1])

        # Sniffing and processing packets
        bpf_filter = "ip and (tcp or udp)"
        scapy.sniff(iface=interface, prn=self.packet_callback, store=False, promisc=True,
                    filter=bpf_filter, stop_filter=lambda p: not self.is_sniffing)


    def start_sniffing(self):
        if self.is_sniffing:
            return
        # For pcap file name
        os.makedirs('RAW', exist_ok=True)
        date_time = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
        self.raw_file_path = os.path.join(os.getcwd(), 'RAW', f'packet_{date_time}.pcap')


        # Start Sniff Thread
        self.is_sniffing = True
        self.sniff_thread = threading.Thread(target=self.sniff_packets, daemon=True, args=(self.iface_selected[1], date_time,))
        self.sniff_thread.start()

        gui_main.start_button_pressed(self)
        print("Start Sniffing Packets")

    def stop_sniffing(self):
        # Stop Sniff Thread
        self.is_sniffing = False

        gui_main.stop_button_pressed(self)
        print("Stop Sniffing Packets")



if __name__ == "__main__":
    # Check if scapy is available
    if not scapy.conf.use_pcap:
        messagebox.showerror("Error", "\"Npcap\" is not installed."
                                      "\nPlease install \"Npcap\" with 'Winpcap API-compatible mode'")
        exit(1)

    root = tk.Tk()
    pss = PacketParser(root)
    # GUI Title
    root.title(f"Packet Parsing Software {VERSION}")
    # Run GUI Application
    root.mainloop()