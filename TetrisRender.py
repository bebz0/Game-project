import pygame
import numpy as np
import random
import sys
import traceback

CELL = 30
COLS, ROWS = 10, 20
WIDTH, HEIGHT = CELL * COLS, CELL * ROWS
PREVIEW_WIDTH = 170
TOTAL_WIDTH = WIDTH + PREVIEW_WIDTH
FPS = 60

class TetrisRenderer:
    def __init__(self, colors):
        self.colors = colors

    def _draw_grid(self, surface):
        for y in range(ROWS):
            for x in range(COLS):
                pygame.draw.rect(surface, (60, 60, 60), (x * CELL, y * CELL, CELL, CELL), 1)

    def _draw_block(self, surface, color, rect):
        pygame.draw.rect(surface, color, rect, border_radius=6)
        pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=6)

    def _draw_ghost(self, screen, grid, piece):
        ghost_y = piece.y
        while grid.is_valid_position(piece, y=ghost_y + 1):
            ghost_y += 1
        for bx, by, color in piece.get_blocks(y=ghost_y):
            rect = pygame.Rect(bx * CELL, by * CELL, CELL, CELL)
            s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
            s.fill((*self.colors[color][:3], 40))
            screen.blit(s, rect.topleft)