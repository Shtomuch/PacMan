import copy
import pygame
from classes.animation import Animation
from classes.score import Score
from classes.move_unit import MoveUnit
from classes.next_move import NextMove
from classes.global_vars import GlobalVars
from classes.animation_set import AnimationSet
from classes.coordinates import Coordinate


class Ghost:
    """
    Клас для представлення привида в грі Pac-Man.
    """

    def __init__(self, coordinates: Coordinate, ghost_type: int) -> None:
        """
        Ініціалізація об'єкта привида.
        :param coordinates: Початкові координати привида.
        :param ghost_type: Тип привида (0 - червоний, 1 - рожевий, 2 - блакитний, 3 - оранжевий).
        """
        self.state: str = "in_house"
        self._target: Coordinate = coordinates
        self.move_unit: MoveUnit = MoveUnit(0, self._target)
        self.animation: Animation = Animation(self.get_images(ghost_type), coordinates)
        self.house_timer: float = 0.0
        self.immunity: bool = False
        self.direction: int = 0
        self.score: Score = Score(200)
        self.next_move: NextMove = NextMove('ghost', self.update)
        self.time_to_drop: bool = False
        self.turn_in_house()

    @staticmethod
    def get_images(ghost_type: int) -> list[AnimationSet]:
        """
        Завантажує анімації для привида відповідного типу.
        :param ghost_type: Тип привида.
        :return: Список анімацій привида.
        """
        colors = ["red", "pink", "blue", "orange"]
        color = colors[ghost_type]
        directions = ["right", "down", "left", "up"]
        ghost_animation = []

        for i, d in enumerate(directions):
            frames = [
                pygame.transform.scale(
                    pygame.image.load(f'static_file/ghost_photos/{color}/{color}_{d}_ghost{j}.png'),
                    (GlobalVars.tile_size, GlobalVars.tile_size)
                ) for j in range(1, 3)
            ]
            ghost_animation.append(
                AnimationSet(frames=frames, time=[0.1] * len(frames), name=f"ghost_animation_alive_{i}"))

        for i, d in enumerate(directions):
            frames = [
                pygame.transform.scale(
                    pygame.image.load(f'static_file/ghost_photos/eyes/ghost_eyes_{d}.png'),
                    (GlobalVars.tile_size, GlobalVars.tile_size)
                )
            ]
            ghost_animation.append(
                AnimationSet(frames=frames, time=[0.2] * len(frames), name=f"ghost_animation_dead_{i}"))

        frames = [
            pygame.transform.scale(pygame.image.load(f"static_file/ghost_photos/eaten/eaten_ghost1.png"),
                                   (GlobalVars.tile_size, GlobalVars.tile_size)),
            pygame.transform.scale(pygame.image.load(f"static_file/ghost_photos/eaten/eaten_ghost2.png"),
                                   (GlobalVars.tile_size, GlobalVars.tile_size))
        ]
        ghost_animation.append(AnimationSet(frames=frames, time=[0.2] * len(frames), name="ghost_animation_frightened"))

        return ghost_animation

    @property
    def target(self) -> Coordinate:
        return self._target

    @target.setter
    def target(self, value: Coordinate) -> None:
        raise NotImplementedError("Властивість Ghost.target повинна бути перевизначена у підкласі")

    def turn_frightened(self) -> None:
        self.state = "frightened"
        self.move_unit.speed = 3.5
        self.move_unit.freeze = False
        self.time_to_drop = True

    def turn_alive(self) -> None:
        self.state = "alive"
        self.move_unit.speed = 4.2
        self.move_unit.freeze = False
        self.time_to_drop = True

    def turn_in_house(self) -> None:
        self.state = "in_house"
        self.house_timer = 2.0
        self.move_unit.freeze = True
        self.move_unit.speed = 2

    def death(self) -> None:
        self.score.active()
        self.immunity = True
        self.state = "dead"
        self.move_unit.speed = 9

    def update(self, delta: float) -> None:
        if self.state == "alive":
            self.alive_logic()
        elif self.state == "frightened":
            self.frightened_logic()
        elif self.state == "dead":
            self.dead_logic()
        elif self.state == "in_house":
            self.in_house_logic(delta)

        self.update_target()
        self.move(delta)
        self.animation.position = self.move_unit.coordinates
        self.animation.direction = 0

        if self.state == "frightened":
            self.animation.current_animation = "ghost_animation_frightened"
        else:
            s = "alive" if self.state == "in_house" else self.state
            self.animation.current_animation = f"ghost_animation_{s}_{self.move_unit.direction}"

        self.animation.update(delta)

    def update_target(self) -> None:
        if self.state == "alive":
            self._target = GlobalVars.pacman.move_unit.coordinates
        elif self.state == "frightened":
            self._target = GlobalVars.pacman.move_unit.coordinates
        elif self.state == "in_house":
            self._target = Coordinate(GlobalVars.tilemap.house.x_global,
                                      GlobalVars.tilemap.house.y_global - 3 * GlobalVars.tile_size)
        elif self.state == "dead":
            self._target = GlobalVars.tilemap.house

    def alive_logic(self) -> None:
        if GlobalVars.power_is_active and not self.immunity:
            self.turn_frightened()
        else:
            self.immunity = False

    def frightened_logic(self) -> None:
        if not GlobalVars.power_is_active:
            self.turn_alive()

    def dead_logic(self) -> None:
        if self.move_unit.coordinates == self._target:
            self.turn_in_house()

    def in_house_logic(self, delta: float) -> None:
        self.house_timer -= delta
        if self.house_timer < 0 and self._target == self.move_unit.coordinates:
            self.turn_alive()
        else:
            self.move_unit.freeze = False

    def move(self, delta: float) -> None:
        """
        Обчислює та здійснює рух привида у напрямку цілі, враховуючи його стан.
        """
        ghost = (self.state in ["in_house", "dead"])
        dx = self._target.x_global - self.move_unit.coordinates.x_global
        dy = self._target.y_global - self.move_unit.coordinates.y_global
        if abs(dx) > abs(dy):
            self.direction = 0 if dx > 0 else 2
        else:
            self.direction = 1 if dy > 0 else 3

        if self.state == "frightened":
            self.direction = abs(self.direction - 2)

        if (self.move_unit.direction + self.direction) % 2 == 0 and not self.time_to_drop:
            self.direction = self.move_unit.direction

        tiles = GlobalVars.tilemap.get_neighbour_tiles(self.move_unit.coordinates)
        if not tiles[self.move_unit.direction]:
            pass
        elif tiles[self.move_unit.direction].is_wall and not (tiles[self.move_unit.direction].is_grates and ghost):
            if self.move_unit.direction == self.direction:
                if self.direction % 2 == 0:
                    self.direction = 1 if ((dy > 0) + (self.state == "frightened")) % 2 else 3
                else:
                    self.direction = 0 if ((dx > 0) + (self.state == "frightened")) % 2 else 2
            if tiles[self.direction].is_wall:
                self.direction = (self.direction + 2) % 4

        self.move_unit.move(delta, self.direction, is_ghost=ghost)
        self.time_to_drop = False


