import re
import os
import mmap
import hashlib

import struct

from utils.monitor import ProgressMonitor
from utils.generator.ctype_map import KNOWN_CTYPE_MAP

STOPPED = False

# Regular Expressions
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
        if self.is_up_to_date(): return
        if self.parse_idl_structs() == STOPPED: return
        if self.generate_code()  == STOPPED: return

        self.outputs.append(self.output_name)

    def is_hash_same(self):
        with open(self.output_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        # Read stored hash-value from '{output_path}'
        if ':' in first_line:
            stored_name = first_line.split(':', 1)[0].strip()
            stored_hash = first_line.split(':', 1)[1].strip()
        else:
            print("No hash-value found : {output_path}")
            return False

        current_hash = calculate_hash(self.idl_path)
        return (self.idl_name == stored_name) and (current_hash == stored_hash)

    # Check if parse functions are up-to-date
    def is_up_to_date(self):
        if os.path.exists(self.output_path) and self.is_hash_same():
            print(f"[IDL] '{self.output_name}' up-to-date !")
            return True
        else:
            return False

    # Recursive fmt function for nested structure
    def get_fmt_recursive(self, struct_name):
        fmt = ""
        for ctype, field_name, comment, array_size in self.IDL_CTYPE_MAP.get(struct_name, []):
            if ctype in self.KNOWN_CTYPE_MAP:
                fmt += self.KNOWN_CTYPE_MAP[ctype] * array_size
            elif ctype in self.IDL_CTYPE_MAP:
                fmt += self.get_fmt_recursive(ctype) * array_size
            else:
                print(f"Warning: Struct({struct_name})-Field({field_name}) Unknown ctype: {ctype}")
        return fmt

    def get_dict_recursive(self, struct_name, indent, index):
        lines = []
        current_index = index
        for ctype, field_name, comment, array_size in self.IDL_CTYPE_MAP.get(struct_name, []):
            if ctype in self.KNOWN_CTYPE_MAP:
                for i in range(array_size):
                    key = f"{field_name}[{i}]" if array_size > 1 else field_name
                    lines.append(f"{indent}'{key}': data[{current_index}],")
                    current_index += 1
            elif ctype in self.IDL_CTYPE_MAP:
                for i in range(array_size):
                    nested_lines, next_index = self.get_dict_recursive(ctype, indent + "    ", current_index)
                    key = f"{field_name}[{i}]" if array_size > 1 else field_name
                    lines.append(f"{indent}'{key}': {{")
                    lines.extend(nested_lines)
                    lines.append(f"{indent}}},")
                    current_index = next_index
            else:
                lines.append(f"{indent}# Unknown type {ctype} for field {field_name}")
        return lines, current_index

    def parse_idl_structs(self):
        with open(self.idl_path, 'r') as f:
            content = f.read()
        # Parse all structs in IDL file
        typedef_matches = list(typedef_pattern.finditer(content))
        struct_matches = list(struct_pattern.finditer(content))         # TODO: check if memory is ok
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

            # Parse by each line
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

        # Recursive for Nested Structures
        fmt = self.get_fmt_recursive(struct_name)
        size = struct.calcsize(fmt)

        dict_lines, _ = self.get_dict_recursive(struct_name, "    ", 0)

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
        generated_code = f"# {self.idl_name} : {calculate_hash(self.idl_path)}\n"
        generated_code += f"# Auto-generated parsing function\n\n"
        generated_code += "import struct\n\n"
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

    class FAKEPARENT:
        def __init__(self):
            self.is_running = True

    eie_file_path = "../../IDL/EIE_Msg.idl"
    tie_file_path = "../../IDL/TIE_Msg.idl"

    parent = FAKEPARENT()

    code_generator = ParsingFunctionGenerator()
    code_generator.run(eie_file_path)
    code_generator.run(tie_file_path)
    print(code_generator.results)
