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


class Grid:
    def __init__(self):
        self.cells = np.zeros((ROWS, COLS), dtype=int)

    def is_valid_position(self, piece, shape=None, x=None, y=None):
        blocks = piece.get_blocks(shape, x, y)
        for bx, by, _ in blocks:
            if bx < 0 or bx >= COLS or by >= ROWS:
                return False
            if by >= 0 and self.cells[by, bx]:
                return False
        return True

    def place_piece(self, piece):
        for bx, by, color in piece.get_blocks():
            self.cells[by, bx] = color
        return self.clear_lines()

    def clear_lines(self):
        non_full_rows = self.cells[np.any(self.cells == 0, axis=1)]
        cleared = ROWS - non_full_rows.shape[0]
        new_rows = np.zeros((cleared, COLS), dtype=int)
        self.cells = np.vstack([new_rows, non_full_rows])
        return cleared

    def reset(self):
        self.cells = np.zeros((ROWS, COLS), dtype=int)


class ScoreManager:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.lines_cleared = 0

    def add_lines(self, lines):
        self.lines_cleared += lines
        self.score += lines * 100 * self.level
        self.level = self.lines_cleared // 10 + 1

    def get_fall_delay(self):
        return max(50, 600 - (self.level - 1) * 50)

    def reset(self):
        self.score = 0
        self.level = 1
        self.lines_cleared = 0


class GameBase(ABC):
    def __init__(self):
        self.colors = [
            (30, 30, 30), (0, 255, 255), (0, 0, 255), (255, 165, 0),
            (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)
        ]

    @abstractmethod
    def run(self):
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

    def update(self, dt):
        if self.game_state == "playing" and not self.game_over:
            self.fall_timer += dt
            if self.fall_timer >= self.score_manager.get_fall_delay():
                self.current_piece.y += 1
                if not self.grid.is_valid_position(self.current_piece):
                    self.current_piece.y -= 1
                    self._place_piece()
                self.fall_timer = 0

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

    def render(self, screen, game):
        screen.fill(self.colors[0])
        if game.game_state == "start":
            self._draw_start_screen(screen)
        elif game.game_state == "playing":
            if not game.game_over:
                self._draw_ghost(screen, game.grid, game.current_piece)
                for bx, by, color in game.current_piece.get_blocks():
                    self._draw_block(screen, self.colors[color],
                                     pygame.Rect(bx * CELL, by * CELL, CELL, CELL))
            for y in range(ROWS):
                for x in range(COLS):
                    if game.grid.cells[y, x]:
                        self._draw_block(screen, self.colors[game.grid.cells[y, x]],
                                         pygame.Rect(x * CELL, y * CELL, CELL, CELL))
            self._draw_grid(screen)
            pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, HEIGHT), 3)
            self._draw_next_piece(screen, game.next_piece)
            font = pygame.font.SysFont('consolas', 24)
            score_text = font.render(f'Score: {game.score_manager.score}', True, (255, 255, 255))
            level_text = font.render(f'Level: {game.score_manager.level}', True, (255, 255, 255))
            screen.blit(score_text, (WIDTH + 20, 20))
            screen.blit(level_text, (WIDTH + 20, 50))
            font_small = pygame.font.SysFont('consolas', 16)
            controls = [
                "Controls:",
                "← → Move",
                "↓ Soft drop",
                "↑ Rotate",
                "Space Hard drop"
            ]
            for i, line in enumerate(controls):
                text = font_small.render(line, True, (200, 200, 200))
                screen.blit(text, (WIDTH + 20, 250 + i * 20))
            if game.game_over:
                self._draw_game_over(screen, game.score_manager.score, game.score_manager.level)
        pygame.display.flip()


if __name__ == "__main__":
    game = TetrisGame()
    game.run()