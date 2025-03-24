import copy
import os

import pygame

from classes.animation import Animation
from classes.animation_set import AnimationSet
from classes.coordinates import Coordinate
from classes.global_vars import GlobalVars
from classes.move_unit import MoveUnit
from classes.next_move import NextMove
from classes.score import Score


class Ghost:
    """
    Базовий клас примари. Може бути в одному з кількох станів:
    'alive', 'frightened', 'dead', 'in_house'.
    """

    def __init__(self, coordinates, ghost_type):
        self.state = "in_house"
        self.target = coordinates

        # Створюємо об'єкт переміщення та анімацію
        self.move_unit = MoveUnit(0, self._target)
        self.animation = Animation(self.get_images(ghost_type), coordinates)

        # Додаткові параметри
        self.house_timer = 0.0
        self.immunity = False
        self.direction = 0
        self.score = Score(200)
        self.next_move = NextMove('ghost', self.update)
        self.time_to_drop = False

        # Початковий стан примари в будинку
        self.turn_in_house()

    @staticmethod
    def get_images(ghost_type):
        """
        Завантаження зображень та створення наборів анімацій:
        - 4 напрямки для 'alive' (кожен по 2 кадри),
        - 4 напрямки для 'dead' (кожен по 1 кадру),
        - 1 анімація для 'frightened' (2 кадри).
        """
        colors = ["red", "pink", "blue", "orange"]
        color = colors[ghost_type]
        directions = ["right", "down", "left", "up"]
        ghost_animation = []

        # Анімації для стану "alive"
        for i, d in enumerate(directions):
            frames_alive = []
            for j in range(1, 3):
                frames_alive.append(
                    pygame.transform.scale(
                        pygame.image.load(
                            os.path.join('static_file', 'ghost_photos',
                                         color, f'{color}_{d}_ghost{j}.png')
                        ),
                        (GlobalVars.tile_size, GlobalVars.tile_size)
                    )
                )
            ghost_animation.append(
                AnimationSet(
                    frames=frames_alive,
                    time=[0.1] * len(frames_alive),
                    name=f"ghost_animation_alive_{i}"))

        # Анімації для стану "dead"
        for i, d in enumerate(directions):
            frames_dead = [
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join('static_file', 'ghost_photos',
                                     'eyes', f'ghost_eyes_{d}.png')
                    ),
                    (GlobalVars.tile_size, GlobalVars.tile_size)
                )
            ]
            ghost_animation.append(
                AnimationSet(frames=frames_dead, time=[0.2] * len(frames_dead),
                             name=f"ghost_animation_dead_{i}")
            )

        # Анімація для стану "frightened"
        frames_frightened = [
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join('static_file', 'ghost_photos',
                                 'eaten', 'eaten_ghost1.png')
                ),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            ),
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join('static_file', 'ghost_photos',
                                 'eaten', 'eaten_ghost2.png')
                ),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        ghost_animation.append(
            AnimationSet(
                frames=frames_frightened,
                time=[0.2] *
                len(frames_frightened),
                name="ghost_animation_frightened"))
        return ghost_animation

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        raise NotImplementedError(
            "Властивість Ghost.target() повинна бути перевизначена у підкласі")

    def turn_frightened(self):
        """
        Перехід до стану 'frightened' (ляклива примара).
        Збільшується швидкість руху, призупиняємо імунітет.
        """
        self.state = "frightened"
        self.move_unit.speed = 3.5
        self.move_unit.freeze = False
        self.time_to_drop = True

    def turn_alive(self):
        """
        Перехід до стану 'alive' (звичайна примара).
        """
        self.state = "alive"
        self.move_unit.speed = 4.2
        self.move_unit.freeze = False
        self.time_to_drop = True

    def turn_in_house(self):
        """
        Перехід у стан 'in_house' (примара в будинку).
        """
        self.state = "in_house"
        self.house_timer = 2.0
        self.move_unit.freeze = True
        self.move_unit.speed = 2

    def death(self):
        """
        Обробка смерті примари: нараховуються очки, увімкнено імунітет,
        стан змінюється на 'dead' і збільшується швидкість.
        """
        self.score.active()
        self.immunity = True
        self.state = "dead"
        self.move_unit.speed = 9

    def update(self, delta):
        """
        Основна логіка оновлення стану примари:
         - Залежить від поточного стану (alive, frightened, dead, in_house).
         - Оновлює ціль, рух та анімацію.
        """
        if self.state == "alive":
            self.alive_logic()
        elif self.state == "frightened":
            self.frightened_logic()
        elif self.state == "dead":
            self.dead_logic()
        elif self.state == "in_house":
            self.in_house_logic(delta)

        self.update_target()
        self.move(delta)

        self.animation.position = self.move_unit.coordinates
        self.animation.direction = 0

        if self.state == "frightened":
            self.animation.current_animation = "ghost_animation_frightened"
        else:
            s = "alive" if self.state == "in_house" else self.state
            self.animation.current_animation = f"ghost_animation_{s}_{
                self.move_unit.direction}"

        self.animation.update(delta)

    def update_target(self):
        """
        Оновлення координат цілі залежно від стану примари:
         - alive: ціль - Pac-Man
         - frightened: ціль - Pac-Man (але з логікою у move)
         - in_house: ціль - вихід із будинку
         - dead: ціль - будинок
        """
        if self.state == "alive":
            self.target = GlobalVars.pacman.move_unit.coordinates
        elif self.state == "frightened":
            self._target = GlobalVars.pacman.move_unit.coordinates
        elif self.state == "in_house":
            self._target = Coordinate(
                GlobalVars.tilemap.house.x_global,
                GlobalVars.tilemap.house.y_global - 3 * GlobalVars.tile_size
            )
        elif self.state == "dead":
            self.target = GlobalVars.tilemap.house

    def alive_logic(self):
        if GlobalVars.power_is_active:
            if not self.immunity:
                self.turn_frightened()
        else:
            self.immunity = False

    def frightened_logic(self):
        # Якщо дія Power закінчилася, повернутися до alive
        if not GlobalVars.power_is_active:
            self.turn_alive()

    def dead_logic(self):
        # Якщо примара дісталася цілі, переходить у будинок
        if self.move_unit.coordinates == self._target:
            self.turn_in_house()

    def in_house_logic(self, delta):
        # Таймер перебування в будинку
        self.house_timer -= delta
        if self.house_timer < 0:
            if self._target == self.move_unit.coordinates:
                self.turn_alive()
            else:
                self.move_unit.freeze = False

    def move(self, delta):
        """
        Логіка руху примари. Враховує:
         - Стан (dead, in_house).
         - Напрямок руху.
         - Перевірку стін та використання координат цілі (target).
        """
        ghost = self.state in ["in_house", "dead"]
        dx = self._target.x_global - self.move_unit.coordinates.x_global
        dy = self._target.y_global - self.move_unit.coordinates.y_global

        # Вибираємо напрямок руху
        if abs(dx) > abs(dy):
            self.direction = 0 if dx > 0 else 2
        else:
            self.direction = 1 if dy > 0 else 3

        # У стані frightened примара частково рухається у протилежний бік
        if self.state == "frightened":
            self.direction = abs(self.direction - 2)

        # Якщо напрямок незмінний, не перевизначаємо його
        if (self.move_unit.direction +
                self.direction) % 2 == 0 and not self.time_to_drop:
            self.direction = self.move_unit.direction

        # Перевірка сусідніх тайлів
        tiles = GlobalVars.tilemap.get_neighbour_tiles(
            self.move_unit.coordinates)
        if not tiles[self.move_unit.direction]:
            pass
        elif tiles[self.move_unit.direction].is_wall and not (tiles[self.move_unit.direction].is_grates and ghost):
            if self.move_unit.direction == self.direction:
                if self.direction % 2 == 0:
                    self.direction = 1 if (
                        (dy > 0) + (self.state == "frightened")) % 2 else 3
                else:
                    self.direction = 0 if (
                        (dx > 0) + (self.state == "frightened")) % 2 else 2
            if tiles[self.direction].is_wall:
                self.direction = (self.direction + 2) % 4

        self.move_unit.move(delta, self.direction, is_ghost=ghost)
        self.time_to_drop = False


