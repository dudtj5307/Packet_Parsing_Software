import os
import sys
import psutil
import datetime
import threading

from tkinter import Tk as Tk_root
from tkinter import messagebox

import scapy.all as scapy
from scapy.arch import get_windows_if_list
from scapy.utils import PcapWriter

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal

from GUI.gui_main import MainWindow

from utils.ip_config import IP_Config
from utils.parser.log import ParseHistoryLog


# Distribution Info
LAST_UPDATE, VERSION = "2025.03.20", "v0.0"

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


class PacketParser(QObject):
    tcp_num_set = pyqtSignal(str, name="tcp_num_set")
    udp_num_set = pyqtSignal(str, name="udp_num_set")

    def __init__(self):
        super().__init__(None)

        # Sniff Packets
        scapy.conf.verb = 0
        self.is_sniffing = False
        self.sniff_thread = None
        self.pcap_writer = None

        self.pkt_tcp_num = 0
        self.pkt_udp_num = 0

        # selected interface from settings combobox
        self.iface_selected = ["No", "Interface", "Selected"]

        # Load IP_Config Settings
        self.ip_config = IP_Config()
        self.iface_selected = self.ip_config.get('interface')

        # Saving raw packet number
        self.log = ParseHistoryLog()

        # For File Opener
        self.root = Tk_root()
        self.root.withdraw()

        # For Icons setting
        self.internal_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.getcwd()

        self.main_window = MainWindow(self)
        self.main_window.set_icon_path(os.path.join(self.internal_path, 'GUI', 'res'))

        self.tcp_num_set.connect(self.main_window.tcp_num_set)
        self.udp_num_set.connect(self.main_window.udp_num_set)

    def packet_callback(self, packet):
        if not self.is_sniffing:
            return
        # Return if no 'IP' layer or no 'Raw' layer
        if not packet.haslayer(IP) or not packet.haslayer('Raw'):
            return
        if packet.haslayer(TCP):
            self.pkt_tcp_num += 1
            self.tcp_num_set.emit(str(self.pkt_tcp_num))
        elif packet.haslayer(UDP):
            self.pkt_udp_num += 1
            self.udp_num_set.emit(str(self.pkt_udp_num))
        else:
            return
        self.pcap_writer.write(packet)
        # print(packet[IP].src, packet[IP].dst)

    def sniff_packets(self, interface=None):
        # Raw file name
        os.makedirs('RAW', exist_ok=True)
        file_header = self.main_window.edit_file_name.text().lstrip() or "raw"
        date_time = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
        raw_file_path = os.path.join(os.getcwd(), 'RAW', f'{file_header}_{date_time}.pcap')

        # Set text (gui_main) - raw file path
        self.main_window.raw_path_set(raw_file_path)

        # Open pcap_writer
        self.pcap_writer = PcapWriter(raw_file_path, append=True, sync=True, linktype=1)

        # Sniffing packets
        bpf_filter = "ip and (tcp or udp)"
        scapy.sniff(iface=interface, prn=self.packet_callback, store=False, promisc=True,
                    filter=bpf_filter, stop_filter=lambda p: not self.is_sniffing)

        # Close pcap_writer
        self.pcap_writer.close()

        # Delete if zero packets
        total_packet_num = self.pkt_tcp_num + self.pkt_udp_num
        # if total_packet_num == 0 and os.path.exists(raw_file_path):
        #     os.remove(raw_file_path)
        #     return
        # Save to log for parsing
        self.log.update(raw_file_path, total_packet_num)

    def start_sniffing(self):
        # Check validation of iface_selected
        self.iface_selected = self.ip_config.get('interface')

        match_iface = list(filter(lambda x: x['name']==self.iface_selected[1], get_windows_if_list()))
        if not match_iface or self.iface_selected[0] not in match_iface[0]['ips']:
            messagebox.showerror("Network Error", "Select a new Network Interface")
            self.main_window.open_settings()
            return False

        # Start Sniff Thread
        self.is_sniffing = True
        self.sniff_thread = threading.Thread(target=self.sniff_packets, daemon=True, args=(self.iface_selected[1],))
        self.sniff_thread.start()

        # Initialize packet monitoring
        self.pkt_tcp_num, self.pkt_udp_num = 0, 0

        print("Start Sniffing Packets")
        return True

    def stop_sniffing(self):
        # Stop sniff thread
        self.is_sniffing = False
        self.send_dummy_packet()
        self.sniff_thread.join()

        print("Stop Sniffing Packets")

    # Stops sniff thread right away
    def send_dummy_packet(self):
        scapy.sendp(Ether(dst="ff:ff:ff:ff:ff:ff") / IP(dst="255.255.255.255") / UDP(dport=9999),
                    iface=self.iface_selected[1])


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
