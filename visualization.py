import sys, os, random
import pygame
from pygame.locals import *
from math import sqrt
from Vertex import Vertex
from Grid import CompleteGraph, RandomGraph
from swarm import Swarm

def main():
	pygame.init()
	pygame.display.set_caption('Graph Exploration')
	clock = pygame.time.Clock()
	
	sizex = 700
	sizey = 700
	background_color = (227, 232, 239)
	vertex_color = (83, 87, 94)
	edge_color = (83, 87, 94)

	screen = pygame.display.set_mode((sizex, sizey))
	background = pygame.Surface((sizex, sizey))
	background.fill(background_color)

	grid = CompleteGraph(10)
	swarm = Swarm(3)
	swarm.startup_sequence(grid.list_of_vertices[0])
	# vertex_set = {1: [2, 3, 4], 2: [1, 4], 3: [1], 4: [1, 2], 5: [1, 2], 6: [5, 6], 8:[], 9:[], 10:[]}
	
	margin = 100
	spacing = int((sizex - 2*margin)/sqrt(len(grid.list_of_vertices)))
	x = 0
	y = 0

	for vertex in grid.list_of_vertices:
		vertex.coords = (x + margin, y + margin)
		x += spacing
		if x >= sizex - margin:
			x = 0
			y += spacing

	state_to_color_mapping = {'red': pygame.Color('red'), 'yellow': pygame.Color('yellow'), 'green': pygame.Color('green')}

	while True:
		clock.tick(2)
		if not all([True if robot.state == "standby" else False for robot in swarm.swarm]):
			swarm.update()

			background.fill(background_color)
		
			for start_vertex in grid.list_of_vertices:
				pygame.draw.circle(background, state_to_color_mapping[start_vertex.state], start_vertex.coords, 5)
				if any(robot.current == start_vertex for robot in swarm.swarm):
					pygame.draw.circle(background, vertex_color, start_vertex.coords, 15, 3)
				print(start_vertex.name + ": " + start_vertex.state)
				for end_vertex in start_vertex.neighbors:
					pygame.draw.line(background, vertex_color, start_vertex.coords, end_vertex.coords)

			print("")
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		screen.blit(background, (0,0))
		pygame.display.update()

if __name__ == '__main__': main()