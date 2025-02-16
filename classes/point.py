"""Модуль для об'єктів, що дають бали: фрукти, монети та великі монети."""

import pygame
from classes.score import Score
from classes.animation import Animation
from classes.animation_set import AnimationSet
from classes.global_vars import GlobalVars
from classes.next_move import NextMove
from classes.power import Power


class Point:
    """Базовий клас для об'єктів, що дають бали."""
    def __init__(self, coordinates, points=0) -> None:
        self.coordinates = coordinates
        self.animation = Animation(self.get_images(), coordinates)  # Ініціалізація анімації
        self.score = Score(points)  # Встановлення балів
        self.next_move = NextMove("point", self.update)  # Реєстрація оновлення

    @staticmethod
    def get_images():
        pass  # Має бути перевизначено у нащадків

    def disappear(self) -> None:
        self.score.active()  # Активує рахунок
        self.next_move.remove_func()  # Зупиняє оновлення

    def update(self, delta: float) -> None:
        self.animation.update(delta)  # Оновлення анімації


class Cherry(Point):
    """Вишня, що дає 100 балів."""
    def __init__(self, coordinates) -> None:
        super().__init__(coordinates, points=100)

    @staticmethod
    def get_images() -> list:
        cherry_frames = [
            pygame.transform.scale(
                pygame.image.load('static_file\\fruits_photos\\cherry.png'),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        # Повертає набір анімації для вишні
        cherry_animation = [AnimationSet(frames=cherry_frames, time=[0.2] * len(cherry_frames), name="chery_animation")]
        return cherry_animation


class Strawberry(Point):
    """Полуниці, що дають 300 балів."""
    def __init__(self, coordinates) -> None:
        super().__init__(coordinates, points=300)

    @staticmethod
    def get_images() -> list:
        strawberry_frames = [
            pygame.transform.scale(
                pygame.image.load('static_file\\fruits_photos\\strawberry.png'),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        # Повертає набір анімації для полуниці
        strawberry_animation = [AnimationSet(frames=strawberry_frames, time=[0.2] * len(strawberry_frames), name="strawberry_animation")]
        return strawberry_animation


class Dot(Point):
    """Монета, що дає 10 балів."""
    def __init__(self, coordinates) -> None:
        super().__init__(coordinates, points=10)

    @staticmethod
    def get_images() -> list:
        dot_frames = [
            pygame.transform.scale(
                pygame.image.load('static_file\\coin_photos\\coin.png'),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            ),
            pygame.transform.scale(
                pygame.image.load("static_file\\coin_photos\\smaller_coin.png"),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        # Повертає набір анімації для монети
        dot_animation = [AnimationSet(frames=dot_frames, time=[0.5] * len(dot_frames), name="dot_animation")]
        return dot_animation


class BigDot(Point):
    """Велика монета, що дає 50 балів та активує ефект Power."""
    def __init__(self, coordinates) -> None:
        super().__init__(coordinates, points=50)

    @staticmethod
    def get_images() -> list:
        big_dot_frames = [
            pygame.transform.scale(
                pygame.image.load('static_file\\coin_photos\\big_coin.png'),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            ),
            pygame.transform.scale(
                pygame.image.load("static_file\\coin_photos\\smaller_big_coin.png"),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        # Повертає набір анімації для великої монети
        big_dot_animation = [AnimationSet(frames=big_dot_frames, time=[0.1] * len(big_dot_frames), name="big_dot_animation")]
        return big_dot_animation

    def update(self, delta: float) -> None:
        self.animation.update(delta)  # Оновлення анімації

    def disappear(self) -> None:
        super().disappear()  # Виконує базову логіку зникнення
        Power.activate()  # Активує ефект Power
