import os
import pygame
from classes.animation import Animation
from classes.animation_set import AnimationSet
from classes.global_vars import GlobalVars
from classes.next_move import NextMove
from classes.score import Score
from classes.power import Power

class BigDot:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.animation = Animation(BigDot.get_images(), coordinates)
        self.score = Score(50)
        self.next_move = NextMove('point', self.update)

    @staticmethod
    def get_images() -> list:
        big_coin_path = os.path.join("static_file", "coin_photos", "big_coin.png")
        smaller_big_coin_path = os.path.join("static_file", "coin_photos", "smaller_big_coin.png")
        frame1 = pygame.transform.scale(
            pygame.image.load(big_coin_path),
            (GlobalVars.tile_size, GlobalVars.tile_size)
        )
        frame2 = pygame.transform.scale(
            pygame.image.load(smaller_big_coin_path),
            (GlobalVars.tile_size, GlobalVars.tile_size)
        )
        frames = [frame1, frame2]
        return [AnimationSet(frames=frames, time=[0.1] * len(frames), name="big_dot_animation")]

    def update(self, delta):
        self.animation.update(delta)

    def disappear(self):
        self.score.active()
        Power.activate()
        self.next_move.remove_func()