
import numpy as np

class Robot(object):

    def __init_(self):
        self.current = None
        self.memory = []
        self.distance = 0
        self.rebalancing = False
        self.path = []


    def start(self, starting_node):
        self.current = starting_node
        self.current.weight = 0
        self.memory.append(self.current)


    def move(self):
        neighbors = self.find_next_move()
        if neighbors:
            next_move = np.random.choice(neighbors)
            move_from, move_to = self.make_move(next_move)
        else:
            move_from, move_to = self.retrace()

        return move_from, move_to, neighbors

    
    def rebalance(self):
        next_move = self.path.pop()
        self.current = next_move
        distance += 1
        if not self.path:
            self.rebalancing = False


    def retrace(self):
        last_move = self.memory.pop()
        self.current.state = "green"
        self.current = last_move
        distance -= 1
        return None, last_move

    def make_move(self, next_move):
        prev = self.current
        self.current.state = "yellow"
        self.current = next_move
        distance += 1
        current_weight = self.current.weight
        self.current.weight = distance if distance < current_weight else current_weight
        self.memory.append(self.current)
        return prev, self.current


    def find_next_move(self):
        neigbors = self.current.getNeighbors()
        unexplored = [node for node in neighbors if node.state != "green"]
        return unexplored if unexplored else None


    def get_position(self):
        return self.current
