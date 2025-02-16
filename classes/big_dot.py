"""Модуль для роботи з об'єктом BigDot (велика монета, що дає додаткові бали та активує ефект Power)."""

from classes.animation import Animation
from classes.global_vars import GlobalVars
from classes.power import Power
from classes.score import Score
from classes.next_move import NextMove
import pygame
from classes.animation_set import AnimationSet

class BigDot:
    """Клас, що представляє велику монету в грі."""
    def __init__(self, coordinates) -> None:
        """Ініціалізація BigDot: координати, анімація, рахунок і реєстрація оновлення."""
        self.coordinates = coordinates
        self.animation = Animation(BigDot.get_images(), coordinates)  # створення анімації
        self.score = Score(50)  # встановлення балів
        self.next_move = NextMove('point', self.update)  # реєстрація функції оновлення

    @staticmethod
    def get_images() -> list:
        """Повертає набір анімації для BigDot."""
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
        big_dot_animation = [AnimationSet(frames=big_dot_frames, time=[0.1] * len(big_dot_frames), name="big_dot_animation")]
        return big_dot_animation

    def update(self, delta: float) -> None:
        """Оновлює анімацію BigDot."""
        self.animation.update(delta)

    def disappear(self) -> None:
        """Активує рахунок, запускає ефект Power та зупиняє оновлення."""
        self.score.active()        # активуємо рахунок
        Power.activate()           # активуємо ефект Power
        self.next_move.remove_func()  # зупиняємо оновлення
