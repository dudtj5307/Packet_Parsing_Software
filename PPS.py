import os
import sys
import time
import datetime
import json
import threading

import tkinter as tk
import scapy.all as scapy

from GUI import gui_main, gui_settings
from IDL.auto_generate import IDL_CODE_GENERATION


LAST_UPDATE, VERSION = "2025.03.02", "v0.0"


Ether, IP, TCP, UDP, ICMP, ARP = scapy.Ether, scapy.IP, scapy.TCP, scapy.UDP, scapy.ICMP, scapy.ARP

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
        self.current_path = os.getcwd()
        self.pcap_file_path = ""
        self.csv_file_path = ""

        # default configuration data
        self.config_data = {'INTERNAL_IPS_24': '192.168.0',
                            'adoc_ip1':  2, 'adoc_ip2':  3, 'adoc_ip3': 99,
                            'wcc_ip1' :  8, 'wcc_ip2' : 10, 'wcc_ip3' : 13,
                            'dlu_ip1' : 27, 'dlu_ip2' : 28, 'dlu_ip3' : 30,

                            'pcap_path': "", 'csv_path' : "",
                            'iface_selected': "",}

        # selected interface from settings combobox
        self.iface_selected = ""

        self.load_config_data()

        # Auto-generator for IDL parsing-functions
        self.generator = IDL_CODE_GENERATION()

        gui_main.create_widgets(self)

    def load_config_data(self):
        try:
            with open("GUI/settings.conf", "r") as file:
                self.config_data = json.load(file)
        except FileNotFoundError:
            # make file, if no config file
            self.save_config_data()

        self.iface_selected = self.config_data['iface_selected']
        print("Load Complete!")

    def save_config_data(self, changes={}):
        self.config_data.update(changes)
        os.makedirs("GUI", exist_ok=True)
        with open("GUI/settings.conf", "w") as file:
            json.dump(self.config_data, file, indent=4)
        print("Save Complete!")

    def packet_callback(self, packet):
        if not packet.haslayer(IP):
            return
        # Check IP Number
        src_ip, dst_ip = packet[IP].src, packet[IP].dst

        # Internal IPs (192.168.0.X)
        # if src_ip.startswith('192.168.0') and dst_ip.startswith('192.168.0'):
        #     src_ip_4th = int(src_ip.split('.')[3])
        #     dst_ip_4th = int(dst_ip.split('.')[3])
        #     if src_ip_4th not in self.config_data.values() or dst_ip_4th not in self.config_data.values():
        #         return
        # else:
        #     return

        if packet.haslayer(TCP): self.pkt_tcp_num += 1
        else:                    self.pkt_udp_num += 1

        scapy.wrpcap(self.pcap_file_path, packet, append=True)


    def sniff_packets(self, interface=None, date_time=""):
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
        self.pcap_file_path = f"RAW/packet_{date_time}.pcap"

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
    # path change
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))

    print(os.getcwd())
    root = tk.Tk()
    pss = PacketParser(root)

    root.title(f"Packet Parsing Software {VERSION}")




    root.mainloop()