import random
from typing import List, Callable, Union, Optional

from classes.coordinates import Coordinate
from classes.tile import Tile
from classes.point import Dot, BigDot, Cherry, Strawberry  # Припускаємо, що Cherry і Strawberry також тут
from classes.global_vars import GlobalVars
from classes.next_move import NextMove


class Tilemap:
    """
    Клас для побудови та управління картою плиток.
    """

    def __init__(self, board: List[List[int]], max_height: float, max_width: float) -> None:
        """
        Ініціалізуємо карту плиток.

        :param board: Двовимірний список, де кожне значення — це ідентифікатор плитки.
        :param max_height: Максимальна висота ігрової зони.
        :param max_width: Максимальна ширина ігрової зони.
        """
        # Розрахунок розміру плитки за висотою та шириною
        h: float = max_height / len(board)
        w: float = max_width / len(board[0])
        GlobalVars.tile_size = min(h, w)

        # Спочатку board – це список списків чисел, пізніше перетворимо його в список списків Tile
        self._tilemap: List[List[Tile]] = board  # type: ignore
        # Ініціалізуємо координати гейту поза межами карти
        self._gates: Coordinate = Coordinate(-100, -100)
        self.construct_tilemap()

        self._timer: float = 0
        self.fruit_spawn: float = 2
        # Ініціалізуємо об'єкт для відкладеного виклику оновлення
        self.next_move: NextMove = NextMove('point', self.update)

    @property
    def house(self) -> Coordinate:
        """
        Повертає координати центру будинку привидів.
        """
        return Coordinate(self._gates.x_global, self._gates.y_global + GlobalVars.tile_size * 2)

    @property
    def pacman_fp(self) -> Coordinate:
        """
        Повертає координати стартової позиції Pac-Man.
        """
        return Coordinate(self._gates.x_global, self._gates.y_global + GlobalVars.tile_size * 5)

    def construct_tilemap(self) -> None:
        """
        Створює карту плиток на основі двовимірного масиву board.
        Кожен елемент board перетворюється у об'єкт Tile.
        """
        # Функція для генерації точок (dot) з можливістю генерації BigDot
        dot_func: Callable[[Coordinate], Union[Dot, BigDot]] = Tilemap.start_generate_dots()

        for y, row in enumerate(self._tilemap):
            for x, tile_id in enumerate(row):
                # Отримуємо центр плитки за координатами x, y
                coord: Coordinate = Coordinate.get_tile_center(x, y)
                tile_obj: Tile = Tile(coord, tile_id)

                # Якщо плитка порожня (tile_id == 0) та не знаходиться в будинку привидів, додаємо точку
                if tile_id == 0 and not self.is_in_ghost_house(coord):
                    tile_obj.add_object(dot_func(tile_obj.coordinates))
                # Якщо плитка з ідентифікатором 7 відповідає за розташування гейту, зберігаємо його координати
                elif tile_id == 7:
                    self._gates = Coordinate(tile_obj.coordinates.x_global - GlobalVars.tile_size * 0.5,
                                             tile_obj.coordinates.y_global)

                # Замінюємо значення у карті на об'єкт Tile
                self._tilemap[y][x] = tile_obj

    @staticmethod
    def start_generate_dots() -> Callable[[Coordinate], Union[Dot, BigDot]]:
        """
        Повертає функцію, яка генерує об'єкт Dot або BigDot на основі випадковості.

        :return: Функція, яка приймає координати та повертає Dot або BigDot.
        """
        chance: float = 0.02

        def inner(coord: Coordinate) -> Union[Dot, BigDot]:
            nonlocal chance
            if random.random() < chance:
                chance = 0.001
                return BigDot(coord)
            else:
                chance *= 1.05
                return Dot(coord)

        return inner

    @property
    def height(self) -> int:
        """
        Повертає кількість рядків у карті плиток.
        """
        return len(self._tilemap)

    @property
    def width(self) -> int:
        """
        Повертає кількість плиток у першому рядку карти.
        """
        return len(self._tilemap[0])

    def get_neighbour_tiles(self, coordinate: Coordinate) -> List[Optional[Tile]]:
        """
        Повертає список сусідніх плиток у порядку: право, вниз, ліво, вверх.

        :param coordinate: Координата плитки, для якої шукаємо сусідів.
        :return: Список сусідніх об'єктів Tile або None, якщо сусідньої плитки немає.
        """
        tx: int = coordinate.x_tile
        ty: int = coordinate.y_tile
        neighbors: List[Optional[Tile]] = []
        # Напрямки: право (0, +1), вниз (+1, 0), ліво (0, -1), вверх (-1, 0)
        for (dy, dx) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ny: int = ty + dy
            nx: int = tx + dx
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append(self._tilemap[ny][nx])
            else:
                neighbors.append(None)
        return neighbors

    def get_tile(self, coordinate: Coordinate) -> Optional[Tile]:
        """
        Повертає плитку за заданими координатами.

        :param coordinate: Координата плитки.
        :return: Об'єкт Tile або None, якщо координати виходять за межі карти.
        """
        tx: int = coordinate.x_tile
        ty: int = coordinate.y_tile
        if 0 <= tx < self.width and 0 <= ty < self.height:
            return self._tilemap[ty][tx]
        return None

    def is_in_ghost_house(self, coord: Coordinate) -> bool:
        """
        Перевіряє, чи знаходиться плитка (за її центром) в межах будинку привидів.

        :param coord: Координата плитки.
        :return: True, якщо плитка знаходиться в будинку привидів, інакше False.
        """
        # Центр будинку привидів
        house_center: Coordinate = self.house
        left_bound: float = house_center.x_global - GlobalVars.tile_size * 2.5
        right_bound: float = house_center.x_global + GlobalVars.tile_size * 2.5
        top_bound: float = house_center.y_global - GlobalVars.tile_size * 1.5
        bottom_bound: float = house_center.y_global + GlobalVars.tile_size * 1.5

        x: float = coord.x_global
        y: float = coord.y_global
        return left_bound <= x <= right_bound and top_bound <= y <= bottom_bound

    def update(self, delta: float) -> None:
        """
        Оновлює стан карти: рахує таймер, генерує фрукти/об'єкти на плитках через певний інтервал.

        :param delta: Зміна часу з останнього оновлення.
        """
        self._timer += delta
        if self._timer < self.fruit_spawn:
            return
        # Скидання таймера після спавну
        self._timer -= self.fruit_spawn

        # Випадкове обрання координат плитки
        x: int = random.randrange(0, self.width)
        y: int = random.randrange(0, self.height)
        tile: Tile = self._tilemap[y][x]
        # Перевірка, що плитка не є стіною, ґратами, вже має об'єкти або знаходиться в будинку привидів
        if not tile.is_wall and not tile.is_grates and not tile.objects and not self.is_in_ghost_house(
                tile.coordinates):
            r: float = random.random()
            # Генерація різних об'єктів на плитці за ймовірністю
            if r < 0.45:
                tile.objects.append(Cherry(tile.coordinates))
            elif r < 0.9:
                tile.objects.append(Strawberry(tile.coordinates))
            else:
                tile.objects.append(BigDot(tile.coordinates))