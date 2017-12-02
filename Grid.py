from Vertex import *
import random
class Grid(object):

    def __init__(self):
        self.list_of_vertices = []


class CompleteGraph(Grid):

    def __init__(self, num):
        super().__init__()

        self.list_of_vertices = [Vertex(name='v'+str(i)) for i in range(num)]

        for i in range(len(self.list_of_vertices)):
                self.list_of_vertices[i].names_of_connections = self.list_of_vertices[0:i] + self.list_of_vertices[i+1::]

class RandomGraph(Grid):
    def __init__(self, num):
        super().__init__()

        self.list_of_vertices = [Vertex(name='v'+str(i)) for i in range(num)]

        self.generate_connections()

    def generate_connections():
        min_connections = 2*len(self.list_of_vertices) - 5
        max_connections = get_max_connections(len(self.list_of_vertices))

        num_of_connections = random.randint(min_connections, max_connections)

        for i in range(num_of_connections):
            loc1, loc2 = generate_random_connection()
            self.list_of_vertices[loc1].append('v'+str(loc2))



        def get_max_connections(num):
            if not num == 1:
                return num - 1 + get_max_connections(num-1)
            else:
                return 0

        def generate_random_connection():
           loc1 = random.randint(0, len(self.list_of_vertices)-1)
           loc2 = random.randint(0, len(self.list_of_vertices)-1)

           if not self.does_connection_exist(loc1, loc2):
               return loc1, loc2
           else:
               return generate_random_connection():

    def does_connection_exist(loc1,loc2):
        for i in self.list_of_vertices[loc1].names_of_connections:
            if int(i[1::) == loc2:
                    return True
        return False
