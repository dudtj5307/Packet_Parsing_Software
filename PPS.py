import os
import json

import tkinter as tk
import scapy.all as scapy

from GUI import gui_main, gui_settings
from IDL.auto_generate import IDL_CODE_GENERATION


LAST_UPDATE, VERSION = "2025.03.02", "v0.0"


class PacketParser:
    def __init__(self, root):
        self.root = root

        self.sniff_thread1 = None
        self.is_sniffing = False

        # Selected Interface from Combobox
        self.iface_selected = ""

        # Packet Monitoring
        self.pkt_tcp_var, self.pkt_tcp_num = tk.StringVar(), 0
        self.pkt_udp_var, self.pkt_udp_num = tk.StringVar(), 0

        self.pkt_tcp_var.set(str(self.pkt_tcp_num))
        self.pkt_udp_var.set(str(self.pkt_udp_num))

        # Flag for printing packets
        self.print_flag = tk.BooleanVar()
        self.print_flag.set(False)
        scapy.conf.verb = 0

        # Default Configuration of GUI data
        self.config_data = {'adoc_ip1':  2, 'adoc_ip2':  3, 'adoc_ip3': 99,
                            'wcc_ip1' :  8, 'wcc_ip2' : 10, 'wcc_ip3' : 13,
                            'dlu_ip1' : 27, 'dlu_ip2' : 28, 'dlu_ip3' : 30,
                            'pcap_path': "", 'csv_path' : "",}

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
        print("Load Complete!")

    def save_config_data(self, changes={}):
        self.config_data.update(changes)
        os.makedirs("GUI", exist_ok=True)
        with open("GUI/settings.conf", "w") as file:
            json.dump(self.config_data, file, indent=4)
        print("Save Complete!")


if __name__ == "__main__":
    root = tk.Tk()
    pss = PacketParser(root)

    root.title(f"Packet Parsing Software {VERSION}")




    root.mainloop()