class Blinky(Ghost):
    """
    Червоний привид, який агресивно переслідує Пакмена
    """

    def __init__(self, coordinates) -> None:
        super().__init__(coordinates, ghost_type=0)
        self.turn_alive()

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value) -> None:
        self._target = copy.deepcopy(value)


class Pinky(Ghost):
    """
    Розовий привид, який переслідує Пакмена, націлившись на 4 клітинку перед ним
    """

    def __init__(self, coordinates) -> None:
        super().__init__(coordinates, ghost_type=1)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value) -> None:
        self._target = copy.deepcopy(value)
        if self.state in ("in_house", "dead"):
            return

        offset = 4 * GlobalVars.tile_size
        direction = GlobalVars.pacman.move_unit.direction

        if direction == 0:
            self._target.x_global += offset
        elif direction == 1:
            self._target.y_global += offset
        elif direction == 2:
            self._target.x_global -= offset
        elif direction == 3:
            self._target.y_global -= offset


class Inky(Ghost):
    """
    Бірюзовий привид, який вибирає координати цілі посередині між Блінкі та Пакменом,
    віддзеркаливши їх відносно координат Блінкі
    """

    def __init__(self, coordinates) -> None:
        super().__init__(coordinates, ghost_type=2)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value) -> None:
        self._target = copy.deepcopy(value)
        if self.state in ("in_house", "dead"):
            self._target.x_global -= GlobalVars.tile_size * 2
            return

        blinky_pos = GlobalVars.ghosts[0].move_unit.coordinates
        mid_x = (self._target.x_global + blinky_pos.x_global) / 2
        mid_y = (self._target.y_global + blinky_pos.y_global) / 2

        self._target.x_global = 2 * blinky_pos.x_global - mid_x
        self._target.y_global = 2 * blinky_pos.y_global - mid_y


class Clyde(Ghost):
    """
    Оранжевий привид, який тікає від Пакмена, але наближується до нього, коли занадто далеко втік
    """

    def __init__(self, coordinates) -> None:
        self.coward: bool = False
        self.coward_distance: int = 8
        self.angry_distance: int = 16
        super().__init__(coordinates, ghost_type=3)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value) -> None:
        self._target = copy.deepcopy(value)
        if self.state in ("in_house", "dead"):
            self._target.x_global += GlobalVars.tile_size * 2
            return

        dist = abs(self._target.x_global - self.move_unit.coordinates.x_global) + \
               abs(self._target.y_global - self.move_unit.coordinates.y_global)

        if self.coward:
            if dist >= GlobalVars.tile_size * self.angry_distance:
                self.coward = False

            delta = GlobalVars.tilemap.width * GlobalVars.tilemap.height
            self._target.x_global += (
                                         -1 if self._target.x_global > self.move_unit.coordinates.x_global else 1) * GlobalVars.tile_size * delta
            self._target.y_global += (
                                         -1 if self._target.y_global > self.move_unit.coordinates.y_global else 1) * GlobalVars.tile_size * delta
        else:
            if dist <= GlobalVars.tile_size * self.coward_distance:
                self.coward = True

