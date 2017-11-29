class Vertex(object):

    def __init__(self, name):
        self.name = name
        self.state = 'not visited'
        self.weight = 10000000000000

    def get_name(self):
        return self.name

    def get_state(self):
        return self.state

    def get_weight(self):
        return self.weight

    def set_weight(self, newWeight):
        self.weight = newWeight

    def set_state_not_visited(self):
        self.state = 'not visited'

    def set_state_incomplete(self):
        self.state = 'incomplete'

    def set_state_complete(self):
        self.state = 'complete'
