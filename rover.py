
from infrastructure.graph import Graph
from nodes.actuator_node import create_actuator_node
from nodes.joystick_node import create_joystick_node

if __name__ == "__main__":
    graph = Graph()
    graph.add_node(create_joystick_node("ps4"))
    graph.add_node(create_actuator_node("front"))
    graph.add_node(create_actuator_node("rear"))
    graph.spin()