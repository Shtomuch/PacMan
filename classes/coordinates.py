from classes.global_vars import GlobalVars

class Coordinate:
    def __init__(self, x, y):
        self.x_global = x
        self.y_global = y

    @property
    def x_tile(self) -> int:
        """Повертає індекс тайла по осі X."""
        return int(self.x_global // GlobalVars.tile_size)

    @property
    def y_tile(self) -> int:
        """Повертає індекс тайла по осі Y."""
        return int(self.y_global // GlobalVars.tile_size)

    def to_center(self) -> "Coordinate":
        """Повертає координати центру найближчого тайла."""
        center = Coordinate.get_tile_center(self.x_tile, self.y_tile)
        return Coordinate(center.x_global - self.x_global, center.y_global - self.y_global)

    @staticmethod
    def get_tile_center(x, y) -> "Coordinate":
        """Повертає глобальні координати центру тайла."""
        x_center = x * GlobalVars.tile_size + GlobalVars.tile_size / 2
        y_center = y * GlobalVars.tile_size + GlobalVars.tile_size / 2
        return Coordinate(x_center, y_center)

    def __eq__(self, other):
        return (abs(self.x_global - other.x_global) < GlobalVars.tile_size / 3 and
                abs(self.y_global - other.y_global) < GlobalVars.tile_size / 3)

    def __str__(self):
        return f"({self.x_global}, {self.y_global})"