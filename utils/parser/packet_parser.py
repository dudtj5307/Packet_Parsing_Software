import os
import sys
import importlib.util
import struct
from datetime import datetime
from collections import defaultdict

import scapy.all as scapy
from scapy.layers.inet import IP, UDP

from utils.config import Config
from utils.monitor import ProgressMonitor
from utils.parser.log import ParseHistoryLog
from utils.parser.ndds import NDDS
from utils.parser.message_map import TIE_LABEL_NAME

LOCAL_IP_PREFIX = '192.168.0.'
NEAR_IP_PREFIX = '192.168.'

MSG_TYPES = defaultdict(lambda: "Undefined")
MSG_TYPES.update({('ADOC','ADOC'): 'EIE', ('ADOC','WCC'): 'EIE', ('WCC','ADOC'): 'EIE', ('WCC', 'WCC'): 'EIE',
                  ('WCC', 'DLU') : 'TIE', ('DLU', 'WCC'): 'TIE', ('DLU','DLU') : 'TIE',
                  ('MDIL', 'MDIL') : 'K_Msg', })

RTPS_HEADER_FMT = ">4s H H 8s"          # Big-endian (>)
RTPS_HEADER_LEN = struct.calcsize(RTPS_HEADER_FMT)

RTPS_SUBHEADER_FMT_1ST = ">B B"         # subtype, endian
RTPS_SUBHEADER_FMT_2ND = [">H", "<H"]   # data_len  ([0] Big-endian > / [1] : Little-endian < )
RTPS_SUBHEADER_LEN = struct.calcsize("BBH")

def sub_header_unpack(data):
    subId, endian = struct.unpack(RTPS_SUBHEADER_FMT_1ST, data[0:2])
    if endian not in [0,1]:
        return 'Invalid', None, None
    data_len = struct.unpack(RTPS_SUBHEADER_FMT_2ND[endian], data[2:4])[0]
    return subId, endian, data_len

