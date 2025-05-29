import pygame
import numpy as np
import random
import sys
import traceback
from abc import ABC, abstractmethod

CELL = 30
COLS, ROWS = 10, 20
WIDTH, HEIGHT = CELL * COLS, CELL * ROWS
PREVIEW_WIDTH = 170
TOTAL_WIDTH = WIDTH + PREVIEW_WIDTH
FPS = 60

class GameBase(ABC):
    def __init__(self):
        pass

class Grid():
    def __init__(self):
        pass

class ScoreManager()
    def __init__(self):
        pass

class Piece():
    def __init__(self):
        pass



class TetrisGame(GameBase):
    def __init__(self):
        super().__init__()
        self.grid = Grid()
        self.score_manager = ScoreManager()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.fall_timer = 0
        self.game_over = False
        self.game_state = "start"

class TetrisRenderer():
    def __init__(self):




    def handle_input(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if self.game_state == "start":
                if event.key == pygame.K_RETURN:
                    self.game_state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    return False
            elif self.game_state == "playing":
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "start"
                        self.reset()
                else:
                    new_x, new_y = self.current_piece.x, self.current_piece.y
                    new_shape = self.current_piece.shape
                    if event.key == pygame.K_LEFT:
                        new_x -= 1
                    elif event.key == pygame.K_RIGHT:
                        new_x += 1
                    elif event.key == pygame.K_DOWN:
                        new_y += 1
                    elif event.key == pygame.K_UP:
                        new_shape = self.current_piece.rotate()
                    elif event.key == pygame.K_SPACE:
                        while self.grid.is_valid_position(self.current_piece, y=self.current_piece.y + 1):
                            self.current_piece.y += 1
                        self._place_piece()
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "start"
                        self.reset()
                    if self.grid.is_valid_position(self.current_piece, new_shape, new_x, new_y):
                        self.current_piece.x, self.current_piece.y = new_x, new_y
                        self.current_piece.shape = new_shape
        return True

    def _place_piece(self):
        cleared = self.grid.place_piece(self.current_piece)
        self.score_manager.add_lines(cleared)
        self.current_piece = self.next_piece
        self.next_piece = Piece()
        if not self.grid.is_valid_position(self.current_piece):
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.score_manager.reset()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.fall_timer = 0
        self.game_over = False

    def update(self, dt):
        if self.game_state == "playing" and not self.game_over:
            self.fall_timer += dt
            if self.fall_timer >= self.score_manager.get_fall_delay():
                self.current_piece.y += 1
                if not self.grid.is_valid_position(self.current_piece):
                    self.current_piece.y -= 1
                    self._place_piece()
                self.fall_timer = 0

    def run(self):
        try:
            pygame.init()
            screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
            pygame.display.set_caption("Tetris")
            clock = pygame.time.Clock()
            renderer = TetrisRenderer(self.colors)
            running = True

            while running:
                dt = clock.tick(FPS)
                for event in pygame.event.get():
                    running = self.handle_input(event)
                self.update(dt)
                renderer.render(screen, self)
            pygame.quit()

        except Exception as e:
            print(e)
            traceback.print_exc()
            pygame.quit()
            sys.exit()



