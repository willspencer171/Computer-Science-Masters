"""I've decided to follow along with a tutorial for A* search
that makes heavy use of pygame. I've never used it before
so this could be interesting"""

import pygame
import math
from queue import PriorityQueue
from typing import Self, Callable
from scipy.spatial import distance
import sys

WIN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("A* Path Finding Visualisation")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GREY = (155, 155, 155)
BLACK = (0, 0, 0)

class Node:
    def __init__(self, row: int, col: int, width: int, total_rows: int):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
    
    @property
    def position(self):
        return (self.row, self.col)

    @property
    def is_closed(self):
        return self.colour == RED
    
    @property
    def is_open(self):
        return self.colour == GREEN
    
    @property
    def is_barrier(self):
        return self.colour == BLACK
    
    @property
    def is_start(self):
        return self.colour == ORANGE
    
    @property
    def is_end(self):
        return self.colour == PURPLE

    def reset(self):
        self.colour = WHITE

    def make_closed(self):
        self.colour = RED
    
    def make_open(self):
        self.colour = GREEN
    
    def make_barrier(self):
        self.colour = BLACK
    
    def make_end(self):
        self.colour = PURPLE
    
    def make_start(self):
        self.colour = ORANGE

    def make_path(self):
        self.colour = CYAN

    def draw(self, win):
        pygame.draw.rect(win, self.colour, 
                         (self.x, self.y, 
                          self.width, self.width))
    
    def update_neighbours(self, grid: list[list[Self]]):
        self.neighbours = []

        candidates = [
            ('up', (self.row - 1, self.col)),
            ('down', (self.row + 1, self.col)),
            ('left', (self.row, self.col - 1)),
            ('right', (self.row, self.col + 1)),
            ('ne', (self.row - 1, self.col + 1)),
            ('nw', (self.row - 1, self.col - 1)),
            ('se', (self.row + 1, self.col + 1)),
            ('sw', (self.row + 1, self.col - 1))
        ]

        for action, (r, c) in candidates:
            try:
                if not grid[r][c].is_barrier and not grid[r][c].is_closed and r*c > 0:
                    self.neighbours.append((action, grid[r][c]))
            except IndexError:
                continue
    
def h(p1, p2) -> int:
    """Heuristic function for A* algorithm"""
    return max(distance.euclidean(p1, p2), distance.hamming(p1, p2))

def reconstruct_path(path, current, draw):
    while current in path:
        current = path[current]
        current.make_path()
        draw()

def A_star(draw_func: Callable, grid: list[list[Node]], start: Node, end: Node):
    count = 0
    frontier = PriorityQueue()
    frontier.put((0, count, start))
    path = {}
    actions = {}
    g_score = {tile: float('inf') for row in grid for tile in row}
    g_score[start] = 0

    f_score = {tile: float('inf') for row in grid for tile in row}
    f_score[start] = h(start.position, end.position)

    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = frontier.get()[2]
        current.update_neighbours(grid)
        
        if current == end:
            reconstruct_path(path, current, draw_func)
            return True
        
        for action, neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                path[neighbour] = current
                actions[neighbour] = action
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.position, end.position)
                if neighbour not in frontier.queue:
                    count += 1
                    frontier.put((f_score[neighbour], count, neighbour))
                    if neighbour != end:
                        neighbour.make_open()
            
        draw_func()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width) -> list[list[Node]]:
    """Create data structure containing all nodes"""
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tile = Node(i, j, gap, rows)
            grid[i].append(tile)

    return grid

def draw_grid(win, rows, width):
    """Draw gridlines on window"""
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    """Draw window contents"""
    win.fill(WHITE)

    for row in grid:
        for tile in row:
            tile.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width) -> tuple[int, int]:
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return (row, col)

def main(win, width, rows):
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue

            if pygame.mouse.get_pressed()[0]: # Left mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                try:
                    tile = grid[row][col]
                except IndexError:
                    continue

                if not start:
                    start = tile
                    start.make_start()

                elif not end and tile != start:
                    end = tile
                    end.make_end()
                
                elif tile != end and tile != start:
                    tile.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # Right mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                tile = grid[row][col]

                tile.reset()

                if tile == start:
                    start = None
                
                if tile == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started and start and end:
                    start.update_neighbours(grid)
                
                    A_star(lambda: draw(win, grid, rows, width), grid, start, end)

            
                if event.key == pygame.K_ESCAPE:
                    started = False
                    start = None
                    end = None
                    for row in grid:
                        for tile in row:
                            if not tile.is_start or not tile.is_end:
                                tile.reset()

    
    pygame.quit()


main(WIN, 800, 70)
