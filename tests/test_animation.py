from unittest.mock import MagicMock

import pytest

from classes.animation import Animation


@pytest.fixture
def sample_animation_sets():
    anim1 = MagicMock()
    anim1.name = "Idle"
    anim2 = MagicMock()
    anim2.name = "Run"
    return [anim1, anim2]


@pytest.fixture
def sample_coordinates():
    position = MagicMock()
    position.x_global = 50
    position.y_global = 100
    return position


@pytest.fixture
def sample_animation(sample_animation_sets, sample_coordinates):
    return Animation(sample_animation_sets, sample_coordinates)


def test_initial_state(
        sample_animation,
        sample_animation_sets,
        sample_coordinates):
    assert sample_animation.sets == sample_animation_sets
    assert sample_animation.position == sample_coordinates
    assert sample_animation.animation_set == sample_animation_sets[0]
    assert sample_animation.direction == 0
    assert sample_animation.freeze is False


def test_current_animation_getter(sample_animation):
    assert sample_animation.current_animation == "Idle"


def test_current_animation_setter(sample_animation, sample_animation_sets):
    sample_animation.current_animation = "Run"
    assert sample_animation.animation_set == sample_animation_sets[1]

    sample_animation.current_animation = "NonExisting"
    # Повертається до першого сету
    assert sample_animation.animation_set == sample_animation_sets[0]


def test_update_when_frozen(sample_animation):
    sample_animation.freeze = True
    sample_animation.update(100)
    sample_animation.animation_set.draw.assert_called_once_with(
        sample_animation.position)
    sample_animation.animation_set.update.assert_not_called()


def test_update_when_not_frozen(sample_animation):
    sample_animation.freeze = False
    sample_animation.update(100)
    sample_animation.animation_set.update.assert_called_once_with(
        100, sample_animation.position)
