
from robot import Robot
import time

class Swarm(object):

    def __init__(self, n):
        self.hive = None
        self.swarm = [Robot() for i in range(n)]
        self.map = {}
        self.efficiency = {}
        self.unknown_territory = set()


    def startup_sequence(self, vertex):
        self.hive = vertex
        for robot in self.swarm:
            robot.start(self.hive)


    def update(self):
        for robot in self.swarm:
            if robot.state != "standby":
                self.command_robot(robot)           #have the robot move around like normal
            else:                                 #currently broken
                self.waypoint_navigation(robot)     #have the robot move to the nearest red spot


    def command_robot(self, robot):
        original, neighbors, move = robot.move()
        if neighbors:
            self.unknown_territory.update(neighbors)

        try:
            self.map[original.name].update([vertex.name for vertex in neighbors])
        except KeyError:
            self.map[original.name] = set()
            self.map[original.name].update([vertex.name for vertex in neighbors])


    def waypoint_navigation(self, robot):
        waypoint = self.choose_waypoint()
        if waypoint:
            path = self.find_path(waypoint)
            robot.state = "rebalance"
            robot.path = path


    def find_path(self, vertex):
        path = []
        while vertex != self.hive:

            path.append(vertex)
            vertex = min(vertex.neighbors, key = lambda v: v.weight)

        return path


    def choose_waypoint(self):
        unexplored_area = [area for area in self.unknown_territory if area.state == "red"]
        if unexplored_area:
            waypoint = min(unexplored_area, key = lambda vertex: min(vertex.neighbors, key = lambda neighbor: neighbor.weight).weight)
            return waypoint
