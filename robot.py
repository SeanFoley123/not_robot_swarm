
import numpy as np

class Robot(object):

    def __init_(self):
        self.current = None
        self.memory = []


    def start(self, current):
        self.current = current
        self.memory.append(self.current)


    def move(self):
        next_move = self.find_next_move()
        if next_move:
            move_from, move_to = self.make_move(next_move)
        else:
            move_from, move_to = self.retrace()

        return move_from, move_to


    def retrace(self):
        last_move = self.memory.pop()
        self.current = last_move
        return None, last_move

    def make_move(self, next_move):
        prev = self.current
        self.current = next_move
        next_move.visited = True
        self.memory.append(self.current)
        return prev, next_move


    def find_next_move(self):
        neigbors = self.current.getNeighbors()
        unexplored = [node for node in neighbors if node.visited is False]
        return np.random.choice(unexplored) if unexplored else None


    def get_position(self):
        return self.current
