MDIL_ALPHABETS = 'ABCDEFGHIJKLMNPQ'
TDIL_J_ALPHABETS = '01234567ABCDEFGHJKLMNPQRSTUVWXYZ'

def get_string_self(num):
    return str(num)

def get_string_FMT_04X(num):
    return format(int(num), '04X')

def get_string_FMT_05X(num):
    return format(int(num), '05X')

def get_string_FMT_05o(num):
    return format(int(num), '05o')

def get_string_FMT_08b(num):
    return format(int(num), '08b')

def get_string_FMT_016b(num):
    return format(int(num), '016b')

def get_string_MDIL(num):
    if type(num) != int: return f"ErrorType({num}({type(num)})";
    if num > 65535: return f"ErrorNum({num})"
    if num == 127:
        return "QH"
    alpha, octet = divmod(num, 512)
    alpha1, alpha2 = divmod(alpha, 8)
    return f"{MDIL_ALPHABETS[alpha1]}{MDIL_ALPHABETS[alpha2]}{octet:03o}"

def get_string_TDIL_B(num):
    if type(num) != int: return f"ErrorType({num}({type(num)})";
    if num > 4095: return f"ErrorNum({num})"
    return f"{num:04o}"

def get_string_TDIL_J(num):
    if type(num) != int: return f"ErrorType({num}({type(num)})";
    if num > 524287: return f"ErrorNum({num})"

    alpha, octet = divmod(num, 512)
    alpha1, alpha2 = divmod(alpha, 32)
    return f"{TDIL_J_ALPHABETS[alpha1]}{TDIL_J_ALPHABETS[alpha2]}{octet:03o}"

# TN_TYPE Values
MDIL   = 4
TDIL_B = 5
TDIL_J = 6

# Convert functions
CONVERT_TN_FUNCS = {'MDIL'  : get_string_MDIL,   MDIL  : get_string_MDIL,
                    'TDIL_B': get_string_TDIL_B, TDIL_B: get_string_TDIL_B,
                    'TDIL_J': get_string_TDIL_J, TDIL_J: get_string_TDIL_J,}

# Returns string of func name (used in generator)
CONVERT_TN_FUNCS_STR = {'MDIL'  : "get_string_MDIL",
                        'TDIL_B': "get_string_TDIL_B",
                        'TDIL_J': "get_string_TDIL_J",}

# format strings
for fmt in ['04X', '05X', '05o', '08b', '016b']:
    CONVERT_TN_FUNCS[fmt] = (lambda f: lambda x: format(int(x), f))(fmt)
    CONVERT_TN_FUNCS_STR[fmt] = f"get_string_FMT_{fmt}"


if __name__ == "__main__":
    print(get_string_MDIL('65535'))
    print(get_string_TDIL_B(4095))
    print(get_string_TDIL_J(524287))