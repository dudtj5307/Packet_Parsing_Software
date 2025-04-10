# EIE_Msg.idl : f5ba4d014a5ab09f055c249cdf8bb7bdba05cec6d1eeec930f3f24ce12cd7e32
# Auto-generated parsing function

import struct

# Parse struct 'trkNo'
def parse_trkNo(endian, data):
    size = 20
    if len(data) != size:
        print(f'[parse_trkNo] Invalid data size: {len(data)} (20)')
        return None
    fmt  = ['>HHIIB3xi',
            '<HHIIB3xi',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'trkNo1': data[0],
    'trkNo2': data[1],
    'trkNo3': data[2],
    'trkNo4': data[3],
    'trkNo5': data[4],
    'trkNo6': data[5],
    }
    return result

# Parse struct 'EIE_0xD001'
def parse_EIE_0xD001(endian, data):
    size = 156
    if len(data) != size:
        print(f'[parse_EIE_0xD001] Invalid data size: {len(data)} (156)')
        return None
    fmt  = ['>38I4B',
            '<38I4B',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'type1': data[0:38],
    'type2': data[1:5],
    }
    return result

# Parse struct '_trkNo'
def parse__trkNo(endian, data):
    size = 20
    if len(data) != size:
        print(f'[parse__trkNo] Invalid data size: {len(data)} (20)')
        return None
    fmt  = ['>HHIIB3xi',
            '<HHIIB3xi',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'trkNo1': data[0],
    'trkNo2': data[1],
    'trkNo3': data[2],
    'trkNo4': data[3],
    'trkNo5': data[4],
    'trkNo6': data[5],
    }
    return result

# Parse struct 'EIE_header'
def parse_EIE_header(endian, data):
    size = 84
    if len(data) != size:
        print(f'[parse_EIE_header] Invalid data size: {len(data)} (84)')
        return None
    fmt  = ['>HHIIB3xiHHIIB3xiHHIIB3xiHHIIB3xiH2x',
            '<HHIIB3xiHHIIB3xiHHIIB3xiHHIIB3xiH2x',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'srcTN[0]': {
        'trkNo1': data[0],
        'trkNo2': data[1],
        'trkNo3': data[2],
        'trkNo4': data[3],
        'trkNo5': data[4],
        'trkNo6': data[5],
    },
    'srcTN[1]': {
        'trkNo1': data[6],
        'trkNo2': data[7],
        'trkNo3': data[8],
        'trkNo4': data[9],
        'trkNo5': data[10],
        'trkNo6': data[11],
    },
    'dstTN[0]': {
        'trkNo1': data[12],
        'trkNo2': data[13],
        'trkNo3': data[14],
        'trkNo4': data[15],
        'trkNo5': data[16],
        'trkNo6': data[17],
    },
    'dstTN[1]': {
        'trkNo1': data[18],
        'trkNo2': data[19],
        'trkNo3': data[20],
        'trkNo4': data[21],
        'trkNo5': data[22],
        'trkNo6': data[23],
    },
    'msgType': data[24],
    }
    return result

# Parse struct '_EIE_0xD001'
def parse__EIE_0xD001(endian, data):
    size = 156
    if len(data) != size:
        print(f'[parse__EIE_0xD001] Invalid data size: {len(data)} (156)')
        return None
    fmt  = ['>IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIBBBB',
            '<IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIBBBB',]
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
    'type2[0]': data[38],
    'type2[1]': data[39],
    'type2[2]': data[40],
    'type2[3]': data[41],
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
    size = 88
    if len(data) != size:
        print(f'[parse_EIE_0x0301] Invalid data size: {len(data)} (88)')
        return None
    fmt  = ['>HHIIB3xiHHIIB3xiHHIIB3xiHHIIB3xiHBxH2x',
            '<HHIIB3xiHHIIB3xiHHIIB3xiHHIIB3xiHBxH2x',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'header': {
        'srcTN[0]': {
            'trkNo1': data[0],
            'trkNo2': data[1],
            'trkNo3': data[2],
            'trkNo4': data[3],
            'trkNo5': data[4],
            'trkNo6': data[5],
        },
        'srcTN[1]': {
            'trkNo1': data[6],
            'trkNo2': data[7],
            'trkNo3': data[8],
            'trkNo4': data[9],
            'trkNo5': data[10],
            'trkNo6': data[11],
        },
        'dstTN[0]': {
            'trkNo1': data[12],
            'trkNo2': data[13],
            'trkNo3': data[14],
            'trkNo4': data[15],
            'trkNo5': data[16],
            'trkNo6': data[17],
        },
        'dstTN[1]': {
            'trkNo1': data[18],
            'trkNo2': data[19],
            'trkNo3': data[20],
            'trkNo4': data[21],
            'trkNo5': data[22],
            'trkNo6': data[23],
        },
        'msgType': data[24],
    },
    'type1': data[25],
    'type2': data[26],
    }
    return result

