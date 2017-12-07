from Grid import *
from swarm import Swarm
from pprint import PrettyPrinter
from time import time
pp = PrettyPrinter()

class Main(object):

    def __init__(self, grid_size, num_robots):
        self.grid_size, self.num_robots = grid_size, num_robots
        self.grid = CompleteGraph(self.grid_size)
        self.swarm = Swarm(self.num_robots)
        self.swarm.startup_sequence(self.grid.list_of_vertices[0])


    def reset(self):
        self.grid = CompleteGraph(self.grid_size)
        self.swarm = Swarm(self.num_robots)
        self.swarm.startup_sequence(self.grid.list_of_vertices[0])


    def run(self):
        start = time()
        while not (all([True if robot.state == "standby" else False for robot in self.swarm.swarm]) and (not [area for area in self.swarm.unknown_territory if area.state == "red"])):
            self.swarm.update()

        actual_graph = {vertex.name:{neighbor.name for neighbor in vertex.neighbors} for vertex in self.grid.list_of_vertices}
        if actual_graph == self.swarm.map:
            return time()-start
        else:
            raise ValueError("You done g00fed")


if __name__=="__main__":
    alg = Main(100, 3)
    # for k in range(10, 110, 10):
    times = []
    # alg.grid_size = k

    for i in range(1000):
        times.append(alg.run())
        alg.reset()
        if i%100 == 0:
            print(i)

    print str((sum(times)/1000.0)*1000) + " ms"
