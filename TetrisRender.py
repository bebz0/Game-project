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

    def _draw_next_piece(self, screen, piece):
        preview_x = WIDTH + 20
        preview_y = 107
        font = pygame.font.SysFont('consolas', 20)
        text = font.render('NEXT:', True, (255, 255, 255))
        screen.blit(text, (preview_x, preview_y - 23))
        pygame.draw.rect(screen, (40, 40, 40), (preview_x - 5, preview_y - 5, 110, 110))
        pygame.draw.rect(screen, (100, 100, 100), (preview_x - 5, preview_y - 5, 110, 110), 2)
        offset_x = (4 - piece.shape.shape[1]) * CELL // 4
        offset_y = (4 - piece.shape.shape[0]) * CELL // 4
        for y in range(piece.shape.shape[0]):
            for x in range(piece.shape.shape[1]):
                if piece.shape[y, x]:
                    small_rect = pygame.Rect(
                        preview_x + x * 20 + offset_x,
                        preview_y + y * 20 + offset_y,
                        20, 20
                    )
                    self._draw_block(screen, self.colors[piece.color], small_rect)