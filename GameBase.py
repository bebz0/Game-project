class GameBase(ABC):
    def __init__(self):
        self.colors = [
            (30, 30, 30), (0, 255, 255), (0, 0, 255), (255, 165, 0),
            (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)
        ]

    @abstractmethod
    def run(self):
        pass


if __name__ == "__main__":
    game = TetrisGame()
    game.run()