# Parse struct 'EIE_0x0302'
def parse_EIE_0x0302(endian, data):
    size = 100
    if len(data) != size:
        print(f'[parse_EIE_0x0302] Invalid data size: {len(data)} (100)')
        return None
    fmt  = ['>HHIIB3xiHHIIB3xiHHIIB3xiHHIIB3xiH2xIHBxihcx',
            '<HHIIB3xiHHIIB3xiHHIIB3xiHHIIB3xiH2xIHBxihcx',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'header': {
        'srcTN[0]': {
            'trkNo1': data[0],
            'trkNo2': data[1],
            'trkNo3': data[2],
            'trkNo4': data[3],
            'trkNo5': data[4],
            'trkNo6': data[5],
        },
        'srcTN[1]': {
            'trkNo1': data[6],
            'trkNo2': data[7],
            'trkNo3': data[8],
            'trkNo4': data[9],
            'trkNo5': data[10],
            'trkNo6': data[11],
        },
        'dstTN[0]': {
            'trkNo1': data[12],
            'trkNo2': data[13],
            'trkNo3': data[14],
            'trkNo4': data[15],
            'trkNo5': data[16],
            'trkNo6': data[17],
        },
        'dstTN[1]': {
            'trkNo1': data[18],
            'trkNo2': data[19],
            'trkNo3': data[20],
            'trkNo4': data[21],
            'trkNo5': data[22],
            'trkNo6': data[23],
        },
        'msgType': data[24],
    },
    'type1': data[25],
    'type2': data[26],
    'type3': data[27],
    'type4': data[28],
    'type5': data[29],
    'type6': data[30],
    }
    return result

# Parse struct 'strHeader'
def parse_strHeader(endian, data):
    size = 8
    if len(data) != size:
        print(f'[parse_strHeader] Invalid data size: {len(data)} (8)')
        return None
    fmt  = ['>HHBB2x',
            '<HHBB2x',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'type': data[0],
    'size': data[1],
    'id': data[2],
    'unit': data[3],
    }
    return result

# Parse struct 'trkNoSys'
def parse_trkNoSys(endian, data):
    size = 12
    if len(data) != size:
        print(f'[parse_trkNoSys] Invalid data size: {len(data)} (12)')
        return None
    fmt  = ['>HHHBBi',
            '<HHHBBi',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'trkNo': data[0],
    'trkNo_MDIL': data[1],
    'trkNo_TDIL_B': data[2],
    'trkNoMITS': data[3],
    'trkNoMFR': data[4],
    'trkNo_TDIL_J': data[5],
    }
    return result

# Parse struct 'EIE_0x70F3'
def parse_EIE_0x70F3(endian, data):
    size = 52
    if len(data) != size:
        print(f'[parse_EIE_0x70F3] Invalid data size: {len(data)} (52)')
        return None
    fmt  = ['>HHBBHccccccccccccccccccccccccccccccccccccccccc3x',
            '<HHBBHccccccccccccccccccccccccccccccccccccccccc3x',]
    data = struct.unpack(fmt[endian], data)
    result = {
    'header': {
        'type': data[0],
        'size': data[1],
        'id': data[2],
        'unit': data[3],
    },
    'statusId': data[4],
    'statusString[0]': data[5],
    'statusString[1]': data[6],
    'statusString[2]': data[7],
    'statusString[3]': data[8],
    'statusString[4]': data[9],
    'statusString[5]': data[10],
    'statusString[6]': data[11],
    'statusString[7]': data[12],
    'statusString[8]': data[13],
    'statusString[9]': data[14],
    'statusString[10]': data[15],
    'statusString[11]': data[16],
    'statusString[12]': data[17],
    'statusString[13]': data[18],
    'statusString[14]': data[19],
    'statusString[15]': data[20],
    'statusString[16]': data[21],
    'statusString[17]': data[22],
    'statusString[18]': data[23],
    'statusString[19]': data[24],
    'statusString[20]': data[25],
    'statusString[21]': data[26],
    'statusString[22]': data[27],
    'statusString[23]': data[28],
    'statusString[24]': data[29],
    'statusString[25]': data[30],
    'statusString[26]': data[31],
    'statusString[27]': data[32],
    'statusString[28]': data[33],
    'statusString[29]': data[34],
    'statusString[30]': data[35],
    'statusString[31]': data[36],
    'statusString[32]': data[37],
    'statusString[33]': data[38],
    'statusString[34]': data[39],
    'statusString[35]': data[40],
    'statusString[36]': data[41],
    'statusString[37]': data[42],
    'statusString[38]': data[43],
    'statusString[39]': data[44],
    'statusString[40]': data[45],
    }
    return result

