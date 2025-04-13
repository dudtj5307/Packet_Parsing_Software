import os
import csv
from collections import defaultdict

from utils.monitor import ProgressMonitor
from utils.idl_config import IDL_Config
from utils.creator.convert_functions import *


def dict_key_flatten(dictionary, keys):
    new_dict = {}
    for k, v in dictionary.items():
        if k in keys and isinstance(v, dict):
            new_dict.update(v)
        else:
            new_dict[k] = v
    return new_dict





print("dict", convert_recursive({}, ""))

class CsvCreator:
    def __init__(self):
        self.monitor = ProgressMonitor()

        self.packet_infos = []
        self.csv_file_path = ""
        self.outputs = []

        self.idl_config = IDL_Config()

        self.convert_common = defaultdict(lambda: [])
        self.convert_custom = defaultdict(lambda: [])


    def run(self, packet_infos, csv_file_path):
        self.packet_infos = packet_infos
        self.csv_file_path = csv_file_path

        # Convert format of fields in CSV (based on idl_params.conf - 'convert')
        self.run_converting()

        if self.monitor.update_check_stop('csv', task_idx=-1, task_total=1, prior_status=0.3): return

        # Create CSV - all.csv
        self.make_csv_all()

        if self.monitor.update_check_stop('csv', task_idx=-1, task_total=1, prior_status=0.6): return

        # Create CSV - by each MSG_NAMES
        self.make_csv_separate()


    def run_convert_custom(self, msg_name):
        field_list = self.convert_custom[msg_name]
        for field_name, field_format in field_list:
            if field_name in info['DATA'].keys():
                origin_val = info['DATA'][field_name]
                # If str, change to int
                if isinstance(origin_val, str):
                    origin_val = int(origin_val)

                val_list = list(origin_val) if isinstance(origin_val, (list, tuple)) else [origin_val]

                if field_format in CONVERT_FUNCS:
                    converted = [CONVERT_FUNCS[field_format](v) for v in val_list]
                else:
                    converted = [format(int(v), field_format) for v in val_list]

                if isinstance(origin_val, tuple):
                    info['DATA'][field_name] = tuple(converted)
                elif isinstance(origin_val, list):
                    info['DATA'][field_name] = converted
                else:
                    info['DATA'][field_name] = converted[0]

    # TODO: How to change convert_commons
    def run_convert_common(self, dictionary, find):
        for key, val in dictionary.items():
            if key in self.convert_common:
                for field_name, field_format in self.convert_common[key]:
                    pass

            if type(val) == dict:
                convert_recursive(val, find)
            else:
                if key in find:
                    val_dict[key] = find[key](val_dict[key])


    # Converts certain field formats (based on the idl_params.conf)
    def run_converting(self):
        # Get convert info
        self.convert_common.update(self.idl_config.get('convert_common'))
        self.convert_custom.update(self.idl_config.get('convert_custom'))

        for info in self.packet_infos:
            try:
                # Convert common fields
                self.run_convert_common(info)

                # Convert custom fields
                self.run_convert_custom(info['MSG_NAME'])

            except Error as e:
                print(f"[Creator] {e}")
                continue



    def get_unique_value(self, colname):
        return set(map(lambda info: info[colname], self.packet_infos))

    def make_csv_all(self):
        csv_save_path = os.path.join(self.csv_file_path, "all.csv")
        with open(csv_save_path, mode="w", encoding="utf-8", newline="") as file:
            fieldnames = self.packet_infos[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()            # Write Header
            writer.writerows(self.packet_infos)  # Write Data

    def make_csv_separate(self):
        # Get uniq msg_names
        uniq_msg_names = self.get_unique_value("MSG_NAME")

        # Make CSV by each names
        for idx, msg_name in enumerate(uniq_msg_names):
            packet_filtered = [dict_key_flatten(info, ['DATA']) for info in self.packet_infos if info["MSG_NAME"] == msg_name]

            csv_save_path = os.path.join(self.csv_file_path, f"{msg_name}.csv")
            with open(csv_save_path, mode="w", encoding="utf-8", newline="") as file:
                fieldnames = packet_filtered[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()                # Write Header
                writer.writerows(packet_filtered)   # Write Data

            if self.monitor.update_check_stop('csv', task_idx=idx, task_total=len(uniq_msg_names), prior_status=0.6): return
