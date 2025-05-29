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