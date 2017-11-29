
from robot import Robot
from sets import Set

class Swarm(object):

    def __init__(self, n):
        self.swarm = [Robot() for i in range(n)]
        self.map = {}
        self.efficiency = {}


    def startup_sequence(self, node):
        for robot in self.swarm:
            robot.start(node)

#TODO switch code to build a map by recording all neighbors, currently just traverses vertices but doesn't account for all edges
    def update(self):
        for robot in self.swarm:
            original, move = robot.move()
            try:
                self.efficiency[move] += 1
            except KeyError:
                self.efficiency[move] = 1
            if original:
                try:
                    self.map[original].add(move)
                except KeyError:
                    self.map[original] = Set()
