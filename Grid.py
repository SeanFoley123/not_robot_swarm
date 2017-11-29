from Vertex import *

class Grid(object):

    def __init__(self, num):
        self.list_of_vertices = []
        self.generate_complete_graph(num)

    def generate_complete_graph(self, num_of_vertices):

        self.list_of_vertices = []
        for i in range(num_of_vertices):
            connections = []
            for j in range(num_of_vertices):
                if not j == i:
                    connections.append('v'+str(j))


            v = Vertex(name='v'+str(i), names_of_connections = connections)
            self.list_of_vertices.append(v)


