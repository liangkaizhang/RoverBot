import queue
import threading
from collections import defaultdict
import logging

class PubSub:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(PubSub, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self._queue = queue.Queue()
        self._topics_to_callbacks = defaultdict(list)
        self._should_run = True

    def publish(self, topic: str, msg):
        for callback in self._topics_to_callbacks[topic]:
            self._queue.put((callback, msg))

    def add_subscriber(self, topic: str, callback):
        self._topics_to_callbacks[topic].append(callback)

    def spin(self, num_threads=1):
        for _ in range(num_threads):
           thread = threading.Thread(target=self._worker_fn, daemon=True)
           thread.start()
    
    def stop(self):
        self._should_run = False

    def _worker_fn(self):
        while self._should_run:
            callback, msg = self._queue.get()
            self._queue.task_done()
            callback(msg)

