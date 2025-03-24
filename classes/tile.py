import os

import pygame

from classes.animation import Animation
from classes.animation_set import AnimationSet
from classes.global_vars import GlobalVars
from classes.next_move import NextMove


class Tile:
    def __init__(self, coordinates, tile_id):
        # Ініціалізація плитки з заданими координатами та ідентифікатором
        self.coordinates = coordinates
        self._tile_id = tile_id

        # Створення анімації для плитки
        self.animation = Animation(self._get_images(), coordinates)
        # Визначення, чи є плитка стіною (ідентифікатори 1-6) або ґратами
        # (ідентифікатор 7)
        self.is_wall = 1 <= tile_id <= 6
        self.is_grates = (tile_id == 7)

        # Реєстрація функції оновлення через NextMove
        self.next_move = NextMove('tile', self.update)
        self.objects = []

    def add_object(self, obj):
        # Додаємо об'єкт до списку об'єктів на плитці
        self.objects.append(obj)

    def remove_object(self, obj):
        # Видаляємо об'єкт із списку об'єктів на плитці
        self.objects.remove(obj)

    def _get_images(self):
        # Визначення зображень для плитки залежно від її ідентифікатора
        images = {
            7: ("entry", "grate_animation"),
            5: ("right_up", "right_up_animation"),
            6: ("left_up", "left_up_animation"),
            4: ("right_down", "right_down_animation"),
            3: ("left_down", "left_down_animation"),
            2: ("horizontal", "horizontal_animation"),
            1: ("vertical", "vertical_animation"),
            0: ("void", "void_animation")
        }

        if self._tile_id in images:
            img_name, anim_name = images[self._tile_id]
        else:
            img_name, anim_name = images[0]

        img_path = os.path.join(
            "static_file", "map_walls_photos", f"{img_name}.png")
        frame = pygame.transform.scale(
            pygame.image.load(img_path),
            (GlobalVars.tile_size, GlobalVars.tile_size)
        )
        frames = [frame]
        return [
            AnimationSet(
                frames=frames,
                time=[0.2] *
                len(frames),
                name=anim_name)]

    def update(self, delta):
        # Оновлюємо анімацію плитки
        self.animation.update(delta)
