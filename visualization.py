import sys, os, random
import pygame
from pygame.locals import *
import pygame.image as img
from math import sqrt
from Vertex import Vertex
from Grid import CompleteGraph, RandomGraph, BottleNeckGraph, GridGraph, TripleGraph
from swarm import Swarm
from time import sleep
from pprint import PrettyPrinter
import numpy as np
import copy as cp

class Point:
	''' 
	Point object for use with function getKeyFrames(). Has two attributes, x and y for x and y position
	'''
	def __init__(self):
		self.x  = 0
		self.y = 0


class Visualizer(object):
	'''
	Visualizer object to help structure the code for animation. Attributes are all pygame objects, swarm of robots, and grid
	'''

	def __init__(self):
		#Start Pygame
		pygame.init()
		pygame.display.set_caption('Graph Exploration')

		#Create Pygame variables
		self.clock = pygame.time.Clock()
		self.sizex = 700
		self.sizey = 700
		self.imgCounter = 0
		self.font = pygame.font.SysFont('Roboto', 25)
		self.background_color = (227, 232, 239)
		self.robot_color = (83, 87, 94)
		self.edge_color = (83, 87, 94)
		self.state_to_color_mapping = {'red': pygame.Color('red'), 'yellow': pygame.Color('yellow'), 'green': pygame.Color('green')}
		self.screen = pygame.display.set_mode((self.sizex, self.sizey))
		self.background = pygame.Surface((self.sizex, self.sizey))

		#Create Grid for robots to walk on
		self.grid = TripleGraph()

		#Create swarm of robots
		self.swarm = Swarm(2)
		self.swarm.startup_sequence(self.grid.list_of_vertices[0])
		self.old_vertices = None
		swarm = Swarm(3)
		swarm.startup_sequence(self.grid.list_of_vertices[0])

		#Set Main loop to running
		self._running = True

		#Draw graph into window
		self.background.fill(self.background_color)
		self.space_out_vertices(self.grid)
		self.draw_grid()
		pygame.draw.circle(self.background, self.robot_color, self.swarm.hive.coords, 15, 3)
		self.screen.blit(self.background, (0,0))
		pygame.display.update()
		sleep(1)


	def on_event(self):
		'''
		Manages inputs for Pygame loop. In this case it is just what to do when the game quits
		'''

		for event in pygame.event.get():
			if event.type == QUIT:
				self._running = False
				

	def on_update(self):
		'''
		Manages upkeep that needs to be done every game loop. This is updating robot vertices and drawing on the graph
		'''

		if not (all([True if robot.state == "standby" else False for robot in self.swarm.swarm]) and (not [area for area in self.swarm.unknown_territory if area.state == "red"])):
			self.old_vertices = [robot.current.coords for robot in self.swarm.swarm]
			self.swarm.update()
			self.draw()

		sleep(.25)


	def on_exit(self):
		'''
		Manages what to do when the game loop exits. This is determining efficiency of robots and exiting pygame.
		'''
		for vertex, frequency in self.swarm.efficiency.items():
			print(vertex.name + " visited " + str(frequency) + " times")
		pygame.quit()
		sys.exit()

	def main(self):
		'''
		Main Pygame Loop. 
		'''

		while self._running:
			self.on_event()
			self.on_update()
		self.on_exit()


	def space_out_vertices(self, grid):
		'''
		Spaces out vertices of the grid. Takes grid object as an argument
		'''

		#Sets margins and spacing
		margin = 100
		spacing = int((self.sizex - 2*margin)/sqrt(len(self.grid.list_of_vertices)))
		x = 100
		y = 100

		#Runs through all vertices in the grid
		for vertex in self.grid.list_of_vertices:
			#Sets vertex coordinates
			vertex.coords = (x, y)

			#Increment Spacing
			x += spacing
			if x >= self.sizex - margin:
				x = 100
				y += spacing


	def getKeyFrames(self, recurseLevel, pt1, pt2):
		'''
		Gets frames for robot animation. This is the animation between two vertices. 

		Arguments:
		recurseLevel: Int. Current level of recursion. Increments every time program goes deeper
		pt1: Point(): Current point of the robot.
		pt2: Point(): Point to move the robot to.

		Returns:
		frames1: List of tuples: Each tuple is an equally spaced point between the two given points. 
		Program uses these as in between frames for robot animation
		'''

		#Instantiate midpoint
		midpoint = Point()

		#Check current recursion depth
		if recurseLevel >= 3:
		#If at depth three, determine and return midpoint
			midpoint.x = (pt1.x + pt2.x)/2
			midpoint.y = (pt1.y + pt2.y)/2
			return [midpoint]
		else:
			#Otherwise, determine midpoint and find midpoints between midpoint and both endpoints
			midpoint.x = (pt1.x + pt2.x)/2
			midpoint.y = (pt1.y + pt2.y)/2
			frames1 = self.getKeyFrames(recurseLevel+1, pt1, midpoint)
			frames2 = self.getKeyFrames(recurseLevel+1, midpoint, pt2)

			#Add both sets of frames to the same list
			frames1.extend(frames2)

			return frames1


	def draw(self):
		'''
		Draws robots and graph. 
		'''

		#Instantiate 2 point objects and list of frames to animate
		pt1 = Point()
		pt2 = Point()
		frames =  []

		#Run through list of robots in the swarm
		for i, robot in enumerate(self.swarm.swarm):
			#Get animation frames for each robot and append list of frames
			pt1.x = self.old_vertices[i][0]
			pt1.y = self.old_vertices[i][1]
			pt2.x = robot.current.coords[0]
			pt2.y = robot.current.coords[1]

			#frames is a list of each list of animation frames for each robot
			frames.append(self.getKeyFrames(0, pt1, pt2))
		
			#For the length of a set of frames
		for i in range(len(frames[0])):
			#if Pygame loop is still running
			if self._running:
			#Wait
				self.clock.tick(len(frames[0])+1)

				#Check to see if we exited the Pygame loop
				self.on_event()	

				#Redraw blank background
				self.background.fill(self.background_color)

				#For each separate robots frames draw the robot at its current frame
				for k in range(len(frames)):

					self.draw_grid()
					pygame.draw.circle(self.background, self.robot_color, (frames[k][i].x, frames[k][i].y), 15, 3)

				#Update the screen
				self.screen.blit(self.background, (0, 0))
				pygame.display.update()

				#If we want to save an animation this will be uncommented
				#img.save(self.background, str(self.imgCounter)+'.jpg')
				self.imgCounter+=1
			else:
				self.on_exit()

		#Repeated code to get last frame of robot animation
		#ow
		self.clock.tick(len(frames[0])+1)
		self.background.fill(self.background_color)
		for robot in self.swarm.swarm:
			self.draw_grid()
			pygame.draw.circle(self.background, self.robot_color, robot.current.coords, 15, 3)

		self.screen.blit(self.background, (0, 0))
		pygame.display.update()
		#img.save(self.background, str(self.imgCounter)+'.jpg')
		self.imgCounter+=1

	def draw_grid(self):
		'''
		Draws the grid of vertices on the window
		'''

		#For each vertex
		for start_vertex in self.grid.list_of_vertices:
			for end_vertex in start_vertex.neighbors:
				#Draw a line between Vertex and its connections
				pygame.draw.line(self.background, self.edge_color, start_vertex.coords, end_vertex.coords)
		#For each vertex
		for start_vertex in self.grid.list_of_vertices:

			#If the vertex isn't the starting point
			if start_vertex != self.swarm.hive:
				#Label the vertex and draw it
				text = self.font.render(start_vertex.name, True, self.edge_color)
				pygame.draw.circle(self.background, self.state_to_color_mapping[start_vertex.state], start_vertex.coords, 5)
				self.background.blit(text, (start_vertex.coords[0]-4, start_vertex.coords[1]+4))
			else:
				#Otherwise, draw a house
				pygame.draw.rect(self.background, self.robot_color, pygame.Rect(start_vertex.coords[0]-8, start_vertex.coords[1]-8, 16, 16))
				pygame.draw.polygon(self.background, self.robot_color, (
					(start_vertex.coords[0]-8, start_vertex.coords[1]-8),
					(start_vertex.coords[0]+8, start_vertex.coords[1]-8),
					(start_vertex.coords[0], start_vertex.coords[1]-15)
					)
				)




if __name__ == '__main__': 

	vis = Visualizer()
	vis.main()
