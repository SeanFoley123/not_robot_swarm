
from robot import Robot

class Swarm(object):

    def __init__(self, n):
        self.hive = None
        self.swarm = [Robot() for i in range(n)]
        self.map = {}
        self.efficiency = {}
        self.unknown_territory = set()


    def startup_sequence(self, node):
        self.hive = node
        for robot in self.swarm:
            robot.start(node)


    def update(self):
        for robot in self.swarm:
            print(robot.current.name + ", " + robot.state)
            if robot.state != "standby":
                self.command_robot(robot)
            else:
                self.waypoint_navigation(robot)
        print('')


    def command_robot(self, robot):
        original, neighbors, move = robot.move()
        if neighbors:
            self.unknown_territory.update(neighbors)
        try:
            self.efficiency[move] += 1
        except KeyError:
            self.efficiency[move] = 1
        if original:
            try:
                self.map[original.name].update([node.name for node in neighbors])
            except KeyError:
                self.map[original.name] = set()
                self.map[original.name].update([node.name for node in neighbors])


    def waypoint_navigation(self, robot):
        waypoint = self.choose_waypoint()
        if waypoint:
            path = self.find_path(waypoint)
            robot.state = "rebalance"
            robot.path = path


    def find_path(self, node):
        path = []
        while node != self.hive:
            for k, v in self.map.items():
                if v == node:
                    path.append(k)
                    node = k

        return path


    def choose_waypoint(self):
        unexplored_area = [area for area in self.unknown_territory if area.state == "red"]
        if unexplored_area:
            waypoint = unexplored_area[0]
            for node in unexplored_area:
                if node.weight < waypoint.weight:
                    waypoint = node.weight

            return waypoint
