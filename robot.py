
import numpy as np

class Robot(object):

    def __init_(self):
        self.current = None
        self.rebalancing = False
        self.path = []


    def start(self, starting_node):
        self.current = starting_node
        self.current.weight = 0
        self.path.append(self.current)


    def move(self):
        unexplored = [node for node in self.current.neighbors if node.state == "red"]
        if not neighbors:
            self.current.state = "green"
            next_state = self.path.pop()

        elif len(neighbors) == 1:
            self.current.state = "green"
            next_state = neighbors[0]
            self.path.append(next_state)

        else:
            self.current.state = "yellow"
            next_state = np.random.choice(neighbors)
            self.path.append(next_state)

        self.current = next_state
        self.current.weight = self.distance if self.distance < self.current.weight else self.current.weight

    
    def rebalance(self):
        next_move = self.path.pop()
        self.current = next_move
        distance += 1
        if not self.path:
            self.rebalancing = False


    @property
    def distance(self):
        # The current distance from the hive (in the path we took, not necessarily the shortest)
        return len(self.path) - 1
