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

class Piece:
    SHAPES = [
        np.array([[1, 1, 1, 1]]),      
        np.array([[2, 0, 0], [2, 2, 2]]),  
        np.array([[0, 0, 3], [3, 3, 3]]),  
        np.array([[4, 4], [4, 4]]),        
        np.array([[0, 5, 5], [5, 5, 0]]),  
        np.array([[0, 6, 0], [6, 6, 6]]),  
        np.array([[7, 7, 0], [0, 7, 7]])   
    ]

    def __init__(self, shape_idx=None):
        if shape_idx is None:
            shape_idx = random.randint(0, len(self.SHAPES) - 1)
        self.shape = self.SHAPES[shape_idx].copy()
        self.color = shape_idx + 1
        self.x = COLS // 2 - self.shape.shape[1] // 2
        self.y = 0

    def rotate(self):
        return np.rot90(self.shape, k=-1)

    def get_blocks(self, shape=None, x=None, y=None):
        if shape is None: shape = self.shape
        if x is None: x = self.x
        if y is None: y = self.y
        blocks = []
        for row in range(shape.shape[0]):
            for col in range(shape.shape[1]):
                if shape[row, col]:
                    blocks.append((x + col, y + row, self.color))
        return blocks