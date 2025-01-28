

class Board:
    def __init__(self, board_data, tile_images, tile_size=30):
        self.board_data = board_data
        self.tile_images = tile_images
        self.tile_size = tile_size
        self.rows = len(board_data)
        self.cols = len(board_data[0]) if board_data else 0
        self.background_surface = self._create_static_surface()

    def _create_static_surface(self):
        import pygame
        surf = pygame.Surface((self.cols * self.tile_size, self.rows * self.tile_size))
        surf.fill((0, 0, 0))
        for r in range(self.rows):
            for c in range(self.cols):
                tile_id = self.board_data[r][c]
                img = self.tile_images.get(tile_id)
                if img:  # якщо це, наприклад, стіна чи щось, що треба малювати
                    tile_surf = pygame.transform.scale(img, (self.tile_size, self.tile_size))
                    surf.blit(tile_surf, (c * self.tile_size, r * self.tile_size))
        return surf

    def draw(self, screen):
        screen.blit(self.background_surface, (0, 0))

    def is_wall(self, tile_x, tile_y):
        """Перевірка, чи цей тайл є стіною (ID >= 3 чи якось інакше)."""
        # У вашому випадку: 3..8 — це частини стін.
        if 0 <= tile_y < self.rows and 0 <= tile_x < self.cols:
            tid = self.board_data[tile_y][tile_x]
            return tid in [3 ,4 ,5 ,6 ,7 ,8]  # або інша логіка
        return True  # за межами — вважаємо стіною

    def is_gate(self, tile_x, tile_y):
        """Приклад, якщо треба перевірити, чи це 'ворота' (ID=9)."""
        if 0 <= tile_y < self.rows and 0 <= tile_x < self.cols:
            return self.board_data[tile_y][tile_x] == 9
        return False