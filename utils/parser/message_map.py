from collections import defaultdict

# TIE Label Map
TIE_LABEL_NAME = {
    0 : 'SYS',      '0' : 'SYS',
    1 : 'SURV',     '1' : 'SURV',
    2 : 'EW',       '2' : 'EW',
    3 : 'CMD',      '3' : 'CMD',
    4 : 'INFO',     '4' : 'INFO',
    5 : 'EXT',      '5' : 'EXT',
    6 : 'FILT',     '6' : 'FILT',
    7 : 'INTELLI',  '7' : 'INTELLI',
    8 : 'PTXT',     '8' : 'PTXT',
    9 : 'MISC',     '9' : 'MISC',
    11: 'TEST',     '11': 'TEST',
}

MDIL_ALPHABETS = 'ABCDEFGHIJKLMNPQ'
def get_MDIL_STR(num):
    if type(num) != int: return f"ErrorType({num}({type(num)})";
    if num > 65535: return f"ErrorNum({num})"
    if num == 127:
        return "QH"
    alpha, octet = divmod(num, 512)
    alpha1, alpha2 = divmod(alpha, 8)
    return f"{MDIL_ALPHABETS[alpha1]}{MDIL_ALPHABETS[alpha2]}{octet:03o}"

def get_TDILB_STR(num):
    if type(num) != int: return f"ErrorType({num}({type(num)})";
    if num > 4095: return f"ErrorNum({num})"
    return f"{num:04o}"

TDILJ_ALPHABETS = '01234567ABCDEFGHJKLMNPQRSTUVWXYZ'
def get_TDILJ_STR(num):
    if type(num) != int: return f"ErrorType({num}({type(num)})";
    if num > 524287: return f"ErrorNum({num})"

    alpha, octet = divmod(num, 512)
    alpha1, alpha2 = divmod(alpha, 32)
    return f"{TDILJ_ALPHABETS[alpha1]}{TDILJ_ALPHABETS[alpha2]}{octet:03o}"

if __name__ == "__main__":
    print(get_MDIL_STR(65535))
    print(get_TDILB_STR(4095))
    print(get_TDILJ_STR(524287))


# if __name__ == '__main__':
#     for label in range(0, 12):
#         if label == 10: continue
#         for sublabel in range(1, 16):
#             tie_name = f'IEM_{TIE_LABEL_NAME[label]}_{label:X}{sublabel:02}'
#             print(tie_name)