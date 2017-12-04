import sys, os, random
import pygame
from pygame.locals import *
from math import sqrt
from Vertex import Vertex
from Grid import CompleteGraph, RandomGraph, BottleNeckGraph
from swarm import Swarm
from pprint import PrettyPrinter

sizex = 700
sizey = 700
background_color = (227, 232, 239)
robot_color = (83, 87, 94)
edge_color = (83, 87, 94)
state_to_color_mapping = {'red': pygame.Color('red'), 'yellow': pygame.Color('yellow'), 'green': pygame.Color('green')}
pp = PrettyPrinter()

def space_out_vertices(grid):
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


def draw_robots(background, grid, swarm):
	for start_vertex in grid.list_of_vertices:
		pygame.draw.circle(background, state_to_color_mapping[start_vertex.state], start_vertex.coords, 5)
		if any(robot.current == start_vertex for robot in swarm.swarm):
			pygame.draw.circle(background, robot_color, start_vertex.coords, 15, 3)
		for end_vertex in start_vertex.neighbors:
			pygame.draw.line(background, edge_color, start_vertex.coords, end_vertex.coords)



def main():
	pygame.init()
	pygame.display.set_caption('Graph Exploration')
	clock = pygame.time.Clock()

	grid = RandomGraph(50, 0)
	space_out_vertices(grid)
	swarm = Swarm(3)
	swarm.startup_sequence(grid.list_of_vertices[0])

	screen = pygame.display.set_mode((sizex, sizey))
	background = pygame.Surface((sizex, sizey))

	background.fill(background_color)
	draw_robots(background, grid, swarm)
	screen.blit(background, (0,0))
	pygame.display.update()

	while True:
		clock.tick(2)
		if not all([True if robot.state == "standby" else False for robot in swarm.swarm]):
			swarm.update()
			background.fill(background_color)
			draw_robots(background, grid, swarm)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				for vertex, frequency in swarm.efficiency.items():
					print(vertex.name + " visited " + str(frequency) + " times")
				pygame.quit()
				sys.exit()

		screen.blit(background, (0,0))
		pygame.display.update()

if __name__ == '__main__': main()