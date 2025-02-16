import math
import pygame

from classes import Power
from classes.global_vars import GlobalVars
from classes.interface import Interface
from classes.tilemap import Tilemap
from classes.pacman import Pacman
from classes.ghost import Blinky, Pinky, Inky, Clyde
from classes.coordinates import Coordinate
from classes.next_move import NextMove



class Level:
    def __init__(self, board, pacman_health=3, bg_color=(0, 20, 0), screen_w=900, screen_h=950):
        """
        board         – двовимірний список (карта рівня).
        pacman_health – кількість життів.
        bg_color      – колір фону (R,G,B).
        screen_w      – фіксована ширина екрану (за замовчуванням 900).
        screen_h      – фіксована висота екрану (за замовчуванням 950).
        """
        # Очищаємо список привидів
        GlobalVars.ghosts = []

        height, width = 1000, 600
        GlobalVars.tilemap = Tilemap(board, max_height=height, max_width=width)
        self.height = (GlobalVars.tilemap.height + 2) * GlobalVars.tile_size
        self.width = GlobalVars.tilemap.width * GlobalVars.tile_size

        # GlobalVars.tilemap = Tilemap(board, max_height=screen_h, max_width=screen_w)
        #
        # self.width = screen_w
        # self.height = screen_h

        GlobalVars.screen = pygame.display.set_mode((self.width, self.height))
        self.bg_color = bg_color
        GlobalVars.pacman = type('', (), {})()
        GlobalVars.pacman.health = pacman_health
        self.interface = Interface()
        self.reset_positions()
        # # Створюємо Пакмена
        # GlobalVars.pacman = Pacman(GlobalVars.tilemap.pacman_fp, pacman_health)
        #
        # # Створюємо привидів
        # hc = GlobalVars.tilemap.house
        #
        # self.ghosts_start = { name: c for (name, c) in ghost_positions }

    def update(self, delta: float) -> bool:
        """
        Основний цикл оновлення:
          1) Зчитування івентів.
          2) Заливка фоном + NextMove.activate(delta).
          3) Перевірка колізій (Pac-Man vs Ghosts).
          4) Якщо Pac-Man помирає — перевірка життя. Якщо ще лишилися, reset_positions().
             Якщо життя = 0 — повертаємо False (завершуємо гру).
        """
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

        # Очищуємо екран + оновлюємо всі NextMove
        GlobalVars.screen.fill(self.bg_color)
        NextMove.activate(delta)

        # Перевірка колізій Pac-Man vs Ghosts
        px = GlobalVars.pacman.move_unit.coordinates.x_global
        py = GlobalVars.pacman.move_unit.coordinates.y_global

        for ghost in GlobalVars.ghosts:
            gx = ghost.move_unit.coordinates.x_global
            gy = ghost.move_unit.coordinates.y_global

            dist = math.hypot(px - gx, py - gy)  # або (dx*dx + dy*dy)**0.5
            # Можна орієнтуватися ~ на розмір tile, щоб вважати об'єкти "дотичними"
            # Наприклад, якщо dist < 0.75 * GlobalVars.tile_size
            if dist < 0.75 * GlobalVars.tile_size:
                if ghost.state == "frightened":
                    ghost.death()
                elif ghost.state == "alive":
                    GlobalVars.pacman.death()
                    self.reset_positions()


                # # Якщо привид не "dead" і не "в будинку" (бо тоді він неактивний)
                # if ghost.state in ("alive", "exiting_house"):
                #     GlobalVars.pacman.death()
                #     ghost.state = "alive"
                #
                #     if GlobalVars.pacman.health <= 0:
                #         # Якщо життя вичерпалися, завершуємо гру
                #         return False
                #
                # elif ghost.state == "frightened":
                #     # Якщо є Power, привид стає "dead"
                #     ghost.death()
                #     # ghost.go_to_house()
                #
                # else:
                #     # Інакше вмирає Пакмен
                #     GlobalVars.pacman.death()
                #     ghost.state = "alive"
                #     ghost.immunity = False

        return True

    def reset_positions(self):
        Power.reset()
        GlobalVars.pacman = Pacman(GlobalVars.tilemap.pacman_fp, GlobalVars.pacman.health)
        hc = GlobalVars.tilemap.house

        for ghost in GlobalVars.ghosts:
            ghost.next_move.remove_func()

        GlobalVars.ghosts = []
        GlobalVars.ghosts.append(Blinky(Coordinate(hc.x_global, hc.y_global - GlobalVars.tile_size * 3)))
        GlobalVars.ghosts.append(Pinky(hc))
        GlobalVars.ghosts.append(Inky(hc))
        GlobalVars.ghosts.append(Clyde(hc))

        if self.interface:
            self.interface.delete_health()
        # GlobalVars.pacman.move_unit.coordinates.x_global = self.pacman_start.x_global
        # GlobalVars.pacman.move_unit.coordinates.y_global = self.pacman_start.y_global
        # GlobalVars.pacman.move_unit.direction = 0



