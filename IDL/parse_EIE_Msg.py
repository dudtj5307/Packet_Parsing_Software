# EIE_Msg.idl : 94b053f3c4e75b9b66760ec41c83bacf5499926853c5afbdd2feb720d322bbc5
# Auto-generated parsing function

import struct

# Parse trkNo data
def parse_trkNo(data):
    size = 12
    if len(data) != size:
        print(f'data: {len(data)} / size: 12')
        return None
    fmt  = '>HHII'
    data = struct.unpack(fmt, data)
    result = {
    'trkNo1': data[0],
    'trkNo2': data[1],
    'trkNo3': data[2],
    'trkNo4': data[3],
    }
    return result

# Parse EIE_header data
def parse_EIE_header(data):
    size = 26
    if len(data) != size:
        print(f'data: {len(data)} / size: 26')
        return None
    fmt  = '>HHIIHHIIH'
    data = struct.unpack(fmt, data)
    result = {
    'srcTN': {
        'trkNo1': data[0],
        'trkNo2': data[1],
        'trkNo3': data[2],
        'trkNo4': data[3],
    },
    'dstTN': {
        'trkNo1': data[4],
        'trkNo2': data[5],
        'trkNo3': data[6],
        'trkNo4': data[7],
    },
    'msgType': data[8],
    }
    return result

# Parse EIE_0x0301 data
def parse_EIE_0x0301(data):
    size = 29
    if len(data) != size:
        print(f'data: {len(data)} / size: 29')
        return None
    fmt  = '>HHIIHHIIHBH'
    data = struct.unpack(fmt, data)
    result = {
    'header': {
        'srcTN': {
            'trkNo1': data[0],
            'trkNo2': data[1],
            'trkNo3': data[2],
            'trkNo4': data[3],
        },
        'dstTN': {
            'trkNo1': data[4],
            'trkNo2': data[5],
            'trkNo3': data[6],
            'trkNo4': data[7],
        },
        'msgType': data[8],
    },
    'type1': data[9],
    'type2': data[10],
    }
    return result

# Parse EIE_0x0302 data
def parse_EIE_0x0302(data):
    size = 40
    if len(data) != size:
        print(f'data: {len(data)} / size: 40')
        return None
    fmt  = '>HHIIHHIIHIHBihc'
    data = struct.unpack(fmt, data)
    result = {
    'header': {
        'srcTN': {
            'trkNo1': data[0],
            'trkNo2': data[1],
            'trkNo3': data[2],
            'trkNo4': data[3],
        },
        'dstTN': {
            'trkNo1': data[4],
            'trkNo2': data[5],
            'trkNo3': data[6],
            'trkNo4': data[7],
        },
        'msgType': data[8],
    },
    'type1': data[9],
    'type2': data[10],
    'type3': data[11],
    'type4': data[12],
    'type5': data[13],
    'type6': data[14],
    }
    return result

# Parse EIE_0x0303 data
def parse_EIE_0x0303(data):
    size = 40
    if len(data) != size:
        print(f'data: {len(data)} / size: 40')
        return None
    fmt  = '>HHIIHHIIHIHBihc'
    data = struct.unpack(fmt, data)
    result = {
    'header': {
        'srcTN': {
            'trkNo1': data[0],
            'trkNo2': data[1],
            'trkNo3': data[2],
            'trkNo4': data[3],
        },
        'dstTN': {
            'trkNo1': data[4],
            'trkNo2': data[5],
            'trkNo3': data[6],
            'trkNo4': data[7],
        },
        'msgType': data[8],
    },
    'type1': data[9],
    'type2': data[10],
    'type3': data[11],
    'type4': data[12],
    'type5': data[13],
    'type6': data[14],
    }
    return result

