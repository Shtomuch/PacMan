import pytest
from unittest.mock import Mock
from classes.coordinates import Coordinate
from classes.global_vars import GlobalVars
from classes.move_unit import MoveUnit


@pytest.fixture
def mock_global_vars():
    """Фікстура для підготовки GlobalVars."""
    GlobalVars.tile_size = 10
    GlobalVars.tilemap = Mock()
    GlobalVars.tilemap.width = 20
    GlobalVars.tilemap.get_neighbour_tiles.return_value = [Mock(is_wall=False, is_grates=False)] * 4
    GlobalVars.tilemap.get_tile.return_value = Mock(is_wall=False, is_grates=False)


@pytest.fixture
def move_unit(mock_global_vars):
    """Фікстура для створення MoveUnit."""
    coordinates = Coordinate(44, 44)
    move = MoveUnit(speed=2, coordinates=coordinates)
    return move


@pytest.mark.parametrize("new_direction, expected_direction", [
    (0, 0), (1, 1), (2, 2), (3, 3)
])
def test_move_unit_initial_direction(move_unit, new_direction, expected_direction):
    """Перевіряємо, чи змінюється напрямок руху після `move`"""
    move_unit.move(0.1, new_direction)
    assert move_unit.direction == expected_direction


def test_move_unit_freeze(move_unit):
    """Перевіряємо, що якщо `freeze=True`, рух не відбувається."""
    move_unit.freeze = True
    dist = move_unit.move(0.1, 1)
    assert dist == 0


def test_move_unit_wall_collision(move_unit):
    """Перевіряємо, що рух зупиняється при зіткненні зі стіною."""
    GlobalVars.tilemap.get_neighbour_tiles.return_value[1].is_wall = True
    move_unit.direction = 1
    c = Coordinate.get_tile_center(move_unit.coordinates.x_tile, move_unit.coordinates.y_tile).y_global
    move_unit.move(0.1, 1)
    assert abs(move_unit.coordinates.y_global - c) < 1e-10 # Персонаж не повинен пройти крізь стіну


def test_move_unit_teleport(move_unit):
    """Перевіряємо, чи працює телепортація через край карти."""
    move_unit.coordinates.x_global = -GlobalVars.tile_size*2
    move_unit.direction = 2
    GlobalVars.tilemap.get_tile.return_value = None
    GlobalVars.tilemap.get_neighbour_tiles.return_value[2] = None
    move_unit.move(0.1, 2)
    assert move_unit.coordinates.x_global > 0  # Персонаж має телепортуватися вправо

@pytest.mark.parametrize("direction, new_direction", [
    (0, 1), (0, 3), (1, 2), (1, 0)
])
def test_move_unit_initial_direction(move_unit, direction, new_direction):
    """Перевіряємо, чи змінюється напрямок руху після `move`"""
    move_unit.direction = direction
    move_unit.move(0.1, new_direction)
    assert move_unit._is_turn > 0
