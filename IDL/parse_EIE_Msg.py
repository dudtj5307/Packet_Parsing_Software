# EIE_Msg.idl : a9e813579c10d0aada95dd2524c9888c45f48c7e0ae4914aff82dc2438d02318

import struct

# Parse msgType data
def parse_msgType(data):
    fmt = 'i'
    data = struct.unpack(fmt, data)
    result = {
    'a': data[0],
    }
    return result

# Parse trkNo data
def parse_trkNo(data):
    fmt = 'iHHII'
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
    fmt = 'iHHIIiHHIIB'
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
    fmt = 'iHHIIiHHIIBIHBihc'
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

# Parse EIE_0x302 data
def parse_EIE_0x302(data):
    fmt = 'iHHIIiHHIIBIHBihc'
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
    fmt = 'iHHIIiHHIIBIHBihc'
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

