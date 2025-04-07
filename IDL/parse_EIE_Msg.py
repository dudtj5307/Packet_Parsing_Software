# EIE_Msg.idl : 0671b934a4cfc7a32f86c1e3b3dbd697a339aba843c9fa32fe5ea1d7b73dc35f
# Auto-generated parsing function

import struct

# Parse struct 'trkNo'
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

# Parse struct '_trkNo'
def parse__trkNo(data):
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

# Parse struct 'EIE_header'
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

# Parse struct 'EIE_0x0301'
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

# Parse struct 'EIE_0x0302'
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

# Parse struct 'EIE_0x0303'
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

