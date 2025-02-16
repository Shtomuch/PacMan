import os
import pygame
from classes.score import Score
from classes.animation import Animation
from classes.animation_set import AnimationSet
from classes.global_vars import GlobalVars
from classes.next_move import NextMove


class Fruit:
    def __init__(self, coordinates, points=0):
        # Ініціалізація об'єкта Fruit з координатами та кількістю балів
        self.coordinates = coordinates
        self.animation = Animation(self.get_images(), coordinates)
        self.score = Score(points)
        self.next_move = NextMove("point", self.update)

    @staticmethod
    def get_images():
        # Метод має бути перевизначений у підкласах; повертає порожній список
        return []

    def disappear(self):
        # Активуємо набір балів та видаляємо функцію оновлення
        self.score.active()
        self.next_move.remove_func()

    def update(self, delta):
        # Оновлюємо анімацію об'єкта Fruit
        self.animation.update(delta)


class Cherry(Fruit):
    def __init__(self, coordinates):
        # Вишня дає 100 балів
        super().__init__(coordinates, points=100)

    @staticmethod
    def get_images() -> list:
        # Завантаження зображення для вишні з використанням os.path.join
        cherry_path = os.path.join("static_file", "fruits_photos", "cherry.png")
        cherry_frame = pygame.transform.scale(
            pygame.image.load(cherry_path),
            (GlobalVars.tile_size, GlobalVars.tile_size)
        )
        cherry_frames = [cherry_frame]
        # Створення AnimationSet для вишні
        cherry_animation = [AnimationSet(frames=cherry_frames, time=[0.2] * len(cherry_frames), name="chery_animation")]
        return cherry_animation


class Strawberry(Fruit):
    def __init__(self, coordinates):
        # Полуниці дають 300 балів
        super().__init__(coordinates, points=300)

    @staticmethod
    def get_images():
        # Завантаження зображення для полуниці з використанням os.path.join
        strawberry_path = os.path.join("static_file", "fruits_photos", "strawberry.png")
        strawberry_frame = pygame.transform.scale(
            pygame.image.load(strawberry_path),
            (GlobalVars.tile_size, GlobalVars.tile_size)
        )
        strawberry_frames = [strawberry_frame]
        # Створення AnimationSet для полуниці
        strawberry_animation = [
            AnimationSet(frames=strawberry_frames, time=[0.2] * len(strawberry_frames), name="strawberry_animation")]
        return strawberry_animation