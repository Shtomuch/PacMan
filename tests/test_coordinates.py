import pytest
from classes.coordinates import Coordinate
from classes.global_vars import GlobalVars

@pytest.fixture
def setup_tile_size():
    """
    Фікстура, щоб встановити розмір GlobalVars.tile_size до якогось тестового значення
    перед кожним тестом, і при потребі скинути його після.
    """
    GlobalVars.tile_size = 10
    yield
    # Якщо треба, можна скинути до попереднього значення або ініціалізувати іншим чином.

def test_x_tile_y_tile(setup_tile_size):
    coord = Coordinate(21, 39)
    # За tile_size = 10:
    #   x_tile = 21 // 10 = 2
    #   y_tile = 39 // 10 = 3
    assert coord.x_tile == 2
    assert coord.y_tile == 3

def test_get_tile_center(setup_tile_size):
    # Має повернути координати центру тайла (x, y),
    #  де центр = (x * tile_size + tile_size/2, y * tile_size + tile_size/2)
    c = Coordinate.get_tile_center(2, 3)
    # При tile_size=10 => x_center= 2*10+5=25, y_center=3*10+5=35
    assert c.x_global == 25
    assert c.y_global == 35

def test_to_center(setup_tile_size):
    coord = Coordinate(21, 39)
    shift = coord.to_center()
    # Тепер center буде (25,35)  (див. вище)
    # shift має дорівнювати (25-21, 35-39) = (4, -4)
    assert shift.x_global == 4
    assert shift.y_global == -4

def test_eq_true(setup_tile_size):
    # __eq__ повертає True, якщо різниця по X та Y < tile_size/3 => 10/3 ≈ 3.33
    c1 = Coordinate(20, 30)
    c2 = Coordinate(22.5, 32.5)  # різниця (2.5, 2.5) => 2.5 < 3.33 => мають бути рівні
    assert c1 == c2

def test_eq_false(setup_tile_size):
    # Тут різниця більша, ніж tile_size/3
    c1 = Coordinate(20, 30)
    c2 = Coordinate(24, 34)  # різниця (4, 4) => 4 >= 3.33 => не рівні
    assert c1 != c2

def test_str():
    c = Coordinate(1.2, 3.4)
    # Перевірка рядкового представлення
    assert str(c) == "(1.2, 3.4)"