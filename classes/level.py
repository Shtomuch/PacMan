"""Модуль для управління рівнем гри Pac-Man."""

import math
import pygame
from typing import List, Tuple

from classes import Power
from classes.global_vars import GlobalVars
from classes.interface import Interface
from classes.tilemap import Tilemap
from classes.pacman import Pacman
from classes.ghost import Blinky, Pinky, Inky, Clyde
from classes.coordinates import Coordinate
from classes.next_move import NextMove

class Level:
    """Клас для управління рівнем гри."""
    def __init__(self, board: List[List[int]], pacman_health: int = 3, bg_color: Tuple[int, int, int] = (0, 20, 0), screen_w: int = 900, screen_h: int = 950) -> None:
        """Ініціалізація рівня, екрану та початкових позицій."""
        GlobalVars.ghosts = []  # Очищення списку привидів
        height: int = 1000
        width: int = 600
        GlobalVars.tilemap = Tilemap(board, max_height=height, max_width=width)
        self.height: int = (GlobalVars.tilemap.height + 2) * GlobalVars.tile_size
        self.width: int = GlobalVars.tilemap.width * GlobalVars.tile_size
        GlobalVars.screen = pygame.display.set_mode((self.width, self.height))
        self.bg_color: Tuple[int, int, int] = bg_color
        GlobalVars.pacman = type('', (), {})()  # Тимчасовий об'єкт для Pac-Man
        GlobalVars.pacman.health = pacman_health
        self.interface: Interface = Interface()
        self.reset_positions()  # Встановлення початкових позицій

    def update(self, delta: float) -> bool:
        """Оновлення гри: обробка подій, руху та колізій."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    GlobalVars.pacman.direction = 0
                elif event.key == pygame.K_DOWN:
                    GlobalVars.pacman.direction = 1
                elif event.key == pygame.K_LEFT:
                    GlobalVars.pacman.direction = 2
                elif event.key == pygame.K_UP:
                    GlobalVars.pacman.direction = 3
        if GlobalVars.pacman.health <= 0:
            return False
        GlobalVars.screen.fill(self.bg_color)  # Заливка екрану фоном
        NextMove.activate(delta)
        px: float = GlobalVars.pacman.move_unit.coordinates.x_global
        py: float = GlobalVars.pacman.move_unit.coordinates.y_global
        for ghost in GlobalVars.ghosts:
            gx: float = ghost.move_unit.coordinates.x_global
            gy: float = ghost.move_unit.coordinates.y_global
            dist: float = math.hypot(px - gx, py - gy)
            if dist < 0.75 * GlobalVars.tile_size:
                if ghost.state == "frightened":
                    ghost.death()
                elif ghost.state == "alive":
                    GlobalVars.pacman.death()
                    self.reset_positions()
        return True

    def reset_positions(self) -> None:
        """Скидання позицій Пакмена та привидів."""
        Power.reset()
        GlobalVars.pacman = Pacman(GlobalVars.tilemap.pacman_fp, GlobalVars.pacman.health)
        hc: Coordinate = GlobalVars.tilemap.house
        for ghost in GlobalVars.ghosts:
            ghost.next_move.remove_func()
        GlobalVars.ghosts = []
        # Встановлення початкових позицій привидів
        GlobalVars.ghosts.append(Blinky(Coordinate(hc.x_global, hc.y_global - GlobalVars.tile_size * 3)))
        GlobalVars.ghosts.append(Pinky(hc))
        GlobalVars.ghosts.append(Inky(hc))
        GlobalVars.ghosts.append(Clyde(hc))
        if self.interface:
            self.interface.delete_health()
