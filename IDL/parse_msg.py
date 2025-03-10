import struct
from datetime import datetime
from collections import defaultdict

import scapy.all as scapy

from IDL.auto_generate import IDL_FUNC_GENERATOR
from IDL import parse_EIE_Msg
from IDL import parse_TIE_Msg
# from IDL import parse_K_Msg
# from IDL import parse_X_Msg


Ether, IP, TCP, UDP, ICMP, ARP = scapy.Ether, scapy.IP, scapy.TCP, scapy.UDP, scapy.ICMP, scapy.ARP

LOCAL_IP_PREFIX = "192.168.45."
NEAR_IP_PREFIX = "192.168."

SYS_TYPES = defaultdict(lambda: "Undefined")
MSG_TYPES = defaultdict(lambda: "Undefined")
MSG_TYPES.update({('ADOC','ADOC'): 'EIE', ('ADOC','WCC'): 'EIE', ('WCC','ADOC'): 'EIE', ('WCC', 'WCC'): 'EIE',
                  ('WCC', 'DLU') : 'TIE', ('DLU', 'WCC'): 'TIE', ('DLU','DLU') : 'TIE',})

code_generator = IDL_FUNC_GENERATOR()

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
    import time
    start = time.time()
    # IP update from config_data
    update_system_type(self.config_data)
    # Read raw pcap files
    with scapy.PcapReader(raw_file_path) as packets:
        for packet in packets:
            # Filter Packets without data (ex. ACK, FIN, SYN msgs)
            if not packet.haslayer('Raw'):
                continue
            date, _time = datetime.fromtimestamp(float(packet.time)).strftime("%Y-%m-%d %H:%M:%S.%f").split(" ")
            src_ip,  dst_ip  = packet[IP].src,    packet[IP].dst
            src_sys, dst_sys = SYS_TYPES[src_ip], SYS_TYPES[dst_ip]
            msg_type = MSG_TYPES[(src_sys, dst_sys)]
            raw_data = packet['Raw'].load
            data = parse_data(msg_type, raw_data)
            packet_info = {'date': date, 'time': _time,'src_ip': src_ip, 'dst_ip':dst_ip,
                           'src_sys':src_sys, 'dst_sys':dst_sys, 'msg_type':msg_type, 'data':data}
            # print(packet_info)
    print(time.time() - start)
# Parse if EIE or TIE or K or X or J
def parse_data(msg_type, data):
    type_function_name = f'parse_{msg_type}'
    if type_function_name in globals():
        return globals()[type_function_name](data)
    else:
        # print(f"Can not find msg type '{msg_type}'")
        return None

def parse_EIE(data):
    # Find TIE type from TIE header
    eie_type = struct.unpack('>H', data[0:2])[0]
    eie_type = 0x301
    EIE_function_name = f'parse_EIE_{hex(eie_type)}'
    if EIE_function_name in parse_EIE_Msg.__dict__:
        return parse_EIE_Msg.__dict__[EIE_function_name](data)
    else:
        # print(f"Can not find type 'EIE_{hex(eie_type)}'")
        return None

def parse_TIE(data):
    # Find TIE type from TIE header
    tie_type = struct.unpack('>H', data[0:2])[0]
    print(tie_type)
    tie_type = 0x301
    TIE_function_name = f'parse_TIE_{hex(tie_type)}'
    if TIE_function_name in parse_TIE_Msg.__dict__:
        return parse_TIE_Msg.__dict__[TIE_function_name](data)
    else:
        # print(f"Can not find type 'TIE_{hex(tie_type)}'")
        return None




if __name__ == "__main__":
    pass
    # raw_file = r"C:\Users\74841\ProjectPPS\RAW\packet_250305_173850.pcap"
    #
    # raw_to_csv('a,', raw_file)
