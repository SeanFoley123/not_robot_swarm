
import numpy as np

class Robot(object):

    def __init__(self):
        self.current = None
        self.memory = []
        self.path = []
        self.state = "normal"


    def start(self, starting_node):
        self.current = starting_node
        self.current.weight = 0


    def move(self):
        original = self.current
        original_neighbors = self.current.neighbors

        if self.state == "normal":
            unexplored = [node for node in original_neighbors if node.state == "red"]
            if not unexplored:
                self.current.state = "green"
                next_state = self.memory.pop()
                if self.distance == 0:
                    self.state = "standby"

            elif len(unexplored) == 1:
                self.current.state = "green"
                next_state = unexplored[0]
                self.memory.append(next_state)

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

        return original, self.current, original_neighbors


    @property
    def distance(self):
        # The current distance from the hive (in the path we took, not necessarily the shortest)
        return len(self.memory) - 1
