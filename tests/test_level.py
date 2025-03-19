# import pytest
# import math
# from unittest.mock import patch, MagicMock

# import pygame

# # Припустимо, що ваш клас Level лежить у файлі level.py
# from classes.level import Level
# from classes.global_vars import GlobalVars
# from classes.tilemap import Tilemap
# from classes.pacman import Pacman
# from classes.ghost import Blinky, Pinky, Inky, Clyde


# @pytest.fixture
# def sample_board():
#     """
#     Простий двовимірний список, який виступатиме в ролі карти рівня.
#     Ви можете підставити будь-яку іншу матрицю, яка підходить для тестів.
#     """
#     return [
#         [1, 1, 1, 1, 1, 1],
#         [1, 0, 0, 0, 0, 1],
#         [1, 0, 2, 0, 0, 1],
#         [1, 0, 0, 0, 0, 1],
#         [1, 1, 1, 1, 1, 1],
#     ]


# @pytest.fixture
# def mock_pygame_display():
#     """
#     Фікстура, що 'глушить' pygame.display.set_mode і повертає фейковий Surface,
#     у якого методи (зокрема fill) можна викликати без помилок.
#     """
#     with patch('pygame.display.set_mode') as mock_set_mode:
#         # Створюємо підроблений Surface
#         fake_surface = MagicMock(spec=pygame.Surface)
#         # Повертаємо його з set_mode
#         mock_set_mode.return_value = fake_surface
#         yield fake_surface


# @pytest.fixture
# def mock_pygame_events():
#     """
#     Фікстура, що 'глушить' pygame.event.get, аби ми могли керувати подіями.
#     За замовчуванням події порожні.
#     """
#     with patch('pygame.event.get', return_value=[]):
#         yield


# @pytest.fixture
# def mock_pygame_fill():
#     """
#     Фікстура, що 'глушить' screen.fill(...) для уникнення реальних операцій малювання.
#     """
#     with patch('pygame.Surface.fill', return_value=None) as mock_fill:
#         yield mock_fill


# @pytest.mark.usefixtures("mock_pygame_display")
# class TestLevelInitialization:
#     """
#     Тести, що перевіряють роботу конструктора (__init__) і початкову ініціалізацію.
#     """
#     def test_init_creates_tilemap(self, sample_board):
#         """
#         Перевіряємо, що після створення Level
#         з'являється коректний Tilemap у GlobalVars.
#         """
#         lvl = Level(sample_board)
#         assert GlobalVars.tilemap is not None, "Tilemap не створився!"
#         assert isinstance(GlobalVars.tilemap, Tilemap), "GlobalVars.tilemap має бути Tilemap!"

#     def test_init_creates_pacman_and_ghosts(self, sample_board):
#         """
#         Перевіряємо, що виклик __init__ (через reset_positions)
#         створює Pacman та 4 привидів.
#         """
#         lvl = Level(sample_board, pacman_health=3)
#         assert GlobalVars.pacman is not None, "Pacman не створився!"
#         assert isinstance(GlobalVars.pacman, Pacman), "GlobalVars.pacman має бути Pacman!"

#         assert len(GlobalVars.ghosts) == 4, "Має бути 4 привиди (Blinky, Pinky, Inky, Clyde)!"
#         ghost_types = {type(g) for g in GlobalVars.ghosts}
#         assert {Blinky, Pinky, Inky, Clyde} == ghost_types, "Набір привидів не відповідає очікуваному!"

#     def test_init_sets_pacman_health(self, sample_board):
#         """
#         Перевіряємо, що кількість життів Pac-Man встановлюється згідно з аргументом pacman_health.
#         """
#         lvl = Level(sample_board, pacman_health=5)
#         assert GlobalVars.pacman.health == 5, "Не встановилася кількість життів Pac-Man!"


# @pytest.mark.usefixtures("mock_pygame_display")
# class TestLevelResetPositions:
#     """
#     Тести, що перевіряють метод reset_positions.
#     """
#     def test_reset_positions_recreates_pacman_and_ghosts(self, sample_board):
#         lvl = Level(sample_board, pacman_health=3)
#         old_pacman = GlobalVars.pacman
#         old_ghosts = GlobalVars.ghosts[:]

#         lvl.reset_positions()
#         # Перевіряємо, що Pacman створився новий
#         assert GlobalVars.pacman is not None
#         assert GlobalVars.pacman != old_pacman, "reset_positions має створювати нового Pacman!"

