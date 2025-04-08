# EIE_Msg.idl : a15b44cc93cb29e260ab1e78f188326f593b1ec52babf0eff4fc119599b9ab76
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
    size = 156
    if len(data) != size:
        print(f'[parse_EIE_0xD001] Invalid data size: {len(data)} (156)')
        return None
    fmt  = ['>IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII',
            '<IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'type1[0]': data[0],
    'type1[1]': data[1],
    'type1[2]': data[2],
    'type1[3]': data[3],
    'type1[4]': data[4],
    'type1[5]': data[5],
    'type1[6]': data[6],
    'type1[7]': data[7],
    'type1[8]': data[8],
    'type1[9]': data[9],
    'type1[10]': data[10],
    'type1[11]': data[11],
    'type1[12]': data[12],
    'type1[13]': data[13],
    'type1[14]': data[14],
    'type1[15]': data[15],
    'type1[16]': data[16],
    'type1[17]': data[17],
    'type1[18]': data[18],
    'type1[19]': data[19],
    'type1[20]': data[20],
    'type1[21]': data[21],
    'type1[22]': data[22],
    'type1[23]': data[23],
    'type1[24]': data[24],
    'type1[25]': data[25],
    'type1[26]': data[26],
    'type1[27]': data[27],
    'type1[28]': data[28],
    'type1[29]': data[29],
    'type1[30]': data[30],
    'type1[31]': data[31],
    'type1[32]': data[32],
    'type1[33]': data[33],
    'type1[34]': data[34],
    'type1[35]': data[35],
    'type1[36]': data[36],
    'type1[37]': data[37],
    'type1[38]': data[38],
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
    size = 50
    if len(data) != size:
        print(f'[parse_EIE_header] Invalid data size: {len(data)} (50)')
        return None
    fmt  = ['>HHIIHHIIHHIIHHIIH',
            '<HHIIHHIIHHIIHHIIH',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'srcTN[0]': {
        'trkNo1': data[0],
        'trkNo2': data[1],
        'trkNo3': data[2],
        'trkNo4': data[3],
    },
    'srcTN[1]': {
        'trkNo1': data[4],
        'trkNo2': data[5],
        'trkNo3': data[6],
        'trkNo4': data[7],
    },
    'dstTN[0]': {
        'trkNo1': data[8],
        'trkNo2': data[9],
        'trkNo3': data[10],
        'trkNo4': data[11],
    },
    'dstTN[1]': {
        'trkNo1': data[12],
        'trkNo2': data[13],
        'trkNo3': data[14],
        'trkNo4': data[15],
    },
    'msgType': data[16],
    }
    return result

# Parse struct '_EIE_0xD001'
def parse__EIE_0xD001(endian, data):
    size = 156
    if len(data) != size:
        print(f'[parse__EIE_0xD001] Invalid data size: {len(data)} (156)')
        return None
    fmt  = ['>IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII',
            '<IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'type1[0]': data[0],
    'type1[1]': data[1],
    'type1[2]': data[2],
    'type1[3]': data[3],
    'type1[4]': data[4],
    'type1[5]': data[5],
    'type1[6]': data[6],
    'type1[7]': data[7],
    'type1[8]': data[8],
    'type1[9]': data[9],
    'type1[10]': data[10],
    'type1[11]': data[11],
    'type1[12]': data[12],
    'type1[13]': data[13],
    'type1[14]': data[14],
    'type1[15]': data[15],
    'type1[16]': data[16],
    'type1[17]': data[17],
    'type1[18]': data[18],
    'type1[19]': data[19],
    'type1[20]': data[20],
    'type1[21]': data[21],
    'type1[22]': data[22],
    'type1[23]': data[23],
    'type1[24]': data[24],
    'type1[25]': data[25],
    'type1[26]': data[26],
    'type1[27]': data[27],
    'type1[28]': data[28],
    'type1[29]': data[29],
    'type1[30]': data[30],
    'type1[31]': data[31],
    'type1[32]': data[32],
    'type1[33]': data[33],
    'type1[34]': data[34],
    'type1[35]': data[35],
    'type1[36]': data[36],
    'type1[37]': data[37],
    'type1[38]': data[38],
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
    'type1[0]': data[0],
    'type1[1]': data[1],
    'type1[2]': data[2],
    'type1[3]': data[3],
    'type1[4]': data[4],
    'type2[0]': data[5],
    'type2[1]': data[6],
    'type2[2]': data[7],
    'type2[3]': data[8],
    'type2[4]': data[9],
    }
    return result

# Parse struct 'EIE_0x0301'
def parse_EIE_0x0301(endian, data):
    size = 53
    if len(data) != size:
        print(f'[parse_EIE_0x0301] Invalid data size: {len(data)} (53)')
        return None
    fmt  = ['>HHIIHHIIHHIIHHIIHBH',
            '<HHIIHHIIHHIIHHIIHBH',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'header': {
        'srcTN[0]': {
            'trkNo1': data[0],
            'trkNo2': data[1],
            'trkNo3': data[2],
            'trkNo4': data[3],
        },
        'srcTN[1]': {
            'trkNo1': data[4],
            'trkNo2': data[5],
            'trkNo3': data[6],
            'trkNo4': data[7],
        },
        'dstTN[0]': {
            'trkNo1': data[8],
            'trkNo2': data[9],
            'trkNo3': data[10],
            'trkNo4': data[11],
        },
        'dstTN[1]': {
            'trkNo1': data[12],
            'trkNo2': data[13],
            'trkNo3': data[14],
            'trkNo4': data[15],
        },
        'msgType': data[16],
    },
    'type1': data[17],
    'type2': data[18],
    }
    return result

# Parse struct 'EIE_0x0302'
def parse_EIE_0x0302(endian, data):
    size = 64
    if len(data) != size:
        print(f'[parse_EIE_0x0302] Invalid data size: {len(data)} (64)')
        return None
    fmt  = ['>HHIIHHIIHHIIHHIIHIHBihc',
            '<HHIIHHIIHHIIHHIIHIHBihc',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'header': {
        'srcTN[0]': {
            'trkNo1': data[0],
            'trkNo2': data[1],
            'trkNo3': data[2],
            'trkNo4': data[3],
        },
        'srcTN[1]': {
            'trkNo1': data[4],
            'trkNo2': data[5],
            'trkNo3': data[6],
            'trkNo4': data[7],
        },
        'dstTN[0]': {
            'trkNo1': data[8],
            'trkNo2': data[9],
            'trkNo3': data[10],
            'trkNo4': data[11],
        },
        'dstTN[1]': {
            'trkNo1': data[12],
            'trkNo2': data[13],
            'trkNo3': data[14],
            'trkNo4': data[15],
        },
        'msgType': data[16],
    },
    'type1': data[17],
    'type2': data[18],
    'type3': data[19],
    'type4': data[20],
    'type5': data[21],
    'type6': data[22],
    }
    return result

# Parse struct 'EIE_0x0303'
def parse_EIE_0x0303(endian, data):
    size = 64
    if len(data) != size:
        print(f'[parse_EIE_0x0303] Invalid data size: {len(data)} (64)')
        return None
    fmt  = ['>HHIIHHIIHHIIHHIIHIHBihc',
            '<HHIIHHIIHHIIHHIIHIHBihc',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'header': {
        'srcTN[0]': {
            'trkNo1': data[0],
            'trkNo2': data[1],
            'trkNo3': data[2],
            'trkNo4': data[3],
        },
        'srcTN[1]': {
            'trkNo1': data[4],
            'trkNo2': data[5],
            'trkNo3': data[6],
            'trkNo4': data[7],
        },
        'dstTN[0]': {
            'trkNo1': data[8],
            'trkNo2': data[9],
            'trkNo3': data[10],
            'trkNo4': data[11],
        },
        'dstTN[1]': {
            'trkNo1': data[12],
            'trkNo2': data[13],
            'trkNo3': data[14],
            'trkNo4': data[15],
        },
        'msgType': data[16],
    },
    'type1': data[17],
    'type2': data[18],
    'type3': data[19],
    'type4': data[20],
    'type5': data[21],
    'type6': data[22],
    }
    return result

