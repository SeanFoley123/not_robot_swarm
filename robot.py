
import numpy as np

class Robot(object):
    '''
    Object used to represent robots on the grid
    Attributes:
    current: Vertex(): Current vertex of the robot
    memory: List: All vertices the robot has been to
    path: List: Instructions on how to get to the next vertex
    state: String: Current State of the robot. States are "normal," "rebalance," "standby"
    '''

    def __init__(self):
        self.current = None
        self.memory = []             #stores the way you got here
        self.path = []               #a variable for the swarm to instruct you to follow a certain path
        self.state = "normal"

    def start(self, starting_vertex):
        '''
        Sets position the robot starts in
        '''
        self.current = starting_vertex
        self.current.weight = 0


    def move(self):
        '''
        Logic detailing how the robot moves. Looks for last incomplete vertex to complete. 

        '''
        yield self.current            #returning the starting vertex
        yield self.current.neighbors           #returning the original neighbors

        #If robot state is normal
        if self.state == "normal":

            #Is there an unexplored vertex next to me?
            unexplored = [vertex for vertex in self.current.neighbors if vertex.state == "red"]
            if not unexplored:              # if there is no adjacent untouched vertex
                #No? Set Vertex state to complete and move to the last vertex in my memory
                self.current.state = "green"
                next_state = self.memory.pop()

                #If robot is at home go to standby state
                if self.distance == 0:
                    self.state = "standby"

            else:
                #Yes? Set current vertex state to incomplete and go one of the adjacent unexplored vertices
                self.current.state = "yellow"
                next_state = np.random.choice(unexplored)
                self.memory.append(self.current)

        #If robot state is rebalancing
        elif self.state == "rebalance":
            #Get next vertex from assigned path
            next_state = self.path.pop()

            self.memory.append(self.current)

            #If no more instructions, set state to normal
            if not self.path:
                self.state = "normal"

        #Move robot to next vertex
        self.current = next_state
        #Set Vertex distance from home
        self.current.weight = self.distance if self.distance < self.current.weight else self.current.weight     
        yield self.current                # returning ending vertex


    @property
    def distance(self):
        '''
        The current distance from the hive (in the path we took, not necessarily the shortest)
        '''
        return len(self.memory)
