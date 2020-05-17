from typing import Generic, List, TypeVar
import struct

T = TypeVar("T")
INT_MAX = (1 << 31) - 1
INT_MIN = -1 << 31
ENCODING = "utf-8"


def raise_(ex):
    raise ex


size_dict = {
    int: 4,
    bool: 1,
    float: 4,
    "str_length": 8,
}
# find a way to set default size for int
pack_dict = {
    int: (
        lambda obj: struct.pack("i", obj)
    ),  # if INT_MIN <= obj <= INT_MAX else pack("q", obj)),
    bool: (lambda obj: struct.pack("?", obj)),
    float: (lambda obj: struct.pack("f", obj)),
    bytes: (lambda obj: struct.pack("q{}s".format(len(obj)), len(obj), obj)),
    str: (
        lambda obj: struct.pack("q{}s".format(len(obj)), len(obj), obj.encode(ENCODING))
    ),
    list: (lambda obj: b"".join([pack(x) for x in vars(obj)])),
    set: (lambda obj: raise_(NotImplementedError)),
    dict: (lambda obj: raise_(NotImplementedError)),
    tuple: (lambda obj: raise_(NotImplementedError)),
}

unpack_dict = {
    int: (
        lambda _, data: (
            struct.unpack("i", data[: size_dict[int]])[0],
            data[size_dict[int]:],
        )
    ),
    bool: (
        lambda _, data: (
            struct.unpack("?", data[: size_dict[bool]])[0],
            data[size_dict[bool]:],
        )
    ),
    float: (
        lambda _, data: (
            struct.unpack("f", data[: size_dict[float]])[0],
            data[size_dict[float]:],
        )
    ),
    bytes: (lambda _, data: unpack_bytes(data)),
    str: (lambda _, data: unpack_string(data)),
    list: (lambda obj, _: raise_(NotImplementedError)),
    set: (lambda obj, _: raise_(NotImplementedError)),
    dict: (lambda obj, _: raise_(NotImplementedError)),
    tuple: (lambda obj, _: raise_(NotImplementedError)),
}


def unpack_string(data: bytes):
    result, data = unpack_bytes(data)
    return result.decode(ENCODING), data


def unpack_bytes(data: bytes):
    length = struct.unpack("q", data[: size_dict["str_length"]])[0]
    data = data[size_dict["str_length"]:]
    return struct.unpack("{}s".format(length), data[:length])[0], data[length:]


def pack(obj: T) -> bytes:
    return pack_dict.get(
        type(obj), lambda o: b"".join([pack(o.__getattribute__(x)) for x in vars(o)])
    )(obj)


def _unpack(data: bytes, obj: T) -> (T, bytes):
    if type(obj) in unpack_dict:
        return unpack_dict[type(obj)](obj, data)
    else:
        for v in vars(obj):
            (result, data) = unpack(data, obj.__getattribute__(v))
            obj.__dict__[v] = result
    return obj, data


def unpack(data: bytes, obj: T) -> (T, bytes):
    return _unpack(data, obj)[0]
