import pytest
from unittest.mock import patch, MagicMock
import pygame
import os

# Припустимо, що Dot лежить у файлі classes/dot.py
from classes.dot import Dot
from classes.coordinates import Coordinate
from classes.global_vars import GlobalVars
from classes.animation_set import AnimationSet

@pytest.fixture
def mock_pygame_image():
    """
    Фікстура, що підміняє pygame.image.load і pygame.transform.scale,
    аби не завантажувати реальні файли під час тестів.
    """
    with patch('pygame.image.load', return_value=MagicMock(spec=pygame.Surface)) as mock_load, \
         patch('pygame.transform.scale', return_value=MagicMock(spec=pygame.Surface)) as mock_scale:
        yield (mock_load, mock_scale)

@pytest.fixture
def mock_os_path_join():
    """
    Фікстура, що підміняє os.path.join, щоб не залежати від реальної файлової системи.
    """
    with patch('os.path.join', side_effect=lambda *args: "/".join(args)) as mock_join:
        yield mock_join


# ------------------ ТЕСТ КОНСТРУКТОРА (__init__) ------------------
@pytest.mark.usefixtures("mock_pygame_image", "mock_os_path_join")
def test_dot_init():
    """
    Перевіряє, що у Dot:
      - зберігаються координати
      - створюється animation, score, next_move
    """
    GlobalVars.tile_size = 16
    coord = Coordinate(10, 20)
    dot = Dot(coord)

    assert dot.coordinates == coord, "Dot має зберігати передані координати."
    assert hasattr(dot, 'animation'), "Dot має поле animation."
    assert hasattr(dot, 'score'), "Dot має поле score."
    assert hasattr(dot, 'next_move'), "Dot має поле next_move."


# ------------------ ТЕСТ СТАТИЧНОГО МЕТОДУ get_images() ------------------
@pytest.mark.usefixtures("mock_pygame_image", "mock_os_path_join")
def test_dot_get_images():
    """
    Перевіряє, що get_images() повертає список із 1 AnimationSet,
    у якого 2 кадри.
    """
    GlobalVars.tile_size = 32
    frames = Dot.get_images()
    # Очікуємо, що буде рівно 1 AnimationSet
    assert len(frames) == 1, "Dot.get_images має повертати список із 1 AnimationSet."
    anim_set = frames[0]
    assert isinstance(anim_set, AnimationSet), "Повернений елемент має бути AnimationSet."
    # Перевіримо, що в AnimationSet.frames є 2 кадри
    assert len(anim_set.frames) == 2, "Dot має мати 2 кадри (coin.png і smaller_coin.png)."
    assert anim_set.name == "dot_animation", "Назва анімації має бути 'dot_animation'."


# ------------------ ТЕСТ МЕТОДУ update(delta) ------------------
def test_dot_update():
    """
    Перевіряємо, що update(delta) викликає animation.update(delta).
    """
    # Створимо Dot із замоканою анімацією
    with patch('classes.dot.Animation', autospec=True) as mock_anim_class:
        mock_anim = MagicMock()
        mock_anim_class.return_value = mock_anim

        dot = Dot(Coordinate(5, 5))
        dot.update(delta=0.1)
        # Перевіряємо, чи викликали animation.update(0.1)
        mock_anim.update.assert_called_once_with(0.1)


# ------------------ ТЕСТ МЕТОДУ disappear() ------------------
def test_dot_disappear():
    """
    Перевіряємо, що disappear():
      - викликає score.active()
      - викликає next_move.remove_func()
    """
    with patch('classes.dot.Animation', autospec=True), \
         patch('classes.dot.Score', autospec=True) as mock_score_class, \
         patch('classes.dot.NextMove', autospec=True) as mock_nextmove_class:
        # Створимо підроблені об'єкти для score і next_move
        mock_score_obj = MagicMock()
        mock_score_class.return_value = mock_score_obj

        mock_nextmove_obj = MagicMock()
        mock_nextmove_class.return_value = mock_nextmove_obj

        dot = Dot(Coordinate(10, 10))
        dot.disappear()

        # Перевіряємо, що викликалися score.active() і next_move.remove_func()
        mock_score_obj.active.assert_called_once()
        mock_nextmove_obj.remove_func.assert_called_once()
