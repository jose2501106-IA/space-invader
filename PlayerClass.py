import pygame

from BulletClass import Bullet
from ShipClass import Ship


class Player(Ship):
    PLAYER_IMAGE = None
    BULLET_IMAGE = None

    @classmethod
    def load_assets(cls):
        if cls.PLAYER_IMAGE is not None:
            return
        cls.PLAYER_IMAGE = pygame.image.load('img/player_image.png').convert_alpha()
        cls.BULLET_IMAGE = pygame.image.load('img/bullet_image.png').convert_alpha()

    def __init__(self, x, y, x_speed, y_speed, health=100):
        super().__init__(x, y, health)
        # Auto-load defensivo: idealmente main.py llamó load_assets() tras
        # set_mode, pero si no, lo hacemos ahora.
        if Player.PLAYER_IMAGE is None:
            Player.load_assets()

        self.x_speed = x_speed
        self.y_speed = y_speed
        self.ship_img = Player.PLAYER_IMAGE
        self.bullet_img = Player.BULLET_IMAGE
        self.bullet_speed = -10
        self.max_health = health
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.creation_cooldown_counter = 0
        self.max_amount_bullets = 3
        # Reinicio explícito (aunque Ship.__init__ ya los pone como instancia).
        self.bullets = []
        self.bullet_cooldown_counter = 0

    # FIX: paréntesis mal cerrados en los .md originales y uso de WIDTH/HEIGHT
    # globales — aquí los recibimos como parámetros.
    def move(self, screen_width, screen_height):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 0:
            self.y -= self.y_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and \
                self.y < screen_height - self.get_height() - 60:
            self.y += self.y_speed
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 0:
            self.x -= self.x_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and \
                self.x < screen_width - self.get_width():
            self.x += self.x_speed

    def increase_speed(self):
        if self.x_speed < 10:
            self.x_speed += 1.25
            self.y_speed += 1.25
        else:
            self.x_speed = 10
            self.y_speed = 8
        if self.cool_down > 25:
            self.cool_down *= 0.9

    def create_bullets(self):
        if len(self.bullets) < self.max_amount_bullets and \
                self.creation_cooldown_counter == 0:
            self.bullets.append(Bullet(self.x, self.y, self.bullet_img))
            self.creation_cooldown_counter = 1
        # Limpia las balas ya disparadas que salieron por arriba.
        self.fired_bullets = [b for b in self.fired_bullets if b.y > -40]

    def cooldown(self):
        if self.bullet_cooldown_counter >= 20:
            self.bullet_cooldown_counter = 0
        elif self.bullet_cooldown_counter > 0:
            self.bullet_cooldown_counter += 1

        if self.creation_cooldown_counter >= self.cool_down:
            self.creation_cooldown_counter = 0
        elif self.creation_cooldown_counter > 0:
            self.creation_cooldown_counter += 1

    def fire(self, window):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and len(self.bullets) > 0 and \
                self.bullet_cooldown_counter == 0:
            bullet = self.bullets[-1]
            bullet.x = self.x + (self.get_width() - bullet.img.get_width()) / 2
            bullet.y = self.y + 10
            self.fired_bullets.append(bullet)
            self.bullets.pop()
            self.bullet_cooldown_counter = 1
            self.creation_cooldown_counter = 1

        for bullet in self.fired_bullets:
            bullet.move(self.bullet_speed)
            bullet.draw(window)

    # FIX: el original retorna en la primera iteración (sale del loop con la
    # primera bala que mira, hubiese o no colisión). Aquí recorremos todas
    # las balas, removemos solo la que efectivamente impacta y devolvemos True.
    def hit(self, enemy):
        for bullet in self.fired_bullets:
            if bullet.collision(enemy):
                self.fired_bullets.remove(bullet)
                self.creation_cooldown_counter = int(self.cool_down * 0.8)
                return True
        return False
