from Vertex import *

class Grid(object):

    def __init__(self):
        self.list_of_vertices = []


class CompleteGraph(Grid):

    def __init__(self, num):
        super().__init__()

        self.list_of_vertices = [Vertex(name='v'+str(i)) for i in range(num)]

        for i in range(len(self.list_of_vertices)):
                self.list_of_vertices[i].names_of_connections = self.list_of_vertices[0:i] + self.list_of_vertices[i+1::]
