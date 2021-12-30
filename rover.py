import time
import threading

from drivers.actuator import ActuatorConfig, Actuator
from drivers.joystick import PS4Joystick

MAX_SPEED = 300

class RoverDriver:
    def __init__(self):
        config_front = ActuatorConfig(port="/dev/ttyTHS1", reversed=False)
        self._actuator_front = Actuator(config_front)
        config_rear = ActuatorConfig(port="/dev/ttyS1", reversed=True)
        self._actuator_rear = Actuator(config_rear)
        self._speed = 0
        self._steer = 0
        self._rate_hz = 10
        self._is_on = True
        self._thread = None

    def set_speed(self, speed):
        self._speed = speed
    
    def set_steer(self, steer):
        self._steer = steer
    
    def __runner__(self):
        while self._is_on:
            start_time = time.time()
            self._actuator_front.write(self._speed, self._steer)
            self._actuator_rear.write(self._speed, self._steer)
            sleep_time = 1.0 / self._rate_hz - (time.time() - start_time)
            if sleep_time > 0.0:
                time.sleep(sleep_time)
    
    def spin(self):
        self._thread = threading.Thread(target=self.__runner__, daemon=True)
        self._thread.start()

    def stop(self):
        self._is_on = False


if __name__ == "__main__":
    js = PS4Joystick()
    assert js.init() == True
    time.sleep(0.5)

    driver = RoverDriver()
    driver.spin()
    while True:
        button, button_state, axis, axis_val = js.poll()
        if axis == "left_stick_vert":
            print(f'{axis}: {axis_val}')
            speed = int(-MAX_SPEED * axis_val)
            driver.set_speed(speed)
        if axis == "right_stick_horz":
            print(f'{axis}: {axis_val}')
            steer = int(-MAX_SPEED * axis_val)
            driver.set_steer(steer)
