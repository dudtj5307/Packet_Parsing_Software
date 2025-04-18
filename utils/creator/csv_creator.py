import os
import csv
from collections import defaultdict

from utils.monitor import ProgressMonitor
from utils.idl_config import IDL_Config
from utils.convert_functions import CONVERT_TN_FUNCS


def dict_key_flatten(dictionary, keys):
    new_dict = {}
    for k, v in dictionary.items():
        if k in keys and isinstance(v, dict):
            new_dict.update(v)
        else:
            new_dict[k] = v
    return new_dict


class CsvCreator:
    def __init__(self):
        self.monitor = ProgressMonitor()

        self.packet_infos = []
        self.csv_file_path = ""
        self.outputs = []

        # Get dynamic convert fields
        self.idl_config = IDL_Config()
        self.dynamic_convert = defaultdict(lambda: {})
        self.dynamic_convert.update(self.idl_config.get('dynamic_convert'))


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

    def run_converting(self):
        for info in self.packet_infos:
            try:
                # Convert dynamic fields
                self.run_dynamic_convert(info)

            except Exception as e:
                print(f"[Creator] {e}")
                continue

    # "idl_params.conf" - 'dynamic_convert'
    def run_dynamic_convert(self, info):
        msg_name = info['MSG_NAME']
        dynamic_field = self.dynamic_convert[msg_name]

        # Only exception for 'IEM_INFO_406'
        if msg_name == "IEM_INFO_406":
            self.convert_IEM_INFO_406_DATA(info['DATA'])
            return

        for field_name_array, field_values in info['DATA'].items():
            field_name = field_name_array.split('[')[0]
            if field_name not in dynamic_field:
                continue
            # Get TN_TYPE FIELD_NAME
            tn_type_field = dynamic_field[field_name]
            if tn_type_field not in info['DATA']:
                continue
            # Get dynamic TN_TYPE
            tn_type = info['DATA'][tn_type_field]
            info['DATA'][field_name_array] = CONVERT_TN_FUNCS[tn_type](field_values)

    # TODO: check if right
    def convert_IEM_INFO_406_DATA(self, data):
        sub_tn_type = data['SUBJECT_TN_TYPE']
        for i in range(19):
            data[f'SUBJECT_TN_ARRAY[{i}]']   = CONVERT_TN_FUNCS[sub_tn_type](data[f'SUBJECT_TN_ARRAY[{i}]'])      # 'SUBJECT_TN_ARRAY'
            data[f'SUBJECT_TN_ARRAY2[{i}]']  = CONVERT_TN_FUNCS[sub_tn_type](data[f'SUBJECT_TN_ARRAY2[{i}]'])     # 'SUBJECT_TN_ARRAY2'
            data[f'TARGET_TN_ARRAY[{i}]']    = CONVERT_TN_FUNCS[data[f'TARGET_TN_TYPE[{i}]']](data[f'TARGET_TN_ARRAY[{i}]'])        # 'TARGET_TN_ARRAY'
            data[f'TARGET_TN_J_ARRAY[{i}]']  = CONVERT_TN_FUNCS[data[f'TARGET_TN_J_TYPE[{i}]']](data[f'TARGET_TN_J_ARRAY[{i}]'])    # 'TARGET_TN_J_ARRAY'
            data[f'TARGET_TN_J_ARRAY2[{i}]'] = CONVERT_TN_FUNCS[data[f'TARGET_TN_J_TYPE2[{i}]']](data[f'TARGET_TN_J_ARRAY2[{i}]'])  # 'TARGET_TN_J_ARRAY2'

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


if __name__ == "__main__":
    a = "strHeader[0]"
    b = "strHeader"
    print(a.split("["))
    print(b.split("0"))


    d = {'MSG_NAME': "IEM_SURV_103",
         'DATA': {
             'TN_ARRAY[0]': 1000, 'TN_ARRAY[1]': 2000, 'TN_ARRAY[2]': 3000, 'TN_ARRAY[3]': 4000, 'TN_TYPE': 4,
             'REPORTING_SRC_TN_VALUE': 1000, 'REPORTING_SRC_TN_TYPE': 4}
         }

    c = CsvCreator()
    c.run_dynamic_convert(d)
    print(d)