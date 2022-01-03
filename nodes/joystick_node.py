import attr
import time

from drivers.joystick import PS4Joystick
from infrastructure.node import Node
from infrastructure.pubsub import PubSub

def _speed_handler(value: float) -> float:
    return -value

def _steer_handler(value: float) -> float:
    return -value

_AXIS_TO_TOPICS = {"left_stick_vert": ("/speed", _speed_handler),
                   "right_stick_horz": ("/steer", _steer_handler),
                   }

class Ps4JoystickNode(Node):

    def __init__(self):
        super().__init__(name="joystick")
        self._joystick = PS4Joystick()
        assert self._joystick.init() == True
        time.sleep(0.5)

    def _run_once(self):
        button, button_state, axis, axis_val = self._joystick.poll()
        pubsub = PubSub()
        if axis in _AXIS_TO_TOPICS:
            topic, handler = _AXIS_TO_TOPICS[axis]
            pubsub.publish(topic, handler(axis_val))



def create_joystick_node(name: str) -> Node:
    if name == "ps4":
        return Ps4JoystickNode()
    else:
        raise NameError('Actuator not exist.')

    