from collections import defaultdict
import scapy.all as scapy

from IDL import parse_data
from IDL.auto_generate import IDL_CODE_GENERATION

Ether, IP, TCP, UDP, ICMP, ARP = scapy.Ether, scapy.IP, scapy.TCP, scapy.UDP, scapy.ICMP, scapy.ARP

from IDL import *

LOCAL_IP_PREFIX = "192.168.45."
NEAR_IP_PREFIX = "192.168."

SYS_TYPES = defaultdict(lambda: "Undefined")
MSG_TYPES = defaultdict(lambda: "Undefined")
MSG_TYPES.update({('ADOC','ADOC'): 'EIE', ('ADOC','WCC'): 'EIE', ('WCC','ADOC'): 'EIE', ('WCC', 'WCC'): 'EIE',
                  ('WCC', 'DLU') : 'TIE', ('DLU', 'WCC'): 'TIE', ('DLU','DLU') : 'TIE',})

code_generator = IDL_CODE_GENERATION()

def update_system_type(config_data):
    global SYS_TYPES
    local = {key: LOCAL_IP_PREFIX + val for key, val in config_data['IP_local'].items()}
    SYS_TYPES.update({local['adoc_ip1']:'ADOC', local['adoc_ip2']:'ADOC', local['adoc_ip3']:'ADOC',
                      local['wcc_ip1']: 'WCC',  local['wcc_ip2']: 'WCC',  local['wcc_ip3']: 'WCC',
                      local['dlu_ip1']: 'DLU',  local['dlu_ip2']: 'DLU',  local['dlu_ip3']: 'DLU'})
    SYS_TYPES['192.168.45.179'] = 'WCC'

def raw_to_csv(self, raw_file_path):
    # Parsing function auto-generation
    self.idl_file_paths = ['IDL/EIE_Msg.idl']
    for idl_file_path in self.idl_file_paths:
        code_generator.set(idl_file_path)
        code_generator.run()

    # IP update from config_data
    update_system_type(self.config_data)

    # Read raw files
    with scapy.PcapReader(raw_file_path) as packets:
        for packet in packets:
            # Filter Packets without data (ex. ACK, FIN, SYN msgs)
            if not packet.haslayer('Raw'):
                continue
            src_ip, dst_ip = packet[IP].src, packet[IP].dst
            src_sys, dst_sys = SYS_TYPES[src_ip], SYS_TYPES[dst_ip]
            msg_type = MSG_TYPES[(src_sys, dst_sys)]
            raw_data = packet['Raw'].load
            data = parse_data.parse_type(msg_type, raw_data)
            print(data)

            packet_info = {'src_ip': src_ip, 'dst_ip':dst_ip,'src_sys':src_sys, 'dst_sys':dst_sys, 'msg_type':msg_type, 'data':data}

            # print(packet_info)


if __name__ == "__main__":
    pass
    # raw_file = r"C:\Users\74841\ProjectPPS\RAW\packet_250305_173850.pcap"
    #
    # raw_to_csv('a,', raw_file)
