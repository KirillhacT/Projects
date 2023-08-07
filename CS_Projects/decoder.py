import io
import pprint

string_arr = [b'sysName']
primitive_arr = [b'desc', b'index', b'active', b'ID', b'dType', b'keyCode', b'pressed', b'released']
obj_res = b'Event:'

hashed = {
    1: 1, #int8_t
    2: 2, #int16_t
    3: 4, #int32_t
    4: 8, #int64_t 
    11: 1, #bool
}


pp = pprint.PrettyPrinter()

def bytes_to_int(file, byte_count):
    return int.from_bytes(file.read(byte_count), 'big')


def bytes_read_with_condition(file, condition: str):
    if condition == "string":
        return file.read(1).decode('utf-8')
    assert False, "Not implemented"

def _primitive_parsing(file, params: dict) -> None:
    wrapper = bytes_to_int(file, 1)
    params['wrapper'] = wrapper
    type = bytes_to_int(file, 1)
    params['type'] = type   
    value = bytes_to_int(file, hashed[type])
    params['value'] = value

    size = bytes_to_int(file, 4)
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
    params['value'] = "".join(array) if condition == "string" else None
    size = bytes_to_int(file, 4)
    params['size'] = size

def _event_parser(file, params) -> dict:
    wrapper = bytes_to_int(file, 1)
    params['wrapper'] = wrapper
    count = bytes_to_int(file, 2)
    attr_object = []
    for i in range(count):
        attr_params = {}
        attr_name = _read_name(file)
        attr_params["name"] = attr_name
        if attr_name in string_arr:
            _array_parsing(file, attr_params, "string")
        elif attr_name in primitive_arr:
            _primitive_parsing(file, attr_params)
        else:
            _event_parser(file, attr_params)
        attr_object.append(attr_params)
    params["attributes"] = attr_object
    size = bytes_to_int(file, 4)
    params['size'] = size
    return params
    
def _read_name(file) -> bytes:
    name_lenght = bytes_to_int(file, 2)
    name = file.read(name_lenght)
    return name     


with open('Sysinfo.ttc', 'rb') as file:
    params = {}
    system_name_lenght = bytes_to_int(file, 2)
    system_name = file.read(system_name_lenght)
    params['system_name'] = system_name
    params = _event_parser(file, params)
    pp.pprint(params)