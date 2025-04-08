# TIE_Msg.idl : 63658ddf41ed6fe9a75ab3bf92864d52f912166281e5cf6ee2a1acfcc3cd16c3
# Auto-generated parsing function

import struct

# Parse struct 'TIE_HEADER'
def parse_TIE_HEADER(endian, data):
    size = 6
    if len(data) != size:
        print(f'[parse_TIE_HEADER] Invalid data size: {len(data)} (6)')
        return None
    fmt  = ['>BBHBB',
            '<BBHBB',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'MESSAGE_LEVEL': data[0],
    'MESSAGE_SUBLEVEL': data[1],
    'MESSAGE_LENGTH': data[2],
    'ORIGINATOR': data[3],
    'SEQUENCE_NUMBER': data[4],
    }
    return result

# Parse struct '_TIE_HEADER'
def parse__TIE_HEADER(endian, data):
    size = 6
    if len(data) != size:
        print(f'[parse__TIE_HEADER] Invalid data size: {len(data)} (6)')
        return None
    fmt  = ['>BBHBB',
            '<BBHBB',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'MESSAGE_LEVEL': data[0],
    'MESSAGE_SUBLEVEL': data[1],
    'MESSAGE_LENGTH': data[2],
    'ORIGINATOR': data[3],
    'SEQUENCE_NUMBER': data[4],
    }
    return result

# Parse struct 'IEM_SYS_005'
def parse_IEM_SYS_005(endian, data):
    size = 8
    if len(data) != size:
        print(f'[parse_IEM_SYS_005] Invalid data size: {len(data)} (8)')
        return None
    fmt  = ['>BBHBBH',
            '<BBHBBH',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'HEADER_FRAME': {
        'MESSAGE_LEVEL': data[0],
        'MESSAGE_SUBLEVEL': data[1],
        'MESSAGE_LENGTH': data[2],
        'ORIGINATOR': data[3],
        'SEQUENCE_NUMBER': data[4],
    },
    'CBIT_RESULT': data[5],
    }
    return result

