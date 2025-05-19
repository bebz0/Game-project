import pygame
import numpy as np
import sys

CELL = 30
COLS, ROWS = 10, 20
WIDTH, HEIGHT = CELL * COLS, CELL * ROWS
FPS = 60


colors = [
    (30, 30, 30),      
    (0, 255, 255),     
    (0, 0, 255),       
    (255, 165, 0),     
    (255, 255, 0),     
    (0, 255, 0),       
    (128, 0, 128),     
    (255, 0, 0)        
]


shapes = [
    np.array([[1, 1, 1, 1]]),                    
    np.array([[2, 0, 0], [2, 2, 2]]),          
    np.array([[0, 0, 3], [3, 3, 3]]),           
    np.array([[4, 4], [4, 4]]),                 
    np.array([[0, 5, 5], [5, 5, 0]]),           
    np.array([[0, 6, 0], [6, 6, 6]]),           
    np.array([[7, 7, 0], [0, 7, 7]])            
]

def draw_grid(surface):
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(surface, (60, 60, 60), (x * CELL, y * CELL, CELL, CELL), 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(colors[0])
        draw_grid(screen)
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, HEIGHT), 3)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if name == "main":
    main()
