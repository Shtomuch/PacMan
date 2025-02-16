"""Модуль для роботи з фруктами в грі (анімовані об’єкти, що дають бали)."""

from classes.score import Score
from classes.animation import Animation
import pygame
from classes.animation_set import AnimationSet
from classes.global_vars import GlobalVars
from classes.next_move import NextMove

class Fruit:
    """Базовий клас фрукта з анімацією, рахунком та логікою зникнення."""
    def __init__(self, coordinates, points: int = 0) -> None:
        # Ініціалізація координат, анімації, рахунку та оновлення
        self.coordinates = coordinates
        self.animation = Animation(self.get_images(), coordinates)
        self.score = Score(points)
        self.next_move = NextMove("point", self.update)

    @staticmethod
    def get_images() -> list:
        """Повертає список наборів анімації (порожній за замовчуванням)."""
        return []
    
    def disappear(self) -> None:
        """Активує рахунок та зупиняє оновлення анімації."""
        self.score.active()  # активуємо рахунок
        self.next_move.remove_func()  # зупиняємо оновлення

    def update(self, delta: float) -> None:
        """Оновлює анімацію фрукта."""
        self.animation.update(delta)


class Cherry(Fruit):
    """Клас для вишні з 100 балами."""
    def __init__(self, coordinates) -> None:
        super().__init__(coordinates, points=100)

    @staticmethod
    def get_images() -> list:
        """Завантажує зображення вишні та повертає набір анімації."""
        cherry_frames = [
            pygame.transform.scale(
                pygame.image.load('static_file\\fruits_photos\\cherry.png'),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        # Створюємо набір анімації для вишні
        cherry_animation = [AnimationSet(frames=cherry_frames, time=[0.2] * len(cherry_frames), name="chery_animation")]
        return cherry_animation


class Strawberry(Fruit):
    """Клас для полуниці з 300 балами."""
    def __init__(self, coordinates) -> None:
        super().__init__(coordinates, points=300)

    @staticmethod
    def get_images() -> list:
        """Завантажує зображення полуниці та повертає набір анімації."""
        strawberry_frames = [
            pygame.transform.scale(
                pygame.image.load('static_file\\fruits_photos\\strawberry.png'),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        # Створюємо набір анімації для полуниці
        strawberry_animation = [AnimationSet(frames=strawberry_frames, time=[0.2] * len(strawberry_frames), name="strawberry_animation")]
        return strawberry_animation