class PacketParser:
    def __init__(self):
        self.SYS_TYPES = defaultdict(lambda: "Unknown")
        self.config = Config()
        self.log = ParseHistoryLog()
        self.monitor = ProgressMonitor()
        self.parsing_function_paths = []
        self.imported_modules = {}

    # Dynamic Import of generated-parsing functions
    def import_functions(self, parsing_function_paths):
        for parsing_code_path in parsing_function_paths:
            module_filename = os.path.basename(parsing_code_path)
            module_name = f"{os.path.splitext(module_filename)[0]}"
            full_path = os.path.abspath(os.path.join('IDL', parsing_code_path))

            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Parsing module file not found: {full_path}")

            # Load the module from the file path
            spec = importlib.util.spec_from_file_location(module_name, full_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Add to globals and sys.modules if needed
            self.imported_modules[module_name] = module

    # Update IP infos from config_data
    def update_system_type(self, config_data):
        # Local IPs
        local = {key: LOCAL_IP_PREFIX + str(val) for key, val in config_data['IP_local'].items()}
        self.SYS_TYPES.update({local['adoc_ip1']:'ADOC', local['adoc_ip2']:'ADOC', local['adoc_ip3']:'ADOC',
                               local['wcc_ip1']: 'WCC',  local['wcc_ip2']: 'WCC',  local['wcc_ip3']: 'WCC', local['wcc_ip4']: 'WCC',
                               local['dlu_ip1']: 'DLU',  local['dlu_ip2']: 'DLU',  local['dlu_ip3']: 'DLU'})
        # Near IPs
        range_mdil = range(int(config_data['IP_near']['mdil_ip1']), int(config_data['IP_near']['mdil_ip2']) + 1)
        near = {NEAR_IP_PREFIX + str(IP_C) + '.' + config_data['IP_near']['mdil_ip3'] : 'MDIL' for IP_C in range_mdil}
        self.SYS_TYPES.update(near)

    def estimated_packet_num(self, file_path):
        os.path.getsize(file_path)
        return 660000

    def run(self, raw_file_path):
        packet_infos = []
        self.update_system_type(self.config.get())
        import time
        start = time.time()

        # Get packet number from log
        total_packets = self.log.get(raw_file_path)

        # No previous parsing log
        if total_packets is None:
            total_packets = self.estimated_packet_num(raw_file_path)

        # Zero packets          # TODO: How to handle zero packets...
        if total_packets == 0:
            total_packets = 1

        # Read raw pcap files
        with scapy.PcapReader(raw_file_path) as packets:
            idx = -1
            for packet in packets:
                idx += 1
                # Update monitoring and Check if Stopped
                if self.monitor.update_check_stop('parse', task_idx=idx, task_total=total_packets): return

                # Filter Packets without data (ex. ACK, FIN, SYN msgs)
                if not packet.haslayer('Raw'):
                    continue
                raw_data = packet['Raw'].load
                date, _time = datetime.fromtimestamp(float(packet.time)).strftime("%Y-%m-%d %H:%M:%S.%f").split(" ")
                src_ip,  dst_ip  = packet[IP].src, packet[IP].dst
                src_sys, dst_sys = self.SYS_TYPES[src_ip], self.SYS_TYPES[dst_ip]
                msg_type = MSG_TYPES[(src_sys, dst_sys)]
                if msg_type == 'Undefined':
                    continue      # TODO: For testing

                print(date, _time, src_ip, dst_ip, src_sys, dst_sys, msg_type)

                if packet.haslayer(UDP) and packet.haslayer(NDDS):
                    results = self.parse_RTPS(msg_type, raw_data)
                else:   # TODO: [TCP] MDIL, J-Msg, X-Msg, JREAP case
                    continue

                for msg_name, data in results:
                    packet_info = {'DATE': f"{date}'", 'TIME': f"{_time}'",'SENDER': f"{src_sys}({src_ip})", 'RECEIVER': f"{dst_sys}({dst_ip})",
                                   'MSG_NAME':msg_name, 'DATA':data}
                    packet_infos.append(packet_info)

        # Updates raw file's total packet number
        total_packets = idx + 1
        self.log.update(raw_file_path, total_packets)

        return packet_infos

    def parse_RTPS(self, msg_type, data):
        SUBHEAD_LEN = RTPS_SUBHEADER_LEN  # 4
        parse_results = []

        pkt_len = len(data)
        if pkt_len < SUBHEAD_LEN:
            return []
        idx = 0
        while idx + SUBHEAD_LEN <= pkt_len:
            # Parse Sub-Msg Header
            sub_id, endian, data_len = sub_header_unpack(data[idx:idx + SUBHEAD_LEN])    # [idx : idx + 4]
            idx += SUBHEAD_LEN

            # Check valid of subheader
            if sub_id == 'Invalid': return parse_results         # Invalid Endian Value
            if idx + data_len > pkt_len:  return parse_results   # Invalid data length
            if data_len == 0: continue              # Skip if 'data_len == 0'

            # Parse data if 'sub_id = 0x03(NOKEY_DATA)'
            if sub_id == 0x03:
                result = self.parse_data(msg_type, endian, data[idx + 16 : idx + 16 + data_len])  # TODO: 16 byte from etc infos
                if result[1]:
                    parse_results.append(result)
            idx += data_len
        return parse_results

    # Parse if EIE or TIE or K or X or J
    def parse_data(self, msg_type, endian, data):
        if msg_type == 'EIE':
            return self.parse_EIE(endian, data)
        elif msg_type == 'TIE':
            return self.parse_TIE(endian, data)
        else:
            print(f"[parse_data] Can not find msg type '{msg_type}'")
            return None, None

    # noinspection PyUnresolvedReferences
    def parse_EIE(self, endian, data):
        # Find EIE type from EIE header
        type_fmt = ['>H', '<H']
        eie_type = struct.unpack(type_fmt[endian], data[0:2])[0]        # Find right EIE header name
        eie_name = f'EIE_0x{eie_type:04X}'

        EIE_module = self.imported_modules.get("parse_EIE_Msg", None)
        EIE_func_name = f'parse_{eie_name}'

        if EIE_module and hasattr(EIE_module, EIE_func_name):
            return eie_name, getattr(EIE_module, EIE_func_name)(endian, data)
        else:
            print(f"[parse_EIE] Can not find EIE type '{eie_name}'")
            return None, None

    # noinspection PyUnresolvedReferences
    def parse_TIE(self, endian, data):
        # Find TIE type from TIE header
        label = struct.unpack('B', data[0:1])[0]
        sublabel = struct.unpack('B', data[1:2])[0]

        tie_name = f'IEM_{TIE_LABEL_NAME[label]}_{sublabel:03X}'

        TIE_module = self.imported_modules.get("parse_TIE_Msg", None)
        TIE_func_name = f'parse_{tie_name}'

        if TIE_module and hasattr(TIE_module, TIE_func_name):
            return tie_name, getattr(TIE_module, TIE_func_name)(endian, data)
        else:
            print(f"[parse_TIE] Can not find TIE type '{tie_name}'")
            return None, None

    def parse_MDIL(self, data):
        mdil_type = struct.unpack('H', data[0:2])[0]



if __name__ == "__main__":
    # raw_file = r"C:\Users\74841\ProjectPPS\RAW\packet_250305_173850.pcap"
    #
    # raw_to_csv('a,', raw_file)

    # parsing_codes = ['parse_EIE_Msg.py', 'parse_TIE_Msg.py']
    #
    # packet_parser = PacketParser(parsing_codes)
    a = (None, None)
    b = (123, None)
    if a[0]:
        print(a)

    if b[0]:
        print(b)