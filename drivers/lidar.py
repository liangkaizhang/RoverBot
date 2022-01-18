import attr
from typing import Optional
import serial
import time

from drivers.utils import check_sum


@attr.s(frozen=True, auto_attribs=True)
class LidarConfig:
    port: str = "/dev/ttyUSB0"
    baudrate: int = 230400


@attr.s(auto_attribs=True)
class LidarDataFrame:
    angle: float
    rpm: float
    intensity: float
    range_m: float


class Lidar:

    def __init__(self, config: LidarConfig):
        self._serial = serial.Serial(config.port, config.baudrate, timeout=1)
        self._start_frame = 0xFA
        self.stop()
        time.sleep(0.2)

    def start(self) -> bool:
        num_bytes = self._serial.write(b'b')
        return bool(num_bytes)

    def stop(self) -> bool:
        num_bytes = self._serial.write(b'e')
        return bool(num_bytes)

    def read(self) -> Optional[LidarDataFrame]:
        bytes = self._serial.read()
        while (not bytes) or (bytes[0] != 0xfa):
            bytes = self._serial.read()

        bytes = self._serial.read(41)
        base_angle = (bytes[0] - 160) * 6
        rpm = bytes[2] * 256 + bytes[1]
        for offset in range(6):
            angle = base_angle + offset
            intensity = bytes[6 * offset + 4] * 256 + bytes[6 * offset + 3]
            range_m = bytes[6 * offset + 6] * 256 + bytes[6 * offset + 5]
            yield LidarDataFrame(angle, rpm, intensity, range_m)


    def __del__(self):
        self.stop()
        self._serial.close()