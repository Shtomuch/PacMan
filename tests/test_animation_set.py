from unittest.mock import MagicMock

import pygame
import pytest

from classes.animation_set import AnimationSet
from classes.global_vars import GlobalVars


@pytest.fixture
def setup_pygame():
    pygame.init()
    GlobalVars.screen = pygame.Surface((800, 600))  # Імітація екрану
    yield
    pygame.quit()


@pytest.fixture
def sample_animation():
    frames = [pygame.Surface((10, 10)) for _ in range(3)]  # 3 тестових кадри
    time = [100, 150, 200]  # Час затримки кадрів
    return AnimationSet(frames, time, "test_animation")


def test_initialization(sample_animation):
    """
    Перевіряє коректність ініціалізації об'єкта AnimationSet.
    """
    assert sample_animation.frames is not None
    assert sample_animation.time == [100, 150, 200]
    assert sample_animation.name == "test_animation"
    assert sample_animation.frame == 0
    assert sample_animation._timer == 0
    assert sample_animation.direction == 0
    assert sample_animation.cycle is True


def test_draw_no_frames(setup_pygame):
    """
    Перевіряє метод draw для випадку, коли список кадрів порожній.
    """
    anim = AnimationSet([], [], "empty_animation")
    position = MagicMock()
    position.x_global = 100
    position.y_global = 100
    anim.draw(position)  # Не повинно нічого малювати і не падати


def test_draw(sample_animation, setup_pygame):
    """
    Перевіряє, що метод draw коректно працює з реальними кадрами.
    """
    position = MagicMock()
    position.x_global = 100
    position.y_global = 100

    # Виклик draw не повинен спричиняти помилки
    sample_animation.draw(position)


def test_update_no_frames(setup_pygame):
    """
    Перевіряє метод update при відсутності кадрів.
    """
    anim = AnimationSet([], [], "empty_animation")
    position = MagicMock()
    anim.update(50, position)  # Не повинно оновлюватися і не падати


def test_update(sample_animation, setup_pygame):
    """
    Перевіряє логіку оновлення кадрів у методі update.
    """
    position = MagicMock()
    position.x_global = 100
    position.y_global = 100

    sample_animation.update(50, position)
    assert sample_animation.frame == 0  # Кадр не повинен змінитися (50 < 100)

    sample_animation.update(100, position)
    assert sample_animation.frame == 1  # Кадр повинен змінитися (50+100 > 100)

    sample_animation.update(200, position)
    assert sample_animation.frame == 2  # Наступний кадр

    sample_animation.update(300, position)

    # Додаємо друк
    print(
        f"Frame after last update: {
            sample_animation.frame}, Timer: {
            sample_animation._timer}")

    assert sample_animation.frame == 0  # Повертається до початку через цикл
