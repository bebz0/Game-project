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
    (0, 255, 255),  # I
    (0, 0, 255),  # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),  # S
    (128, 0, 128),  # T
    (255, 0, 0)  # Z
]

shapes = [
    np.array([[1, 1, 1, 1]]),  # I
    np.array([[2, 0, 0], [2, 2, 2]]),  # J
    np.array([[0, 0, 3], [3, 3, 3]]),  # L
    np.array([[4, 4], [4, 4]]),  # O
    np.array([[0, 5, 5], [5, 5, 0]]),  # S
    np.array([[0, 6, 0], [6, 6, 6]]),  # T
    np.array([[7, 7, 0], [0, 7, 7]])  # Z
]


def get_shape_index(current):
    for i, shape in enumerate(shapes):
        if np.array_equal(current, shape):
            return i
    raise ValueError("Shape not found in shapes list")


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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw(screen, grid, current, pos, color)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()