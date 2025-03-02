# Pac-Man

This is a small Pac-Man clone written in Python using Pygame. The goal of this project is to demonstrate how a 2D game similar to Pac-Man can be structured: there is a tile-based board, collisions, a main character (Pac-Man), AI elements (ghosts), collectible items (Points), animations, and so on.

## Features

- 	Pac-Man style game: The main character (Pac-Man) has multiple lives, and the board contains dots, big dots, and fruits that yield points.
- 	Object-Oriented Logic: A classic structure with separate classes for:
- 	Pacman — handles movement logic, animations, and health.
- 	Point, Dot, BigDot, Cherry, Strawberry — collectible items that increase the score.
- 	Tilemap — manages the board with various tiles (walls, gates, empty tiles, etc.).
- 	GlobalVars — global variables and settings (tile size, current score, whether the “Power” mode is active, etc.).
- 	NextMove — an update scheduler that processes update() methods in a sequence of queues.
- 	Simple scheduling (NextMove): Executes updates in multiple “priority layers,” so different types of objects can be updated in order.
- 	Animation: Implemented through Animation and AnimationSet classes. Each object can have multiple frames and frame durations.
- 	Flexible extension: It is easy to add new fruit classes or other objects and modify the board because it is defined by a 2D array.

## Requirements

- 	Python 3.9+ (recommended)
- 	Pygame 2.1+

## Installation and Run

1.	Clone or download this repository:

        git clone https://github.com/Shtomuch/PacMan.git
        cd PacMan

2.	Ensure you have Pygame installed:

        pip install pygame


3.	Run the main script:

         python main.py


4.	The console will prompt for the number of lives and a background color (simply press Enter for default values).
5.	A start screen reading “Press any key to start the game” will appear. Press any key to begin.

## Project Structure

Key files and directories:

- 	main.py — Entry point that launches the main game loop, processes events, and creates the window.
- 	board.py — Contains the board layout (2D array) for the maze.
- 	classes/ — Main directory with all class definitions:
- 	global_vars.py — Contains global variables (GlobalVars).
- 	move_unit.py — Logic for moving units, including speed and direction.
- 	next_move.py — Schedules the update() calls.
- 	tile.py, tilemap.py — Represent individual tiles and the overall tilemap.
- 	point.py — Defines collectible items (Dot, BigDot, Cherry, Strawberry).
- 	pacman.py — The main hero character.
- 	ghost.py (if present) — Logic for ghosts (not shown in detail here).
- 	level.py — Puts everything together and initializes the level.
- 	animation.py, animation_set.py — Manage sprites and frame-based animations.
- 	score.py — Score handling logic.
- 	static_file/ — Folder containing images (sprites) for characters, coins, tiles, etc.
- 	fonts/ — Custom fonts for text rendering.

## Gameplay

1.	Pac-Man Movement:
 
    - 	(If implemented) arrow keys or WASD can be used to change Pacman.direction.
    - 	Event handling is typically in main.py or level.py.
  	
3.	Scoring:
   
    - 	Small dots (Dot) yield 10 points,
    - 	Big dots (BigDot) give 50,
    - 	Fruits (Cherry, Strawberry) give 100 or 300.
    - 	When Pac-Man eats a BigDot, Power mode activates.
  
5.	Continuation and Game Over:
     
   - Pac-Man has a certain number of lives, which decrease upon death.
   - 	When lives are zero, the game ends and shows the final score.

## Configuration & Improvements

- Difficulty: Adjust Pac-Man’s speed, fruit spawn frequency, and Power duration in Power class.
- Screen size: Defined in main.py and set by get_game_params().
- Possible Enhancements:
- Add ghost AI with various chase modes.
- Use custom textures or sprites for a unique style.
- Implement level transitions or multiple rounds.

## License

This project can be used as an example without strict limitations. However, keep in mind potential copyright issues on assets (sprites, fonts, sounds). If you plan to publish or monetize, please verify usage rights.

## Author & Contributions

- @Shtomuch.
- Feel free to open Pull Requests or Issues for improvements or bug fixes.

Enjoy Pac-Man! If you have any questions, open an Issue.

Happy Coding & Have Fun!
