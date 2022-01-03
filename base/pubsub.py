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

    def publish(self, topic: str, msg):
        self._queue.put((topic, msg))

    def add_subscriber(self, topic: str, callback):
        self._topics_to_callbacks[topic].append(callback)

    def spin(self):
        while True:
            topic, msg = self._queue.get()
            self._queue.task_done()
            for callback in self._topics_to_callbacks[topic]:
                callback(msg)

