from classes.coordinates import Coordinate
from classes.global_vars import GlobalVars


class MoveUnit:
    """
    Клас для управління рухом об'єкта в грі.
    """
    def __init__(self, speed: float, coordinates: Coordinate) -> None:
        """
        Ініціалізація рухомого об'єкта.
        :param speed: Швидкість руху.
        :param coordinates: Поточні координати об'єкта.
        """
        self.speed: float = speed
        self.coordinates: Coordinate = coordinates
        self.direction: int = 0  # 0=право, 1=вниз, 2=влево, 3=вверх
        self.freeze: bool = False
        self._is_turn: float = -1

    def _reset_turn(self) -> None:
        """
        Скидає лічильник повороту.
        """
        self._is_turn = GlobalVars.tile_size

    def move(self, delta: float, new_direction: int, is_ghost: bool = False) -> float:
        """
        Виконує рух об'єкта та повертає пройдену відстань від центру.
        :param delta: Часовий крок руху.
        :param new_direction: Новий напрям руху.
        :param is_ghost: Чи є об'єкт привидом.
        :return: Відстань, яку пройшов об'єкт від центру тайла.
        """
        if self.freeze:
            return 0

        if (new_direction + self.direction) % 2 == 0:
            self.direction = new_direction

        tiles = GlobalVars.tilemap.get_neighbour_tiles(self.coordinates)
        dist: float = self.speed * delta * GlobalVars.tile_size
        self._is_turn -= dist
        center: Coordinate = Coordinate.get_tile_center(self.coordinates.x_tile, self.coordinates.y_tile)
        tile = GlobalVars.tilemap.get_tile(self.coordinates)
        dist = self._change_position(dist, center)

        if dist > 0:
            if not tiles[new_direction] or not tiles[self.direction]:
                if not tile:
                    if self.direction == 0 and self.coordinates.x_tile > 0:
                        self.coordinates.x_global -= (GlobalVars.tilemap.width + 2) * GlobalVars.tile_size
                    elif self.direction == 2 and self.coordinates.x_tile < 0:
                        self.coordinates.x_global += (GlobalVars.tilemap.width + 2) * GlobalVars.tile_size
                return dist

            if (new_direction + self.direction) % 2 == 1 and 0 > self._is_turn and \
                not (tiles[new_direction].is_wall or (tiles[new_direction].is_grates and not is_ghost)):
                self._change_position(-dist, center)
                self.direction = new_direction
                self._reset_turn()
                return self.move(dist / self.speed / GlobalVars.tile_size, new_direction, is_ghost)

            if tiles[self.direction].is_wall or (tiles[self.direction].is_grates and not is_ghost):
                self._change_position(-dist, center)

        return dist

    def _change_position(self, dist: float, center: Coordinate) -> float:
        """
        Оновлює координати об'єкта відповідно до напрямку руху.
        :param dist: Відстань переміщення.
        :param center: Центр поточного тайла.
        :return: Відстань від центру тайла після переміщення.
        """
        if self.direction == 0:  # вправо
            self.coordinates.x_global += dist
            return self.coordinates.x_global - center.x_global
        elif self.direction == 1:  # вниз
            self.coordinates.y_global += dist
            return self.coordinates.y_global - center.y_global
        elif self.direction == 2:  # вліво
            self.coordinates.x_global -= dist
            return -self.coordinates.x_global + center.x_global
        elif self.direction == 3:  # вгору
            self.coordinates.y_global -= dist
            return -self.coordinates.y_global + center.y_global
