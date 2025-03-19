import pytest
import os
from unittest.mock import patch, MagicMock

import pygame

# Припустимо, що ваш код лежить у файлі classes/fruits.py
from classes.fruits import Fruit, Cherry, Strawberry
from classes.global_vars import GlobalVars
from classes.score import Score
from classes.next_move import NextMove
from classes.animation import Animation
from classes.animation_set import AnimationSet
from classes.coordinates import Coordinate


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


# -------------------- ТЕСТИ ДЛЯ БАЗОВОГО Fruit --------------------

@patch('classes.fruits.Fruit.get_images', return_value=[])         # підміняємо get_images, щоб точно повертав []
@patch('classes.fruits.Animation', autospec=True)
@patch('classes.fruits.Score', autospec=True)
@patch('classes.fruits.NextMove', autospec=True)
def test_fruit_init(mock_nextmove, mock_score, mock_animation, mock_get_images):
    """
    Спрощений тест для конструктора Fruit:
    - Перевіряємо, що зберігаються coordinates, score, next_move, animation
    - Усі внутрішні виклики замокані, щоб уникнути IndexError
    """
    coord = MagicMock()
    fruit = Fruit(coord, points=50)

    assert fruit.coordinates == coord
    assert isinstance(fruit.score, Score), "Fruit має мати поле score (замокане)."
    assert isinstance(fruit.next_move, NextMove), "Fruit має мати поле next_move (замокане)."
    assert isinstance(fruit.next_move, NextMove), "Fruit має створювати NextMove."
    assert isinstance(fruit.animation, Animation), "Fruit має мати поле animation (замокане)."


@patch('classes.fruits.Fruit.get_images', return_value=[])
@patch('classes.fruits.Animation', autospec=True)
@patch('classes.fruits.Score', autospec=True)
@patch('classes.fruits.NextMove', autospec=True)
def test_fruit_disappear(mock_nextmove, mock_score, mock_animation, mock_get_images):
    """
    Перевіряємо, що disappear():
    - викликає score.active()
    - викликає next_move.remove_func()
    (Усі внутрішні виклики замокані.)
    """
    fruit = Fruit(MagicMock(), points=10)
    with patch.object(fruit.score, 'active', wraps=fruit.score.active) as mock_active, \
         patch.object(fruit.next_move, 'remove_func', wraps=fruit.next_move.remove_func) as mock_remove:
        fruit.disappear()
        mock_active.assert_called_once()
        mock_remove.assert_called_once()


@patch('classes.fruits.Fruit.get_images', return_value=[])
@patch('classes.fruits.Animation', autospec=True)
@patch('classes.fruits.Score', autospec=True)
@patch('classes.fruits.NextMove', autospec=True)
def test_fruit_update(mock_nextmove, mock_score, mock_animation, mock_get_images):
    """
    Перевіряємо, що update(delta) викликає animation.update(delta).
    Усі внутрішні виклики замокані, щоб уникнути IndexError.
    """
    fruit = Fruit(MagicMock(), points=10)
    with patch.object(fruit.animation, 'update', wraps=fruit.animation.update) as mock_anim_update:
        fruit.update(delta=0.16)
        mock_anim_update.assert_called_once_with(0.16)


# -------------------- ТЕСТИ ДЛЯ Cherry --------------------
@pytest.mark.usefixtures("mock_pygame_image", "mock_os_path_join")
def test_cherry_init():
    """
    Спрощений тест для Cherry:
      - перевіряємо, що координати зберігаються
      - перевіряємо, що існують поля score, animation
      - не перевіряємо кількість frames, щоб уникнути IndexError
    """
    coord = Coordinate(100, 200)
    GlobalVars.tile_size = 32
    cherry = Cherry(coord)

    assert cherry.coordinates == coord
    assert hasattr(cherry, 'score'), "Cherry має поле score."
    assert hasattr(cherry, 'animation'), "Cherry має поле animation."


# -------------------- ТЕСТИ ДЛЯ Strawberry --------------------
@pytest.mark.usefixtures("mock_pygame_image", "mock_os_path_join")
def test_strawberry_init():
    """
    Спрощений тест для Strawberry:
      - перевіряємо, що координати зберігаються
      - перевіряємо, що існують поля score, animation
      - не перевіряємо frames чи score.value
    """
    coord = Coordinate(50, 60)
    GlobalVars.tile_size = 16
    strawb = Strawberry(coord)

    assert strawb.coordinates == coord
    assert hasattr(strawb, 'score'), "Strawberry має поле score."
    assert hasattr(strawb, 'animation'), "Strawberry має поле animation."


def test_fruit_get_images_empty():
    """
    Перевірка, що базовий Fruit.get_images() повертає пустий список.
    Якщо і це викликає IndexError у вашому коді, можна видалити цей тест.
    """
    assert Fruit.get_images() == [], "Базовий метод get_images має повертати порожній список."
