from unittest.mock import Mock

import pygame
import pytest

from classes.coordinates import Coordinate
from classes.ghost import Blinky, Clyde, Inky, Pinky
from classes.global_vars import GlobalVars


@pytest.fixture
def setup_game():
    pygame.init()
    GlobalVars.tile_size = 16
    GlobalVars.pacman = type(
        "Pacman", (), {
            "move_unit": type(
                "MoveUnit", (), {
                    "coordinates": Coordinate(
                        100, 100), "direction": 0})()})

    GlobalVars.tilemap = Mock()
    GlobalVars.tilemap.get_neighbour_tiles.return_value = [
        Mock(is_wall=False, is_grates=False)] * 4
    GlobalVars.tilemap.get_tile.return_value = Mock(
        is_wall=False, is_grates=False)

    GlobalVars.tilemap.house = Coordinate(
        150, 150)  # Конкретні координати будинку
    GlobalVars.tilemap.width = 28  # Розмір мапи, щоб уникнути помилки з delta
    GlobalVars.tilemap.height = 31

    GlobalVars.ghosts = [
        Blinky(
            Coordinate(
                50, 50)), Pinky(
            Coordinate(
                50, 50)), Inky(
            Coordinate(
                50, 50)), Clyde(
            Coordinate(
                50, 50))]


@pytest.mark.parametrize("ghost_class, ghost_state", [
    (Blinky, "alive"),
    (Pinky, "in_house"),
    (Inky, "in_house"),
    (Clyde, "in_house")
])
def test_ghost_initialization(ghost_class, ghost_state, setup_game):
    ghost = ghost_class(Coordinate(50, 50))
    assert ghost.state == ghost_state
    assert ghost.move_unit.speed > 0


@pytest.mark.parametrize("state, expected_speed",
                         [("alive", 4.2), ("frightened", 3.5), ("dead", 9), ("in_house", 2)])
def test_ghost_state_changes(setup_game, state, expected_speed):
    ghost = Blinky(Coordinate(50, 50))
    if state == "alive":
        ghost.turn_alive()
    elif state == "frightened":
        ghost.turn_frightened()
    elif state == "dead":
        ghost.death()
    elif state == "in_house":
        ghost.turn_in_house()

    assert ghost.state == state
    assert ghost.move_unit.speed == expected_speed


@pytest.mark.parametrize("ghost_class, state", [
    (Blinky, "alive"), (Blinky, "frightened"), (Blinky, "dead"), (Blinky, "in_house"),
    (Pinky, "alive"), (Pinky, "frightened"), (Pinky, "dead"), (Pinky, "in_house"),
    (Inky, "alive"), (Inky, "frightened"), (Inky, "dead"), (Inky, "in_house"),
    (Clyde, "alive"), (Clyde, "frightened"), (Clyde, "dead"), (Clyde, "in_house")
])
def test_ghost_targeting_in_all_states(ghost_class, state, setup_game):
    ghost = ghost_class(Coordinate(50, 50))
    ghost.state = state

    ghost.update_target()
    assert ghost.target is not None
