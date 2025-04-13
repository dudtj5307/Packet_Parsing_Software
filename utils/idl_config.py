import os
import json
import re

from copy import deepcopy

IDL_CONFIG_FILE_NAME = 'IDL/idl_params.conf'

# Singleton Configuration
class IDL_Config:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(IDL_Config, cls).__new__(cls)
            cls.__instance._settings = deepcopy(DEFAULT_IDL_CONFIG_DATA)
        return cls.__instance

    def __init__(self):
        self.load_config_file()
        # print("[IDL_Config] 'idl_params.conf' loaded!")

    def same_keys(self, dict1, dict2):
        if set(dict1.keys()) != set(dict2.keys()):
            return False
        for key, dict1_val in dict1.items():
            dict2_val = dict2[key]
            if type(dict1_val) != type(dict2_val):
                return False
        return True

    def load_config_file(self, path=None):
        try:
            with open(path if path else IDL_CONFIG_FILE_NAME, "r") as file:
                self._settings = json.load(file)
                if not self.same_keys(self._settings, DEFAULT_IDL_CONFIG_DATA):
                    raise KeyError("[Error] Invalid Dictionary Keys")
        except Exception as e:
            print(f"[IDL_Config] {e}! / 'idl_params.conf' reset!")
            # Reset configuration
            self._settings = deepcopy(DEFAULT_IDL_CONFIG_DATA)
            self.save_config_file()

    def save_config_file(self):
        os.makedirs('IDL', exist_ok=True)
        json_str = json.dumps(self._settings)
        json_str = json_str.replace(': {', ': {\n        ').replace('}, ', '\n    },\n    ').replace('"], "' , '"],\n        "')
        json_str = json_str.replace('{"', '{\n    "')#.replace('", "', '",\n        "')
        with open("IDL/idl_params.conf", "w") as file:
            file.write(json_str)
            # json.dump(self._settings, file, indent=4, separators=(',', ':'))
        print("[IDL_Config] 'idl_params.conf' saved!")

    def get(self, key=None):
        self.load_config_file()
        if key is None:
            return deepcopy(self._settings)
        elif key == 'idl_paths':
            return [path for path in self._settings.get('idl_paths', {}).values() if path]
        else:
            return deepcopy(self._settings.get(key, {}))


