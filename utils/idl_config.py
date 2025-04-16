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
        json_str = json.dumps(self._settings, indent=4)
        json_str = re.sub(r'\[\s*((?:"[^"]+",?\s*\n\s*)+)\]',
                          lambda m: '[' + ', '.join([x.strip().rstrip(',') for x in m.group(1).split('\n') if x.strip()]) + ']', json_str)
        json_str = re.sub(r'\{\s*\n\s*((?:"[^"]+"\s*:\s*"[^"]+",?\s*\n\s*)+)\s*\}',
                          lambda m: '{' + ', '.join(line.strip().rstrip(',') for line in m.group(1).split('\n') if line.strip()) + '}',json_str)
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
        # EIE MSG
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
        'EIE_0x81D1' : ['textMsg'],
        'EIE_0xE020' : ['scenarioCtrl'],
        'EIE_0xE021' : ['scenarioCtrl'],
        'EIE_0xEFA0' : ['rawData'],
        'EIE_0xEFA1' : ['rawData'],
        'EIE_0xF133' : ['data'],
        'EIE_0xF156' : ['etc'],

        # TIE MSG
        'IEM_SYS_011' : ['VERSION'],
        'IEM_SYS_014' : ['ERR_MSG_KOR', 'ERR_MSG_ENG'],
        'IEM_SYS_015' : ['SEND_DATA', 'RECV_DATA'],
        'IEM_SYS_016' : ['SEND_DATA', 'RECV_DATA'],
        'IEM_CMD_304' : ['VOICE_CALL_SIGN'],
        'IEM_INFO_407' : ['POINTER_TEXT'],
        'IEM_EXT_513'  : ['ASCII_TEXT'],
        'IEM_PTXT_801' : ['FREE_TEXT'],
        'IEM_MISC_914' : ['FREE_TEXT'],
    },

    'group': {
        # EIE MSG
        'EIE_0x9220' : ['j3_2_Air', 'j3_3_Surface', 'j3_4_Subsurface', 'j3_5_Land', 'j3_6_Space', 'j3_7_Ewpi'],
        'EIE_0x9221' : ['j3_2_Air', 'j3_3_Surface', 'j3_4_Subsurface', 'j3_5_Land', 'j3_6_Space', 'j3_7_Ewpi'],
        'EIE_0x9230' : ['j2_x_filter', 'j3_x_filter', 'j7_x_filter', 'j9_x_filter', 'j10_x_filter', 'j13_x_filter', 'j28_x_filter'],
        'EIE_0x9231' : ['j2_x_filter', 'j3_x_filter', 'j7_x_filter', 'j9_x_filter', 'j10_x_filter', 'j13_x_filter', 'j28_x_filter'],
        'EIE_0x9250' : ['j3_2_Air',	'j3_3_Surface', 'j3_4_Subsurface',	 'j3_5_Land', 'j3_6_Space', 'j3_7_Ewpi', 'j2_x_ppli'],
        'EIE_0x9251' : ['j3_2_Air',	'j3_3_Surface', 'j3_4_Subsurface',	 'j3_5_Land', 'j3_6_Space', 'j3_7_Ewpi', 'j2_x_ppli'],
        'EIE_0x9260' : ['j3_2_Air',	'j3_3_Surface', 'j3_4_Subsurface',	 'j3_5_Land', 'j3_6_Space', 'j3_7_Ewpi', 'j2_x_ppli'],
        'EIE_0x9261' : ['j3_2_Air',	'j3_3_Surface', 'j3_4_Subsurface',	 'j3_5_Land', 'j3_6_Space', 'j3_7_Ewpi', 'j2_x_ppli'],
        'EIE_0x92A0' : ['j2_x_ageLimit', 'j3_x_ageLimit', 'j7_x_ageLimit', 'j9_x_ageLimit', 'j10_x_ageLimit', 'j13_x_ageLimit', 'j28_x_ageLimit'],
        'EIE_0x92A1' : ['j2_x_ageLimit', 'j3_x_ageLimit', 'j7_x_ageLimit', 'j9_x_ageLimit', 'j10_x_ageLimit', 'j13_x_ageLimit', 'j28_x_ageLimit'],
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
        # ↓ ===== Check DAS ===== ↓ #
        'EIE_0xF113' : ['mmr'],
        'EIE_0xF114' : ['nfz'],
        'EIE_0xF115' : ['kob'],
        'EIE_0xF119' : ['tss'],
        'EIE_0xF12A' : ['TM_IdParam'],
        'EIE_0xF12B' : ['TM_ClassParam'],
        'EIE_0xF12C' : ['TM_TrackingParam'],
        'EIE_0xF130' : ['MFR_IffAvailArea'],
        # ↑ ===== Check DAS ===== ↑ #
    },

    # Generator
    'struct_convert': {
        # EIE MSG
        'strHeader' : {'type': '04X'},
        'trkNoSys'  : {'trkNo_MDIL'  : 'MDIL',
                       'trkNo_TDIL_B': 'TDIL_B',
                       'trkNo_TDIL_J': 'TDIL_J'},

        'EIE_0x70F1': {'errCode' : '04X'},
        'EIE_0x70F3': {'statusId': '04X'},
        'EIE_0x9271': {'sourceTN': '05o'},


        # TIE MSG
        'TN_PAIR' : {'ATDL_TN_VALUE'  : 'MDIL',
                     'TADIL_TN_VALUE' : 'TDIL_B',
                     'TADILJ_TN_VALUE': 'TDIL_J'},

        'IEM_SYS_004': {'SITE_NUMBER': 'TDIL_J'},
        'IEM_SYS_005': {'CBIT_RESULT': '016b'},
        'IEM_FILT_611': {'STN_ARR_TO_FILTER': '05o'},

    },

    'dynamic_convert': {
        # TIE MSG
        'IEM_SURV_102': {'TN_ARRAY': 'TN_TYPE'},
        'IEM_SURV_103': {'TN_ARRAY': 'TN_TYPE', 'REPORTING_SRC_TN_VALUE' : 'REPORTING_SRC_TN_TYPE'},
        'IEM_SURV_104': {'REPORTING_SRC_TN_VALUE' : 'REPORTING_SRC_TN_TYPE'},

        'IEM_SURV_106': {'TN_ARRAY' : 'TN_TYPE', 'TN_ARRAY2' : 'TN_TYPE'},
        'IEM_SURV_107': {'TN_ARRAY' : 'TN_TYPE', 'REPORTING_SRC_TN_VALUE': 'REPORTING_SRC_TN_TYPE'},
        'IEM_SURV_108': {'TN_ARRAY' : 'TN_TYPE', 'REPORTING_SRC_TN_VALUE': 'REPORTING_SRC_TN_TYPE'},
        'IEM_SURV_109': {'TN_ARRAY' : 'TN_TYPE', 'REPORTING_SRC_TN_VALUE': 'REPORTING_SRC_TN_TYPE'},
        'IEM_SURV_110': {'TN_ARRAY' : 'TN_TYPE', 'REPORTING_SRC_TN_VALUE': 'REPORTING_SRC_TN_TYPE'},
        'IEM_SURV_112': {'TN_ARRAY2': 'TN_TYPE'},
        'IEM_SURV_113': {'TN_ARRAY2': 'TN_TYPE', 'REPORTING_SRC_TN_VALUE': 'REPORTING_SRC_TN_TYPE'},
        'IEM_SURV_114': {'TN_ARRAY' : 'TN_TYPE', 'REPORTING_SRC_TN_VALUE': 'REPORTING_SRC_TN_TYPE'},

        'IEM_EW_201': {'TN_ARRAY': 'TN_TYPE'},
        'IEM_EW_202': {'TN_ARRAY': 'TN_TYPE', 'REPORTING_SRC_TN_VALUE': 'REPORTING_SRC_TN_TYPE', 'TN_ORIGIN_VALUE': 'TN_ORIGIN_TYPE'},

        'IEM_CMD_301': {'ADDRESSEE_TN_ARRAY': 'ADDRESSEE_TN_TYPE', 'ORIGINATOR_TN_VALUE': 'ORIGINATOR_TN_TYPE', 'OBJECTIVE_TN_ARRAY': 'OBJECTIVE_TN_TYPE'},
        'IEM_CMD_302': {'FWS_TN_ARRAY': 'FWS_TN_TYPE', 'TARGET_TN_ARRAY': 'TARGET_TN_TYPE'},
        'IEM_CMD_303': {'FWS_TN_ARRAY': 'FWS_TN_TYPE', 'TN_VALUE_SOURCE': 'TN_TYPE_SOURCE'},
        'IEM_CMD_304': {'TN_VALUE': 'TN_TYPE', 'TN_VALUE_SOURCE': 'TN_TYPE_SOURCE'},
        'IEM_CMD_305': {'TN_VALUE': 'TN_TYPE', 'OBJECTIVE_TN_VALUE': 'OBJECTIVE_TN_TYPE'},

        'IEM_INFO_401': {'TN_ARRAY': 'TN_TYPE'},
        'IEM_INFO_402': {'TN_VALUE': 'TN_TYPE'},
        'IEM_INFO_403': {'TN_ARRAY': 'TN_TYPE', 'TN_ARRAY2': 'TN_TYPE'},
        'IEM_INFO_404': {'TN_ARRAY': 'TN_TYPE', 'REPORTING_SRC_TN_VALUE': 'REPORTING_SRC_TN_TYPE', 'TN_ARRAY2': 'TN_TYPE'},
        'IEM_INFO_405': {'TN_ARRAY': 'TN_TYPE', 'REPORTING_SRC_TN_VALUE': 'REPORTING_SRC_TN_TYPE', 'TN_ARRAY2': 'TN_TYPE'},
        'IEM_INFO_406': {'SUBJECT_TN_ARRAY' : 'SUBJECT_TN_TYPE', 'TARGET_TN_ARRAY': 'TARGET_TN_TYPE', 'TARGET_TN_J_ARRAY': 'TARGET_TN_J_TYPE',
                         'SUBJECT_TN_ARRAY2': 'SUBJECT_TN_TYPE', 'TARGET_TN_J_ARRAY2': 'TARGET_TN_J_TYPE2'},
        'IEM_INFO_407': {'TN_ORIG_VALUE' : 'TN_ORIG_TYPE',  'TN_ADDR1_VALUE': 'TN_ADDR1_TYPE', 'TN_ADDR2_VALUE': 'TN_ADDR2_TYPE',
                         'TN_ADDR3_VALUE': 'TN_ADDR3_TYPE', 'TN_ADDR4_VALUE': 'TN_ADDR4_TYPE', 'TN_ADDR5_VALUE': 'TN_ADDR5_TYPE'},
        'IEM_INFO_408': {'TN_ARRAY_SUBJ': 'TN_TYPE_SUBJ', 'TN_ARRAY_ASSOC': 'TN_TYPE_ASSOC', 'TN_VALUE_ORIG': 'TN_TYPE_ORIG'},
        'IEM_INFO_409': {'DUR_TN_ARRAY': 'DUR_TN_TYPE',  'TN_ADDR_VALUE': 'TN_ADDR_TYPE',  'DUR_TN_ARRAY2': 'DUR_TN_TYPE'},
        'IEM_INFO_410': {'TN_ARRAY': 'TN_TYPE', 'TN_ARRAY2': 'TN_TYPE'},
        'IEM_INFO_411': {'RETAINED_TN_VALUE': 'RETAINED_TN_TYPE', 'DROPPED_TN_VALUE': 'DROPPED_TN_TYPE'},
        'IEM_INFO_413': {'TN_ARRAY': 'TN_TYPE'},
        'IEM_INFO_414': {'DROPPED_TN_VALUE' : 'DROPPED_TN_TYPE', 'RETAINED_TN_VALUE': 'RETAINED_TN_TYPE'},

        'IEM_EXT_501': {'RELAY_SITE_NUMBER': 'RELAY_SITE_TYPE', 'SITE_NUMBER': 'SITE_TYPE'},
        'IEM_EXT_502': {'REMOTE_SITE_VALUE': 'REMOTE_SITE_TYPE'},
        'IEM_EXT_503': {'SITE_NUMBER': 'SITE_TYPE'},
        'IEM_EXT_504': {'SITE_NUMBER': 'SITE_TYPE'},
        'IEM_EXT_509': {'ICC_SITE_NUMBER': 'ICC_SITE_TYPE', 'AECS_SITE_NUMBER': 'AECS_SITE_TYPE'},
        'IEM_EXT_510': {'SITE_NUMBER': 'SITE_TYPE'},
        'IEM_EXT_511': {'SITE_NUMBER': 'SITE_TYPE'},
        'IEM_EXT_512': {'SITE_NUMBER': 'SITE_TYPE'},
        'IEM_EXT_513': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_EXT_514': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_EXT_515': {'SITE_NUMBER': 'SITE_TYPE'},

        'IEM_FILT_603': {'ADDRESSEE_TN_VALUE': 'ADDRESSEE_TN_TYPE'},
        'IEM_FILT_604': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_605': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_606': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_607': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_608': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_609': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_610': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_611': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_612': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_613': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_614': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_615': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_616': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},
        'IEM_FILT_617': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_DEST_VALUE': 'TN_DEST_TYPE'},

        'IEM_INTELLI_701': {'TN_ARRAY': 'TN_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_INTELLI_702': {'TN_ARRAY': 'TN_TYPE'},

        'IEM_PTXT_801': {'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'TN_ADDR_ARRAY': 'TN_ADDR_TYPE'},
        'IEM_PTXT_802': {'SITE_NUMBER': 'SITE_TYPE'},
        'IEM_MISC_901': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_902': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_903': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_904': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_905': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_906': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_907': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_908': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_909': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE', 'MSL_TN_VALUE': 'MSL_TN_TYPE', 'TARGET_TN_VALUE': 'TARGET_TN_TYPE'},
        'IEM_MISC_910': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_911': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_912': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_913': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_914': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_915': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_916': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
        'IEM_MISC_917': {'SITE_NUMBER': 'SITE_TYPE', 'TN_ORIG_VALUE': 'TN_ORIG_TYPE'},
    },
}


'''
================================Creator===========================
# Special Case #
#'EIE_0x7010' : 너무많음.... 30개 세트로 묶기?

	# 'IEM_INFO_406': 
	# 'TARGET_TN_ARRAY'   : 'TARGET_TN_TYPE'     -> list : list
	# 'TARGET_TN_J_ARRAY' : 'TARGET_TN_J_TYPE'   -> list : list
	# 'TARGET_TN_J_ARRAY2': 'TARGET_TN_J_TYPE2' -> list : list

'''





