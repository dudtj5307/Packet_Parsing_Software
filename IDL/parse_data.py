import struct

from . import parse_EIE_Msg
from . import parse_TIE_Msg
# from . import parse_K_Msg
# from . import parse_X_Msg

def parse_type(msg_type, data):
    type_function_name = f'parse_{msg_type}'
    if type_function_name in globals():
        return globals()[type_function_name](data)
    else:
        print(f"Can not find msg type '{msg_type}'")
        return None

def parse_EIE(data):
    # Find TIE type from TIE header
    eie_type = struct.unpack('>H', data[0:2])[0]
    eie_type = 0x301
    EIE_function_name = f'parse_EIE_{hex(eie_type)}'
    if EIE_function_name in parse_EIE_Msg.__dict__:
        return parse_EIE_Msg.__dict__[EIE_function_name](data)
    else:
        print(f"Can not find type 'EIE_{hex(eie_type)}'")
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
        print(f"Can not find type 'TIE_{hex(tie_type)}'")
        return None

if __name__ == '__main__':
    # fmt = 'iHHIIiHHIIBIHBihc'
    # data = [1] * 16 + [b'0']
    # data = struct.pack(fmt, *data)

    # result = parse_EIE(0x302, data)
    # print(result)
    # result = parse_EIE(0x300, data)
    # print(result)
    pass