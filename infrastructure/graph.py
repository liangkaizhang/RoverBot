from infrastructure.node import Node
from infrastructure.pubsub import PubSub

class Graph:

    def __init__(self):
        self._nodes = []
        self._pubsub = PubSub()
    
    def add_node(self, node: Node):
        self._nodes.append(node)
    
    def spin(self):
        for node in self._nodes:
            node.start()
        self._pubsub.spin()

