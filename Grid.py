from Vertex import *

class Grid(object):

    def __init__(self):
        self.list_of_vertices = []


class CompleteGraph(Grid):

    def __init__(self, num):
        super().__init__()

        self.list_of_vertices = [Vertex(name='v'+str(i)) for i in range(num)]

        for i in range(num):
            connections = []
            for j in range(num):
                if not j == i:
                    connections.append('v'+str(j))

            self.list_of_vertices.append(v)
