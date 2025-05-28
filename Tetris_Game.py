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
