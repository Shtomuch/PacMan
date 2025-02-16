from classes.global_vars import GlobalVars


class Coordinate:
    """
    Клас для роботи з координатами в грі.
    """
    def __init__(self, x: float, y: float) -> None:
        """
        Ініціалізація координат.
        :param x: Глобальна координата x.
        :param y: Глобальна координата y.
        """
        self.x_global: float = x
        self.y_global: float = y

    @property
    def x_tile(self) -> int:
        """
        Повертає індекс тайла по x.
        """
        return int(self.x_global // GlobalVars.tile_size)

    @property
    def y_tile(self) -> int:
        """
        Повертає індекс тайла по y.
        """
        return int(self.y_global // GlobalVars.tile_size)

    def to_center(self) -> "Coordinate":
        """
        Повертає координати до найближчого центру тайла.
        """
        c: Coordinate = self.get_tile_center(self.x_tile, self.y_tile)
        x: float = c.x_global - self.x_global
        y: float = c.y_global - self.y_global
        return Coordinate(x, y)

    @staticmethod
    def get_tile_center(x: int, y: int) -> "Coordinate":
        """
        Повертає глобальні координати центру тайла.
        :param x: Індекс тайла по x.
        :param y: Індекс тайла по y.
        :return: Координати центру тайла.
        """
        x_global: float = x * GlobalVars.tile_size + GlobalVars.tile_size / 2
        y_global: float = y * GlobalVars.tile_size + GlobalVars.tile_size / 2
        return Coordinate(x_global, y_global)
