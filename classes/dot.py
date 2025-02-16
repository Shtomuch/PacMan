"""Модуль для роботи з об'єктом Dot (монета, що дає бали)."""

from tkinter.font import names  # імпорт (може не використовуватись)
import pygame
from classes.score import Score
from classes.animation import Animation
from classes.next_move import NextMove
from classes.animation_set import AnimationSet
from classes.global_vars import GlobalVars

class Dot:
    """Клас Dot представляє монету з анімацією, рахунком та логікою зникнення."""
    def __init__(self, coordinates) -> None:
        """Ініціалізація Dot з координатами."""
        self.coordinates = coordinates
        self.animation = Animation(Dot.get_images(), coordinates)  # створення анімації
        self.score = Score(10)  # встановлення балів
        self.next_move = NextMove('point', self.update)  # реєстрація функції оновлення

    @staticmethod
    def get_images() -> list:
        """Повертає список з набором анімації для Dot."""
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
        dot_animation = [AnimationSet(frames=dot_frames, time=[0.2] * len(dot_frames), name="dot_animation")]
        return dot_animation

    def update(self, delta: float) -> None:
        """Оновлення анімації Dot."""
        self.animation.update(delta)

    def disappear(self) -> None:
        """Активує рахунок і припиняє оновлення анімації."""
        self.score.active()  # активуємо рахунок
        self.next_move.remove_func()  # зупиняємо оновлення
