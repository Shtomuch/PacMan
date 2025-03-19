import pytest
import pygame
from unittest.mock import patch, MagicMock

# Припустимо, що ваші класи лежать у файлі classes/points.py
from classes.point import Point, BigDot
from classes.global_vars import GlobalVars
from classes.coordinates import Coordinate
from classes.animation_set import AnimationSet
from classes.power import Power


@pytest.fixture
def mock_pygame_surface():
    """
    Повертаємо реальні pygame.Surface, щоб
    pygame.transform.scale не скаржився на MagicMock замість Surface.
    """
    pygame.display.init()  # Щоб можна було створювати Surface без помилки
    with patch('pygame.image.load', return_value=pygame.Surface((10, 10))) as mock_load, \
         patch('pygame.transform.scale', side_effect=lambda surf, size: pygame.Surface(size)) as mock_scale:
        yield (mock_load, mock_scale)
    pygame.display.quit()


@pytest.fixture
def mock_os_path_join():
    """
    'Глушимо' os.path.join, щоб не залежати від реальної файлової системи.
    """
    with patch('os.path.join', side_effect=lambda *args: "/".join(args)) as mock_join:
        yield mock_join


@pytest.fixture
def mock_point_get_images():
    """
    Підмінимо Point.get_images, щоб воно не було None і не спричиняло 'NoneType' помилок.
    Повернемо список із одним AnimationSet (у якого порожній список frames).
    """
    empty_animset = AnimationSet(frames=[], time=[], name='empty')
    with patch.object(Point, 'get_images', return_value=[empty_animset]):
        yield


# ------------------- ТЕСТИ ДЛЯ Point -------------------
@pytest.mark.usefixtures("mock_pygame_surface", "mock_os_path_join", "mock_point_get_images")
def test_point_init():
    coord = Coordinate(10, 20)
    p = Point(coord, points=99)
    assert p.coordinates == coord
    assert p.animation is not None
    assert p.score is not None
    assert p.next_move is not None


@pytest.mark.usefixtures("mock_pygame_surface", "mock_os_path_join", "mock_point_get_images")
def test_point_disappear():
    p = Point(Coordinate(5, 5), points=99)
    with patch.object(p.score, 'active', wraps=p.score.active) as mock_active, \
         patch.object(p.next_move, 'remove_func', wraps=p.next_move.remove_func) as mock_remove:
        p.disappear()
        mock_active.assert_called_once()
        mock_remove.assert_called_once()


@pytest.mark.usefixtures("mock_pygame_surface", "mock_os_path_join", "mock_point_get_images")
def test_point_update():
    p = Point(Coordinate(5, 5), points=99)
    with patch.object(p.animation, 'update', wraps=p.animation.update) as mock_anim_update:
        p.update(delta=0.2)
        mock_anim_update.assert_called_once_with(0.2)


# ------------------- ТЕСТИ ДЛЯ BigDot -------------------
@pytest.mark.usefixtures("mock_pygame_surface", "mock_os_path_join")
@patch.object(BigDot, 'get_images', return_value=[AnimationSet(frames=[], time=[], name='empty')])
def test_big_dot_update(mock_get_images):
    bd = BigDot(Coordinate(50, 50))
    with patch.object(bd.animation, 'update', wraps=bd.animation.update) as mock_anim_update:
        bd.update(0.3)
        mock_anim_update.assert_called_once_with(0.3)


@pytest.mark.usefixtures("mock_pygame_surface", "mock_os_path_join")
@patch('classes.power.Power.activate', autospec=True)
@patch.object(BigDot, 'get_images', return_value=[AnimationSet(frames=[], time=[], name='empty')])
def test_big_dot_disappear(mock_get_images, mock_power_activate):
    bd = BigDot(Coordinate(60, 60))
    with patch.object(bd.score, 'active', wraps=bd.score.active) as mock_active, \
         patch.object(bd.next_move, 'remove_func', wraps=bd.next_move.remove_func) as mock_remove:
        bd.disappear()
        mock_active.assert_called_once()
        mock_remove.assert_called_once()
        mock_power_activate.assert_called_once()
