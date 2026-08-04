import pygame
import heapq

pygame.init()

WIDTH = 600
ROWS = 30
CELL = WIDTH // ROWS
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Visualizer (A*)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GRAY = (200, 200, 200)

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * CELL
        self.y = col * CELL
        self.color = WHITE
        self.neighbors = []
        self.g = float("inf")
        self.f = float("inf")
        self.parent = None

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, CELL, CELL))

    def __lt__(self, other):
        return False

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and grid[self.row + 1][self.col].color != BLACK:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and grid[self.row - 1][self.col].color != BLACK:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < ROWS - 1 and grid[self.row][self.col + 1].color != BLACK:
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and grid[self.row][self.col - 1].color != BLACK:
            self.neighbors.append(grid[self.row][self.col - 1])

def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def a_star(start, end, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    start.g = 0
    start.f = heuristic(start, end)

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heapq.heappop(open_set)[1]

        if current == end:
            while current.parent:
                current.color = PURPLE
                current = current.parent
                draw_grid(grid)
            return True

        for neighbor in current.neighbors:
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                neighbor.f = temp_g + heuristic(neighbor, end)
                heapq.heappush(open_set, (neighbor.f, neighbor))
                neighbor.color = GREEN

        draw_grid(grid)
        if current != start:
            current.color = RED

    return False

def draw_grid(grid):
    screen.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw()
    for i in range(ROWS):
        pygame.draw.line(screen, GRAY, (0, i * CELL), (WIDTH, i * CELL))
        pygame.draw.line(screen, GRAY, (i * CELL, 0), (i * CELL, WIDTH))
    pygame.display.update()

def make_grid():
    return [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]

grid = make_grid()
start = grid[2][2]
end = grid[25][25]
start.color = BLUE
end.color = BLUE

# Create walls
for i in range(10, 20):
    grid[i][15].color = BLACK

for row in grid:
    for node in row:
        node.update_neighbors(grid)

running = True
while running:
    draw_grid(grid)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                a_star(start, end, grid)

pygame.quit()

