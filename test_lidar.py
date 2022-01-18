from nodes.lidar_node import create_lidar_node
from nodes.lidar_plotter_node import create_lidar_plotter_node
from base.graph import Graph

import math
import numpy as np
import cv2

if __name__ == "__main__":
    graph = Graph()
    graph.add_node(create_lidar_node("lds-01"))
    plotter_node = create_lidar_plotter_node()
    graph.add_node(plotter_node)
    graph.start()

    # out = cv2.VideoWriter('lidar.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 10, (1080, 720))
    while True:
        plot = plotter_node.get_plot()
        cv2.imshow("lidar", plot)
        # out.write(plot)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            graph.stop()
            break

    # out.release()

 
        

