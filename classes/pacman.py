import os
import pygame

# Імпортуємо класи для анімації, управління, глобальних змінних та ін.
from classes.animation import Animation
from classes.animation_set import AnimationSet
from classes.global_vars import GlobalVars
from classes.move_unit import MoveUnit
from classes.next_move import NextMove
from classes.point import Point

class Pacman:
    """
    Клас Pacman: керує логікою пересування, анімацією та здоров'ям Pac-Man.
    """
    def __init__(self, first_pos, health):
        # Створюємо об'єкт для пересування
        self.move_unit = MoveUnit(4, first_pos)
        # Ініціалізуємо анімацію Pac-Man
        self.animation = Animation(Pacman._get_images(), first_pos)
        # Початковий напрямок руху та кількість життів
        self.direction = 0
        self.health = health
        # Додаємо в планувальник оновлення
        self.next_move = NextMove('pacman', self.update)

    @staticmethod
    def _get_images() -> list:
        """
        Завантаження зображень Pac-Man для анімації.
        """
        pacman_frames = [
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join('static_file', 'pacman_photos', f'pacman{i}.png')
                ),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
            for i in range(1, 5)
        ]
        pacman_animation = [
            AnimationSet(frames=pacman_frames, time=[0.1, 0.05] * 2, name="pacman_animation")
        ]
        return pacman_animation

    def death(self):
        """
        Обробка смерті Pac-Man: зменшення здоров'я та видалення з планувальника.
        """
        self.health -= 1
        self.next_move.remove_func()

    def update(self, delta):
        """
        Оновлення стану Pac-Man:
        - Розрахунок руху.
        - Перевірка на збір об'єктів (Point).
        - Оновлення позиції та напрямку анімації.
        """
        # Оновлюємо позицію
        d = self.move_unit.move(delta, self.direction)

        # Перевіряємо тайл, де знаходиться Pac-Man
        tile = GlobalVars.tilemap.get_tile(self.move_unit.coordinates)
        if tile:
            # Якщо є об'єкти та певний кадр анімації, збираємо Points
            if tile.objects and self.animation.animation_set.frame == 2 or (GlobalVars.tile_size / 4 > d > 0):
                for obj in tile.objects:
                    if isinstance(obj, Point):
                        obj.disappear()
                        tile.remove_object(obj)

        # Оновлюємо анімацію
        self.animation.position = self.move_unit.coordinates
        self.animation.direction = self.move_unit.direction
        self.animation.update(delta)