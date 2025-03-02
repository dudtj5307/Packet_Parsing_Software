import re
import os
import mmap
import hashlib

# C 타입과 Python struct 모듈 포맷 코드 매핑 (필요에 따라 추가)
KNOWN_TYPE_MAP = {
    'char'          : 'c',
    'uchar'         : 'B',
    'unsigned char' : 'B',

    'short'          : 'h',
    'ushort'         : 'H',
    'unsigned short' : 'H',

    'int'   : 'i',
    'uint'  : 'I',
    'unsigned int' : 'I',
}

# struct 정의: 'struct <구조체이름> { ... }'
struct_pattern = re.compile(r'struct\s+(\w+)\s*\{([^}]+)}', re.MULTILINE | re.DOTALL)
# 필드 패턴: ex) "uchar valid,       // 100~200"
field_pattern = re.compile(r'\s*(\w+)\s+(\w+)\s*(?:;?\s*(//.*))?')


def calculate_hash(filepath, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        # 파일 전체를 메모리 매핑 (파일 크기가 매우 클 경우 메모리 사용량에 주의)
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            hash_func.update(mm)
    return hash_func.hexdigest()


class IDL_CODE_GENERATION():
    def __init__(self):
        self.idl_path = ""
        self.idl_name = ""

        self.output_path = ""
        self.output_name = ""

        # Saving all the structs
        self.KNOWN_TYPE_MAP = KNOWN_TYPE_MAP
        self.IDL_TYPE_MAP   = {}

    def idl_changed(self):
        with open(self.output_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        # Read stored hash-value from '{output_path}'
        if ':' in first_line:
            stored_hash = first_line.split(':', 1)[1].strip()
        else:
            print("No hash-value found : {output_path}")
            return True
        # Calculate current hash-value from '{idl_path}'
        current_hash = calculate_hash(self.idl_path)
        return stored_hash != current_hash

    def parse_idl_file(self):
        with open(self.idl_path, 'r') as f:
            content = f.read()
        # Parse all structs in IDL file
        for struct_match in struct_pattern.finditer(content):
            struct_name = struct_match.group(1)
            struct_body = struct_match.group(2)
            fields = []
            # 각 줄마다 필드 파싱 (빈 줄은 건너뜀)
            for line in struct_body.splitlines():
                line = line.strip()
                if not line:
                    continue
                # 끝에 붙은 콤마 제거
                line = line.rstrip(',')
                field_match = field_pattern.match(line)
                if field_match:
                    ctype = field_match.group(1)
                    field_name = field_match.group(2)
                    comment = field_match.group(3) if field_match.group(3) else ""
                    fields.append((ctype, field_name, comment))

            self.IDL_TYPE_MAP[struct_name] = fields

    # Recursive fmt function for nested structure
    def get_fmt_recursive(self, struct_name):
        fields = self.IDL_TYPE_MAP.get(struct_name, [])
        fmt = ""
        for ctype, field_name, comment in fields:
            if ctype in self.KNOWN_TYPE_MAP:
                fmt += self.KNOWN_TYPE_MAP[ctype]
            elif ctype in self.IDL_TYPE_MAP:
                fmt += self.get_fmt_recursive(ctype)     # Recursive
            else:
                print(f"Warning: Struct({struct_name})-Field({field_name}) Unknown type: {ctype}")
        return fmt

    def get_dict_recursive(self, struct_name, indent, index):
        lines = []
        current_index = index
        for ctype, field_name, comment in self.IDL_TYPE_MAP[struct_name]:
            if ctype in self.KNOWN_TYPE_MAP:
                lines.append(f"{indent}'{field_name}': data[{current_index}],")
                current_index += 1
            elif ctype in self.IDL_TYPE_MAP:
                nested_lines, next_index = self.get_dict_recursive(ctype, indent + "    ", current_index)
                lines.append(f"{indent}'{field_name}': {{")
                lines.extend(nested_lines)
                lines.append(f"{indent}}},")
                current_index = next_index
            else:
                lines.append(f"{indent}# Unknown type {ctype} for field {field_name}")
        return lines, current_index

    def generate_parse_function(self, struct_name):
        # # Annotation
        # fields = self.IDL_TYPE_MAP.get(struct_name, [])
        # range_comments = {name: comment.strip() for ctype, name, comment in fields if comment}

        # Recursive for Nested Structures
        fmt = self.get_fmt_recursive(struct_name)
        dict_lines, _ = self.get_dict_recursive(struct_name, "    ", 0)

        func_lines = list()
        func_lines.append(f"# Parse {struct_name} data")
        func_lines.append(f"def parse_{struct_name}(data):")
        func_lines.append(f"    fmt = '{fmt}'")
        func_lines.append("    data = struct.unpack(fmt, data)")
        func_lines.append("    result = {")
        func_lines.extend(dict_lines)
        func_lines.append("    }")
        func_lines.append("    return result")
        return "\n".join(func_lines)

    def generate_code(self):
        generated_code = f"# {self.idl_name} : {calculate_hash(self.idl_path)}\n\n"
        generated_code += "import struct\n\n"
        # Auto-generate code by struct name
        for struct_name in self.IDL_TYPE_MAP:
            generated_code += self.generate_parse_function(struct_name) + "\n\n"

        with open(self.output_path, 'w') as f:
            f.write(generated_code)
        print(f"* Auto-Generated : {self.output_name}")

    def set(self, idl_path):
        # IDL path for parsing & code generation
        self.idl_path = idl_path

        # Output path
        idl_folder, self.idl_name = os.path.split(idl_path)
        self.output_name = f"parse_{self.idl_name.split('.')[0]}.py"
        self.output_path = os.path.join(idl_folder, self.output_name)
        self.IDL_TYPE_MAP = {}

    def run(self):
        # Check if auto-generated code is up-to-date
        if os.path.exists(self.output_path) and not self.idl_changed():
            print(f"* Already Exists : {self.output_name}")
            # return    # To Be Restored

        self.parse_idl_file()
        self.generate_code()

    def reset(self):
        self.__init__()


if __name__ == '__main__':
    idl_file_path = "EIE_Msg.idl"  # 분석할 IDL 파일 이름

    code_generator = IDL_CODE_GENERATION()
    code_generator.set(idl_file_path)
    code_generator.run()
