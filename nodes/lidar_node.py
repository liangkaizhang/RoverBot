from drivers.lidar import LidarConfig, Lidar
from base.node import Node
from base.pubsub import PubSub

class LidarNode(Node):

    def __init__(self):
        super().__init__(name="lidar")
        self._lidar = Lidar(LidarConfig())
        assert self._lidar.start() == True

    def _run_once(self):
        data_frames = self._lidar.read()
        pubsub = PubSub()
        for df in data_frames:
            pubsub.publish("/lidar", df)
    
    def __del__(self):
        self._lidar.stop()


def create_lidar_node(name: str) -> Node:
    if name == "lds-01":
        return LidarNode()
    else:
        raise NameError('Actuator not exist.')