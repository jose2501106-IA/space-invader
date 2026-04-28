import pygame


class Game:
    def __init__(self, font, FPS, lives, window, screen_width, screen_height,
                 bullets=0, clock=None):
        self.font = font
        self.FPS = FPS
        self.lives = lives
        self.window = window
        self.WIDTH = screen_width
        # FIX: usar HEIGHT (los .md originales escriben HEIGTH con typo).
        self.HEIGHT = screen_height
        self.bullets = bullets
        self.clock = clock or pygame.time.Clock()
        self.level = 1
        self.count = 0

        # Cargamos los assets en __init__ (no a nivel de módulo) para que
        # pygame.init() y set_mode ya hayan corrido cuando esto se ejecute.
        self.bullet_image = pygame.image.load('img/bullet_image.png').convert_alpha()

    # FIX: receive events list to avoid double event.get() race
    def escape(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return True
        return False

    def over(self):
        if self.lives <= 0:
            label = self.font.render('GAME OVER', True, (255, 255, 255))
            self.window.blit(
                label,
                (self.WIDTH / 2 - label.get_width() / 2,
                 self.HEIGHT / 2 - label.get_height() / 2),
            )
            pygame.display.update()
            self.count += 1
            # FIX: usar >= en vez de == para no perder el frame exacto.
            if self.count >= self.FPS * 3:
                return True
            return False
        return False

    def reload_bullet(self, bullet):
        self.bullets = bullet

    def draw_HUD(self):
        lives_label = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        level_label = self.font.render(f'Level: {self.level}', True, (255, 255, 255))
        self.window.blit(lives_label, (10, 10))
        self.window.blit(
            level_label,
            (self.WIDTH - level_label.get_width() - 10, 10),
        )

        bw = self.bullet_image.get_width()
        bh = self.bullet_image.get_height()
        for i in range(self.bullets):
            self.window.blit(
                self.bullet_image,
                (self.WIDTH - (i + 1) * (bw + 4) - 6,
                 self.HEIGHT - bh - 10),
            )
