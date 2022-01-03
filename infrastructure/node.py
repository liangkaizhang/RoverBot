from threading import Thread
import time

class Node(Thread):

    def __init__(self, name=None, rate_hz=None, daemon=False) -> None:
        super().__init__()
        self.name = name
        self.rate_hz = rate_hz
        self.daemon = daemon
        self.should_run = True

    def run(self):
        while self.should_run:
            start_time = time.time()
            self._run_once()
            if self.rate_hz:
                sleep_time = 1.0 / self.rate_hz - (time.time() - start_time)
                if sleep_time > 0.0:
                    time.sleep(sleep_time)

    def stop(self):
        self.should_run = False

    def _run_once(self):
        return NotImplemented
