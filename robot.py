
import numpy as np

class Robot(object):

    def __init__(self):
        self.current = None
        self.memory = []             #stores the way you got here
        self.path = []               #a variable for the swarm to instruct you to follow a certain path
        self.state = "normal"


    def start(self, starting_node):
        self.current = starting_node
        self.current.weight = 0
        self.memory.append(self.current)


    def move(self):
        yield self.current           #returning the starting vertex
        yield self.current.neighbors           #returning the original neighbors

        if self.state == "normal":
            unexplored = [node for node in self.current.neighbors if node.state == "red"]
            if not unexplored:
                print("reversing: " + str([vertex.name for vertex in self.memory]))
                self.current.state = "green"
                next_state = self.memory.pop()
                if self.distance == 0:
                    print("done")
                    self.state = "standby"

            else:
                self.current.state = "yellow"
                next_state = np.random.choice(unexplored)
                self.memory.append(next_state)

        elif self.state == "rebalancing":
            next_state = self.path.pop()
            self.memory.append(next_state)
            if not self.path:
                self.state = "normal"

        self.current = next_state
        self.current.weight = self.distance if self.distance < self.current.weight else self.current.weight     

        yield self.current                # returning ending vertex


    @property
    def distance(self):
        # The current distance from the hive (in the path we took, not necessarily the shortest)
        return len(self.memory)
