import pytest
import os
from unittest.mock import patch, MagicMock

import pygame

# Припустимо, що ваш код лежить у файлі fruit.py або у відповідному модулі:
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
    Фікстура, що підміняє pygame.image.load і pygame.transform.scale, 
    аби не завантажувати реальні файли під час тестів.
    """
    with patch('pygame.image.load', return_value=MagicMock(spec=pygame.Surface)) as mock_load, \
         patch('pygame.transform.scale', return_value=MagicMock(spec=pygame.Surface)) as mock_scale:
        yield (mock_load, mock_scale)


@pytest.fixture
def mock_os_path_join():
    """
    Фікстура, що підміняє os.path.join, аби відстежити, які шляхи формуються.
    """
    with patch('os.path.join', side_effect=lambda *args: "/".join(args)) as mock_join:
        yield mock_join


def test_fruit_init():
    """
    Тестуємо базовий конструктор Fruit:
    - Чи зберігаються координати
    - Чи створюється Score(points)
    - Чи створюється NextMove із функцією self.update
    - Чи створюється Animation із пустим набором зображень (оскільки get_images() -> [])
    """
    coord = MagicMock()
    fruit = Fruit(coord, points=50)
    
    assert fruit.coordinates == coord, "Fruit має зберігати передані координати."
    assert isinstance(fruit.score, Score), "Fruit має мати поле score типу Score."
    assert fruit.score.value == 50, "Fruit має зберігати кількість балів, переданих у конструктор."
    assert isinstance(fruit.next_move, NextMove), "Fruit має створювати NextMove."
    assert fruit.next_move.func == fruit.update, "NextMove має викликати метод update фрукту."
    
    # Перевірка анімації: базовий Fruit.get_images() повертає [] => animationSet порожній
    assert isinstance(fruit.animation, Animation), "Має бути Animation-об'єкт."
    # Перевіримо, що у fruit.animation.frames = []
    # (оскільки get_images() -> [], Animation конструюється з порожнім списком)
    assert len(fruit.animation.frames) == 0, "У базового Fruit не повинно бути зображень (get_images -> [])."


def test_fruit_disappear():
    """
    Тестуємо метод disappear():
    - викликає score.active()
    - викликає next_move.remove_func()
    """
    fruit = Fruit(MagicMock(), points=10)
    with patch.object(fruit.score, 'active', wraps=fruit.score.active) as mock_active, \
         patch.object(fruit.next_move, 'remove_func', wraps=fruit.next_move.remove_func) as mock_remove:
        fruit.disappear()
        mock_active.assert_called_once()
        mock_remove.assert_called_once()


def test_fruit_update():
    """
    Тестуємо метод update():
    - має викликати animation.update(delta)
    """
    fruit = Fruit(MagicMock(), points=10)
    with patch.object(fruit.animation, 'update', wraps=fruit.animation.update) as mock_anim_update:
        fruit.update(delta=0.16)
        mock_anim_update.assert_called_once_with(0.16)


@pytest.mark.usefixtures("mock_pygame_image", "mock_os_path_join")
def test_cherry_init():
    """
    Перевіряємо, що Cherry правильно ініціалізується:
    - points = 100
    - get_images() завантажує 1 зображення (cherry.png)
    - створює AnimationSet із правильною назвою
    """
    coord = Coordinate(100, 200)
    GlobalVars.tile_size = 32  # Припустимо, розмір tile = 32
    cherry = Cherry(coord)
    
    assert cherry.coordinates == coord
    assert cherry.score.value == 100, "Cherry має давати 100 балів."
    assert len(cherry.animation.frames) == 1, "Cherry має 1 AnimationSet."
    
    anim_set = cherry.animation.frames[0]
    assert isinstance(anim_set, AnimationSet), "Повинна бути AnimationSet."
    assert anim_set.name == "chery_animation", "Назва анімації має бути 'chery_animation'."


@pytest.mark.usefixtures("mock_pygame_image", "mock_os_path_join")
def test_strawberry_init():
    """
    Перевіряємо, що Strawberry правильно ініціалізується:
    - points = 300
    - get_images() завантажує 1 зображення (strawberry.png)
    - створює AnimationSet із правильною назвою
    """
    coord = Coordinate(50, 60)
    GlobalVars.tile_size = 16
    strawb = Strawberry(coord)
    
    assert strawb.coordinates == coord
    assert strawb.score.value == 300, "Strawberry має давати 300 балів."
    assert len(strawb.animation.frames) == 1, "Strawberry має 1 AnimationSet."
    
    anim_set = strawb.animation.frames[0]
    assert isinstance(anim_set, AnimationSet), "Повинна бути AnimationSet."
    assert anim_set.name == "strawberry_animation", "Назва анімації має бути 'strawberry_animation'."


def test_fruit_get_images_empty():
    """
    Перевірка, що базовий Fruit.get_images() повертає пустий список.
    """
    assert Fruit.get_images() == [], "Базовий метод get_images має повертати порожній список."
