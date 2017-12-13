from Vertex import *
import numpy as np
import random
from math import floor, ceil, sqrt
import copy as copy

class Grid(object):
    '''
    Object meant to represent the graph that robots travel on.
    Contains a list of vertices
    '''
    def __init__(self):
        self.list_of_vertices = []


class CompleteGraph(Grid):

    def __init__(self, num):
        super(CompleteGraph, self).__init__()

        self.list_of_vertices = [Vertex(name='v'+str(i)) for i in range(num)]

        for i in range(len(self.list_of_vertices)):
                self.list_of_vertices[i].neighbors = self.list_of_vertices[0:i] + self.list_of_vertices[i+1::]


class RandomGraph(Grid):
    def __init__(self, num, sparseness = .5):
        # sparseness ranges from 0 to 1, with .5 being an average graph
        super(RandomGraph, self).__init__()

        self.list_of_vertices = [Vertex(name='v'+str(i)) for i in range(num)]
        for i in range(len(self.list_of_vertices)):
            self.list_of_vertices[i].neighbors = []

        self.generate_connections(sparseness)

    def generate_connections(self, sparseness):
        def get_max_connections(num):
            if not num == 1:
                return num - 1 + get_max_connections(num-1)
            else:
                return 0

        def generate_random_connection():
           loc1 = np.random.choice(self.list_of_vertices)
           loc2 = np.random.choice(self.list_of_vertices)

           if not loc1 in loc2.neighbors and not loc1 == loc2:
               return loc1, loc2
           else:
               return generate_random_connection()

        def initialize_graph_connections():
          vertices = copy.copy(self.list_of_vertices)
          choice1 = np.random.choice(vertices)
          chosen_vertices = [choice1]
          for i in range(len(self.list_of_vertices)-1):
            unconnected_vertex = np.random.choice(vertices)
            connected_vertex = np.random.choice(chosen_vertices)
            connect_vertices(unconnected_vertex, connected_vertex)
            chosen_vertices.append(unconnected_vertex)
            vertices.pop(vertices.index(unconnected_vertex))
          self.list_of_vertices = chosen_vertices


        def connect_vertices(loc1, loc2):
           loc1.neighbors.append(loc2)
           loc2.neighbors.append(loc1)


        initialize_graph_connections()
        max_connections = get_max_connections(len(self.list_of_vertices))
        # get gaussian distribution with mean skewed by sparseness
        num_of_connections = np.random.randint(0, max_connections - len(self.list_of_vertices) - 1)



        for i in range(num_of_connections):
            loc1, loc2 = generate_random_connection()
            connect_vertices(loc1, loc2)


class BottleNeckGraph(Grid):
    def __init__(self, num, sparseness = 0.5):
        super(BottleNeckGraph, self).__init__()

        side1 = RandomGraph(num/2, sparseness)
        side2 = RandomGraph(num - num/2, sparseness)

        for i, q in enumerate(side2.list_of_vertices):
            q.name = 'v' + str(int(q.name[1::]) + i + 1)


        self.list_of_vertices.extend(side1.list_of_vertices)
        self.list_of_vertices.extend(side2.list_of_vertices)
        self.list_of_vertices[len(side1.list_of_vertices)-1].neighbors.append(self.list_of_vertices[len(side1.list_of_vertices)])
        self.list_of_vertices[len(side1.list_of_vertices)].neighbors.append(self.list_of_vertices[len(side1.list_of_vertices)-1])


class GridGraph(Grid):
    def __init__(self, num):
        super(GridGraph, self).__init__()
        vertex_matrix = []
        v = 0
        for i in range(int(floor(sqrt(num)))):
            matrix = []
            for k in range(int(ceil(sqrt(num)))):
                 matrix.append(Vertex(name='v'+str(v)))
                 v += 1
            vertex_matrix.append(matrix)

        for k in range(len(vertex_matrix)):
            # iterate rows
            for i in range(len(vertex_matrix[k])):
                # iterate columns
                current_vertex = vertex_matrix[k][i]
                if i > 0:
                    current_vertex.neighbors.append(vertex_matrix[k][i-1])
                if i < len(vertex_matrix[k]) - 1:
                    current_vertex.neighbors.append(vertex_matrix[k][i+1])
                if k > 0:
                    current_vertex.neighbors.append(vertex_matrix[k-1][i])
                if k < len(vertex_matrix) - 1:
                    current_vertex.neighbors.append(vertex_matrix[k+1][i])
            self.list_of_vertices.extend(vertex_matrix[k])


class TripleGraph(Grid):
    def __init__(self):
        hive = Vertex('v0')
        arm1 = [Vertex('v' + str(i)) for i in range(1, 5)]
        arm2 = [Vertex('v' + str(i)) for i in range(5, 12)]
        arm3 = [Vertex('v' + str(i)) for i in range(12, 24)]
        hive.neighbors.extend([arm1[0], arm2[0], arm3[0]])
        for arm in [arm1, arm2, arm3]:
            arm[0].neighbors.append(hive)
            for i in range(len(arm) - 1):
                arm[i].neighbors.append(arm[i+1])
                arm[i+1].neighbors.append(arm[i])
        self.list_of_vertices = [hive] + arm1 + arm2 + arm3

