from Vertex import *
import numpy as np
import random

class Grid(object):

    def __init__(self):
        self.list_of_vertices = []


class CompleteGraph(Grid):

    def __init__(self, num):
        super(CompleteGraph, self).__init__()

        self.list_of_vertices = [Vertex(name='v'+str(i)) for i in range(num)]

        for i in range(len(self.list_of_vertices)):
                self.list_of_vertices[i].neighbors = self.list_of_vertices[0:i] + self.list_of_vertices[i+1::]


class RandomGraph(Grid):
    def __init__(self, num):
        super().__init__()

        self.list_of_vertices = [Vertex(name='v'+str(i)) for i in range(num)]
        for i in range(len(self.list_of_vertices)):
            self.list_of_vertices[i].neighbors = []
        self.generate_connections()

    def generate_connections(self):
        def get_max_connections(num):
            if not num == 1:
                return num - 1 + get_max_connections(num-1)
            else:
                return 0

        def generate_random_connection():
           loc1 = np.random.choice(self.list_of_vertices)
           loc2 = np.random.choice(self.list_of_vertices)

           if not self.does_connection_exist(loc1, loc2) and not loc1 == loc2:
               return loc1, loc2
           else:
               return generate_random_connection()

        min_connections = 2*len(self.list_of_vertices) - 5
        max_connections = get_max_connections(len(self.list_of_vertices))

        num_of_connections = random.randint(min_connections, max_connections)

        for i in range(num_of_connections):
            loc1, loc2 = generate_random_connection()
            loc1.neighbors.append(loc2)
            loc2.neighbors.append(loc1)


    def does_connection_exist(self, loc1, loc2):
        return loc2 in loc1.neighbors
