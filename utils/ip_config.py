import json
from copy import deepcopy

DEFAULT_IP_CONFIG_DATA = {'interface': ["No ", "Interface ", "Selected"],
                       'IP_local': {'adoc_ip1':  "2", 'adoc_ip2':  "3", 'adoc_ip3':  "",
                                    'wcc_ip1' :  "8", 'wcc_ip2' : "10", 'wcc_ip3' : "11", 'wcc_ip4': "13",
                                    'dlu_ip1' : "27", 'dlu_ip2' : "28", 'dlu_ip3' : "30"},
                       'IP_near' : {'mdil_ip1' : "110", 'mdil_ip2' : "116", 'mdil_ip3' : "6"},
                       'IP_ext'  : {'kicc_ip1' : "", 'kicc_ip2' : "", 'kicc_ip3' : "", 'kicc_ip4' : "",
                                    'kamd_ip1' : "", 'kamd_ip2' : "", 'kamd_ip3' : "", 'kamd_ip4' : "",
                                    'picc_ip1' : "", 'picc_ip2' : "", 'picc_ip3' : "", 'picc_ip4' : ""},
                          }

IP_CONFIG_FILE_NAME = 'ip_settings.conf'

# Singleton Configuration
class IP_Config:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(IP_Config, cls).__new__(cls)
            cls.__instance._settings = deepcopy(DEFAULT_IP_CONFIG_DATA)
        return cls.__instance

    def __init__(self):
        self.load_config_file()
        # print("[IP_Config] 'ip_settings.conf' loaded!")

    def same_keys_recursive(self, dict1, dict2):
        if set(dict1.keys()) != set(dict2.keys()):
            return False
        for key, dict1_val in dict1.items():
            dict2_val = dict2[key]
            if type(dict1_val) != type(dict2_val):
                return False
            if isinstance(dict1_val, dict) and isinstance(dict2_val, dict):
                if not self.same_keys_recursive(dict1_val, dict2_val):
                    return False
        return True

    def load_config_file(self, path=None):
        try:
            with open(path if path else IP_CONFIG_FILE_NAME, "r") as file:
                self._settings = json.load(file)
                if not self.same_keys_recursive(self._settings, DEFAULT_IP_CONFIG_DATA):
                    raise KeyError("[Error] Invalid Dictionary Keys")
        except Exception as e:
            print(f"[IP_Config] {e}! / 'ip_settings.conf' reset!")
            # Reset configuration
            self._settings = deepcopy(DEFAULT_IP_CONFIG_DATA)
            self.save_config_file()

    def save_config_file(self):
        with open("ip_settings.conf", "w") as file:
            json.dump(self._settings, file, indent=4)
        print("[IP_Config] 'ip_settings.conf' saved!")

    def get(self, key=None):
        self.load_config_file()
        if key is None:
            return deepcopy(self._settings)
        else:
            return deepcopy(self._settings.get(key, None))

    def update(self, new_settings):
        if isinstance(new_settings, dict):
            self._settings.update(new_settings)
        self.save_config_file()
        self.load_config_file()









