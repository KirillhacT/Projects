import pprint

file_path = "./Main.class"

CONSTANT_Class = 7
CONSTANT_Fieldref = 9
CONSTANT_Methodref = 10
CONSTANT_InterfaceMethodref = 11
CONSTANT_String = 8
CONSTANT_Integer = 3
CONSTANT_Float = 4
CONSTANT_Long = 5
CONSTANT_Double = 6
CONSTANT_NameAndType = 12
CONSTANT_Utf8 = 1
CONSTANT_MethodHandle = 15
CONSTANT_MethodType = 16
CONSTANT_InvokeDynamic = 18

def parse_u1(f): return int.from_bytes(f.read(1), "big")
def parse_u2(f): return int.from_bytes(f.read(2), "big")
def parse_u4(f): return int.from_bytes(f.read(4), "big")
def parse_uN(f, n): return int.from_bytes(f.read(n), "big")

pp = pprint.PrettyPrinter(indent=4)
#Байты в java коде хранятся в big endian

with open(file_path, "rb") as f:
    clazz = {}
    clazz['magic'] = hex(parse_u4(f))
    clazz['minor'] = parse_u2(f)
    clazz['major'] = parse_u2(f)
    constant_pool_count = parse_u2(f)
    constant_pool = []
    for i in range(constant_pool_count-1):
        cp_info = {}
        tag = parse_u1(f)
        if tag == CONSTANT_Methodref:
            cp_info['tag'] = 'CONSTANT_Methodref'
            cp_info['class_index'] = parse_u2(f)
            cp_info['name_and_type_index'] = parse_u2(f)
        elif tag == CONSTANT_Class:
            cp_info['tag'] = 'CONSTANT_Class'
            cp_info['name_index'] = parse_u2(f)
        elif tag == CONSTANT_NameAndType:
            cp_info['tag'] = 'CONSTANT_NameAndType'
            cp_info['name_index'] = parse_u2(f)
            cp_info['descriptor_index'] = parse_u2(f)
        elif tag == CONSTANT_Utf8:
            cp_info['tag'] = 'CONSTANT_Utf8'
            length = parse_u2(f)
            cp_info['bytes'] = f.read(length)
        elif tag == CONSTANT_Fieldref:
            cp_info['tag'] = 'CONSTANT_Fieldref'
            cp_info['class_index'] = parse_u2(f)
            cp_info['name_and_type_index'] = parse_u2(f)
        elif tag == CONSTANT_String:
            cp_info['tag'] = 'CONSTANT_String'
            cp_info['string_index'] = parse_u2(f)
        else:
            raise NotImplementedError(f"Unexpected constant tag {tag} in class file {file_path}")
        constant_pool.append(cp_info)
    clazz['constant_pool'] = constant_pool

print("-------------------------------")
for cp_info in clazz["constant_pool"]:
    if cp_info["tag"] == "CONSTANT_Class":
        index = clazz["constant_pool"][cp_info["name_index"] - 1]
        print(index)
    # print(cp_info)
        
    
