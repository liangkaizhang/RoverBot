import attr
from typing import Optional
from functools import reduce
import serial
import struct
import ctypes as ct


@attr.s(frozen=True, auto_attribs=True)
class ActuatorConfig:
    port: str
    baudrate: int = 115200
    reversed: bool = False
    speed_coeff: float = 1.0
    steer_coeff: float = 1.0


@attr.s(frozen=True, auto_attribs=True)
class ActuatorStatus:
    speed_right: int
    speed_left: int
    battery_voltage: float
    temperature: float

def CheckSum(data) -> int:
    return ct.c_uint16(reduce(lambda x, y: x ^ y, data)).value

class Actuator:

    def __init__(self, config: ActuatorConfig):
        self._serial = serial.Serial(config.port, config.baudrate, timeout=1)
        self._reversed = config.reversed
        self._start_frame = 0xabcd

    def write(self, speed: int, steer: int) -> bool:
        assert abs(speed) <= 1000, f"inputs speed {speed} is out of range -1000 ~ 1000."
        assert abs(steer) <= 1000, f"inputs steer {steer} is out of range -1000 ~ 1000."

        if self._reversed:
            speed = -speed

        speed = ct.c_int16(speed).value
        steer = ct.c_int16(steer).value
        checksum = CheckSum([self._start_frame, steer, speed])
        bytes = struct.pack('HhhH', self._start_frame, steer, speed, checksum)
        num_bytes = self._serial.write(bytes)
        return num_bytes == len(bytes)

    def read(self) -> Optional[ActuatorStatus]:
        data_frame = self._read_data_frame('H')
        if data_frame != self._start_frame:
            return None
        data = [self._start_frame]
        for _ in range(7):
            data.append(self._read_data_frame())
        checksum = self._read_data_frame('H')
        if checksum != CheckSum(data):
            return None
        status = ActuatorStatus(speed_right=-data[3],
                                speed_left=data[4],
                                battery_voltage=float(data[5]) / 100,
                                temperature=float(data[0] / 10))
        print(status)
        return status

        #return status
    def _read_data_frame(self, format='h'):
        bytes = self._serial.read(2)
        return struct.unpack(format, bytes)[0]


    def __del__(self):
        self._serial.close()