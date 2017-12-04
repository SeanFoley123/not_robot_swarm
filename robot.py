
import numpy as np

class Robot(object):

    def __init__(self):
        self.current = None
        self.memory = []             #stores the way you got here
        self.path = []               #a variable for the swarm to instruct you to follow a certain path
        self.state = "normal"


    def start(self, starting_vertex):
        self.current = starting_vertex
        self.current.weight = 0


    def move(self):
        yield self.current            #returning the starting vertex
        yield self.current.neighbors           #returning the original neighbors

        if self.state == "normal":
            unexplored = [vertex for vertex in self.current.neighbors if vertex.state == "red"]
            if not unexplored:              # if there is no adjacent untouched vertex
                self.current.state = "green"
                next_state = self.memory.pop()
                if self.distance == 0:
                    self.state = "standby"

            else:
                self.current.state = "yellow"
                next_state = np.random.choice(unexplored)
                self.memory.append(self.current)

        elif self.state == "rebalance":
            next_state = self.path.pop()
            self.memory.append(self.current)
            if not self.path:
                self.state = "normal"

        self.current = next_state
        self.current.weight = self.distance if self.distance < self.current.weight else self.current.weight     
        yield self.current                # returning ending vertex


    @property
    def distance(self):
        # The current distance from the hive (in the path we took, not necessarily the shortest)
        return len(self.memory)
