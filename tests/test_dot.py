import pytest
from unittest.mock import patch, MagicMock
import pygame

# Припустимо, що Fruit, Cherry, Strawberry оголошені у файлі classes/fruit.py
from classes.fruits import Fruit, Cherry, Strawberry
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


# ------------------- ТЕСТИ ДЛЯ БАЗОВОГО Fruit -------------------
@patch('classes.fruit.Animation', autospec=True)
@patch('classes.fruit.Score', autospec=True)
@patch('classes.fruit.NextMove', autospec=True)
def test_fruit_init(mock_nextmove, mock_score, mock_animation, mock_pygame_image, mock_os_path_join):
    """
    Мінімальний тест перевіряє, що Fruit можна створити без падіння,
    і що поля (coordinates, score, animation, next_move) існують.
    """
    coord = Coordinate(10, 20)
    fruit = Fruit(coord, points=50)

    assert fruit is not None, "Fruit не створився!"
    assert fruit.coordinates == coord
    assert hasattr(fruit, 'score'), "У Fruit має бути поле 'score'"
    assert hasattr(fruit, 'animation'), "У Fruit має бути поле 'animation'"
    assert hasattr(fruit, 'next_move'), "У Fruit має бути поле 'next_move'"

@patch('classes.fruit.Animation', autospec=True)
@patch('classes.fruit.Score', autospec=True)
@patch('classes.fruit.NextMove', autospec=True)
def test_fruit_disappear(mock_nextmove, mock_score, mock_animation, mock_pygame_image, mock_os_path_join):
    """
    Перевіряємо, що метод disappear() викликається без помилок
    і викликає score.active() та next_move.remove_func().
    """
    fruit = Fruit(Coordinate(0, 0), points=10)
    fruit.disappear()

    # Перевіримо, що score.active() викликано
    mock_score.return_value.active.assert_called_once()
    # Перевіримо, що next_move.remove_func() викликано
    mock_nextmove.return_value.remove_func.assert_called_once()

@patch('classes.fruit.Animation', autospec=True)
@patch('classes.fruit.Score', autospec=True)
@patch('classes.fruit.NextMove', autospec=True)
def test_fruit_update(mock_nextmove, mock_score, mock_animation, mock_pygame_image, mock_os_path_join):
    """
    Перевіряємо, що update(delta) викликає animation.update(delta).
    """
    fruit = Fruit(Coordinate(5, 5), points=10)
    fruit.update(delta=0.1)

    # Має викликатися animation.update(0.1)
    mock_animation.return_value.update.assert_called_once_with(0.1)


# ------------------- ТЕСТИ ДЛЯ Cherry -------------------
@pytest.mark.usefixtures("mock_pygame_image", "mock_os_path_join")
@patch('classes.fruit.Animation', autospec=True)
@patch('classes.fruit.Score', autospec=True)
@patch('classes.fruit.NextMove', autospec=True)
def test_cherry_init(mock_nextmove, mock_score, mock_animation):
    """
    Мінімальний тест для Cherry:
    - створюємо об'єкт Cherry
    - перевіряємо, що не падає
    - перевіряємо, що поля існують
    """
    cherry = Cherry(Coordinate(7, 7))
    assert cherry is not None
    assert hasattr(cherry, 'score')
    assert hasattr(cherry, 'animation')
    assert hasattr(cherry, 'next_move')


# ------------------- ТЕСТИ ДЛЯ Strawberry -------------------
@pytest.mark.usefixtures("mock_pygame_image", "mock_os_path_join")
@patch('classes.fruit.Animation', autospec=True)
@patch('classes.fruit.Score', autospec=True)
@patch('classes.fruit.NextMove', autospec=True)
def test_strawberry_init(mock_nextmove, mock_score, mock_animation):
    """
    Мінімальний тест для Strawberry:
    - створюємо об'єкт Strawberry
    - перевіряємо, що не падає
    - перевіряємо, що поля існують
    """
    strawb = Strawberry(Coordinate(10, 10))
    assert strawb is not None
    assert hasattr(strawb, 'score')
    assert hasattr(strawb, 'animation')
    assert hasattr(strawb, 'next_move')
