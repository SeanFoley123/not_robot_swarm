
import numpy as np

class Robot(object):

    def __init__(self):
        self.current = None
        self.memory = []
        self.state = "normal"
        self.path = []


    def start(self, starting_node):
        self.current = starting_node
        self.current.weight = 0


    def move(self):
        neighborhood, valid_neighbors = self.find_next_move()
        if valid_neighbors:
            next_move = np.random.choice(valid_neighbors)
            move_from, move_to = self.make_move(next_move)
        else:
            move_from, move_to = self.retrace()

        return move_from, move_to, neighborhood


    def rebalance(self):
        next_move = self.path.pop()
        prev = self.current
        self.current = next_move
        self.memory.append(prev)
        if not self.path:
            self.state = "normal"


    def retrace(self):
        last_move = self.memory.pop()
        self.current.state = "green"
        self.current = last_move
        if not self.memory:
            self.state = "standby"
        return None, last_move

    def make_move(self, next_move):
        prev = self.current
        self.current.state = "yellow"
        self.current = next_move
        current_weight = self.current.weight
        self.current.weight = self.distance if self.distance < current_weight else current_weight
        self.memory.append(prev)
        return prev, self.current


    def find_next_move(self):
        neighbors = self.current.neighbors
        unexplored = [node for node in neighbors if node.state == "red"]
        return (neighbors, unexplored) if unexplored else (neighbors, None)


    @property
    def distance(self):
        # The current distance from the hive (in the path we took, not necessarily the shortest)
        return len(self.memory) - 1
