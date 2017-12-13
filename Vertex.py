
import numpy as np

class Vertex(object):
    """
    Class representing a vertex of the graph.
    Vertices are distinguished by their names. Their state is used in
    the robots' decision making during exploration, and their weight
    is used to calculate rebalancing paths. Neighbors is the way we
    define adjacency and therefore create a graph with edges
    """

    def __init__(self, name):
        self.name = name
        self.state = 'red'
        self.weight = np.inf
        self.neighbors = []

    # def get_name(self):
    #     return self.name

    # def get_state(self):
    #     return self.state

    # def get_weight(self):
    #     return self.weight

    def set_weight(self, newWeight):
        self.weight = newWeight

    def set_state_not_visited(self):
        self.state = 'red'

    def set_state_incomplete(self):
        self.state = 'yellow'

    def set_state_complete(self):
        self.state = 'green'
