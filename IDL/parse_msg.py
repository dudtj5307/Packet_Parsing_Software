from collections import defaultdict
import scapy.all as scapy

Ether, IP, TCP, UDP, ICMP, ARP = scapy.Ether, scapy.IP, scapy.TCP, scapy.UDP, scapy.ICMP, scapy.ARP

from IDL import *

ips = {'adoc_ip1': "", 'adoc_ip2': "", 'adoc_ip3': "",
       'wcc_ip1' : "", 'wcc_ip2' : "", 'wcc_ip3' : "",
       'dlu_ip1' : "", 'dlu_ip2' : "", 'dlu_ip3' : ""}
SYS_TYPE = defaultdict(list)
MSG_TYPE = defaultdict(lambda: "Undefined")
MSG_TYPE.update({('ADOC', 'ADOC'): 'EIE', ('ADOC', 'WCC'): 'EIE', ('WCC', 'ADOC'): 'EIE', ('WCC', 'WCC'): 'EIE',
                ('WCC', 'DLU'): 'TIE',   ('DLU', 'WCC'): 'TIE',  ('DLU', 'DLU'): 'TIE',})

def raw_to_csv(self, raw_file_path):
    # IP infos from config_data
    global ips, SYS_TYPE
    ips = self.config_data['IP']
    SYS_TYPE.update({'ADOC': [ips['adoc_ip1'], ips['adoc_ip2'], ips['adoc_ip3']],
                     'WCC': [ips['wcc_ip1'],  ips['wcc_ip2'],  ips['wcc_ip3']],
                     'DLU': [ips['dlu_ip1'],  ips['dlu_ip2'],  ips['dlu_ip3']]})
    update_system_type(self.config_data['IP'])

    # Read raw files
    with scapy.PcapReader(raw_file_path) as packets:
        for packet in packets:
            # Filter Packets without data (ex. ACK, FIN, SYN msgs)
            if not packet.haslayer('Raw'):
                continue
            src_ip, dst_ip = packet[IP].src, packet[IP].dst
            sys_types = find_system_type(src_ip, dst_ip)


            print(sys_types)

            # Filter Packets by ip (ex. ACK msgs)
            if src_ip not in ips.values() or dst_ip not in ips.values():
                continue


def update_system_type(ips):

    pass


# Find Name by src & dst
def find_system_type(src, dst):
    data_types = {}
    # Find Device Name (ADOC, WCC, DLU)
    print(SYS_TYPE)
    for sys, ip_list in SYS_TYPE.items():
        if src in ip_list: data_types['src_ip'] = sys
        if dst in ip_list: data_types['dst_ip'] = sys
    return data_types

def find_
    # Find Message Type (EIE, TIE, K, X)
    print(MSG_TYPE)
    print((data_types['src_ip'], data_types['dst_ip'])
    data_types['msg_type'] = MSG_TYPE[(data_types['src_ip'], data_types['dst_ip'])]
    return data_types





if __name__ == "__main__":
    pass
    # raw_file = r"C:\Users\74841\ProjectPPS\RAW\packet_250305_173850.pcap"
    #
    # raw_to_csv('a,', raw_file)
