import re

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

ctype_info = {
    'c': (1, 1),
    'B': (1, 1),
    'h': (2, 2),
    'H': (2, 2),
    'i': (4, 4),
    'I': (4, 4),
    'f': (4, 4),
    'd': (8, 8),
}

def get_padding_size(offset, alignment):
    return (alignment - (offset % alignment)) % alignment


def add_fmt_padding(fmt):
    # Regular Expression : 'num' + 'letter'
    ctypes = re.findall(r'(\d*)([cBhHiIfd])', fmt)

    new_fmt = ""
    offset = 0
    for count_str, ctype in ctypes:
        count = int(count_str) if count_str else 1
        size, alignment = ctype_info[ctype]
        # Add padding
        # pad = get_padding_size(offset, alignment)
        if pad := get_padding_size(offset, alignment):
            new_fmt += (f"{pad}x" if pad > 1 else "x")
            offset += pad

        # Add origin fmt
        new_fmt += f"{count_str}{ctype}"
        offset += size * count

    # TODO: How to do last padding
    max_alignment = 0
    for _, ctype in ctypes:
        max_alignment = max(max_alignment, ctype_info[ctype][1])
    if max_alignment:
        if last_pad := get_padding_size(offset, max_alignment) :
            new_fmt += (f"{last_pad}x" if last_pad > 1 else "x")
            offset += last_pad

    return new_fmt

if __name__ == "__main__":
    import struct

    orig_fmt = "HHIIBid"
    new_fmt = add_fmt_padding(orig_fmt)

    orig_size = struct.calcsize(orig_fmt)
    new_size = struct.calcsize(new_fmt)

    print("Origin fmt :", orig_fmt, orig_size)
    print("Padded fmt :", new_fmt, new_size)