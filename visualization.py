import sys, os, random
import pygame
from pygame.locals import *
from math import sqrt
from Vertex import Vertex
from Grid import CompleteGraph, RandomGraph, BottleNeckGraph, GridGraph
from swarm import Swarm
from pprint import PrettyPrinter
import numpy as np
import copy as cp
sizex = 700
sizey = 700
background_color = (227, 232, 239)
robot_color = (0, 0, 255)
edge_color = (83, 87, 94)
state_to_color_mapping = {'red': pygame.Color('red'), 'yellow': pygame.Color('yellow'), 'green': pygame.Color('green')}
pp = PrettyPrinter()

<<<<<<< HEAD

class Point:
	def __init__(self):
		self.x  = 0
		self.y = 0

def space_out_vertices(grid):
	margin = 100
	spacing = int((sizex - 2*margin)/sqrt(len(grid.list_of_vertices)))
	x = 100
	y = 100

	for vertex in grid.list_of_vertices:
		# vertex.coords = (np.random.randint(margin, sizex-margin), np.random.randint(margin, sizey-margin))
		vertex.coords = (x, y)
		x += spacing
		if x >= sizex - margin:
			x = 100
			y += spacing


class Visualizer(object):

	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Graph Exploration')
		self.clock = pygame.time.Clock()
		self._running = True
		self.sizex = 700
		self.sizey = 700
		self.grid = RandomGraph(20, 0)
		self.space_out_vertices()
		self.swarm = Swarm(3)
		self.swarm.startup_sequence(self.grid.list_of_vertices[0])



		self.background_color = (227, 232, 239)
		self.robot_color = (83, 87, 94)
		self.edge_color = (83, 87, 94)
		self.state_to_color_mapping = {'red': pygame.Color('red'), 'yellow': pygame.Color('yellow'), 'green': pygame.Color('green')}

<<<<<<< HEAD
		self.screen = pygame.display.set_mode((self.sizex, self.sizey))
		self.background = pygame.Surface((self.sizex, self.sizey))

		grid = GridGraph(40)
		space_out_vertices(grid)
		swarm = Swarm(3)
		swarm.startup_sequence(grid.list_of_vertices[0])


		self.background.fill(background_color)
		self.draw_graph()
		self.empty_graph = self.background
		self.draw_robots(None)
		self.screen.blit(self.background, (0,0))
		pygame.display.update()

	def on_event(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self._running = False
				

	def on_update(self):
		#print([area for area in swarm.unknown_territory if area.state == "red"])

		if not (all([True if robot.state == "standby" else False for robot in self.swarm.swarm]) and (not [area for area in self.swarm.unknown_territory if area.state == "red"])):
			old_vertices = [robot.current.coords for robot in self.swarm.swarm]
			self.swarm.update()
			self.background.fill(self.background_color)
			self.draw_robots(old_vertices)
		
		self.screen.blit(self.empty_graph, (0,0))
		pygame.display.update()


	def on_exit(self):
		for vertex, frequency in self.swarm.efficiency.items():
			print(vertex.name + " visited " + str(frequency) + " times")
		pygame.quit()
		sys.exit()

	def main(self):
		while self._running:
			self.on_event()
			self.on_update()
		self.on_exit()

	def draw_graph(self):
		for start_vertex in self.grid.list_of_vertices:
			for end_vertex in start_vertex.neighbors:
				pygame.draw.line(self.background, self.edge_color, start_vertex.coords, end_vertex.coords)

		for start_vertex in self.grid.list_of_vertices:
			pygame.draw.circle(self.background, self.state_to_color_mapping[start_vertex.state], start_vertex.coords, 5)


	def draw_robots(self, old_vertices):


			# if any(robot.current == start_vertex for i, robot in enumerate(swarm.swarm)):
			# 	animate_robot(old_vertices[i], robot.current)
			# 	pygame.draw.circle(background, robot_color, start_vertex.coords, 15, 3)
			for i, robot in enumerate(self.swarm.swarm):
				if robot.current == start_vertex and not old_vertices == None:
					animate_robot(self.background, self.robot_color, old_vertices[i], robot.current)
				pygame.draw.circle(self.background, self.robot_color, start_vertex.coords, 15, 3)
		

	def space_out_vertices(self):
		margin = 100
		#spacing = int((self.sizex - 2*margin)/sqrt(len(self.grid.list_of_vertices)))
		x = 0
		y = 0

		for vertex in self.grid.list_of_vertices:
			vertex.coords = (np.random.randint(margin, self.sizex-margin), np.random.randint(margin, self.sizey-margin))
			# x += spacing
			# if x >= sizex - margin:
			# 	x = 0
			# 	y += spacing

	def getKeyFrames(self, level, pt1, pt2):
		midpoint = Point()
		if level >= 4:
			midpoint.x = (pt1.x + pt2.x)/2
			midpoint.y = (pt1.y + pt2.y)/2
			return [midpoint]
		else:
			midpoint.x = (pt1.x + pt2.x)/2
			midpoint.y = (pt1.y + pt2.y)/2
			frames1 = self.getKeyFrames(level+1, pt1, midpoint)
			frames2 = self.getKeyFrames(level+1, midpoint, pt2)
			frames1.extend(frames2)

			return frames1


	def draw_robots(self, old_vertices):
		for start_vertex in self.grid.list_of_vertices:
			for end_vertex in start_vertex.neighbors:
				pygame.draw.line(self.background, self.edge_color, start_vertex.coords, end_vertex.coords)

		for start_vertex in self.grid.list_of_vertices:
			pygame.draw.circle(self.background, self.state_to_color_mapping[start_vertex.state], start_vertex.coords, 5)
			# if any(robot.current == start_vertex for i, robot in enumerate(swarm.swarm)):
			# 	animate_robot(old_vertices[i], robot.current)
			# 	pygame.draw.circle(background, robot_color, start_vertex.coords, 15, 3)
			for i, robot in enumerate(self.swarm.swarm):
				if robot.current == start_vertex and not old_vertices == None:
					self.animate_robot(old_vertices[i], robot.current)
					pygame.draw.circle(self.background, self.robot_color, start_vertex.coords, 15, 3)


	def animate_robot(self, current_vertex, next_vertex):
		pt1 = Point()
		pt2 = Point()
		pt1.x = current_vertex[0]
		pt1.y = current_vertex[1]
		pt2.x = next_vertex.coords[0]
		pt2.y = next_vertex.coords[1]

		frames = self.getKeyFrames(0, pt1, pt2)
		print frames

		for i in frames:
			self.background = self.empty_graph
			pygame.draw.circle(self.background, self.robot_color, (i.x, i.y), 15, 3)
			self.screen.blit(self.empty_graph, (0, 0))
			pygame.display.update()


if __name__ == '__main__': main()

