from base.node import Node
from base.pubsub import PubSub

class Graph:

    def __init__(self):
        self._nodes = []
        self._pubsub = PubSub()
        self._should_run = True
    
    def add_node(self, node: Node):
        self._nodes.append(node)

    def start(self):
        for node in self._nodes:
            node.start()
        self._pubsub.spin(num_threads=8)

    def stop(self):
        for node in self._nodes:
            node.stop()
        self._pubsub.stop()

    def spin(self):
        self.start()
        while self._should_run:
            pass

