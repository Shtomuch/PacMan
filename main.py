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
      - колір фону (r,g,b),
      - розміри екрану (w,h).
    Якщо користувач нічого не вводить або вводить некоректно,
    беремо дефолтні значення:
      - 3 життя,
      - фон (0,20,0),
      - розміри: 900x950.
    """
    try:
        lives = int(input("Введіть кількість життів (дефолт = 3): ") or 3)
    except ValueError:
        lives = 3

    try:
        color_input = input("Введіть колір фону (r,g,b), дефолт=(0,20,0): ")
        if not color_input.strip():
            raise ValueError
        r, g, b = map(int, color_input.split(","))
        bg_color = (r, g, b)
    except ValueError:
        bg_color = (0, 20, 0)

    try:
        size_input = input("Введіть ширину та висоту (w,h) (дефолт 900 на 950): ")
        if not size_input.strip():
            raise ValueError
        width, height = map(int, size_input.split(","))
    except ValueError:
        width = 900
        height = 950

    return lives, bg_color, width, height


def wait_for_keypress(screen, overlay, draw_callback):
    """
    Загальна функція для очікування натискання клавіші,
    оновлюючи екран із заданим overlay і викликом функції для малювання.
    """
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

        screen.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        draw_callback(screen)
        pygame.display.flip()


def show_start_overlay(screen):
    """
    Відображає напівпрозорий стартовий екран з текстом:
    "Натисніть будь-яку клавішу, щоб розпочати гру".
    Якщо текст занадто широкий, розбиває його на два рядки.
    """
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # 50% прозорості

    font = pygame.font.SysFont("static_file\\fonts\\PressStart2P.ttf", 36)
    text = "Натисніть будь-яку клавішу, щоб розпочати гру"

    # Встановлюємо максимальну ширину тексту з відступом:
    max_width = screen.get_width() - 40

    # Розбиваємо текст на рядки, якщо він занадто широкий.
    if font.size(text)[0] > max_width:
        words = text.split()
        mid = len(words) // 2
        lines = [" ".join(words[:mid]), " ".join(words[mid:])]
    else:
        lines = [text]

    text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]
    total_height = sum(surf.get_height() for surf in text_surfaces) + (len(text_surfaces) - 1) * 10
    start_y = (screen.get_height() - total_height) // 2

    def draw_overlay(surf):
        y = start_y
        for ts in text_surfaces:
            rect = ts.get_rect(center=(surf.get_width() // 2, y + ts.get_height() // 2))
            surf.blit(ts, rect)
            y += ts.get_height() + 10

    wait_for_keypress(screen, overlay, draw_overlay)


def show_end_overlay(screen, final_score):
    """
    Відображає напівпрозорий екран завершення гри з фінальним рахунком.
    """
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # напівпрозорий фон

    font = pygame.font.SysFont("static_file\\fonts\\PressStart2P.ttf", 36)
    lines = [
        f"Гру завершено. Ваш рахунок: {int(final_score)}",
        "Натисніть будь-яку клавішу,",
        "щоб закрити гру",
    ]
    text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]
    total_height = sum(s.get_height() for s in text_surfaces) + (len(text_surfaces) - 1) * 40
    start_y = (screen.get_height() - total_height) // 2

    def draw_overlay(surf):
        y = start_y
        for ts in text_surfaces:
            rect = ts.get_rect(center=(surf.get_width() // 2, y + ts.get_height() // 2))
            surf.blit(ts, rect)
            y += ts.get_height() + 40

    wait_for_keypress(screen, overlay, draw_overlay)


def main():
    # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man Clone")

    lives, bg_color, width, height = get_game_params()
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