import pygame

from classes.global_vars import GlobalVars


class AnimationSet:
    def __init__(self, frames, time, name):
        """
        frames – список кадрів (pygame.Surface).
        time – список затримок для кожного кадру.
        name – ім'я анімації.
        """
        self.frames = frames
        self.time = time
        self.name = name

        self._timer = 0
        self.frame = 0
        self.direction = 0
        self.cycle = True

    def draw(self, position):
        if not self.frames:
            return

        current_frame = self.frames[self.frame]
        rotated_frame = pygame.transform.rotate(
            current_frame, -90 * self.direction)
        frame_rect = rotated_frame.get_rect()
        draw_position = (
            position.x_global - frame_rect.width // 2,
            position.y_global - frame_rect.height // 2
        )
        GlobalVars.screen.blit(rotated_frame, draw_position)

    def update(self, delta, position):
        """Оновлюємо поточний кадр, враховуючи delta-час та налаштування."""
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
                    self._timer = 0
                else:
                    self.frame -= 1
