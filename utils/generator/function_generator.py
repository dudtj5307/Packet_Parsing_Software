import re
import os
import mmap
import hashlib

import struct

from utils.monitor import ProgressMonitor
from utils.idl_config import IDL_Config
from utils.generator.ctype_map import KNOWN_CTYPE_MAP, add_fmt_padding
from utils.convert_functions import CONVERT_TN_FUNCS_STR

STOPPED = False

# Regular Expressions
comment_del_pattern = re.compile(r'/\*[\s\S]*?\*/|^\s*//.*$', re.MULTILINE)
typedef_pattern = re.compile(r'typedef\s+struct\s+(\w+)?\s*\{([\s\S]*?)\}\s*(\w+)\s*;', re.MULTILINE)   # 'typedef struct'
struct_pattern = re.compile(r'struct\s+(\w+)\s*\{([^}]+)}', re.MULTILINE | re.DOTALL)  # 'struct <name> { ... }'
# field_pattern = re.compile(r'\s*((?:\w+\s+)*\w+)\s+(\w+)\s*(?:;?\s*(//.*))?')
field_pattern = re.compile(r'\s*((?:\w+\s+)*\w+)\s+(\w+)(\s*\[\s*(\d+)\s*\])?\s*;?\s*(//.*)?')


def calculate_hash(filepath, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        # 파일 전체를 메모리 매핑 (파일 크기가 매우 클 경우 메모리 사용량에 주의)
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            hash_func.update(mm)
    return hash_func.hexdigest()

class ParsingFunctionGenerator:
    def __init__(self):
        self.monitor = ProgressMonitor()
        self.idl_path, self.output_path = "", ""
        self.idl_name, self.output_name = "", ""
        self.KNOWN_CTYPE_MAP = KNOWN_CTYPE_MAP        #  OS defined structs
        self.IDL_CTYPE_MAP   = {}                    # IDL defined structs
        self.outputs = []

        self.idl_config = IDL_Config()
        self.IDL_STRING = self.idl_config.get('string')
        self.IDL_GROUP = self.idl_config.get('group')
        self.IDL_CONVERT = self.idl_config.get('struct_convert')

    def set_path(self, idl_path):
        # Initialize
        self.idl_path, self.output_path = "", ""
        self.idl_name, self.output_name = "", ""
        self.IDL_CTYPE_MAP = {}
        # IDL path for parsing & code generation
        self.idl_path = idl_path
        # IDL filename --> Function filename
        idl_folder, self.idl_name = os.path.split(idl_path)
        self.output_name = f"parse_{self.idl_name.split('.')[0]}.py"
        self.output_path = os.path.join(idl_folder, self.output_name)

    def reset(self):
        self.idl_path, self.output_path = "", ""
        self.idl_name, self.output_name = "", ""
        self.IDL_CTYPE_MAP = {}

    def run(self, idl_path):
        # Reset attributes before running
        self.set_path(idl_path)
        # if self.is_up_to_date(): return   # TODO: disable update skipping
        if self.find_idl_structs() == STOPPED: return
        if self.generate_code()  == STOPPED: return

        self.outputs.append(self.output_name)
        print(f"[IDL] '{self.output_name}' generated !")

    def is_hash_same(self):
        with open(self.output_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        try:
            # Read stored hash-value from '{output_path}'
            stored_name = first_line.split(':', 1)[0].strip().split(' ')[1]
            stored_hash = first_line.split(':', 1)[1].strip()
            current_hash = calculate_hash(self.idl_path)
            # Compare file name & hash value
            return (self.idl_name == stored_name) and (current_hash == stored_hash)
        except:
            return False

    # Check if parse functions are up-to-date
    def is_up_to_date(self):
        if os.path.exists(self.output_path) and self.is_hash_same():
            print(f"[IDL] '{self.output_name}' up-to-date !")
            self.outputs.append(self.output_name)
            return True
        else:
            return False

    def parse_struct_recursive(self, struct_name, indent="", current_index=0):
        fmt = ""
        lines = []
        string_fields = self.IDL_STRING.get(struct_name, [])
        group_fields = self.IDL_GROUP.get(struct_name, [])
        convert_fields = self.IDL_CONVERT.get(struct_name, [])
        for ctype, field_name, comment, array_size in self.IDL_CTYPE_MAP.get(struct_name, []):
            if ctype in self.KNOWN_CTYPE_MAP:
                # ['string'] fields
                if field_name in string_fields and array_size >= 1:
                    fmt += f'{array_size}s'
                    lines.append(f"{indent}'{field_name}': data[{current_index}].decode('ascii', errors='replace'),")   # TODO: check if ascii is correct
                    current_index += 1
                # ['group'] fields
                elif field_name in group_fields and array_size >= 1:
                    fmt += f'{array_size}{self.KNOWN_CTYPE_MAP[ctype]}'
                    lines.append(f"{indent}'{field_name}': data[{current_index}:{current_index+array_size}],")
                    current_index += array_size
                else:
                    fmt += self.KNOWN_CTYPE_MAP[ctype] * array_size
                    for i in range(array_size):
                        key = f'{field_name}[{i}]' if array_size > 1 else field_name
                        # ['struct_convert'] fields
                        data = f"{CONVERT_TN_FUNCS_STR[convert_fields[field_name]]}(data[{current_index}])" \
                                if field_name in convert_fields else f"data[{current_index}]"
                        lines.append(f"{indent}'{key}': {data},")
                        current_index += 1

            elif ctype in self.IDL_CTYPE_MAP:
                for i in range(array_size):
                    nested_fmt, nested_lines, next_index = self.parse_struct_recursive(ctype, indent+"    ", current_index)
                    fmt += nested_fmt
                    key = f"{field_name}[{i}]" if array_size > 1 else field_name
                    lines.append(f"{indent}'{key}': {{")
                    lines.extend(nested_lines)
                    lines.append(f"{indent}}},")
                    current_index = next_index
            else:
                print(f"[Generator] Struct({struct_name})-Field({field_name}) Unknown ctype: {ctype}")
                lines.append(f"{indent}# Unknown type {ctype} for field {field_name}")

        return fmt, lines, current_index

    def find_idl_structs(self):
        with open(self.idl_path, 'r') as f:
            content = f.read()
        # Parse all structs in IDL file
        content = comment_del_pattern.sub('', content)              # Clean useless comments
        typedef_matches = list(typedef_pattern.finditer(content))   # Find typedef structs  (C style)
        struct_matches = list(struct_pattern.finditer(content))     # Find   all   structs  (C++ style)
        total_structs = typedef_matches + struct_matches

        for idx, struct_match in enumerate(total_structs):
            if self.monitor.update_check_stop('idl', task_idx=idx, task_total=len(total_structs) * 2):
                return STOPPED

            # 'struct' or 'typedef struct'
            if struct_match.re == struct_pattern:
                struct_name = struct_match.group(1)     # struct name
            else:
                struct_name = struct_match.group(3)     # typedef struct name
            struct_body = struct_match.group(2)

            # parse by each line
            fields = []
            for line in struct_body.splitlines():
                line = line.strip()
                if not line:
                    continue
                line = line.rstrip(',')
                field_match = field_pattern.match(line)
                if field_match:
                    ctype, field_name = field_match.group(1), field_match.group(2)
                    comment = field_match.group(3).strip() if field_match.group(3) else ""
                    array_size = int(field_match.group(4)) if field_match.group(4) else 1
                    fields.append((ctype, field_name, comment, array_size))
            self.IDL_CTYPE_MAP[struct_name] = fields
        return True

    def generate_parse_function(self, struct_name):
        # # Comments
        # fields = self.IDL_TYPE_MAP.get(struct_name, [])
        # range_comments = {name: comment.strip() for ctype, name, comment in fields if comment}

        # Get 'fmt' & 'dict_line' recursively (for nested struct)
        fmt, dict_lines, _ = self.parse_struct_recursive(struct_name, "    ")
        fmt = add_fmt_padding(fmt)      # Add padding
        size = struct.calcsize(fmt)

        func_lines = list()
        func_lines.append(f"# Parse struct '{struct_name}'")
        func_lines.append(f"def parse_{struct_name}(endian, data):")
        func_lines.append(f"    size = {size}")
        func_lines.append(f"    if len(data) != size:")
        func_lines.append(f"        print(f\'[parse_{struct_name}] Invalid data size: {{len(data)}} ({size})')")
        func_lines.append(f"        return None")
        func_lines.append(f"    fmt  = ['>{fmt}',")                    # > : Big Endian / < : Little Endian
        func_lines.append(f"            '<{fmt}',]")
        func_lines.append("    data = struct.unpack(fmt[endian], data)")
        func_lines.append("    result = {")
        func_lines.extend(dict_lines)
        func_lines.append("    }")
        func_lines.append("    return result")
        return "\n".join(func_lines)

    def generate_code(self):
        generated_code  = f"# {self.idl_name} : {calculate_hash(self.idl_path)}\n"
        generated_code += f"# Auto-generated parsing function\n\n"
        generated_code += "import struct\n"
        generated_code += "from utils.convert_functions import *\n\n"
        # Auto-generate code by struct name
        for idx, struct_name in enumerate(self.IDL_CTYPE_MAP):
            # Update monitoring and Check if Stopped
            if self.monitor.update_check_stop('idl', task_idx=idx, task_total=len(self.IDL_CTYPE_MAP), prior_status=0.5):
                return STOPPED

            generated_code += self.generate_parse_function(struct_name) + "\n\n"

        with open(self.output_path, 'w') as f:
            f.write(generated_code)
        # print(f"[IDL] '{self.output_name}' auto-generated !")
        return True


if __name__ == '__main__':
    comment_re = re.compile(r'/\*[\s\S]*?\*/|^\s*//.*$', re.MULTILINE)

    # 예시: 원본 C 코드
    code = """
    // typedef struct Foo {      // 이 entire struct는 주석!
    typedef struct Foo {
        int a;       //
        // float b;  // 이 필드는 주석
        char name[32];
    } Foo;
    """

    # 2) 주석 제거
    code_clean = comment_re.sub('', code)
    print(code_clean)
