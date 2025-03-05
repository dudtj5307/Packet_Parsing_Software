import struct

import parse_EIE_Msg
import parse_TIE_Msg
# import parse_K_Msg
# import parse_X_Msg

def parse_EIE(msgType, data):
    function_name = f'parse_EIE_{hex(msgType)}'
    if function_name in parse_EIE_Msg.__dict__:
        return parse_EIE_Msg.__dict__[function_name](data)
    else:
        print(f"Can not find type 'EIE_{hex(msgType)}'")

def parse_TIE(msgType, data):
    function_name = f'parse_TIE_{hex(msgType)}'
    if function_name in parse_TIE_Msg.__dict__:
        return parse_TIE_Msg.__dict__[function_name](data)
    else:
        print(f"Can not find type 'TIE_{hex(msgType)}'")


if __name__ == '__main__':
    fmt = 'iHHIIiHHIIBIHBihc'
    data = [1] * 16 + [b'0']
    data = struct.pack(fmt, *data)

    result = parse_EIE(0x302, data)
    print(result)
    result = parse_EIE(0x300, data)
    print(result)