#         # І привиди теж
#         assert len(GlobalVars.ghosts) == 4
#         for ghost in GlobalVars.ghosts:
#             assert ghost not in old_ghosts, "reset_positions має створювати нові об'єкти привидів!"


# @pytest.mark.usefixtures("mock_pygame_display", "mock_pygame_fill")
# class TestLevelUpdate:
#     """
#     Тести, що перевіряють логіку методу update.
#     """
#     def test_update_returns_false_on_quit_event(self, sample_board):
#         """
#         Якщо у черзі подій є pygame.QUIT, метод update має повернути False.
#         """
#         lvl = Level(sample_board)
        
#         # Підробимо події, що містять pygame.QUIT
#         with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.QUIT)]):
#             cont = lvl.update(delta=0.1)
#         assert cont is False, "При наявності QUIT має повертати False!"

#     def test_update_returns_false_if_pacman_health_zero(self, sample_board):
#         """
#         Якщо у Pac-Man закінчилося здоров'я, update має повернути False.
#         """
#         lvl = Level(sample_board, pacman_health=0)
#         with patch('pygame.event.get', return_value=[]):
#             cont = lvl.update(delta=0.1)
#         assert cont is False, "Якщо здоров'я Pac-Man <= 0, метод update має повертати False!"

#     def test_update_changes_pacman_direction(self, sample_board):
#         """
#         Перевірка, що натискання клавіш змінює напрямок Pac-Man.
#         """
#         lvl = Level(sample_board)
#         with patch('pygame.event.get', return_value=[
#             pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
#         ]):
#             lvl.update(delta=0.1)
#         assert GlobalVars.pacman.direction == 2, "K_LEFT має виставляти напрямок = 2!"

#     def test_update_collision_pacman_ghost_death(self, sample_board):
#         """
#         Перевіряємо, що при зіткненні з привидом у стані 'alive' викликається death() у Pac-Man,
#         і виконується reset_positions (тобто Pac-Man втрачає життя, а позиції оновлюються).
#         """
#         lvl = Level(sample_board, pacman_health=2)
#         # Розташуємо Pac-Man і Blinky поруч, щоб штучно викликати колізію
#         GlobalVars.pacman.move_unit.coordinates.x_global = 100
#         GlobalVars.pacman.move_unit.coordinates.y_global = 100
        
#         # Знайдемо Blinky і виставимо йому такі самі координати
#         blinky = next(g for g in GlobalVars.ghosts if isinstance(g, Blinky))
#         blinky.move_unit.coordinates.x_global = 100
#         blinky.move_unit.coordinates.y_global = 100
#         blinky.state = "alive"

#         # Простежимо, що викликається death() у Pac-Man.
#         with patch.object(GlobalVars.pacman, 'death', wraps=GlobalVars.pacman.death) as mock_death:
#             lvl.update(delta=0.1)
#             mock_death.assert_called_once()

#         # Після смерті (health зменшується) і reset_positions Pac-Man має ще 1 життя
#         assert GlobalVars.pacman.health == 1, "Pac-Man мав втратити 1 життя (2 -> 1)!"
#         # Перевіримо, що Pac-Man пересоздався (інші координати, інший об'єкт тощо)
#         # Залежить від вашої реалізації, але зазвичай reset_positions створює новий об'єкт Pacman.

#     def test_update_collision_pacman_ghost_frightened(self, sample_board):
#         """
#         Якщо привид у стані 'frightened', він має викликати ghost.death(), а Pac-Man не втрачає життя.
#         """
#         lvl = Level(sample_board, pacman_health=2)
#         # Знайдемо Blinky і виставимо йому такі самі координати, стан frightened
#         blinky = next(g for g in GlobalVars.ghosts if isinstance(g, Blinky))
#         blinky.move_unit.coordinates.x_global = 100
#         blinky.move_unit.coordinates.y_global = 100
#         blinky.state = "frightened"

#         # Аналогічно Pac-Man
#         GlobalVars.pacman.move_unit.coordinates.x_global = 100
#         GlobalVars.pacman.move_unit.coordinates.y_global = 100

#         with patch.object(blinky, 'death', wraps=blinky.death) as mock_ghost_death:
#             lvl.update(delta=0.1)
#             mock_ghost_death.assert_called_once()

#         # Перевіримо, що життя Pac-Man не змінилося
#         assert GlobalVars.pacman.health == 2, "При стані frightened привид має вмирати, а Pac-Man не втрачає здоров'я."
