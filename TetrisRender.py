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

    def _draw_start_screen(self, screen):
        screen.fill((20, 20, 40))
        font_huge = pygame.font.SysFont('consolas', 72, bold=True)
        font_medium = pygame.font.SysFont('consolas', 24)
        font_small = pygame.font.SysFont('consolas', 18)
        font_tiny = pygame.font.SysFont('consolas', 16)
        title_text = font_huge.render('TETRIS', True, (0, 255, 255))
        title_rect = title_text.get_rect(center=(TOTAL_WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)
        start_text = font_medium.render('Press ENTER to start', True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(TOTAL_WIDTH // 2, HEIGHT // 2))
        screen.blit(start_text, start_rect)
        controls = [
            "CONTROLS:",
            "← → - Move left/right",
            "↓ - Soft drop",
            "↑ - Rotate",
            "SPACE - Hard drop"
        ]
        for i, line in enumerate(controls):
            color = (255, 255, 0) if i == 0 else (200, 200, 200)
            font = font_small if i == 0 else font_tiny
            text = font.render(line, True, color)
            text_rect = text.get_rect(center=(TOTAL_WIDTH // 2, HEIGHT // 2 + 80 + i * 25))
            screen.blit(text, text_rect)
        exit_text = font_tiny.render('ESC - Exit', True, (150, 150, 150))
        exit_rect = exit_text.get_rect(center=(TOTAL_WIDTH // 2, HEIGHT - 50))
        screen.blit(exit_text, exit_rect)

    def _draw_game_over(self, screen, score, level):
        overlay = pygame.Surface((TOTAL_WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        box_width = 400
        box_height = 250
        box_x = (TOTAL_WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2
        pygame.draw.rect(screen, (40, 40, 40), (box_x, box_y, box_width, box_height), border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 3, border_radius=15)
        font_large = pygame.font.SysFont('consolas', 48, bold=True)
        font_medium = pygame.font.SysFont('consolas', 32)
        font_small = pygame.font.SysFont('consolas', 20)
        game_over_text = font_large.render('GAME OVER', True, (255, 50, 50))
        game_over_rect = game_over_text.get_rect(center=(TOTAL_WIDTH // 2, box_y + 50))
        screen.blit(game_over_text, game_over_rect)
        score_text = font_medium.render(f'Final score: {score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(TOTAL_WIDTH // 2, box_y + 110))
        screen.blit(score_text, score_rect)
        level_text = font_medium.render(f'Level reached: {level}', True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(TOTAL_WIDTH // 2, box_y + 150))
        screen.blit(level_text, level_rect)
        restart_text = font_small.render('Press R to restart', True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(TOTAL_WIDTH // 2, box_y + 190))
        screen.blit(restart_text, restart_rect)
        quit_text = font_small.render('or ESC to exit', True, (200, 200, 200))
        quit_rect = quit_text.get_rect(center=(TOTAL_WIDTH // 2, box_y + 210))
        screen.blit(quit_text, quit_rect)