import os
import sys
import time
import copy
import json
import psutil
import datetime
import threading

from tkinter import Tk as Tk_root
from tkinter import messagebox

import scapy.all as scapy
from scapy.arch import get_windows_if_list
from scapy.utils import PcapWriter

from PyQt6.QtWidgets import QApplication

from GUI.gui_main import MainWindow

from GUI.gui_settings import DEFAULT_CONFIG_DATA

# Distribution Info
LAST_UPDATE, VERSION = "2025.03.08", "v0.0"

Ether, IP, TCP, UDP, ICMP, ARP = scapy.Ether, scapy.IP, scapy.TCP, scapy.UDP, scapy.ICMP, scapy.ARP

def same_dict_keys_recursive(dict1, dict2):
    if set(dict1.keys()) != set(dict2.keys()):
        return False
    for key, dict1_val in dict1.items():
        dict2_val = dict2[key]
        if type(dict1_val) != type(dict2_val):
            return False
        if isinstance(dict1_val, dict) and isinstance(dict2_val, dict):
            if not same_dict_keys_recursive(dict1_val, dict2_val):
                return False
    return True


class PacketParser:
    def __init__(self):

        # Sniff Packets
        scapy.conf.verb = 0
        self.is_sniffing = False
        self.sniff_thread = None
        self.pcap_writer = None

        # # File paths
        self.raw_file_paths = [""]
        self.csv_file_paths = [""]      # TODO: move to gui_main..?

        self.pkt_tcp_num = 0
        self.pkt_udp_num = 0

        # selected interface from settings combobox
        self.iface_selected = ["No", "Interface", "Selected"]

        # default configuration data
        self.config_data = {}
        self.load_config_data()

        # For File Opener
        self.root = Tk_root()
        self.root.withdraw()

        # For Icons setting
        self.internal_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.getcwd()

        self.main_window = MainWindow(self)
        self.main_window.set_icon_path(os.path.join(self.internal_path, 'GUI', 'res'))

    def load_config_data(self):
        try:
            with open("settings.conf", "r") as file:
                self.config_data = json.load(file)
                if not same_dict_keys_recursive(self.config_data, DEFAULT_CONFIG_DATA):
                    raise KeyError("Invalid Dictionary Keys")
        except Exception as e:
            print(f"# Error in loading configuration : {e}")
            # Reset and Save Default Configuration
            if os.path.exists("settings.conf"):
                os.remove("settings.conf")
            self.config_data = copy.deepcopy(DEFAULT_CONFIG_DATA)
            self.save_config_data()
            messagebox.showerror("Error", f" Invalid File : \'setting.config\' \n Configuration Initialized !! ")

        self.iface_selected = self.config_data['interface']

    def save_config_data(self, changes=None):
        if changes:
            self.config_data.update(changes)
        with open("settings.conf", "w") as file:
            json.dump(self.config_data, file, indent=4)
        print("Saved Configuration as 'setting.conf'")

    def packet_callback(self, packet):
        if not self.is_sniffing:
            return
        if not packet.haslayer(IP):
            return
        if packet.haslayer(TCP):
            self.pkt_tcp_num += 1
            self.main_window.edit_tcp_num.setText(str(self.pkt_tcp_num))
        elif packet.haslayer(UDP):
            self.pkt_udp_num += 1
            self.main_window.edit_udp_num.setText(str(self.pkt_udp_num))
        else:
            return

        self.pcap_writer.write(packet)

    def sniff_packets(self, interface=None, date_time=""):
        # Set text - raw file path
        self.main_window.edit_raw_path.setText(os.path.split(self.raw_file_paths[0])[1])
        # Open pcap_writer
        self.pcap_writer = PcapWriter(self.raw_file_paths[0], append=True, sync=True)
        # Sniffing packets
        bpf_filter = "ip and (tcp or udp)"
        scapy.sniff(iface=interface, prn=self.packet_callback, store=False, promisc=True,
                    filter=bpf_filter, stop_filter=lambda p: not self.is_sniffing)
        # Close pcap_writer
        self.pcap_writer.close()

    def start_sniffing(self):
        if self.iface_selected[1] not in [iface['name'] for iface in get_windows_if_list()]:
            messagebox.showerror("Network Error", "Select a new Network Interface")
            self.main_window.open_settings()
            return False

        # Check raw file name
        os.makedirs('RAW', exist_ok=True)
        file_name_set = self.main_window.edit_file_name.text().strip()
        file_header = file_name_set if file_name_set else "packet"

        # Raw pcap file path
        date_time = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
        self.raw_file_paths = [os.path.join(os.getcwd(), 'RAW', f'{file_header}_{date_time}.pcap')]

        # Start Sniff Thread TODO : settings implement
        self.is_sniffing = True
        self.sniff_thread = threading.Thread(target=self.sniff_packets, daemon=True, args=(self.iface_selected[1], date_time,))
        # self.sniff_thread = threading.Thread(target=self.sniff_packets, daemon=True, args=(None, date_time,))
        self.sniff_thread.start()

        print("Start Sniffing Packets")
        return True

    def stop_sniffing(self):
        # Stop sniff thread
        self.is_sniffing = False
        # Send dummy packet to stop sniffing right away
        scapy.sendp(Ether(dst="ff:ff:ff:ff:ff:ff") / IP(dst="255.255.255.255") / UDP(dport=9999),
                    iface=self.iface_selected[1])
        self.sniff_thread.join()

        print("Stop Sniffing Packets")


if __name__ == "__main__":
    # Check if scapy is available
    if not scapy.conf.use_pcap:
        messagebox.showerror("Error", "\"Npcap\" is not installed."
                             "\nPlease install \"Npcap\" with 'Winpcap API-compatible mode'"); exit(1)

    # Process Priority Elevation
    main_pid = psutil.Process(os.getpid())
    main_pid.nice(psutil.HIGH_PRIORITY_CLASS)

    app = QApplication(sys.argv)

    pss = PacketParser()
    pss.main_window.show()
    app.exec()
