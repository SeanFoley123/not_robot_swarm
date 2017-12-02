import sys, os, random
import pygame
from pygame.locals import *
from math import sqrt
from Vertex import Vertex
from Grid import CompleteGraph, RandomGraph

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

	complete = RandomGraph(10)
	# vertex_set = {1: [2, 3, 4], 2: [1, 4], 3: [1], 4: [1, 2], 5: [1, 2], 6: [5, 6], 8:[], 9:[], 10:[]}
	
	vertex_coords = dict()
	margin = 100
	spacing = int((sizex - 2*margin)/sqrt(len(complete.list_of_vertices)))
	x = 0
	y = 0

	for vertex in complete.list_of_vertices:
		pygame.draw.circle(background, vertex_color, (x + margin, y + margin), 5)
		vertex_coords[vertex] = (x + margin, y + margin)
		x += spacing
		if x >= sizex - margin:
			x = 0
			y += spacing
		
	for start_vertex in complete.list_of_vertices:
		for end_vertex in vertex.names_of_connections:
			pygame.draw.line(background, vertex_color, vertex_coords[start_vertex], vertex_coords[end_vertex])

	while True:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		screen.blit(background, (0,0))
		pygame.display.flip()

if __name__ == '__main__': main()