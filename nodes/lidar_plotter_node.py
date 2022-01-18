import math
from pickletools import uint8
import numpy as np
import cv2

from threading import Lock

from base.node import Node
from base.pubsub import PubSub

mutex = Lock()

class LidarPlotterNode(Node):

    def __init__(self, width=720, height=1080):
        super().__init__(name="lidar_plotter")
        self._data = [None] * 360
        self._height = height
        self._width = width
        self._scale = 0.3
        self._offset_x = 0
        self._offset_y = -100
        # Setup pubsub.
        pubsub = PubSub()
        pubsub.add_subscriber("/lidar", self.update)

    def _run_once(self):
        mutex.acquire()
        self._canvas = np.zeros((self._height, self._width, 3), dtype=np.uint8)
        for data in self._data:
            if not data:
                continue
            x, y, intensity = data
            xc = int(self._width * 0.5) + self._offset_x
            yc = int(self._height * 0.5) + self._offset_y
            xs = int(x * self._scale + self._width * 0.5) + self._offset_x
            ys = int(y * self._scale + self._height * 0.5) + self._offset_y
            ic = int(intensity * 255 / 2000)
            self._canvas = cv2.line(self._canvas, (xc, yc),  (xs, ys), (255, 0, 0), 1)
            self._canvas = cv2.circle(self._canvas, (xs, ys), 2, (0, 0, ic), -1)
        mutex.release()

    def update(self, data_frame):
        if 0 <= data_frame.angle < 360:
            self._data[data_frame.angle] = self._convert(data_frame)

    def _convert(self, data_frame):
        x = data_frame.range_m * math.sin(math.radians(data_frame.angle))
        y = data_frame.range_m * math.cos(math.radians(data_frame.angle))
        return x, y, data_frame.intensity

    def get_plot(self):
        return self._canvas


def create_lidar_plotter_node() -> Node:
    return LidarPlotterNode()