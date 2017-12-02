
import numpy as np

class Robot(object):

    def __init_(self):
        self.current = None
        self.rebalancing = False
        self.path = [] #the path you have followed to get to this point
        self.rebalancing_path = [] #a path given to you by the swarm


    def start(self, starting_node):
        self.current = starting_node
        self.current.weight = 0
        self.path.append(self.current)


    def move(self):
        original = self.current
        original_neighbors = self.current.neighbors

        if not self.rebalancing:
            unexplored = [node for node in original_neighbors if node.state == "red"]
            if not unexplored:
                self.current.state = "green"
                next_state = self.path.pop()

            elif len(unexplored) == 1:
                self.current.state = "green"
                next_state = unexplored[0]
                self.path.append(next_state)

            else:
                self.current.state = "yellow"
                next_state = np.random.choice(unexplored)
                self.path.append(next_state)

        else:
            next_state = self.rebalancing_path.pop()
            self.path.append(next_state)
            if not self.rebalancing_path:
                self.rebalancing = False
                self.rebalancing_path = []

        self.current = next_state
        self.current.weight = self.distance if self.distance < self.current.weight else self.current.weight

        return original, self.current, original_neighbors


    @property
    def distance(self):
        # The current distance from the hive (in the path we took, not necessarily the shortest)
        return len(self.path) - 1
