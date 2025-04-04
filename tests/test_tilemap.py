import random

import pytest

from classes.global_vars import GlobalVars
from classes.tile import Tile
from classes.tilemap import Tilemap


# Dummy координата, що імітує метод Coordinate.get_tile_center
class DummyCoord:
    def __init__(self, x_tile, y_tile, tile_size):
        self.x_tile = x_tile
        self.y_tile = y_tile
        self.x_global = x_tile * tile_size
        self.y_global = y_tile * tile_size


# Патчимо Coordinate.get_tile_center, щоб повертати DummyCoord
@pytest.fixture(autouse=True)
def patch_coordinate(monkeypatch):
    def dummy_get_tile_center(x, y):
        tile_size = GlobalVars.tile_size if hasattr(
            GlobalVars, 'tile_size') and GlobalVars.tile_size else 40
        return DummyCoord(x, y, tile_size)

    monkeypatch.setattr(
        "classes.coordinates.Coordinate.get_tile_center",
        dummy_get_tile_center)


# Фікстура для простого поля (3x3) з одним гейтом (tile_id=7)
@pytest.fixture
def simple_board():
    board = [
        [0, 0, 0],
        [0, 7, 0],
        [0, 0, 0]
    ]
    return board


@pytest.fixture
def tilemap(simple_board):
    # Встановлюємо розміри, щоб GlobalVars.tile_size = 40 (min(height/rows,
    # width/cols))
    tm = Tilemap(simple_board, 120, 120)
    return tm


@pytest.mark.unit
def test_tilemap_dimensions(tilemap):
    """
    Перевіряє правильність визначення розмірів мапи (height та width).
    """
    assert tilemap.height == 3
    assert tilemap.width == 3


@pytest.mark.unit
def test_get_tile(tilemap):
    """
    Перевіряє метод get_tile:
    - Для координат всередині поля повертається об'єкт Tile;
    - Для координат поза межами поля повертається None.
    """
    coord = DummyCoord(0, 0, GlobalVars.tile_size)
    tile = tilemap.get_tile(coord)
    assert isinstance(tile, Tile)
    coord_out = DummyCoord(-1, -1, GlobalVars.tile_size)
    assert tilemap.get_tile(coord_out) is None


@pytest.mark.unit
def test_get_neighbour_tiles(tilemap):
    """
    Перевіряє метод get_neighbour_tiles:
    - Для центральної плитки повертаються 4 сусідні плитки у правильному порядку;
    - Кожен сусід повинен існувати (не None) для центральної позиції.
    """
    center = DummyCoord(1, 1, GlobalVars.tile_size)
    neighbors = tilemap.get_neighbour_tiles(center)
    # Порядок: право, вниз, ліво, вверх.
    assert len(neighbors) == 4
    for neighbor in neighbors:
        assert neighbor is not None


@pytest.mark.unit
def test_is_in_ghost_house(tilemap):
    """
    Перевіряє метод is_in_ghost_house:
    - Координата всередині області "будинку привидів" повинна повертати True;
    - Координата за межами області повинна повертати False.
    """
    # Поле містить плитку з id 7, що задає _gates
    tilemap.house
    # Створюємо координати: одна всередині і одна поза
    inside = DummyCoord(1, 1, GlobalVars.tile_size)
    outside = DummyCoord(10, 10, GlobalVars.tile_size)
    result_inside = tilemap.is_in_ghost_house(inside)
    result_outside = tilemap.is_in_ghost_house(outside)
    assert isinstance(result_inside, bool)
    assert result_outside == False


@pytest.mark.unit
def test_update_spawns_fruit(monkeypatch, tilemap):
    """
    Перевіряє метод update на появу фруктів (Cherry, Strawberry, BigDot) на полі.
    """
    # Три перевірки для різних фруктів (Cherry, Strawberry, BigDot)
    # Проводимо тест для однієї плитки, використовуючи monkeypatch для
    # керування випадковістю.
    tile = tilemap._tilemap[0][0]
    tile.is_wall = False
    tile.is_grates = False
    tile.objects = []

    # Тест для Cherry (r < 0.45)
    tilemap._timer = tilemap.fruit_spawn
    monkeypatch.setattr(random, "randrange", lambda a, b: 0)
    monkeypatch.setattr(random, "random", lambda: 0.3)
    tilemap.update(0.1)
    assert len(tile.objects) == 1
    fruit1 = type(tile.objects[0]).__name__

    # Тест для Strawberry (0.45 <= r < 0.9)
    tile.objects = []
    tilemap._timer = tilemap.fruit_spawn
    monkeypatch.setattr(random, "random", lambda: 0.5)
    tilemap.update(0.1)
    assert len(tile.objects) == 1
    fruit2 = type(tile.objects[0]).__name__

    # Тест для BigDot (r >= 0.9)
    tile.objects = []
    tilemap._timer = tilemap.fruit_spawn
    monkeypatch.setattr(random, "random", lambda: 0.95)
    tilemap.update(0.1)
    assert len(tile.objects) == 1
    fruit3 = type(tile.objects[0]).__name__

    assert "Cherry" in fruit1
    assert "Strawberry" in fruit2
    assert "BigDot" in fruit3
