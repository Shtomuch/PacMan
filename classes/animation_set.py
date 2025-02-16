from classes.global_vars import GlobalVars
import pygame


class AnimationSet:
    """
    Клас для керування анімаціями.
    """

    def __init__(self, frames: list[pygame.Surface], time: list[float], name: str):
        """
        Ініціалізація набору анімацій.

        :param frames: Список кадрів анімації
        :param time: Список часу відображення кожного кадру
        :param name: Назва анімації
        """
        self.frames = frames
        self.time = time
        self.name = name

        self._timer = 0
        self.frame = 0
        self.direction = 0
        self.cycle = True

    def draw(self, position) -> None:
        """
        Відображає поточний кадр анімації, враховуючи позицію як центр.

        :param position: Об'єкт з координатами x_global та y_global
        """
        if not self.frames:
            return

        current_frame = self.frames[self.frame]
        rotated_frame = pygame.transform.rotate(current_frame, -90 * self.direction)
        frame_rect = rotated_frame.get_rect()
        draw_position = (
            position.x_global - frame_rect.width // 2,
            position.y_global - frame_rect.height // 2
        )
        GlobalVars.screen.blit(rotated_frame, draw_position)

    def update(self, delta: float, position) -> None:
        """
        Оновлює поточний кадр анімації на основі delta-часу.

        :param delta: Час, що минув з останнього оновлення
        :param position: Об'єкт з координатами x_global та y_global
        """
        if not self.frames:
            return

        self.draw(position)
        self._timer += delta
        if self._timer < self.time[self.frame]:
            return

        while self._timer > self.time[self.frame]:
            self._timer -= self.time[self.frame]
            self.frame += 1
            if self.frame >= len(self.frames):
                if self.cycle:
                    self.frame = 0
                else:
                    self.frame -= 1