class Blinky(Ghost):
    """
    Blinky (червона примара): агресивно переслідує Pac-Man напряму.
    """

    def __init__(self, coordinates):
        super().__init__(coordinates, ghost_type=0)
        self.turn_alive()

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = copy.deepcopy(value)


class Pinky(Ghost):
    """
    Pinky (рожева примара): намагається передбачити рух Pac-Man,
    випереджає його приблизно на 4 тайли.
    """

    def __init__(self, coordinates):
        super().__init__(coordinates, ghost_type=1)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = copy.deepcopy(value)
        if self.state in ("in_house", "dead"):
            return
        offset = 4 * GlobalVars.tile_size
        d = GlobalVars.pacman.move_unit.direction
        if d == 0:
            self._target.x_global += offset
        elif d == 1:
            self._target.y_global += offset
        elif d == 2:
            self._target.x_global -= offset
        elif d == 3:
            self._target.y_global -= offset


class Inky(Ghost):
    """
    Inky (блакитна примара): вибирає ціль як точку,
    віддзеркалену відносно Blinky.
    """

    def __init__(self, coordinates):
        super().__init__(coordinates, ghost_type=2)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = copy.deepcopy(value)
        if self.state in ("in_house", "dead"):
            self._target.x_global -= GlobalVars.tile_size * 2
            return
        blinky_pos = GlobalVars.ghosts[0].move_unit.coordinates
        mid_x = (self._target.x_global + blinky_pos.x_global) / 2
        mid_y = (self._target.y_global + blinky_pos.y_global) / 2
        self._target.x_global = 2 * blinky_pos.x_global - mid_x
        self._target.y_global = 2 * blinky_pos.y_global - mid_y


class Clyde(Ghost):
    """
    Clyde (помаранчева примара): якщо Pac-Man далеко, переслідує;
    якщо близько, тікає.
    При цьому "близько" і "далеко" визначаються за допомогою
    Manhattan-відстані (coward_distance, angry_distance).
    """

    def __init__(self, coordinates):
        self.coward = False
        self.coward_distance = 8
        self.angry_distance = 16
        super().__init__(coordinates, ghost_type=3)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = copy.deepcopy(value)
        if self.state in ("in_house", "dead"):
            self._target.x_global += GlobalVars.tile_size * 2
            return

        dist = abs(self._target.x_global - self.move_unit.coordinates.x_global) \
            + abs(self._target.y_global - self.move_unit.coordinates.y_global)

        # Перевіряємо, чи треба тікати або переслідувати
        if self.coward:
            if dist >= GlobalVars.tile_size * self.angry_distance:
                self.coward = False

            # Хитрість: віддаляємо ціль від примари
            delta = GlobalVars.tilemap.width * GlobalVars.tilemap.height
            if self._target.x_global - self.move_unit.coordinates.x_global > 0:
                self._target.x_global -= GlobalVars.tile_size * delta
            else:
                self._target.x_global += GlobalVars.tile_size * delta

            if self._target.y_global - self.move_unit.coordinates.y_global > 0:
                self._target.y_global -= GlobalVars.tile_size * delta
            else:
                self._target.y_global += GlobalVars.tile_size * delta
        else:
            if dist <= GlobalVars.tile_size * self.coward_distance:
                self.coward = True
