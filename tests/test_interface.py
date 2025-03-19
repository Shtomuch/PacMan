import pytest
import pygame
from classes.interface import Interface
from classes.global_vars import GlobalVars
from classes.animation import Animation

@pytest.fixture
def setup_interface():
    """
    Фікстура для створення об'єкта Interface перед кожним тестом.
    """
    GlobalVars.tile_size = 10
    GlobalVars.score = 100
    GlobalVars.tilemap = type('MockTilemap', (), {'height': 20})()
    GlobalVars.screen = pygame.Surface((800, 600))
    GlobalVars.pacman = type('MockPacman', (), {'health': 3})()
    interface = Interface()
    yield interface
    del interface  # Очистимо після тестів

def test_pacman_health_initialization(setup_interface):
    """
    Перевіряємо, чи правильно ініціалізується панель здоров'я Pacman.
    """
    interface = setup_interface
    assert len(interface.health_bar.health) == 3  # Має бути 3 життя
    assert all(isinstance(h, Animation) for h in interface.health_bar.health)

def test_delete_health(setup_interface):
    """
    Перевіряємо, чи коректно зменшується кількість здоров'я.
    """
    interface = setup_interface
    initial_health_count = len(interface.health_bar.health)
    interface.delete_health()
    assert len(interface.health_bar.health) == initial_health_count - 1
    interface.delete_health()
    interface.delete_health()
    assert len(interface.health_bar.health) == 0  # Життів не залишилось

def test_delete_health_empty(setup_interface):
    """
    Перевіряємо, чи не відбувається помилка при видаленні здоров'я, коли його вже немає.
    """
    interface = setup_interface
    interface.health_bar.health.clear()
    try:
        interface.delete_health()
        assert True  # Якщо помилка не виникла, тест успішний
    except IndexError:
        pytest.fail("Виникла помилка IndexError при видаленні з порожнього списку.")

def test_draw_misc(setup_interface):
    """
    Перевіряємо, чи коректно малюється інтерфейс без помилок.
    """
    interface = setup_interface
    try:
        interface.draw_misc(0)
        assert True  # Якщо не виникає помилок, тест проходить
    except Exception as e:
        pytest.fail(f"Помилка при виклику draw_misc: {e}")
