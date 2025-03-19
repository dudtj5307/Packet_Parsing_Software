# from pandas import DataFrame

import os
import csv
from utils.monitor import ProgressMonitor

class CsvCreator:
    def __init__(self):
        self.monitor = ProgressMonitor()

        self.packet_infos = []
        self.csv_file_path = ""
        self.outputs = []

    def run(self, packet_infos, csv_file_path):
        self.packet_infos = packet_infos * 10000
        print("id 비교", id(self.packet_infos), id(packet_infos))     # TODO: For Testing
        self.csv_file_path = csv_file_path
        # Create CSV - All
        self.make_csv_all(packet_infos)

        # Create CSV by MSG_NAMES
        uniq_msg_names = self.get_unique_value("MSG_NAME")
        self.make_csv_separate(uniq_msg_names)

    def get_unique_value(self, colname):
        return set(map(lambda info: info[colname], self.packet_infos))

    # TODO: Add monitor update
    def make_csv_all(self, packet_infos):
        csv_save_path = os.path.join(self.csv_file_path, "all.csv")
        with open(csv_save_path, mode="w", encoding="utf-8", newline="") as file:
            fieldnames = packet_infos[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()            # Write Header
            writer.writerows(packet_infos*100000)  # Write Data

    def make_csv_separate(self, uniq_names):
        for idx, name in enumerate(uniq_names):
            if self.monitor.update_check_stop('csv', task_idx=idx, task_total=len(uniq_names), prior_status=0.5): return

            packet_filtered = [info['DATA'] for info in self.packet_infos if info["MSG_NAME"] == name]
            csv_save_path = os.path.join(self.csv_file_path, f"{name}.csv")
            with open(csv_save_path, mode="w", encoding="utf-8", newline="") as file:
                fieldnames = packet_filtered[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()  # Write Header
                writer.writerows(packet_filtered)  # Write Data

        pass


def filter_list_comprehension(data, job):
    return [person for person in data if person["직업"] == job]

if __name__ == "__main__":
    import time
    # 성능 비교
    job = "개발자"

    data = [{"이름": f"사람{i}", "나이": i % 50 + 20, "직업": "개발자" if i % 2 == 0 else "디자이너"} for i in range(10000000)]

    # 리스트 컴프리헨션 테스트
    start_time = time.time()
    filter_list_comprehension(data, job)
    time_list_comprehension = time.time() - start_time
    print(f"리스트 컴프리헨션: {time_list_comprehension:.6f} 초")

    # filter() 함수 테스트
    start_time = time.time()
    filter_with_filter(data, job)
    time_filter = time.time() - start_time
    print(f"filter() 함수: {time_filter:.6f} 초")

    # for loop 테스트
    start_time = time.time()
    filter_with_for_loop(data, job)
    time_for_loop = time.time() - start_time
    print(f"for loop: {time_for_loop:.6f} 초")