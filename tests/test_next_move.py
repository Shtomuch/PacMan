from unittest.mock import Mock

import pytest

from classes.next_move import NextMove


@pytest.fixture(autouse=True)
def reset_next_move():
    """Перед кожним тестом очищаємо список подій."""
    NextMove.list_of_events = []


@pytest.mark.parametrize("name, expected_id", [
    ("tile", 0),
    ("point", 1),
    ("power", 2),
    ("pacman", 3),
    ("ghost", 4),
    ("interface", 5),
])
def test_next_move_initialization(name, expected_id):
    """Тестуємо правильність створення об'єкта NextMove."""
    func_mock = Mock()
    move = NextMove(name, func_mock)

    assert move.id == expected_id
    assert move.func == func_mock
    assert NextMove.list_of_events[expected_id][-1] == func_mock


def test_add_func():
    """Перевіряємо, що функція додається в правильний список подій."""
    func_mock = Mock()
    NextMove("pacman", func_mock)

    assert func_mock in NextMove.list_of_events[3]


def test_activate():
    """Перевіряємо, що функції викликаються при `activate`."""
    func_mock_1 = Mock()
    func_mock_2 = Mock()

    NextMove("tile", func_mock_1)
    NextMove("pacman", func_mock_2)

    NextMove.activate(0.1)

    func_mock_1.assert_called_once_with(0.1)
    func_mock_2.assert_called_once_with(0.1)


def test_remove_func():
    """Перевіряємо, що функція видаляється з черги подій."""
    func_mock = Mock()
    move = NextMove("point", func_mock)

    assert func_mock in NextMove.list_of_events[1]

    move.remove_func()
    assert func_mock not in NextMove.list_of_events[1]
