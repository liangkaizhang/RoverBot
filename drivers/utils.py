from functools import reduce
import ctypes as ct


def check_sum(data) -> int:
    return ct.c_uint16(reduce(lambda x, y: x ^ y, data)).value