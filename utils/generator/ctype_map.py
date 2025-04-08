# C data type map
KNOWN_CTYPE_MAP = {
    'char' : 'c',   'signed char' : 'c',
    'int8' : 'c',   'INT8' : 'c',

    'uchar' : 'B',  'unsigned char' : 'B',
    'uint8' : 'B',  'UINT8' : 'B',
    'octet' : 'B',

    'short' : 'h',  'signed short' : 'h',
    'int16' : 'h',  'INT16' : 'h',

    'ushort' : 'H', 'unsigned short' : 'H',
    'uint16' : 'H', 'UINT16' : 'H',

    'long' : 'i',   'signed long': 'i',
    'int'  : 'i',   'signed int' : 'i',
    'int32': 'i',   'INT32': 'i',

    'uint'  : 'I',  'unsigned int' : 'I',
    'ulong' : 'I',  'unsigned long': 'I',
    'uint32': 'I',  'UINT32' : 'I',

    'float'  : 'f', 'FLOAT': 'f',
    'float32': 'f', 'FLOAT32': 'f',

    'double' : 'd', 'DOUBLE': 'd',
    'float64': 'd', 'FLOAT64': 'd',
}