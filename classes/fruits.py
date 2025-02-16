from classes.score import Score
from classes.animation import Animation
import pygame
from classes.animation_set import AnimationSet
from classes.global_vars import GlobalVars
from classes.next_move import NextMove

class Fruit: 
    def __init__(self, coordinates, points=0):
        self.coordinates = coordinates
        self.animation = Animation(self.get_images(), coordinates)
        self.score = Score(points)
        self.next_move = NextMove("point", self.update)

    @staticmethod
    def get_images():
        return []
    
    def disappear(self):
        self.score.active()
        self.next_move.remove_func()

    def update(self, delta):
        self.animation.update(delta)


class Cherry(Fruit):
    def __init__(self, coordinates):
        super().__init__(coordinates, points=100)

    @staticmethod
    def get_images() -> list:
        cherry_frames = [
            pygame.transform.scale(
            pygame.image.load(f'static_file\\fruits_photos\\cherry.png'), (GlobalVars.tile_size, GlobalVars.tile_size)
            )]
        cherry_animaton = [AnimationSet(frames=cherry_frames, time=[0.2] * len(cherry_frames), name="chery_animation")]
        return cherry_animaton


class Strawberry(Fruit):
    def __init__(self, coordinates):
        super().__init__(coordinates, points=300)

    @staticmethod
    def get_images():
        strawberry_frames = [
            pygame.transform.scale(
            pygame.image.load(f'static_file\\fruits_photos\\strawberry.png'), (GlobalVars.tile_size, GlobalVars.tile_size)
            )]
        strawberry_animaton = [AnimationSet(frames=strawberry_frames, time=[0.2] * len(strawberry_frames), name="strawberry_animation")]
        return strawberry_animaton