DEFAULT_IDL_CONFIG_DATA = {
    'idl_paths': {
        'EIE_Msg'   : "IDL/EIE_Msg.idl",
        'TIE_Msg'   : "IDL/TIE_Msg.idl",
        'MDIL_Msg'  : "",
        'J_Msg'     : "",
        'X_Msg'     : "",
    },

    'string': {
        'fileEntry' : ['filename', 'fileDescription'],
        'iffMode2Code' : ['codeInfo'],
        'EIE_0x0045' : ['voiceCallSign'],
        'EIE_0x0080' : ['textMsg'],
        'EIE_0x0081' : ['textMsg'],
        'EIE_0x1000' : ['name'],
        'EIE_0x1001' : ['name'],
        'EIE_0x2060' : ['etc'],
        'EIE_0x2061' : ['etc'],
        'EIE_0x4000' : ['name'],
        'EIE_0x4001' : ['name'],
        'EIE_0x6020' : ['textMsg'],
        'EIE_0x6023' : ['textMsg'],
        'EIE_0x6031' : ['versionInfo'],
        'EIE_0x70F1' : ['strErrCode'],
        'EIE_0x70F3' : ['statusString'],
        'EIE_0x81C0' : ['textMsg'],
        'EIE_0x81C3' : ['textMsg'],
        'EIE_0x81D1': ['textMsg'],
        'EIE_0xE020' : ['scenarioCtrl'],
        'EIE_0xE021' : ['scenarioCtrl'],
        'EIE_0xEFA0' : ['rawData'],
        'EIE_0xEFA1' : ['rawData'],
        'EIE_0xF133' : ['data'],
        'EIE_0xF156' : ['etc'],
    },

    'group': {
        'EIE_0x9220' : ['j3_2_Air', 'j3_3_Surface', 'j3_4_Subsurface', 'j3_5_Land', 'j3_6_Space', 'j3_7_Ewpi'],
        'EIE_0x9221' : ['j3_2_Air', 'j3_3_Surface', 'j3_4_Subsurface', 'j3_5_Land', 'j3_6_Space', 'j3_7_Ewpi'],
        'EIE_0x9230' : ['j2_x_filter', 'j3_x_filter', 'j7_x_filter', 'j9_x_filter', 'j10_x_filter', 'j13_x_filter', 'j28_x_filter'],
        'EIE_0x9231' : ['j2_x_filter', 'j3_x_filter', 'j7_x_filter', 'j9_x_filter', 'j10_x_filter', 'j13_x_filter', 'j28_x_filter'],
        'EIE_0x9250' : ['j3_2_Air[7]',	'j3_3_Surface[7]', 'j3_4_Subsurface[7]',	 'j3_5_Land[7]', 'j3_6_Space[7]', 'j3_7_Ewpi[7]', 'j2_x_ppli[4]'],
        'EIE_0x9251' : ['j3_2_Air[7]',	'j3_3_Surface[7]', 'j3_4_Subsurface[7]',	 'j3_5_Land[7]', 'j3_6_Space[7]', 'j3_7_Ewpi[7]', 'j2_x_ppli[4]'],
        'EIE_0x9260' : ['j3_2_Air[7]',	'j3_3_Surface[7]', 'j3_4_Subsurface[7]',	 'j3_5_Land[7]', 'j3_6_Space[7]', 'j3_7_Ewpi[7]', 'j2_x_ppli[4]'],
        'EIE_0x9261' : ['j3_2_Air[7]',	'j3_3_Surface[7]', 'j3_4_Subsurface[7]',	 'j3_5_Land[7]', 'j3_6_Space[7]', 'j3_7_Ewpi[7]', 'j2_x_ppli[4]'],
        'EIE_0x92A0' : ['j2_x_ageLimit[8]', 'j3_x_ageLimit[8]', 'j7_x_ageLimit[8]', 'j9_x_ageLimit[8]', 'j10_x_ageLimit[8]', 'j13_x_ageLimit[8]', 'j28_x_ageLimit[8]'],
        'EIE_0x92A1' : ['j2_x_ageLimit[8]', 'j3_x_ageLimit[8]', 'j7_x_ageLimit[8]', 'j9_x_ageLimit[8]', 'j10_x_ageLimit[8]', 'j13_x_ageLimit[8]', 'j28_x_ageLimit[8]'],

        'EIE_0xD001' : ['BIT_Result_DLU', 'BIT_Result_WCC', 'BIT_Result_IPUCP', 'BIT_Result_PCP', 'BIT_Result_DPU', 'BIT_Result_GPS', 'BIT_Result_ADOC1', 'BIT_Result_ADOC2', 'BIT_Result_CCC1', 'BIT_Result_CCC2', 'BIT_Result_CCC3', 'BIT_Result_CCC4', 'BIT_Result_CCC5', 'BIT_Result_reserved2', 'BIT_Result_reserved3'],

        'EIE_0xD901' : ['result'],

        'EIE_0xEF00' : ['Data'],
        'EIE_0xEF01' : ['Data'],
        'EIE_0xEF02' : ['Data'],
        'EIE_0xEF03' : ['Data'],
        'EIE_0xEF04' : ['Data'],
        'EIE_0xEF05' : ['Data'],
        'EIE_0xEF06' : ['Data'],
        'EIE_0xEF07' : ['Data'],
        'EIE_0xEF10' : ['Data'],

        'EIE_0xF113' : ['mmr'],
        'EIE_0xF114' : ['nfz'],
        'EIE_0xF115' : ['kob'],
        'EIE_0xF119' : ['tss'],
        'EIE_0xF12A' : ['TM_IdParam'],
        'EIE_0xF12B' : ['TM_ClassParam'],
        'EIE_0xF12C' : ['TM_TrackingParam'],
        'EIE_0xF130' : ['MFR_IffAvailArea']
    },

    'convert_common': {
        'trkNo' : [['trkNo_MDIL', 'MDIL'], ['trkNo_TDIL_B', 'TDIL_B'], ['trkNo_TDIL_J', 'TDIL_J']],
        'strHeader'  : [['type', '04X']],
    },

    'convert_custom': {
        'EIE_0x70F1' : [['errCode',  '04X']],
        'EIE_0x70F3' : [['statusId', '04X']],
        'EIE_0x9271' : [['sourceTN', '05o']],

        'IEM_SYS_005' : [['CBIT_RESULT', '016b']],
    },
}


'''
================================Creator===========================

# Special Case #
#'EIE_0x7010' : 너무많음.... 30개 세트로 묶기?
'''





