import pygame
import pytest

from classes.global_vars import GlobalVars
from classes.pacman import Pacman
from classes.point import Point


# Dummy класи для тестування
class DummyTile:
    def __init__(self):
        self.objects = []
        self.removed = False

    def remove_object(self, obj):
        self.removed = True


class DummyCoordinate:
    x_tile = 0
    y_tile = 0
    x_global = 0
    y_global = 0


# Створюємо DummyPoint, який наслідує Point для перевірки виклику disappear
class DummyPoint(Point):
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.disappeared = False

    def disappear(self):
        self.disappeared = True


# Фікстура для dummy координати
@pytest.fixture
def dummy_coord():
    return DummyCoordinate()


# Фікстура для dummy плитки
@pytest.fixture
def dummy_tile():
    return DummyTile()


# Фікстура для налаштування GlobalVars.tilemap (всі запити повертають dummy_tile)
@pytest.fixture(autouse=True)
def setup_global_tilemap(dummy_tile):
    class DummyTilemap:
        def get_tile(self, coordinate):
            return dummy_tile

    GlobalVars.tilemap = DummyTilemap()
    GlobalVars.tile_size = 40  # умовне значення


# Фікстура для патчу функцій завантаження зображень у pygame
@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    dummy_surface = object()
    monkeypatch.setattr(pygame.image, "load", lambda path: dummy_surface)
    monkeypatch.setattr(pygame.transform, "scale", lambda surf, size: surf)


@pytest.mark.unit
def test_get_images_returns_animation_set():
    # Перевіряємо, що _get_images повертає список з одним AnimationSet із 4 кадрами
    anim_sets = Pacman._get_images()
    assert isinstance(anim_sets, list)
    assert len(anim_sets) == 1
    animation_set = anim_sets[0]
    assert hasattr(animation_set, "frames")
    assert len(animation_set.frames) == 4


@pytest.mark.unit
def test_death_reduces_health_and_calls_remove(dummy_coord):
    pacman = Pacman(first_pos=dummy_coord, health=3)
    # Використовуємо список для відслідковування виклику remove_func
    called = [False]

    def dummy_remove():
        called[0] = True

    pacman.next_move.remove_func = dummy_remove

    pacman.death()
    assert pacman.health == 2
    assert called[0] == True


@pytest.mark.unit
def test_update_collects_point(dummy_coord, dummy_tile, monkeypatch):
    # Додаємо DummyPoint до плитки
    point = DummyPoint(dummy_coord)
    dummy_tile.objects.append(point)

    pacman = Pacman(first_pos=dummy_coord, health=3)
    # Примусово встановлюємо кадр анімації, що задовольняє умову
    pacman.animation.animation_set.frame = 2
    # Підмінюємо move_unit.move, щоб повертати значення в діапазоні умови (1)
    pacman.move_unit.move = lambda delta, direction: 1

    update_called = [False]

    def dummy_animation_update(delta):
        update_called[0] = True

    pacman.animation.update = dummy_animation_update

    pacman.update(0.1)

    assert point.disappeared, "Point повинен бути зібраний (disappear викликано)"
    assert dummy_tile.removed, "Tile має викликати remove_object для point"
    assert update_called[0] == True
    # Перевіряємо, що позиція та напрямок анімації оновлено
    assert pacman.animation.position == pacman.move_unit.coordinates
    assert pacman.animation.direction == pacman.move_unit.direction
