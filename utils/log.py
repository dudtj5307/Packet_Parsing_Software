import os
import json
from copy import deepcopy

LOG_FOLDER = 'RAW'
LOG_FILE_NAME = 'RAW/history.log'

class ParseHistoryLog:
    def __init__(self):
        self._history = {}
        self.load_log_file()

    def load_log_file(self, path=None):
        os.makedirs(LOG_FOLDER, exist_ok=True)
        try:
            with open(path if path else LOG_FILE_NAME, "r") as file:
                self._history.update(json.load(file))
        except Exception as e:
            # Reset and Save
            self._history = {}
            self.save_log_file()
        print('load', self._history)

    def save_log_file(self):
        with open(LOG_FILE_NAME, "w") as file:
            json.dump(self._history, file, indent=4)

    def get(self, raw_file_path):
        self.load_log_file()
        if raw_file_path in self._history:
            _, raw_file_name = os.path.split(raw_file_path)
            return self._history[raw_file_name]
        else:  return None

    def update(self, raw_file_path, packet_count):
        _, raw_file_name = os.path.split(raw_file_path)
        self._history[raw_file_name] = packet_count
        self.save_log_file()
        print('update', self._history)



