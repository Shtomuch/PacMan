import pygame

from classes import NextMove, AnimationSet, Animation, Coordinate
from classes.score import Score
from classes.global_vars import GlobalVars


class Interface:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font('static_file\\fonts\\PressStart2P.ttf', int(GlobalVars.tile_size/1.2))  # Створюємо шрифт
        self.next_move = NextMove('interface', self.draw_misc)
        self.health_bar = Interface.PacmanHealth()


    class PacmanHealth:
        def __init__(self):
            self.health = []
            for i in range(GlobalVars.pacman.health):
                self.health.append(Animation(Interface.PacmanHealth.get_images(), Coordinate(
                    (10 + i*1.2) * GlobalVars.tile_size, (GlobalVars.tilemap.height + 0.5) * GlobalVars.tile_size
                )))

        @staticmethod
        def get_images():
            health_frames = [
                pygame.transform.scale(
                    pygame.image.load(f'static_file\\pacman_photos\\pacman1.png'),
                    (GlobalVars.tile_size, GlobalVars.tile_size)
                )]
            health_animation = [
                AnimationSet(frames=health_frames, time=[0.2] * len(health_frames), name="health_animation")]
            return health_animation

        def update(self):
            for i in self.health:
                i.update(0)



    def delete_health(self):
        if self.health_bar.health:
            self.health_bar.health.pop()


    def draw_misc(self, _delta):
        """Малює очки на екрані"""
        screen = GlobalVars.screen
        if screen:
            score_text = self.font.render(f'Score: {int(GlobalVars.score)}', True, 'white')
            screen.blit(score_text, (GlobalVars.tile_size/2, GlobalVars.tilemap.height * GlobalVars.tile_size))  # Виводимо текст у нижньому лівому куті
        else:
            print("Error: screen is not initialized in GlobalVars.")

        self.health_bar.update()
