
# Convert functions
CONVERT_COMMON_FUNCS = {
    'MDIL'  : lambda: get_MDIL_STR,
    'TDIL_B': lambda: get_TDIL_B_STR,
    'TDIL_J': lambda: get_TDIL_J_STR,
}
# format Strings
for fmt in ['04X', '05X', '05o', '08b', '016b']:
    CONVERT_COMMON_FUNCS[fmt] = (lambda f: lambda x: format(int(x), f))(fmt)


MDIL_ALPHABETS = 'ABCDEFGHIJKLMNPQ'
def get_MDIL_STR(num):
    if type(num) != int: return f"ErrorType({num}({type(num)})";
    if num > 65535: return f"ErrorNum({num})"
    if num == 127:
        return "QH"
    alpha, octet = divmod(num, 512)
    alpha1, alpha2 = divmod(alpha, 8)
    return f"{MDIL_ALPHABETS[alpha1]}{MDIL_ALPHABETS[alpha2]}{octet:03o}"

def get_TDIL_B_STR(num):
    if type(num) != int: return f"ErrorType({num}({type(num)})";
    if num > 4095: return f"ErrorNum({num})"
    return f"{num:04o}"

TDIL_J_ALPHABETS = '01234567ABCDEFGHJKLMNPQRSTUVWXYZ'
def get_TDIL_J_STR(num):
    if type(num) != int: return f"ErrorType({num}({type(num)})";
    if num > 524287: return f"ErrorNum({num})"

    alpha, octet = divmod(num, 512)
    alpha1, alpha2 = divmod(alpha, 32)
    return f"{TDIL_J_ALPHABETS[alpha1]}{TDIL_J_ALPHABETS[alpha2]}{octet:03o}"

if __name__ == "__main__":
    print(get_MDIL_STR(65535))
    print(get_TDIL_B_STR(4095))
    print(get_TDIL_J_STR(524287))