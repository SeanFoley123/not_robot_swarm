class Vertex(object):

    def __init__(self, name, names_of_connections):
        self.name = name
        self.names_of_connections = names_of_connections
        self.state = 'not visited'

    def get_name(self):
        return self.name

    def get_connections(self):
        return self.names_of_connections

    def get_state(self):
        return self.state

    def set_state_not_visited(self):
        self.state = 'not visited'

    def set_state_incomplete(self):
        self.state = 'incomplete'

    def set_state_complete(self):
        self.state = 'complete'
