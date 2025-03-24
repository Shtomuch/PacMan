from unittest.mock import MagicMock, patch

import pygame
import pytest

from classes.ghost import Blinky, Clyde, Inky, Pinky
from classes.global_vars import GlobalVars
# Припустимо, що ваш клас Level лежить у файлі level.py
from classes.level import Level
from classes.pacman import Pacman
from classes.tilemap import Tilemap


@pytest.fixture
def sample_board():
    """
    Спрощена матриця для tilemap.
    """
    return [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]


@pytest.fixture
def mock_pygame_display():
    """
    Підміняємо pygame.display.set_mode, щоб повернути фейковий Surface.
    Це дозволяє викликати screen.fill(...) без помилок.
    """
    with patch('pygame.display.set_mode') as mock_set_mode:
        fake_surface = MagicMock(spec=pygame.Surface)
        mock_set_mode.return_value = fake_surface
        yield fake_surface


@pytest.mark.usefixtures("mock_pygame_display")
class TestLevelInitialization:
    """
    Тести, що перевіряють лише базову ініціалізацію,
    без виклику складної логіки руху/колізій.
    """

    def test_init_creates_tilemap(self, sample_board):
        Level(sample_board)
        assert GlobalVars.tilemap is not None, "Tilemap не створився!"
        assert isinstance(GlobalVars.tilemap,
                          Tilemap), "GlobalVars.tilemap має бути Tilemap!"

    def test_init_creates_pacman_and_ghosts(self, sample_board):
        lvl = Level(sample_board, pacman_health=3)
        assert isinstance(GlobalVars.pacman,
                          Pacman), "GlobalVars.pacman має бути Pacman!"
        assert len(GlobalVars.ghosts) == 4, "Має бути 4 привиди!"
        ghost_types = {type(g) for g in GlobalVars.ghosts}
        assert {Blinky, Pinky, Inky, Clyde} == ghost_types

    def test_init_sets_pacman_health(self, sample_board):
        lvl = Level(sample_board, pacman_health=5)
        assert GlobalVars.pacman.health == 5, "Не встановилася кількість життів Pac-Man!"


@pytest.mark.usefixtures("mock_pygame_display")
class TestLevelUpdateBasic:
    """
    Мінімальний набір тестів для update, без виклику небезпечної логіки (руху, колізій).
    """

    def test_update_returns_false_on_quit_event(self, sample_board):
        """
        Якщо у черзі подій є pygame.QUIT, метод update має повернути False.
        """
        lvl = Level(sample_board)
        with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.QUIT)]):
            cont = lvl.update(delta=0.1)
        assert cont is False, "При наявності QUIT має повертати False!"

    def test_update_returns_false_if_pacman_health_zero(self, sample_board):
        """
        Якщо у Pac-Man закінчилося здоров'я, update має повернути False.
        """
        lvl = Level(sample_board, pacman_health=0)
        with patch('pygame.event.get', return_value=[]):
            cont = lvl.update(delta=0.1)
        assert cont is False, "Якщо здоров'я Pac-Man <= 0, метод update має повертати False!"
