import io
import pprint

pp = pprint.PrettyPrinter()

def bytes_to_int(file, byte_count):
    return int.from_bytes(file.read(byte_count), 'big')


def bytes_read_with_condition(file, condition: str):
    if condition == "array":
        return int.from_bytes(file.read(8), 'big')
    if condition == "string":
        return file.read(1).decode('utf-8')

def decoder(file_path) -> dict:
    params = {}
    with open(file_path, 'rb') as file:
        name = _read_name(file)
        params["name"] = name
        if b'Test' in name:
            _object_parser(file, params)
        elif name == b'string':
            _array_parsing(file, params, 'string')
        elif name == b'array':
            _array_parsing(file, params, 'array')
        else:
            _primitive_parsing(file, params)
        return params


def _read_name(file) -> bytes:
    name_lenght = bytes_to_int(file, 2)
    name = file.read(name_lenght)
    return name

def _primitive_parsing(file, params: dict) -> None:
    wrapper = bytes_to_int(file, 1)
    params['wrapper'] = wrapper
    type = bytes_to_int(file, 1)
    params['type'] = type

    value = bytes_to_int(file, 4) #int32_t -> 4 bytes
    params['value'] = value

    size = bytes_to_int(file, 4) #int32_t -> 4 bytes
    params['size'] = size


def _array_parsing(file, params: dict, condition: str) -> None:
    wrapper = bytes_to_int(file, 1)
    params['wrapper'] = wrapper
    type = bytes_to_int(file, 1)
    params['type'] = type

    count = bytes_to_int(file, 4)
    array = []
    for i in range(count):
        element = bytes_read_with_condition(file, condition)
        array.append(element)
    params['value'] = array if condition == 'array' else "".join(array)

    size = bytes_to_int(file, 4)
    params['size'] = size


def _object_parser(file, params: dict) -> None:
    wrapper = bytes_to_int(file, 1)
    params['wrapper'] = wrapper
    count = bytes_to_int(file, 2)
    attr_object = []
    for i in range(count):
        attr_params = {}
        attr_name = _read_name(file)
        attr_params["name"] = attr_name
        print(attr_name)
        if attr_name == b"string":
            _array_parsing(file, attr_params, "string")
        elif attr_name == b"array":
            _array_parsing(file, attr_params, "array")
        elif b'Test' in attr_name: #временно
            _object_parser(file, attr_params)
        else:
            _primitive_parsing(file, attr_params)
        attr_object.append(attr_params)
    params["attributes"] = attr_object
    size = bytes_to_int(file, 4)
    params['size'] = size



# print(decoder("int32.ttc"))
# print(decoder("array.ttc"))
# print(decoder("string.ttc"))
pp.pprint(decoder('Test1.ttc'))