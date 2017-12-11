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
sizex = 700
sizey = 700
background_color = (227, 232, 239)
robot_color = (0, 0, 255)
edge_color = (83, 87, 94)
state_to_color_mapping = {'red': pygame.Color('red'), 'yellow': pygame.Color('yellow'), 'green': pygame.Color('green')}
pp = PrettyPrinter()



class Point:
	def __init__(self):
		self.x  = 0
		self.y = 0




class Visualizer(object):

	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Graph Exploration')
		self.clock = pygame.time.Clock()
		self._running = True
		self.sizex = 700
		self.sizey = 700
		self.grid = TripleGraph()
		self.swarm = Swarm(2)
		self.swarm.startup_sequence(self.grid.list_of_vertices[0])
		self.old_vertices = None
		self.imgCounter = 0
		self.font = pygame.font.SysFont('Roboto', 25)

		self.background_color = (227, 232, 239)
		self.robot_color = (83, 87, 94)
		self.edge_color = (83, 87, 94)
		self.state_to_color_mapping = {'red': pygame.Color('red'), 'yellow': pygame.Color('yellow'), 'green': pygame.Color('green')}


		self.screen = pygame.display.set_mode((self.sizex, self.sizey))
		self.background = pygame.Surface((self.sizex, self.sizey))


		self.space_out_vertices(self.grid)
		swarm = Swarm(3)
		swarm.startup_sequence(self.grid.list_of_vertices[0])


		self.background.fill(background_color)
		self.draw_grid()
		pygame.draw.circle(self.background, self.robot_color, self.swarm.hive.coords, 15, 3)
		self.screen.blit(self.background, (0,0))

		pygame.display.update()
		sleep(1)

	def on_event(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self._running = False
				

	def on_update(self):

		if not (all([True if robot.state == "standby" else False for robot in self.swarm.swarm]) and (not [area for area in self.swarm.unknown_territory if area.state == "red"])):
			self.old_vertices = [robot.current.coords for robot in self.swarm.swarm]
			self.swarm.update()
			self.draw()

		sleep(.25)


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


	def space_out_vertices(self, grid):
		margin = 100
		spacing = int((self.sizex - 2*margin)/sqrt(len(self.grid.list_of_vertices)))
		x = 100
		y = 100

		for vertex in self.grid.list_of_vertices:
			# vertex.coords = (np.random.randint(margin, sizex-margin), np.random.randint(margin, sizey-margin))
			vertex.coords = (x, y)
			x += spacing
			if x >= self.sizex - margin:
				x = 100
				y += spacing

	def getKeyFrames(self, recurseLevel, pt1, pt2):
		midpoint = Point()
		if recurseLevel >= 3:
			midpoint.x = (pt1.x + pt2.x)/2
			midpoint.y = (pt1.y + pt2.y)/2
			return [midpoint]
		else:
			midpoint.x = (pt1.x + pt2.x)/2
			midpoint.y = (pt1.y + pt2.y)/2
			frames1 = self.getKeyFrames(recurseLevel+1, pt1, midpoint)
			frames2 = self.getKeyFrames(recurseLevel+1, midpoint, pt2)
			frames1.extend(frames2)

			return frames1

	def draw(self):
		pt1 = Point()
		pt2 = Point()
		frames =  []
		for i, robot in enumerate(self.swarm.swarm):
			pt1.x = self.old_vertices[i][0]
			pt1.y = self.old_vertices[i][1]
			pt2.x = robot.current.coords[0]
			pt2.y = robot.current.coords[1]

			frames.append(self.getKeyFrames(0, pt1, pt2))
		

		for i in range(len(frames[0])):
			self.clock.tick(len(frames[0])+1)
			self.on_event()	
			self.background.fill(self.background_color)
			for k in range(len(frames)):
				self.draw_grid()
				pygame.draw.circle(self.background, self.robot_color, (frames[k][i].x, frames[k][i].y), 15, 3)

			self.screen.blit(self.background, (0, 0))
			pygame.display.update()
			#img.save(self.background, str(self.imgCounter)+'.jpg')
			self.imgCounter+=1
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

		for start_vertex in self.grid.list_of_vertices:
			for end_vertex in start_vertex.neighbors:
				pygame.draw.line(self.background, self.edge_color, start_vertex.coords, end_vertex.coords)

		for start_vertex in self.grid.list_of_vertices:
			if start_vertex != self.swarm.hive:
				text = self.font.render(start_vertex.name, True, self.edge_color)
				pygame.draw.circle(self.background, self.state_to_color_mapping[start_vertex.state], start_vertex.coords, 5)
				self.background.blit(text, (start_vertex.coords[0]-4, start_vertex.coords[1]+4))
			else:
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
