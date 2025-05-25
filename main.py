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


def get_shape_index(current):
    for i, shape in enumerate(shapes):
        if np.array_equal(current, shape):
            return i
    raise ValueError("Shape not found in shapes list")


def rotate(shape):
    return np.rot90(shape, k=-1)


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


def clear_rows(grid):
    non_full_rows = grid[np.any(grid == 0, axis=1)]
    cleared = ROWS - non_full_rows.shape[0]
    new_rows = np.zeros((cleared, COLS), dtype=int)
    return np.vstack([new_rows, non_full_rows]), cleared


def draw_grid(surface):
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(surface, (60, 60, 60), (x * CELL, y * CELL, CELL, CELL), 1)


def draw_block(surface, color, rect):
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=6)


def draw_ghost(screen, grid, shape, pos, color):
    ghost_pos = pos[:]
    while valid(grid, shape, [ghost_pos[0], ghost_pos[1] + 1]):
        ghost_pos[1] += 1
    for y in range(shape.shape[0]):
        for x in range(shape.shape[1]):
            if shape[y, x]:
                rect = pygame.Rect((ghost_pos[0] + x) * CELL, (ghost_pos[1] + y) * CELL, CELL, CELL)
                s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
                s.fill((*colors[color][:3], 40))
                screen.blit(s, rect.topleft)


def draw_next_piece(screen, next_shape, next_color):
    preview_x = WIDTH + 20
    preview_y = 107

    font = pygame.font.SysFont('consolas', 20)
    text = font.render('NEXT:', True, (255, 255, 255))
    screen.blit(text, (preview_x, preview_y - 23))

    pygame.draw.rect(screen, (40, 40, 40), (preview_x - 5, preview_y - 5, 110, 110))
    pygame.draw.rect(screen, (100, 100, 100), (preview_x - 5, preview_y - 5, 110, 110), 2)

    offset_x = (4 - next_shape.shape[1]) * CELL // 4
    offset_y = (4 - next_shape.shape[0]) * CELL // 4

    for y in range(next_shape.shape[0]):
        for x in range(next_shape.shape[1]):
            if next_shape[y, x]:
                small_rect = pygame.Rect(
                    preview_x + x * 20 + offset_x,
                    preview_y + y * 20 + offset_y,
                    20, 20
                )
                draw_block(screen, colors[next_color], small_rect)


def draw_start_screen(screen):
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


def draw_game_over(screen, score, level):
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

    restart_text = font_small.render('Press R to restar', True, (200, 200, 200))
    restart_rect = restart_text.get_rect(center=(TOTAL_WIDTH // 2, box_y + 190))
    screen.blit(restart_text, restart_rect)

    quit_text = font_small.render('or ESC to exit', True, (200, 200, 200))
    quit_rect = quit_text.get_rect(center=(TOTAL_WIDTH // 2, box_y + 210))
    screen.blit(quit_text, quit_rect)


def draw(screen, grid, shape, pos, color, next_shape, next_color, score, level):
    screen.fill(colors[0])

    draw_ghost(screen, grid, shape, pos, color)

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

    draw_next_piece(screen, next_shape, next_color)

    font = pygame.font.SysFont('consolas', 24)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    level_text = font.render(f'Level: {level}', True, (255, 255, 255))
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

    pygame.display.flip()


def init_game():
    grid = np.zeros((ROWS, COLS), dtype=int)
    current = random.choice(shapes)
    next_shape = random.choice(shapes)
    color = get_shape_index(current) + 1
    next_color = get_shape_index(next_shape) + 1
    pos = [COLS // 2 - current.shape[1] // 2, 0]
    score = 0
    level = 1
    lines_cleared = 0
    fall_timer = 0
    fall_delay = 600

    return grid, current, next_shape, color, next_color, pos, score, level, lines_cleared, fall_timer, fall_delay


def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
        pygame.display.set_caption("Тетріс")
        clock = pygame.time.Clock()

        game_state = "start"
        grid, current, next_shape, color, next_color, pos, score, level, lines_cleared, fall_timer, fall_delay = init_game()
        game_over = False
        running = True

        while running:
            dt = clock.tick(FPS)

            if game_state == "playing" and not game_over:
                fall_timer += dt
                level = lines_cleared // 10 + 1
                fall_delay = max(50, 600 - (level - 1) * 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if game_state == "start":
                        if event.key == pygame.K_RETURN:
                            game_state = "playing"
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                    elif game_state == "playing":
                        if game_over:
                            if event.key == pygame.K_r:
                                grid, current, next_shape, color, next_color, pos, score, level, lines_cleared, fall_timer, fall_delay = init_game()
                                game_over = False
                            elif event.key == pygame.K_ESCAPE:
                                game_state = "start"
                                game_over = False
                        else:
                            new_pos = pos[:]
                            new_shape = current
                            if event.key == pygame.K_LEFT:
                                new_pos[0] -= 1
                            elif event.key == pygame.K_RIGHT:
                                new_pos[0] += 1
                            elif event.key == pygame.K_DOWN:
                                new_pos[1] += 1
                            elif event.key == pygame.K_UP:
                                new_shape = rotate(current)
                            elif event.key == pygame.K_SPACE:
                                while valid(grid, current, [pos[0], pos[1] + 1]):
                                    pos[1] += 1
                                for y in range(current.shape[0]):
                                    for x in range(current.shape[1]):
                                        if current[y, x]:
                                            grid[pos[1] + y, pos[0] + x] = color
                                grid, cleared = clear_rows(grid)
                                score += cleared * 100 * level
                                lines_cleared += cleared
                                current = next_shape
                                next_shape = random.choice(shapes)
                                color = next_color
                                next_color = get_shape_index(next_shape) + 1
                                pos = [COLS // 2 - current.shape[1] // 2, 0]
                                if not valid(grid, current, pos):
                                    game_over = True
                                continue
                            elif event.key == pygame.K_ESCAPE:
                                game_state = "start"
                                grid, current, next_shape, color, next_color, pos, score, level, lines_cleared, fall_timer, fall_delay = init_game()
                            if valid(grid, new_shape, new_pos):
                                pos, current = new_pos, new_shape

            if game_state == "playing" and not game_over and fall_timer >= fall_delay:
                pos[1] += 1
                if not valid(grid, current, pos):
                    pos[1] -= 1
                    for y in range(current.shape[0]):
                        for x in range(current.shape[1]):
                            if current[y, x]:
                                grid[pos[1] + y, pos[0] + x] = color
                    grid, cleared = clear_rows(grid)
                    score += cleared * 100 * level
                    lines_cleared += cleared
                    current = next_shape
                    next_shape = random.choice(shapes)
                    color = next_color
                    next_color = get_shape_index(next_shape) + 1
                    pos = [COLS // 2 - current.shape[1] // 2, 0]
                    if not valid(grid, current, pos):
                        game_over = True
                fall_timer = 0

            if game_state == "start":
                draw_start_screen(screen)
                pygame.display.flip()
            elif game_state == "playing":
                if not game_over:
                    draw(screen, grid, current, pos, color, next_shape, next_color, score, level)
                else:
                    screen.fill(colors[0])
                    for y in range(ROWS):
                        for x in range(COLS):
                            if grid[y, x]:
                                draw_block(screen, colors[grid[y, x]], pygame.Rect(x * CELL, y * CELL, CELL, CELL))
                    draw_grid(screen)
                    pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, HEIGHT), 3)
                    draw_game_over(screen, score, level)
                    pygame.display.flip()

    except Exception as e:
        print(e)
        traceback.print_exc()
        pygame.quit()
        sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
