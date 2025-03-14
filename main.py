import pygame
import sys

from board import board
from classes import GlobalVars
from classes.level import Level

pygame.init()
clock = pygame.time.Clock()
fps = 60

# ФІКСОВАНІ РОЗМІРИ ЕКРАНУ:
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700


def get_game_params():
    """
    Запитуємо у користувача через консоль:
      - кількість життів (int),
      - колір фону (r,g,b).
    Якщо користувач нічого не вводить або вводить некоректно,
    беремо дефолтні значення (3 життя, фон (0,20,0)).
    """
    try:
        lives = int(input("Введіть кількість життів (дефолт = 3): ") or 3)
    except ValueError:
        lives = 3

    try:
        color_input = input("Введіть колір фону (r,g,b), дефолт=(0,20,0): ") or "0,20,0"
        r, g, b = map(int, color_input.split(","))
        bg_color = (r, g, b)
    except:
        bg_color = (0, 20, 0)

    try:
        width, height = map(int, input("Введіть ширину та висоту (w,h) (дефолт 900 на 950): ").split(","))
    except:
        width = 900
        height = 950

    return lives, bg_color, width, height


def show_start_overlay(screen):
    """
    Напівпрозорий екран з текстом:
    "Натисніть будь-яку клавішу, щоб розпочати гру",
    з простим переносом рядків, якщо текст занадто широкий.
    """
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # 50% прозорості
    font = pygame.font.Font('static_file\\fonts\\PressStart2P.ttf', 16)
    text = "Натисніть будь-яку клавішу, щоб розпочати гру"

    # Встановлюємо максимальну ширину тексту з невеликим відступом:
    max_width = screen.get_width() - 40

    # Якщо текст перевищує max_width, розбиваємо його приблизно навпіл.
    if font.size(text)[0] > max_width:
        words = text.split()
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        lines = [line1, line2]
    else:
        lines = [text]

    # Рендеримо кожен рядок окремо.
    text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]
    total_height = sum(surf.get_height() for surf in text_surfaces) + (len(text_surfaces) - 1) * 10
    start_y = (screen.get_height() - total_height) // 2

    waiting = True
    while waiting:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

        screen.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        y = start_y
        for surf in text_surfaces:
            rect = surf.get_rect(center=(screen.get_width() // 2, y + surf.get_height() // 2))
            screen.blit(surf, rect)
            y += surf.get_height() + 10
        pygame.display.flip()


def show_end_overlay(screen, final_score):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # напівпрозорий фон

    font = pygame.font.SysFont('static_file\\fonts\\PressStart2P.ttf', 36)
    lines = [
        f"Гру завершено. Ваш рахунок: {int(final_score)}",
        "Натисніть будь-яку клавішу,",
        "щоб закрити гру"
    ]
    text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]
    text_rects = [
        surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + i * 40))
        for i, surface in enumerate(text_surfaces)
    ]

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

        screen.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        # Ітеруємося по кожній парі поверхня/прямокутник:
        for surface, rect in zip(text_surfaces, text_rects):
            screen.blit(surface, rect)
        pygame.display.flip()

def main():
    # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man Clone")

    lives, bg_color, width, height = get_game_params()

    # show_start_overlay(screen)

    level = Level(board, pacman_health=lives, bg_color=bg_color, screen_w=width, screen_h=height)
    show_start_overlay(GlobalVars.screen)

    running = True
    while running:
        delta_time = clock.tick(fps) / 1000.0
        if delta_time > 0.5:
            continue
        running = level.update(delta_time)
        pygame.display.flip()

    # Показуємо екран завершення
    show_end_overlay(GlobalVars.screen, GlobalVars.score)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()