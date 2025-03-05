# EIE_Msg.idl : 9ab22cfa90faa5047f39e8a33b3a2a2b1fb15a3d9ae04627460fc75b48c2c243
# Auto-generated parsing function

import struct

# Parse msgType data
def parse_msgType(data):
    size = 4
    if len(data) != size:
        return None
    fmt  = '>i'
    data = struct.unpack(fmt, data)
    result = {
    'a': data[0],
    }
    return result

# Parse trkNo data
def parse_trkNo(data):
    size = 16
    if len(data) != size:
        return None
    fmt  = '>iHHII'
    data = struct.unpack(fmt, data)
    result = {
    'type': {
        'a': data[0],
    },
    'trkNo1': data[1],
    'trkNo2': data[2],
    'trkNo3': data[3],
    'trkNo4': data[4],
    }
    return result

# Parse EIE_header data
def parse_EIE_header(data):
    size = 33
    if len(data) != size:
        return None
    fmt  = '>iHHIIiHHIIB'
    data = struct.unpack(fmt, data)
    result = {
    'srcTN': {
        'type': {
            'a': data[0],
        },
        'trkNo1': data[1],
        'trkNo2': data[2],
        'trkNo3': data[3],
        'trkNo4': data[4],
    },
    'dstTN': {
        'type': {
            'a': data[5],
        },
        'trkNo1': data[6],
        'trkNo2': data[7],
        'trkNo3': data[8],
        'trkNo4': data[9],
    },
    'msgType': data[10],
    }
    return result

# Parse EIE_0x301 data
def parse_EIE_0x301(data):
    size = 36
    if len(data) != size:
        return None
    fmt  = '>iHHIIiHHIIBBH'
    data = struct.unpack(fmt, data)
    result = {
    'header': {
        'srcTN': {
            'type': {
                'a': data[0],
            },
            'trkNo1': data[1],
            'trkNo2': data[2],
            'trkNo3': data[3],
            'trkNo4': data[4],
        },
        'dstTN': {
            'type': {
                'a': data[5],
            },
            'trkNo1': data[6],
            'trkNo2': data[7],
            'trkNo3': data[8],
            'trkNo4': data[9],
        },
        'msgType': data[10],
    },
    'type1': data[11],
    'type2': data[12],
    }
    return result

# Parse EIE_0x302 data
def parse_EIE_0x302(data):
    size = 51
    if len(data) != size:
        return None
    fmt  = '>iHHIIiHHIIBIHBihc'
    data = struct.unpack(fmt, data)
    result = {
    'header': {
        'srcTN': {
            'type': {
                'a': data[0],
            },
            'trkNo1': data[1],
            'trkNo2': data[2],
            'trkNo3': data[3],
            'trkNo4': data[4],
        },
        'dstTN': {
            'type': {
                'a': data[5],
            },
            'trkNo1': data[6],
            'trkNo2': data[7],
            'trkNo3': data[8],
            'trkNo4': data[9],
        },
        'msgType': data[10],
    },
    'type1': data[11],
    'type2': data[12],
    'type3': data[13],
    'type4': data[14],
    'type5': data[15],
    'type6': data[16],
    }
    return result

# Parse EIE_0x303 data
def parse_EIE_0x303(data):
    size = 51
    if len(data) != size:
        return None
    fmt  = '>iHHIIiHHIIBIHBihc'
    data = struct.unpack(fmt, data)
    result = {
    'header': {
        'srcTN': {
            'type': {
                'a': data[0],
            },
            'trkNo1': data[1],
            'trkNo2': data[2],
            'trkNo3': data[3],
            'trkNo4': data[4],
        },
        'dstTN': {
            'type': {
                'a': data[5],
            },
            'trkNo1': data[6],
            'trkNo2': data[7],
            'trkNo3': data[8],
            'trkNo4': data[9],
        },
        'msgType': data[10],
    },
    'type1': data[11],
    'type2': data[12],
    'type3': data[13],
    'type4': data[14],
    'type5': data[15],
    'type6': data[16],
    }
    return result

