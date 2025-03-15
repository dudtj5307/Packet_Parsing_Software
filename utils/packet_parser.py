import os
import importlib
import struct
from datetime import datetime
from collections import defaultdict

import scapy.all as scapy

from utils.config import Config
from utils.monitor import ProgressMonitor
from utils.log import ParseHistoryLog


Ether, IP, TCP, UDP, ICMP, ARP = scapy.Ether, scapy.IP, scapy.TCP, scapy.UDP, scapy.ICMP, scapy.ARP

LOCAL_IP_PREFIX = '10.30.7.'
NEAR_IP_PREFIX = '192.168.'

MSG_TYPES = defaultdict(lambda: "Undefined")
MSG_TYPES.update({('ADOC','ADOC'): 'EIE', ('ADOC','WCC'): 'EIE', ('WCC','ADOC'): 'EIE', ('WCC', 'WCC'): 'EIE',
                  ('WCC', 'DLU') : 'TIE', ('DLU', 'WCC'): 'TIE', ('DLU','DLU') : 'TIE',
                  ('MDIL', 'MDIL') : 'K_Msg', })

RTPS_header_fmt = ">4s H H 12s"  # Big-endian (>)
RTPS_header_size = struct.calcsize(RTPS_header_fmt)

RTPS_subheader_fmt = ["<B B H", ">B B H"]     # [0] Little-endian (<) / [1] : Big-endian (>)
RTPS_subheader_size = struct.calcsize(RTPS_subheader_fmt[0])

class PacketParser:
    def __init__(self):
        self.SYS_TYPES = defaultdict(lambda: "Undefined")
        self.config = Config()
        self.log = ParseHistoryLog()
        self.monitor = ProgressMonitor()
        self.parsing_function_paths = []

    # Dynamic Import of generated-parsing functions
    def import_functions(self, parsing_functions_paths):
        for parsing_code_path in self.parsing_function_paths:
            module_name = parsing_code_path.split('.py')[0]
            globals()[module_name] = importlib.import_module(f"IDL.{module_name}")

    # Update IP infos from config_data
    def update_system_type(self, config_data):
        local = {key: LOCAL_IP_PREFIX + val for key, val in config_data['IP_local'].items()}
        self.SYS_TYPES.update({local['adoc_ip1']:'ADOC', local['adoc_ip2']:'ADOC', local['adoc_ip3']:'ADOC',
                               local['wcc_ip1']: 'WCC',  local['wcc_ip2']: 'WCC',  local['wcc_ip3']: 'WCC',
                               local['dlu_ip1']: 'DLU',  local['dlu_ip2']: 'DLU',  local['dlu_ip3']: 'DLU'})

        self.SYS_TYPES['10.30.7.255'] = 'WCC'    # TODO: For Testing
        self.SYS_TYPES['10.30.7.255'] = 'WCC'    # TODO: For Testing
        self.SYS_TYPES['10.30.7.66'] = 'WCC'    # TODO: For Testing

    def estimated_packet_num(self, file_path):
        os.path.getsize(file_path)
        return 660000

    def run(self, raw_file_path):
        packet_infos = []
        self.update_system_type(self.config.get())
        import time
        start = time.time()
        total_packets = self.log.get(raw_file_path)
        print(raw_file_path)
        # No previous parsing log
        if total_packets is None: total_packets = self.estimated_packet_num(raw_file_path);print(total_packets)
        # Zero packets
        if total_packets == 0:
            self.monitor.update_and_check_stop('parse', task_idx=0, task_total=1)
            return packet_infos

        self.monitor.update('parse', task_total=total_packets)
        # Read raw pcap files
        with scapy.PcapReader(raw_file_path) as packets:
            idx = -1
            for packet in packets:
                idx += 1
                # Update monitoring and Check if Stopped
                if self.monitor.update_and_check_stop('parse', task_idx=idx): return

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
                packet_infos.append(packet_info)

        # Updates raw file's total packet number
        self.log.update(raw_file_path, idx+1)       # TODO: if len(packets)==0 error
        print(time.time() - start, total_packets)

        return packet_infos

    def parse_RTPS(self, msg_type, data):
        results = []
        HEAD_LEN = RTPS_header_size         # 20
        SUBHEAD_LEN = RTPS_subheader_size   # 4
        pkt_len = len(data)
        if len(data) < HEAD_LEN + SUBHEAD_LEN:
            return None

        # if data[0:4] != b'RTPS': return       # TODO: Delete after testing
        idx = HEAD_LEN
        while idx + SUBHEAD_LEN <= pkt_len-1:
            # Parse Sub-Msg Header
            endian = data[idx+1] & 0x01
            subMsg_header = struct.unpack(RTPS_subheader_fmt[endian], data[idx:idx+SUBHEAD_LEN])
            print(subMsg_header)
            # Sub-Message Header at least 4 bytes
            subMsg_len = subMsg_header[2]
            if subMsg_len < SUBHEAD_LEN: return
            if idx + subMsg_len > pkt_len-1:
                return

            result = self.parse_msg(msg_type, data[idx+SUBHEAD_LEN:idx+subMsg_len])
            if result: result.append(result)

            idx += subMsg_len
            print(idx)

    # Parse if EIE or TIE or K or X or J
    def parse_data(self, msg_type, data):
        type_function_name = f'parse_{msg_type}'
        if type_function_name in globals():
            return globals()[type_function_name](data)
        else:
            # print(f"Can not find msg type '{msg_type}'")
            return None

    # noinspection PyUnresolvedReferences
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

    # noinspection PyUnresolvedReferences
    def parse_TIE(self, data):
        # Find TIE type from TIE header
        tie_type = struct.unpack('>H', data[0:2])[0]
        # print(tie_type)
        tie_type = 0x301
        TIE_function_name = f'parse_TIE_{hex(tie_type)}'
        if TIE_function_name in parse_TIE_Msg.__dict__:
            return parse_TIE_Msg.__dict__[TIE_function_name](data)
        else:
            print(f"Can not find type 'TIE_{hex(tie_type)}'")
            return None

    def parse_MDIL(self, data):
        mdil_type = struct.unpack('H', data[0:2])[0]



if __name__ == "__main__":
    # raw_file = r"C:\Users\74841\ProjectPPS\RAW\packet_250305_173850.pcap"
    #
    # raw_to_csv('a,', raw_file)

    parsing_codes = ['parse_EIE_Msg.py', 'parse_TIE_Msg.py']

    packet_parser = PacketParser(parsing_codes)
