
from robot import Robot
import time

class Swarm(object):
    """
    Class defining a collection of robots
    Swarm is in charge of updating all of the robots, compiling a map, and
    helping robots calculate rebalancing destinations.
    """

    def __init__(self, n):
        """
        Initializes the swarm with n robots
        """
        self.hive = None        #the vertex where the swarm is based
        self.swarm = [Robot() for i in range(n)]        #list of robots
        self.map = {}       #swarm's internal mapping of explored vertices to their neighbors
        self.unknown_territory = set()      #convenience collection of all the unexplored nodes robots have encountered


    def startup_sequence(self, vertex):
        """
        Sets up the swarm and all its robots with a starting vertex
        """
        self.hive = vertex
        for robot in self.swarm:
            robot.start(self.hive)


    def update(self):
        for robot in self.swarm:
            if robot.state != "standby":
                self.command_robot(robot)           #have the robot move around like normal
            else:
                self.waypoint_navigation(robot)     #have the robot move to the nearest red spot


    def command_robot(self, robot):
        original, neighbors, move = robot.move()    #the robot moves and reports its move and what it now sees
        if neighbors:
            self.unknown_territory.update(neighbors)    #all the unexplored neighbors are added to the set
        
        try:            #this try/except updates swarm's knowledge of the original vertex
            self.map[original.name].update([vertex.name for vertex in neighbors])
        except KeyError:
            self.map[original.name] = set()
            self.map[original.name].update([vertex.name for vertex in neighbors])


    def waypoint_navigation(self, robot):
        waypoint = self.choose_waypoint()   #picks the closest unexplored vertex
        if waypoint:
            path = self.find_path(waypoint)     #calculates a path to that vertex and sends the robot on it
            robot.state = "rebalance"
            robot.path = path       #tells the robot to follow that path


    def find_path(self, vertex):
        """
        Function that implements Dijkstra's algorithm; it always chooses the lower weight option until it's
        back at the hive
        """
        path = []
        while vertex != self.hive:
            path.append(vertex)
            vertex = min(vertex.neighbors, key = lambda v: v.weight)

        return path         #returns a list of vertices for the robot to follow to vertex


    def choose_waypoint(self):
        """
        This function finds the unexplored node that has the lowest weight neigbor. This should equate to the
        unexplored node with the shortest path (that the robots have discovered)
        """
        unexplored_area = [area for area in self.unknown_territory if area.state == "red"]
        if unexplored_area:
            waypoint = min(unexplored_area, key = lambda vertex: min(vertex.neighbors, key = lambda neighbor: neighbor.weight).weight)
            return waypoint
