import os
import pygame
from classes.score import Score
from classes.animation import Animation
from classes.next_move import NextMove
from classes.animation_set import AnimationSet
from classes.global_vars import GlobalVars

class Dot:
    def __init__(self, coordinates):
        # Ініціалізація об'єкта Dot з заданими координатами
        self.coordinates = coordinates

        # Створення анімації для об'єкта Dot
        self.animation = Animation(Dot.get_images(), coordinates)
        # Встановлення балів (10 балів)
        self.score = Score(10)
        # Реєстрація функції оновлення через NextMove
        self.next_move = NextMove('point', self.update)

    @staticmethod
    def get_images() -> list:
        # Завантаження та масштабування зображень для анімації Dot
        dot_frames = [
            pygame.transform.scale(
                pygame.image.load(os.path.join("static_file", "coin_photos", "coin.png")),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("static_file", "coin_photos", "smaller_coin.png")),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        # Створення AnimationSet з кадрами та часом відображення
        dot_animation = [AnimationSet(frames=dot_frames, time=[0.2] * len(dot_frames), name="dot_animation")]
        return dot_animation

    def update(self, delta):
        # Оновлення анімації об'єкта Dot
        self.animation.update(delta)

    def disappear(self):
        # Активуємо додавання балів і видаляємо функцію оновлення
        self.score.active()
        self.next_move.remove_func()