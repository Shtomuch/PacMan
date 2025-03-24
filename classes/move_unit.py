# from classes import Tilemap
from classes.coordinates import Coordinate
from classes.global_vars import GlobalVars


class MoveUnit:
    def __init__(self, speed, coordinates):
        self.speed = speed
        self.coordinates = coordinates
        self.direction = 0  # 0=право, 1=вниз, 2=влево, 3=вверх
        self.freeze = False
        self._is_turn = -1

    def _reset_turn(self):
        self._is_turn = GlobalVars.tile_size
        # print("OK")

    def move(
            self,
            delta,
            new_direction,
            is_ghost=False,
            second_chance=False) -> float:
        """Повертає пройдену відстань від центру"""
        if self.freeze:
            return 0

        if (new_direction + self.direction) % 2 == 0:
            self.direction = new_direction
        tiles = GlobalVars.tilemap.get_neighbour_tiles(self.coordinates)

        dist = self.speed * delta * GlobalVars.tile_size
        self._is_turn -= dist
        center = Coordinate.get_tile_center(
            self.coordinates.x_tile, self.coordinates.y_tile)
        tile = GlobalVars.tilemap.get_tile(self.coordinates)
        dist = self._change_position(dist, center)

        if dist > 0:
            if not tiles[new_direction] or not tiles[self.direction]:
                if not tile:
                    if self.direction == 0 and self.coordinates.x_tile > 0:
                        self.coordinates.x_global -= (
                            GlobalVars.tilemap.width + 2) * GlobalVars.tile_size
                    elif self.direction == 2 and self.coordinates.x_tile < 0:
                        self.coordinates.x_global += (
                            GlobalVars.tilemap.width + 2) * GlobalVars.tile_size
                return dist

            if (new_direction + self.direction) % 2 == 1 and 0 > self._is_turn and \
                    not (tiles[new_direction].is_wall or (tiles[new_direction].is_grates and not is_ghost)):
                self._change_position(-dist, center)
                self.direction = new_direction
                self._reset_turn()
                return self.move(
                    dist /
                    self.speed /
                    GlobalVars.tile_size,
                    new_direction,
                    is_ghost)

            if tiles[self.direction].is_wall or (
                    tiles[self.direction].is_grates and not is_ghost):
                self._change_position(-dist, center)
                # if (new_direction+self.direction) % 2 == 1 and not second_chance:
                #     # self.direction = new_direction
                # return self.move(dist / self.speed / GlobalVars.tile_size,
                # new_direction, is_ghost, second_chance=True)

        return dist

        # return self.coordinates

    def _change_position(self, dist, center) -> float:
        if self.direction == 0:  # вправо
            self.coordinates.x_global += dist
            return self.coordinates.x_global - center.x_global
        elif self.direction == 1:  # вниз
            self.coordinates.y_global += dist
            return self.coordinates.y_global - center.y_global
        elif self.direction == 2:  # влево
            self.coordinates.x_global -= dist
            return -self.coordinates.x_global + center.x_global
        elif self.direction == 3:  # вверх
            self.coordinates.y_global -= dist
            return -self.coordinates.y_global + center.y_global
