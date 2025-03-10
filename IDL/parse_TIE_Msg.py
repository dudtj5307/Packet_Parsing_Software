# TIE_Msg.idl : 1b809091394987652a0c645a88e0003aa4e3bf09f927ce98980808af06d05b3d
# Auto-generated parsing function

import struct

# Parse TIE_0x443 data
def parse_TIE_0x443(data):
    size = 15
    if len(data) != size:
        return None
    fmt  = '>IHBihc'
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
    size = 15
    if len(data) != size:
        return None
    fmt  = '>IHBihc'
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
    size = 15
    if len(data) != size:
        return None
    fmt  = '>IHBihc'
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

