from Grid import *
from swarm import Swarm
from pprint import PrettyPrinter
from time import time
import csv

class Main(object):
    """
    the Main running class, mainly used for running the algorithm for accuracy
    and for benchmarking its efficiency. visualization.py was used for actual visualization
    """

    def __init__(self, grid_size, num_robots):
        self.grid_size, self.num_robots = grid_size, num_robots
        self.grid = GridGraph(self.grid_size)
        self.swarm = Swarm(self.num_robots)
        self.swarm.startup_sequence(self.grid.list_of_vertices[0])


    def reset(self):
        """
        resets the map and the robots for iterative testing/benchmarking
        """

        self.grid = GridGraph(self.grid_size)
        self.swarm = Swarm(self.num_robots)
        self.swarm.startup_sequence(self.grid.list_of_vertices[0])


    def run(self):
        """
        runs the algorithms until complete, and keeps track of the number of times it calls update,
        which is considered our benchmark
        """

        profile = 0
        while not (all([True if robot.state == "standby" else False for robot in self.swarm.swarm]) and (not [area for area in self.swarm.unknown_territory if area.state == "red"])):
            self.swarm.update()
            profile += 1

        # makes sure that the map we made is correct to the environment's map
        actual_graph = {vertex.name:{neighbor.name for neighbor in vertex.neighbors} for vertex in self.grid.list_of_vertices}
        if actual_graph == self.swarm.map:
            return profile
        else:
            raise ValueError("You done g00fed")


if __name__=="__main__":
    # benchmark testing for efficiency

    with open("grid_s300r1-256.csv", "wb") as f:
        writer = csv.DictWriter(f, fieldnames=["size", "timesteps"])
        alg = Main(300, 1)
        record = {}
        k = 1
        while k < 300:
            print "what k", k
            times = []
            alg.num_robots = k
            alg.reset()

            for i in range(500):
                times.append(alg.run())
                alg.reset()
                if i%100 == 0:
                    print i

            record[k] = sum(times)/500.0
            writer.writerow({"size":k, "timesteps":sum(times)/500.0})
            k *= 2

        for size, time in record.items():
            print "graph size: ", size, " timesteps: ", time
