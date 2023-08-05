import io


def bytes_to_int(file, byte_count):
    return int.from_bytes(file.read(byte_count), 'big')


def bytes_read_with_condition(file, condition: str):
    if condition == "array":
        return int.from_bytes(file.read(8), 'big')
    if condition == "string":
        return file.read(1).decode('utf-8')


def primitive_decoder(file_path):
    params = {}
    with open(file_path, 'rb') as file:
        name_lenght = bytes_to_int(file, 2)
        name = file.read(name_lenght)
        params['name'] = name
        wrapper = bytes_to_int(file, 1)
        params['wrapper'] = wrapper
        type = bytes_to_int(file, 1)
        params['type'] = type

        value = bytes_to_int(file, 4) #int32_t -> 4 bytes
        params['value'] = value

        size = bytes_to_int(file, 4) #int32_t -> 4 bytes
        params['size'] = size
    return params

def array_decoder(file_path, condition):
        params = {}
        with open(file_path, 'rb') as file:
            name_lenght = bytes_to_int(file, 2)
            name = file.read(name_lenght)
            params['name'] = name
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

            size = bytes_to_int(file, 4) #int32_t -> 4 bytes
            params['size'] = size
        return params

# print(primitive_decoder("int32.ttc"))
print(array_decoder("array.ttc", 'array'))
print(array_decoder("string.ttc", 'string'))