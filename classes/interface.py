import os
import pygame

# Імпортуємо необхідні класи з інших модулів
from classes import NextMove, AnimationSet, Animation, Coordinate
from classes.score import Score
from classes.global_vars import GlobalVars

class Interface:
    """
    Клас Interface: відповідає за відображення інтерфейсу гри (очки, здоров'я та ін.)
    """
    def __init__(self):
        pygame.font.init()
        # Ініціалізуємо шрифт
        self.font = pygame.font.Font(
            os.path.join('static_file', 'fonts', 'PressStart2P.ttf'),
            int(GlobalVars.tile_size / 1.2)
        )
        # Зареєструємо цю функцію у NextMove для подальшого виклику
        self.next_move = NextMove('interface', self.draw_misc)
        # Ініціалізація панелі здоров'я
        self.health_bar = Interface.PacmanHealth()

    class PacmanHealth:
        """
        Внутрішній клас для відображення здоров'я Pacman.
        """
        def __init__(self):
            self.health = []
            # Додаємо анімацію для кожної "життя" Pacman
            for i in range(GlobalVars.pacman.health):
                self.health.append(
                    Animation(
                        Interface.PacmanHealth.get_images(),
                        Coordinate(
                            (10 + i * 1.2) * GlobalVars.tile_size,
                            (GlobalVars.tilemap.height + 0.5) * GlobalVars.tile_size
                        )
                    )
                )

        @staticmethod
        def get_images():
            # Завантажуємо зображення та створюємо набір анімації
            health_frames = [
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join('static_file', 'pacman_photos', 'pacman1.png')
                    ),
                    (GlobalVars.tile_size, GlobalVars.tile_size)
                )
            ]
            health_animation = [
                AnimationSet(
                    frames=health_frames,
                    time=[0.2] * len(health_frames),
                    name="health_animation"
                )
            ]
            return health_animation

        def update(self):
            # Оновлюємо анімацію кожного "життя"
            for i in self.health:
                i.update(0)

    def delete_health(self):
        """
        Видаляємо один елемент здоров'я з панелі.
        """
        if self.health_bar.health:
            self.health_bar.health.pop()

    def draw_misc(self, _delta):
        """
        Метод для відображення додаткової інформації:
         - Відображення очок на екрані;
         - Оновлення панелі здоров'я.
        """
        screen = GlobalVars.screen
        if screen:
            score_text = self.font.render(f'Score: {int(GlobalVars.score)}', True, 'white')
            # Виводимо текст у нижній лівий кут
            screen.blit(score_text, (GlobalVars.tile_size / 2,
                                     GlobalVars.tilemap.height * GlobalVars.tile_size))
        else:
            print("Error: screen is not initialized in GlobalVars.")

        # Оновлюємо відображення здоров'я Pacman
        self.health_bar.update()