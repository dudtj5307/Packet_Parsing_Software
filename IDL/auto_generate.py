import re
import os
import mmap
import hashlib

# C 타입과 Python struct 모듈 포맷 코드 매핑 (필요에 따라 추가)
TYPE_MAPPING = {
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


def calculate_hash(filepath, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        # 파일 전체를 메모리 매핑 (파일 크기가 매우 클 경우 메모리 사용량에 주의)
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            hash_func.update(mm)
    return hash_func.hexdigest()


def idl_changed(idl_path, output_path):
    with open(output_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()

    # Read hash-value from the First Line
    if ':' in first_line:
        stored_hash = first_line.split(':', 1)[1].strip()
    else:
        print("No hash-value found : {output_path}")
        return True

    # 현재 IDL 파일의 해시 값 계산
    current_hash = calculate_hash(idl_path)

    return stored_hash != current_hash


def generate_parse_function(struct_name, fields):
    """ fields: [(ctype, field_name, comment), ...] """

    # 각 필드의 타입을 매핑하여 struct 포맷 문자열 생성
    fmt = ''.join([TYPE_MAPPING.get(ctype, '') for ctype, _, _ in fields])
    # 주석은 별도로 저장할 수 있도록 dict 형태로도 추출 (여기서는 출력하지 않음)
    # range_comments = {name: comment.strip() for ctype, name, comment in fields if comment}

    func_lines = list()
    func_lines.append(f"# Parse {struct_name} packet")
    func_lines.append(f"def parse_{struct_name}(packet):")
    func_lines.append(f"    fmt = '{fmt}'")
    func_lines.append("    data = struct.unpack(fmt, packet)")
    func_lines.append("    result = {")
    for idx, (_, field_name, comment) in enumerate(fields):
        if comment: comment = f"    # {comment.split('//')[1].strip()}"
        func_lines.append(f"        '{field_name}' : data[{idx}],{comment}")
    func_lines.append("    }")
    func_lines.append("    return result")
    return "\n".join(func_lines)


def generate_from_idl(idl_path):
    # Output path
    idl_folder, idl_name = os.path.split(idl_path)
    base, _ = os.path.splitext(idl_name)
    new_file_name = f"parse_{base}.py"
    output_path = os.path.join(idl_folder, new_file_name)

    if os.path.exists(output_path):
        if not idl_changed(idl_path, output_path):
            print(f"* Already Exists : {new_file_name}")
            # return

    # Read IDL file
    with open(idl_path, 'r') as f:
        content = f.read()

    # struct 정의: 'struct <구조체이름> { ... }'
    struct_pattern = re.compile(r'struct\s+(\w+)\s*\{([^}]+)\}', re.MULTILINE | re.DOTALL)
    # 필드 패턴: ex) "uchar valid,       // 100~200"
    field_pattern = re.compile(r'\s*(\w+)\s+(\w+)\s*(?:,?\s*(//.*))?')

    generated_code = f"# {idl_name} : {calculate_hash(idl_path)}\n\n"
    generated_code += "import struct\n\n"

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

        # 구조체 하나당 파싱 함수 생성
        func_code = generate_parse_function(struct_name, fields)
        generated_code += func_code + "\n\n"

    with open(output_path, 'w') as f:
        f.write(generated_code)

    print(f"* Auto-Generated : {new_file_name}")


if __name__ == '__main__':
    idl_file_path = "EIE_Msg.idl"  # 분석할 IDL 파일 이름
    generate_from_idl(idl_file_path)