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