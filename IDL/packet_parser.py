import os
import importlib
import struct
from datetime import datetime
from collections import defaultdict

import scapy.all as scapy

# from IDL import parse_EIE_Msg
# from IDL import parse_TIE_Msg
# from IDL import parse_K_Msg
# from IDL import parse_X_Msg

Ether, IP, TCP, UDP, ICMP, ARP = scapy.Ether, scapy.IP, scapy.TCP, scapy.UDP, scapy.ICMP, scapy.ARP

LOCAL_IP_PREFIX = '10.30.7.'
NEAR_IP_PREFIX = '192.168.'

MSG_TYPES = defaultdict(lambda: "Undefined")
MSG_TYPES.update({('ADOC','ADOC'): 'EIE', ('ADOC','WCC'): 'EIE', ('WCC','ADOC'): 'EIE', ('WCC', 'WCC'): 'EIE',
                  ('WCC', 'DLU') : 'TIE', ('DLU', 'WCC'): 'TIE', ('DLU','DLU') : 'TIE',})

class RAW_PACKET_PARSER:

    def __init__(self, parsing_code_paths, backend=None):   # TODO: None - to be erased
        self.SYS_TYPES = defaultdict(lambda: "Undefined")
        self.backend = backend
        self.parsing_code_paths = parsing_code_paths

        # Dynamic Import of generated-parsing modules
        for parsing_code_path in self.parsing_code_paths:
            module_name = parsing_code_path.split('.py')[0]
            globals()[module_name] = importlib.import_module(f"IDL.{module_name}")

    # Update IP infos from (PPS.py) config_data
    def update_system_type(self, config_data):
        local = {key: LOCAL_IP_PREFIX + val for key, val in config_data['IP_local'].items()}
        self.SYS_TYPES.update({local['adoc_ip1']:'ADOC', local['adoc_ip2']:'ADOC', local['adoc_ip3']:'ADOC',
                               local['wcc_ip1']: 'WCC',  local['wcc_ip2']: 'WCC',  local['wcc_ip3']: 'WCC',
                               local['dlu_ip1']: 'DLU',  local['dlu_ip2']: 'DLU',  local['dlu_ip3']: 'DLU'})

        self.SYS_TYPES['10.30.7.255'] = 'WCC'    # TODO: For Testing
        self.SYS_TYPES['10.30.7.255'] = 'WCC'    # TODO: For Testing
        self.SYS_TYPES['10.30.7.66'] = 'WCC'    # TODO: For Testing

    def run(self, raw_file_path):
        self.update_system_type(self.backend.p_pps.config_data)
        # Read raw pcap files
        with scapy.PcapReader(raw_file_path) as packets:
            for packet in packets:
                # Filter Packets without data (ex. ACK, FIN, SYN msgs)
                if not packet.haslayer('Raw'):
                    continue

                date, _time = datetime.fromtimestamp(float(packet.time)).strftime("%Y-%m-%d %H:%M:%S.%f").split(" ")
                src_ip,  dst_ip  = packet[IP].src, packet[IP].dst
                src_sys, dst_sys = self.SYS_TYPES[src_ip], self.SYS_TYPES[dst_ip]
                msg_type = MSG_TYPES[(src_sys, dst_sys)]
                if msg_type == 'Undefined': continue

                rtps_packet = packet['Raw'].load

                data = self.parse_data(msg_type, rtps_packet)
                if data is None: continue

                packet_info = {'date': date, 'time': _time,'src_ip': src_ip, 'dst_ip':dst_ip,
                               'src_sys':src_sys, 'dst_sys':dst_sys, 'msg_type':msg_type, 'data':data}
                # print(packet_info)
        # return packet_info

    def parse_rtps_packet(self, data):
        magic_number, version, vendor_id, guid_prefix =  struct.upack('>4s 2B 2B 12s', data)
        if magic_number != "RTPS":
            return False

        pass

    # Parse if EIE or TIE or K or X or J
    def parse_data(self, msg_type, data):
        type_function_name = f'parse_{msg_type}'
        if type_function_name in globals():
            return globals()[type_function_name](data)
        else:
            print(f"Can not find msg type '{msg_type}'")
            return None

    def parse_EIE(self, data):
        # Find TIE type from TIE header
        eie_type = struct.unpack('>H', data[0:2])[0]
        eie_type = 0x301
        EIE_function_name = f'parse_EIE_{hex(eie_type)}'
        if EIE_function_name in parse_EIE_Msg.__dict__:
            return parse_EIE_Msg.__dict__[EIE_function_name](data)
        else:
            print(f"Can not find type 'EIE_{hex(eie_type)}'")
            return None

    def parse_TIE(self, data):
        # Find TIE type from TIE header
        tie_type = struct.unpack('>H', data[0:2])[0]
        print(tie_type)
        tie_type = 0x301
        TIE_function_name = f'parse_TIE_{hex(tie_type)}'
        if TIE_function_name in parse_TIE_Msg.__dict__:
            return parse_TIE_Msg.__dict__[TIE_function_name](data)
        else:
            print(f"Can not find type 'TIE_{hex(tie_type)}'")
            return None




if __name__ == "__main__":
    pass
    # raw_file = r"C:\Users\74841\ProjectPPS\RAW\packet_250305_173850.pcap"
    #
    # raw_to_csv('a,', raw_file)

    parsing_code_paths = ['parse_EIE_Msg.py', 'parse_TIE_Msg.py']

    packet_parser = RAW_PACKET_PARSER(parsing_code_paths)
