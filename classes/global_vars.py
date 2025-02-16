import pygame


class GlobalVars:
    """
    Клас для зберігання глобальних змінних гри.
    """
    tile_size: float = 10
    score: float = 0.0
    screen: pygame.Surface = pygame.display.get_surface()
    power_is_active: bool = False
    tilemap = None
    pacman = None
    ghosts: list = []
