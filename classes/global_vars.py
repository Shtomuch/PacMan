import pygame


class GlobalVars:
    tile_size = 10
    score = 0.0
    screen = pygame.display.get_surface()
    power_is_active = False
    tilemap = None
    pacman = None
    ghosts = []