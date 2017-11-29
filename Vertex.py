class Vertex(object):

    def __init__(name=0, names_of_connections=[]):
        self.name = name
        self.names_of_connections = names_of_connections
        self.visited = False

    def get_name():
        return self.name

    def get_connections():
        return self.names_of_connections

    def is_visited():
        return self.visited

    def visit():
        self.visited = True
