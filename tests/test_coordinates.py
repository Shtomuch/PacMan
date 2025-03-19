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
def setup_tile_size():
    """
    Фікстура, щоб встановити GlobalVars.tile_size до тестового значення
    перед кожним тестом.
    """
    GlobalVars.tile_size = 10
    yield
    # За потреби тут можна скинути до іншого значення


@pytest.fixture
def mock_pygame_image():
    """
    'Глушимо' pygame.image.load і pygame.transform.scale,
    щоб не завантажувати реальні файли під час тестів.
    """
    with patch('pygame.image.load', return_value=MagicMock(spec=pygame.Surface)) as mock_load, \
         patch('pygame.transform.scale', return_value=MagicMock(spec=pygame.Surface)) as mock_scale:
        yield (mock_load, mock_scale)


@pytest.fixture
def mock_os_path_join():
    """
    'Глушимо' os.path.join, щоб не залежати від реальної файлової системи.
    """
    with patch('os.path.join', side_effect=lambda *args: "/".join(args)) as mock_join:
        yield mock_join


# ---------------------- ТЕСТИ КЛАСУ Dot ----------------------

@patch('classes.dot.Animation', autospec=True)
@patch('classes.dot.Score', autospec=True)
@patch('classes.dot.NextMove', autospec=True)
def test_dot_init(mock_nextmove, mock_score, mock_animation,
                  mock_pygame_image, mock_os_path_join, setup_tile_size):
    """
    Перевіряємо, що Dot створюється без помилок:
      - поля coordinates, animation, score, next_move існують
      - Score викликано з 10
      - NextMove викликано з ('point', dot.update)
    """
    coord = Coordinate(10, 20)
    dot = Dot(coord)

    assert dot.coordinates == coord
    assert hasattr(dot, 'animation'), "Dot має мати поле animation"
    assert hasattr(dot, 'score'), "Dot має мати поле score"
    assert hasattr(dot, 'next_move'), "Dot має мати поле next_move"

    mock_score.assert_called_once_with(10)
    mock_nextmove.assert_called_once_with('point', dot.update)


@patch('classes.dot.Animation', autospec=True)
@patch('classes.dot.Score', autospec=True)
@patch('classes.dot.NextMove', autospec=True)
def test_dot_disappear(mock_nextmove, mock_score, mock_animation,
                       mock_pygame_image, mock_os_path_join, setup_tile_size):
    """
    Перевіряємо, що disappear():
      - викликає score.active()
      - викликає next_move.remove_func()
    """
    dot = Dot(Coordinate(5, 5))
    dot.disappear()

    mock_score.return_value.active.assert_called_once()
    mock_nextmove.return_value.remove_func.assert_called_once()


@patch('classes.dot.Animation', autospec=True)
@patch('classes.dot.Score', autospec=True)
@patch('classes.dot.NextMove', autospec=True)
def test_dot_update(mock_nextmove, mock_score, mock_animation,
                    mock_pygame_image, mock_os_path_join, setup_tile_size):
    """
    Перевіряємо, що update(delta) викликає animation.update(delta).
    """
    dot = Dot(Coordinate(5, 5))
    dot.update(0.16)
    mock_animation.return_value.update.assert_called_once_with(0.16)


def test_dot_get_images(setup_tile_size, mock_pygame_image, mock_os_path_join):
    """
    Тестуємо реальний get_images() (без мокання AnimationSet),
    але з підміною pygame.image.load, transform.scale, os.path.join.
    Перевіряємо, що повертається список із 1 AnimationSet, у якого 2 кадри.
    """
    frames = Dot.get_images()
    assert len(frames) == 1, "Dot.get_images має повертати список із 1 AnimationSet"

    anim_set = frames[0]
    assert isinstance(anim_set, AnimationSet), "Елемент має бути AnimationSet"
    # Перевіримо, що у AnimationSet.frames 2 кадри
    assert len(anim_set.frames) == 2, "Очікуємо 2 кадри (coin.png і smaller_coin.png)"
    assert anim_set.name == "dot_animation"
