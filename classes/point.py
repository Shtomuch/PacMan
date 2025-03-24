import os

import pygame

from classes.animation import Animation
from classes.animation_set import AnimationSet
from classes.global_vars import GlobalVars
from classes.next_move import NextMove
from classes.power import Power
# Класи для керування очками, анімацією та глобальними змінними
from classes.score import Score


class Point:
    """
    Клас Point: базова точка, яку можна зібрати на ігровому полі.
    """

    def __init__(self, coordinates, points=0):
        # Зберігаємо координати та ініціалізуємо анімацію й очки
        self.coordinates = coordinates
        self.animation = Animation(self.get_images(), coordinates)
        self.score = Score(points)
        # Наступний крок (update) викликає оновлення
        self.next_move = NextMove("point", self.update)

    @staticmethod
    def get_images():
        # Місце для повернення списку анімацій, перевизначається в нащадках
        pass

    def disappear(self):
        # Активація отримання очок і припинення оновлення
        self.score.active()
        self.next_move.remove_func()

    def update(self, delta):
        # Оновлення анімації
        self.animation.update(delta)


class Cherry(Point):
    """
    Клас Cherry: вишня з ігрового поля, дає 100 очок.
    """

    def __init__(self, coordinates):
        super().__init__(coordinates, points=100)

    @staticmethod
    def get_images() -> list:
        # Завантаження зображення вишні та створення анімації
        cherry_frames = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(
                    'static_file', 'fruits_photos', 'cherry.png')),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        cherry_animation = [
            AnimationSet(frames=cherry_frames, time=[
                         0.2] * len(cherry_frames), name="chery_animation")
        ]
        return cherry_animation


class Strawberry(Point):
    """
    Клас Strawberry: полуниця з ігрового поля, дає 300 очок.
    """

    def __init__(self, coordinates):
        super().__init__(coordinates, points=300)

    @staticmethod
    def get_images():
        # Завантаження зображення полуниці та створення анімації
        strawberry_frames = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(
                    'static_file', 'fruits_photos', 'strawberry.png')),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        strawberry_animation = [
            AnimationSet(
                frames=strawberry_frames,
                time=[0.2] *
                len(strawberry_frames),
                name="strawberry_animation")]
        return strawberry_animation


class Dot(Point):
    """
    Клас Dot: маленька крапка (монетка), дає 10 очок.
    """

    def __init__(self, coordinates):
        super().__init__(coordinates, points=10)

    @staticmethod
    def get_images() -> list:
        # Завантаження зображень монет та створення анімації
        dot_frames = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(
                    'static_file', 'coin_photos', 'coin.png')),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join(
                    'static_file', 'coin_photos', 'smaller_coin.png')),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        dot_animation = [
            AnimationSet(
                frames=dot_frames,
                time=[0.5] *
                len(dot_frames),
                name="dot_animation")]
        return dot_animation


class BigDot(Point):
    """
    Клас BigDot: велика крапка (велика монета), дає 50 очок.
    """

    def __init__(self, coordinates):
        super().__init__(coordinates, points=50)

    @staticmethod
    def get_images() -> list:
        # Завантаження зображень великої монети та створення анімації
        big_dot_frames = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(
                    'static_file', 'coin_photos', 'big_coin.png')),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join(
                    'static_file', 'coin_photos', 'smaller_big_coin.png')),
                (GlobalVars.tile_size, GlobalVars.tile_size)
            )
        ]
        big_dot_animation = [
            AnimationSet(frames=big_dot_frames, time=[
                         0.1] * len(big_dot_frames), name="big_dot_animation")
        ]
        return big_dot_animation

    def update(self, delta):
        # Оновлення анімації
        self.animation.update(delta)

    def disappear(self):
        # Активувати очки, а також увімкнути Power
        super().disappear()
        Power.activate()
