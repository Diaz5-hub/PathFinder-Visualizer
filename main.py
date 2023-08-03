import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))  ##create the dimesions
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:  ##keep track of row/column and width to draw itself. need to keep track of neighbors
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):  ##already looked at it means RED
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []  ##checking if row we are at is less than total rows minues 1. want to add 1 to go down a row
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  ##DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  ##UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  ##RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():  ##LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):  ##lt -> less than
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))


def make_grid(rows, width):
    grid = []
    gap = width // rows  ##// is integer division, gives us what the gap should be between each rows, ie width of each cube
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):  ##draw grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))  ##will tell us where to draw the grid line
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:  ##draw all the colors, grid lines on top and then draw everything
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:  ##while is running check every event and check what they are(ie keyboard, mouse cliked, timer)
        draw(win, grid, ROWS, width)  ##drawing every loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:  ##user can only click quit to prevent more clicking which will alter the algorithm
                continue

            if pygame.mouse.get_pressed()[0]:  ##left mouse button
                pos = pygame.mouse.get_pos()  ##get position of x,y coordinate of click
                row, col = get_clicked_pos(pos, ROWS, width)  ##get row and column on grid
                spot = grid[row][col]
                if not start and spot != end:  ##if start or end were not pressed once left mouse was clicked, make it the start or end
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  ##right mouse button
                pos = pygame.mouse.get_pos()  ##get position of x,y coordinate of click
                row, col = get_clicked_pos(pos, ROWS, width)  ##get row and column on grid
                spot = grid[row][col]
                spot.reset()  ##if first spot is right clicked, reset it to white to be able to change the position
                if spot == start:
                    start = None

                elif spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:  ##run the algorithm
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors() ##update neighbros if space is pressed and we've not started algorithm
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
    pygame.quit()


main(WIN, WIDTH)
