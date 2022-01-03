import attr

from drivers.actuator import ActuatorConfig, Actuator
from base.node import Node
from base.pubsub import PubSub

SPEED_LIMIT = 800


@attr.s(frozen=True, auto_attribs=True)
class ActuatorNodeConfig:
    actuator_config: ActuatorConfig
    rate_hz: float = 10
    name: str = None


class ActuatorNode(Node):

    def __init__(self, config: ActuatorNodeConfig):
        super().__init__(name=config.name, rate_hz=config.rate_hz)
        self._actuator = Actuator(config.actuator_config)
        # Driving params.
        self._speed = 0
        self._steer = 0
        self._max_speed = 350
        self._max_steer = 350
        # Setup pubsub.
        pubsub = PubSub()
        pubsub.add_subscriber("/speed", self.set_speed)
        pubsub.add_subscriber("/steer", self.set_steer)
    
    def _run_once(self):
        self._actuator.write(self._speed, self._steer)

    def set_speed(self, speed: float):
        self._speed = int(self._max_speed * speed)
    
    def set_steer(self, steer: float):
        self._steer = int(self._max_steer * steer)

    def set_max_speed(self, max_speed):
        self._max_speed = min(SPEED_LIMIT, max_speed)

    def set_max_steer(self, max_steer):
        self._max_steer = min(SPEED_LIMIT, max_steer)


_FRONT_ACTUATOR_CONFIG = ActuatorNodeConfig(
    ActuatorConfig(port="/dev/ttyTHS1", reversed=False),
    name="front_actuator")


_REAR_ACTUATOR_CONFIG = ActuatorNodeConfig(
    ActuatorConfig(port="/dev/ttyS1", reversed=True),
    name="rear_actuator")


def create_actuator_node(name: str) -> Node:
    if name == "front":
        return ActuatorNode(_FRONT_ACTUATOR_CONFIG)
    elif name == "rear":
        return ActuatorNode(_REAR_ACTUATOR_CONFIG)
    else:
        raise NameError('Actuator not exist.')