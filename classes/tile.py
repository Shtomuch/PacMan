from classes.animation import Animation
from classes.global_vars import GlobalVars
from classes.next_move import NextMove
from classes.animation_set import AnimationSet
import pygame


class Tile:
    def __init__(self, coordinates, tile_id):
        self.coordinates = coordinates
        self._tile_id = tile_id

        self.animation = Animation(self._get_images(), coordinates)
        self.is_wall = (tile_id >= 1) and (tile_id <= 6)  # Предположим 1 = стена
        self.is_grates = (tile_id == 7) # 7 = ворота

        self.next_move = NextMove('tile', self.update)
        self.objects = []



    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def _get_images(self):
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
            frames = [
                pygame.transform.scale(
                pygame.image.load(f'static_file\\map_walls_photos\\{img_name}.png'), (GlobalVars.tile_size, GlobalVars.tile_size)
                )]
            return [AnimationSet(frames=frames, time=[0.2] * len(frames), name=anim_name)]
        else:
            img_name, anim_name = images[0]
            frames = [
                pygame.transform.scale(
                pygame.image.load(f'static_file\\map_walls_photos\\{img_name}.png'), (GlobalVars.tile_size, GlobalVars.tile_size)
                )]
            return [AnimationSet(frames=frames, time=[0.2] * len(frames), name=anim_name)]



    def update(self, delta):
        self.animation.update(delta)