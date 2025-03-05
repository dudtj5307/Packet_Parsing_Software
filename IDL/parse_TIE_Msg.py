# Auto-generated parsing function

import struct

# Parse TIE_0x443 data
def parse_TIE_0x443(data):
    fmt = 'IHBihc'
    data = struct.unpack(fmt, data)
    result = {
    'type1': data[0],
    'type2': data[1],
    'type3': data[2],
    'type4': data[3],
    'type5': data[4],
    'type6': data[5],
    }
    return result

# Parse TIE_0x445 data
def parse_TIE_0x445(data):
    fmt = 'IHBihc'
    data = struct.unpack(fmt, data)
    result = {
    'type1': data[0],
    'type2': data[1],
    'type3': data[2],
    'type4': data[3],
    'type5': data[4],
    'type6': data[5],
    }
    return result

# Parse TIE_0x455 data
def parse_TIE_0x455(data):
    fmt = 'IHBihc'
    data = struct.unpack(fmt, data)
    result = {
    'type1': data[0],
    'type2': data[1],
    'type3': data[2],
    'type4': data[3],
    'type5': data[4],
    'type6': data[5],
    }
    return result

