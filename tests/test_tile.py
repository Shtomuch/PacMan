import pygame
import pytest

from classes.tile import Tile


# Фікстура для патчу функцій завантаження зображень
@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    dummy_surface = object()
    monkeypatch.setattr(pygame.image, "load", lambda path: dummy_surface)
    monkeypatch.setattr(pygame.transform, "scale", lambda surf, size: surf)


# Фікстура для dummy координат
@pytest.fixture
def tile_coordinates():
    class DummyCoord:
        x_global = 0
        y_global = 0

    return DummyCoord()


@pytest.mark.unit
@pytest.mark.parametrize("tile_id, expected_wall, expected_grates, expected_name", [
    (1, True, False, "vertical_animation"),
    (7, False, True, "grate_animation"),
    (0, False, False, "void_animation"),
    (3, True, False, "left_down_animation")
])
def test_tile_properties(
        tile_id,
        expected_wall,
        expected_grates,
        expected_name,
        tile_coordinates):
    tile = Tile(coordinates=tile_coordinates, tile_id=tile_id)
    assert tile.is_wall == expected_wall
    assert tile.is_grates == expected_grates
    # Перевіряємо, що у AnimationSet ім'я містить expected_name
    anim_set = tile.animation.animation_set
    assert expected_name in anim_set.name


@pytest.mark.unit
def test_add_and_remove_object(tile_coordinates):
    tile = Tile(coordinates=tile_coordinates, tile_id=0)
    dummy_obj = object()
    tile.add_object(dummy_obj)
    assert dummy_obj in tile.objects
    tile.remove_object(dummy_obj)
    assert dummy_obj not in tile.objects


@pytest.mark.unit
def test_update_calls_animation_update(tile_coordinates, monkeypatch):
    tile = Tile(coordinates=tile_coordinates, tile_id=0)
    update_called = [False]

    def dummy_update(delta):
        update_called[0] = True

    monkeypatch.setattr(tile.animation, "update", dummy_update)
    tile.update(0.1)
    assert update_called[0]
