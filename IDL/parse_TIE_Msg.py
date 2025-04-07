# TIE_Msg.idl : 1b809091394987652a0c645a88e0003aa4e3bf09f927ce98980808af06d05b3d
# Auto-generated parsing function

import struct

# Parse struct 'TIE_0x443'
def parse_TIE_0x443(endian, data):
    size = 14
    if len(data) != size:
        print(f'[parse_TIE_0x443] Invalid data size: {len(data)} (14)')
        return None
    fmt  = ['>IHBihc',
            '<IHBihc',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'type1': data[0],
    'type2': data[1],
    'type3': data[2],
    'type4': data[3],
    'type5': data[4],
    'type6': data[5],
    }
    return result

# Parse struct 'TIE_0x445'
def parse_TIE_0x445(endian, data):
    size = 14
    if len(data) != size:
        print(f'[parse_TIE_0x445] Invalid data size: {len(data)} (14)')
        return None
    fmt  = ['>IHBihc',
            '<IHBihc',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'type1': data[0],
    'type2': data[1],
    'type3': data[2],
    'type4': data[3],
    'type5': data[4],
    'type6': data[5],
    }
    return result

# Parse struct 'TIE_0x455'
def parse_TIE_0x455(endian, data):
    size = 14
    if len(data) != size:
        print(f'[parse_TIE_0x455] Invalid data size: {len(data)} (14)')
        return None
    fmt  = ['>IHBihc',
            '<IHBihc',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'type1': data[0],
    'type2': data[1],
    'type3': data[2],
    'type4': data[3],
    'type5': data[4],
    'type6': data[5],
    }
    return result

