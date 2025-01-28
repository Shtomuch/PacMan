class Coordinate:

    size = 10
    def __init__(self, x, y):
        self.x_global = x
        self.y_global = y

    def get_x_tile(self) -> int:
        return self.x_global // self.size

    def get_y_tile(self) -> int:
        return self.y_global // self.size