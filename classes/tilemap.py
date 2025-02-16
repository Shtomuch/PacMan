import random

from classes.coordinates import Coordinate
from classes.tile import Tile
from classes.point import *
from classes.global_vars import GlobalVars
from classes.next_move import NextMove

class Tilemap:
      # Для примера

    def __init__(self, board, max_height, max_width):
        h = max_height/len(board)
        w = max_width/len(board[0])
        GlobalVars.tile_size = min(h, w)

        self._tilemap = board
        self._gates = Coordinate(-100, -100)
        self.construct_tilemap()

        self._timer = 0
        self.fruit_spawn = 2
        self.next_move = NextMove('point', self.update)




    @property
    def house(self):
        return Coordinate(self._gates.x_global, self._gates.y_global + GlobalVars.tile_size * 2)

    @property
    def pacman_fp(self):
        return Coordinate(self._gates.x_global, self._gates.y_global + GlobalVars.tile_size * 5)

    def construct_tilemap(self):
          """
          На основе двумерного массива board создаём массив Tile.
          Условимся, что board – список списков, где каждое значение – tile_id.
          """
          dot_func = Tilemap.start_generate_dots()

          for y, row in enumerate(self._tilemap):
              for x, tile_id in enumerate(row):
                  coord = Coordinate.get_tile_center(x, y)
                  tile_obj = Tile(coord, tile_id)

                  if tile_id == 0 and not self.is_in_ghost_house(coord):
                      tile_obj.add_object(dot_func(tile_obj.coordinates))
                  elif tile_id == 7:
                      self._gates = Coordinate(tile_obj.coordinates.x_global - GlobalVars.tile_size * 0.5,
                                               tile_obj.coordinates.y_global)

                  self._tilemap[y][x] = tile_obj

    @staticmethod
    def start_generate_dots():
        chance = 0.02

        def inner(coord):
            nonlocal chance
            if random.random() < chance:
                chance = 0.001
                return BigDot(coord)
            else:
                chance *= 1.05
                return Dot(coord)

        return inner

    @property
    def height(self) -> int:
        return len(self._tilemap)

    @property
    def width(self) -> int:
        return len(self._tilemap[0])

    def get_neighbour_tiles(self, coordinate) -> list:
          """
          Повертаємо сусідні тайли у порядку: право, вниз, ліво, вверх.
          Використовуємо (dy, dx), де перший елемент – зміщення по y, а другий – по x.
          """
          tx = coordinate.x_tile
          ty = coordinate.y_tile
          neighbors = []
          # (dy, dx): право (0, +1), вниз (+1, 0), ліво (0, -1), вверх (-1, 0)
          for (dy, dx) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
              ny = ty + dy
              nx = tx + dx
              if 0 <= nx < self.width and 0 <= ny < self.height:
                  neighbors.append(self._tilemap[ny][nx])
              else:
                  neighbors.append(None)
          return neighbors

    def get_tile(self, coordinate):
        tx = coordinate.x_tile
        ty = coordinate.y_tile
        if 0 <= tx < self.width and 0 <= ty < self.height:
            return self._tilemap[ty][tx]
        return None

    def is_in_ghost_house(self, coord: Coordinate) -> bool:
          """
          Визначаємо, чи належить плитка (за її центром) до доміка привидів.
          Тут можна задати прямокутну область, що покриває будинок.
          Наприклад, якщо двері (гейти) розташовані в певному місці,
          визначаємо область відносно _gates або property house.
          """
          # Приклад: якщо вважаємо, що будинок займає 3x3 плитки,
          # а його центр – self.house (якщо self.house повертає центр доміку)
          house_center = self.house
          left_bound = house_center.x_global - GlobalVars.tile_size * 2.5
          right_bound = house_center.x_global + GlobalVars.tile_size * 2.5
          top_bound = house_center.y_global - GlobalVars.tile_size * 1.5
          bottom_bound = house_center.y_global + GlobalVars.tile_size * 1.5

          x = coord.x_global
          y = coord.y_global
          return left_bound <= x <= right_bound and top_bound <= y <= bottom_bound

    def update(self, delta):
        self._timer += delta
        if self._timer < self.fruit_spawn:
            return
        self._timer -= self.fruit_spawn

        x = random.randrange(0, self.width)
        y = random.randrange(0, self.height)
        tile = self._tilemap[y][x]
        if not tile.is_wall and not tile.is_grates and not tile.objects and not self.is_in_ghost_house(tile.coordinates):
            r = random.random()
            if r < 0.45:
                tile.objects.append(Cherry(tile.coordinates))
            elif r < 0.9:
                tile.objects.append(Strawberry(tile.coordinates))
            else:
                tile.objects.append(BigDot(tile.coordinates))




