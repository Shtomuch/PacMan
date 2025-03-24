from unittest.mock import MagicMock, patch

import pygame
import pytest

from classes.animation_set import AnimationSet
# Припустимо, що BigDot лежить у файлі classes/big_dot.py
from classes.big_dot import BigDot
from classes.coordinates import Coordinate
from classes.global_vars import GlobalVars


@pytest.fixture
def mock_pygame_image():
    """
    Фікстура, що 'глушить' pygame.image.load і pygame.transform.scale,
    аби не завантажувати реальні файли під час тестів.
    """
    with patch('pygame.image.load', return_value=MagicMock(spec=pygame.Surface)) as mock_load, \
            patch('pygame.transform.scale', return_value=MagicMock(spec=pygame.Surface)) as mock_scale:
        yield (mock_load, mock_scale)


@pytest.fixture
def mock_os_path_join():
    """
    Фікстура, що 'глушить' os.path.join, щоб не залежати від реальної файлової системи.
    """
    with patch('os.path.join', side_effect=lambda *args: "/".join(args)) as mock_join:
        yield mock_join


# ------------------ ТЕСТ КОНСТРУКТОРА (__init__) ------------------
@pytest.mark.usefixtures("mock_pygame_image", "mock_os_path_join")
@patch('classes.big_dot.Animation', autospec=True)
@patch('classes.big_dot.Score', autospec=True)
@patch('classes.big_dot.NextMove', autospec=True)
def test_big_dot_init(mock_nextmove, mock_score, mock_animation):
    """
    Перевіряємо, що у BigDot:
      - зберігаються координати
      - створюються animation, score, next_move
    """
    coord = Coordinate(10, 20)
    GlobalVars.tile_size = 16
    dot = BigDot(coord)

    assert dot.coordinates == coord, "BigDot має зберігати передані координати."
    assert dot.animation is not None, "BigDot має поле animation."
    assert dot.score is not None, "BigDot має поле score."
    assert dot.next_move is not None, "BigDot має поле next_move."
    # Якщо треба, можна перевірити виклик Score(50) або NextMove('point', dot.update)
    # mock_score.assert_called_once_with(50)
    # mock_nextmove.assert_called_once_with('point', dot.update)


# ------------------ ТЕСТ СТАТИЧНОГО МЕТОДУ get_images() ------------------
@pytest.mark.usefixtures("mock_pygame_image", "mock_os_path_join")
def test_big_dot_get_images():
    """
    Перевіряємо, що get_images() повертає список із 1 AnimationSet,
    у якого 2 кадри, name="big_dot_animation".
    """
    GlobalVars.tile_size = 32
    frames = BigDot.get_images()
    assert len(frames) == 1, "Очікуємо один AnimationSet."
    anim_set = frames[0]
    assert isinstance(
        anim_set, AnimationSet), "Повернений елемент має бути AnimationSet."
    assert len(
        anim_set.frames) == 2, "Має бути 2 кадри (big_coin.png і smaller_big_coin.png)."
    assert anim_set.name == "big_dot_animation"


# ------------------ ТЕСТ МЕТОДУ update(delta) ------------------
@patch('classes.big_dot.Animation', autospec=True)
def test_big_dot_update(mock_animation):
    """
    Перевіряємо, що update(delta) викликає animation.update(delta).
    """
    mock_anim_obj = MagicMock()
    mock_animation.return_value = mock_anim_obj

    dot = BigDot(Coordinate(5, 5))
    dot.update(delta=0.1)

    mock_anim_obj.update.assert_called_once_with(0.1)


# ------------------ ТЕСТ МЕТОДУ disappear() ------------------
@patch('classes.big_dot.Power.activate', autospec=True)
@patch('classes.big_dot.NextMove', autospec=True)
@patch('classes.big_dot.Score', autospec=True)
@patch('classes.big_dot.Animation', autospec=True)
def test_big_dot_disappear(
        mock_anim,
        mock_score_class,
        mock_nextmove_class,
        mock_power_activate):
    """
    Перевіряємо, що disappear():
      - викликає score.active()
      - викликає Power.activate()
      - викликає next_move.remove_func()
    """
    mock_score_obj = MagicMock()
    mock_score_class.return_value = mock_score_obj

    mock_nextmove_obj = MagicMock()
    mock_nextmove_class.return_value = mock_nextmove_obj

    dot = BigDot(Coordinate(10, 10))
    dot.disappear()

    # Перевіряємо, що викликалися score.active(), Power.activate(),
    # next_move.remove_func()
    mock_score_obj.active.assert_called_once()
    mock_power_activate.assert_called_once()
    mock_nextmove_obj.remove_func.assert_called_once()
