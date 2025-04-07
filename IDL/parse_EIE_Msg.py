# EIE_Msg.idl : 923337d440921b4e447f4272e9b190304a19c2f6ad7353105f361b0642403a24
# Auto-generated parsing function

import struct

# Parse struct 'trkNo'
def parse_trkNo(endian, data):
    size = 12
    if len(data) != size:
        print(f'[parse_trkNo] Invalid data size: {len(data)} (12)')
        return None
    fmt  = ['>HHII',
            '<HHII',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'trkNo1': data[0],
    'trkNo2': data[1],
    'trkNo3': data[2],
    'trkNo4': data[3],
    }
    return result

# Parse struct 'EIE_0xD001'
def parse_EIE_0xD001(endian, data):
    size = 4
    if len(data) != size:
        print(f'[parse_EIE_0xD001] Invalid data size: {len(data)} (4)')
        return None
    fmt  = ['>I',
            '<I',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'type1': data[0],
    }
    return result

# Parse struct '_trkNo'
def parse__trkNo(endian, data):
    size = 12
    if len(data) != size:
        print(f'[parse__trkNo] Invalid data size: {len(data)} (12)')
        return None
    fmt  = ['>HHII',
            '<HHII',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'trkNo1': data[0],
    'trkNo2': data[1],
    'trkNo3': data[2],
    'trkNo4': data[3],
    }
    return result

# Parse struct 'EIE_header'
def parse_EIE_header(endian, data):
    size = 26
    if len(data) != size:
        print(f'[parse_EIE_header] Invalid data size: {len(data)} (26)')
        return None
    fmt  = ['>HHIIHHIIH',
            '<HHIIHHIIH',]
    data = struct.unpack(fmt[endian], data)
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

# Parse struct '_EIE_0xD001'
def parse__EIE_0xD001(endian, data):
    size = 4
    if len(data) != size:
        print(f'[parse__EIE_0xD001] Invalid data size: {len(data)} (4)')
        return None
    fmt  = ['>I',
            '<I',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'type1': data[0],
    }
    return result

# Parse struct 'EIE_0xD010'
def parse_EIE_0xD010(endian, data):
    size = 20
    if len(data) != size:
        print(f'[parse_EIE_0xD010] Invalid data size: {len(data)} (20)')
        return None
    fmt  = ['>HHHHHHHHHH',
            '<HHHHHHHHHH',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'type1': data[0],
    'type2': data[1],
    'type3': data[2],
    'type4': data[3],
    'type5': data[4],
    'type6': data[5],
    'type7': data[6],
    'type8': data[7],
    'type9': data[8],
    'type10': data[9],
    }
    return result

# Parse struct 'EIE_0x0301'
def parse_EIE_0x0301(endian, data):
    size = 29
    if len(data) != size:
        print(f'[parse_EIE_0x0301] Invalid data size: {len(data)} (29)')
        return None
    fmt  = ['>HHIIHHIIHBH',
            '<HHIIHHIIHBH',]
    data = struct.unpack(fmt[endian], data)
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
def parse_EIE_0x0302(endian, data):
    size = 40
    if len(data) != size:
        print(f'[parse_EIE_0x0302] Invalid data size: {len(data)} (40)')
        return None
    fmt  = ['>HHIIHHIIHIHBihc',
            '<HHIIHHIIHIHBihc',]
    data = struct.unpack(fmt[endian], data)
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
def parse_EIE_0x0303(endian, data):
    size = 40
    if len(data) != size:
        print(f'[parse_EIE_0x0303] Invalid data size: {len(data)} (40)')
        return None
    fmt  = ['>HHIIHHIIHIHBihc',
            '<HHIIHHIIHIHBihc',]
    data = struct.unpack(fmt[endian], data)
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

