import time

from drivers.actuator import ActuatorConfig, Actuator

SPEED = 400
STEER = 0
RATE_HZ = 10

if __name__ == "__main__":
    config = ActuatorConfig(port="/dev/cu.usbserial-A6017TPZ", reversed=False)
    actuator = Actuator(config)
    while True:
        start_time = time.time()
        actuator.write(SPEED, STEER)
        actuator.read()
        sleep_time = 1.0 / RATE_HZ - (time.time() - start_time)
        if sleep_time > 0.0:
            time.sleep(sleep_time)
        
