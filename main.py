from Grid import *
from swarm import Swarm

class Main(object):

    def __init__(self):
        self.grid = CompleteGraph(10)
        self.swarm = Swarm(3)
        self.swarm.startup_sequence(self.grid.list_of_vertices[0])


    def run(self):
        while not (all([True if robot.state == "standby" else False for robot in swarm.swarm]) and (not [area for area in swarm.unknown_territory if area.state == "red"])):
            self.swarm.update()

        print(self.swarm.map)


if __name__=="__main__":
    alg = Main()
    alg.run()
