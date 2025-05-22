import pygame
import numpy as np
import random
import sys


CELL = 30
COLS, ROWS = 10, 20
WIDTH, HEIGHT = CELL * COLS, CELL * ROWS
FPS = 60


colors = [
    (30, 30, 30), 
    (0, 255, 255),     # I
    (0, 0, 255),       # J
    (255, 165, 0),     # L
    (255, 255, 0),     # O
    (0, 255, 0),       # S
    (128, 0, 128),     # T
    (255, 0, 0)        # Z
]

shapes = [
    np.array([[1, 1, 1, 1]]),                    # I
    np.array([[2, 0, 0], [2, 2, 2]]),           # J
    np.array([[0, 0, 3], [3, 3, 3]]),           # L
    np.array([[4, 4], [4, 4]]),                 # O
    np.array([[0, 5, 5], [5, 5, 0]]),           # S
    np.array([[0, 6, 0], [6, 6, 6]]),           # T
    np.array([[7, 7, 0], [0, 7, 7]])            # Z
]

def get_shape_index(current):
    for i, shape in enumerate(shapes):
        if np.array_equal(current, shape):
            return i
    raise ValueError("Shape not found in shapes list")

def valid(grid, shape, offset):
    off_x, off_y = offset
    for y in range(shape.shape[0]):
        for x in range(shape.shape[1]):
            if shape[y, x]:
                if x + off_x < 0 or x + off_x >= COLS or y + off_y >= ROWS:
                    return False
                if grid[y + off_y, x + off_x]:
                    return False
    return True

def draw_grid(surface):
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(surface, (60, 60, 60), (x * CELL, y * CELL, CELL, CELL), 1)

def draw_block(surface, color, rect):
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (255, 255, 255), rect, 1)

def draw(screen, grid, shape, pos, color):
    screen.fill(colors[0])
    

    for y in range(shape.shape[0]):
        for x in range(shape.shape[1]):
            if shape[y, x]:
                draw_block(screen, colors[color], pygame.Rect((pos[0] + x) * CELL, (pos[1] + y) * CELL, CELL, CELL))
    

    for y in range(ROWS):
        for x in range(COLS):
            if grid[y, x]:
                draw_block(screen, colors[grid[y, x]], pygame.Rect(x * CELL, y * CELL, CELL, CELL))
    
  
    draw_grid(screen)
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, HEIGHT), 3)
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Тетріс")
    clock = pygame.time.Clock()
    

    grid = np.zeros((ROWS, COLS), dtype=int)

    current = random.choice(shapes)
    color = get_shape_index(current) + 1
    pos = [COLS // 2 - current.shape[1] // 2, 0]

    fall_timer = 0
    fall_delay = 600
    

    running = True
    while running:
        dt = clock.tick(FPS)
        fall_timer += dt
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_pos = pos[:]
                if event.key == pygame.K_LEFT:
                    new_pos[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    new_pos[0] += 1
                elif event.key == pygame.K_DOWN:
                    new_pos[1] += 1

                if valid(grid, current, new_pos):
                    pos = new_pos
        
    
        if fall_timer >= fall_delay:
            pos[1] += 1
            if not valid(grid, current, pos):
                pos[1] -= 1
                for y in range(current.shape[0]):
                    for x in range(current.shape[1]):
                        if current[y, x]:
                            grid[pos[1] + y, pos[0] + x] = color
                current = random.choice(shapes)
                color = get_shape_index(current) + 1
                pos = [COLS // 2 - current.shape[1] // 2, 0]
            fall_timer = 0
        
        
        draw(screen, grid, current, pos, color)
    
    pygame.quit()
    sys.exit()

if name == "main":
    main()
