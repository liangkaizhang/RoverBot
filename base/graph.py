from base.node import Node
from base.pubsub import PubSub

class Graph:

    def __init__(self):
        self._nodes = []
        self._pubsub = PubSub()
    
    def add_node(self, node: Node):
        self._nodes.append(node)
    
    def spin(self):
        for node in self._nodes:
            node.start()
        self._pubsub.spin(num_threads=4)
        while True:
            pass

