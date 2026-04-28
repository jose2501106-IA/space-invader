import random

import pygame

from ShipClass import Ship


class Enemy(Ship):
    # Se llena con load_assets() la primera vez (después de pygame.init()
    # + set_mode), no a nivel de módulo.
    COLOR = None

    @classmethod
    def load_assets(cls):
        if cls.COLOR is not None:
            return
        cls.COLOR = {
            'blue': (
                pygame.image.load('img/enemy_blue_image.png').convert_alpha(),
                pygame.image.load('img/shot_blue.png').convert_alpha(),
            ),
            'green': (
                pygame.image.load('img/enemy_green_image.png').convert_alpha(),
                pygame.image.load('img/shot_green.png').convert_alpha(),
            ),
            'purple': (
                pygame.image.load('img/enemy_purple_image.png').convert_alpha(),
                pygame.image.load('img/shot_purple.png').convert_alpha(),
            ),
        }

    # FIX: parámetro 'speed' (los .md tienen el typo 'spped').
    def __init__(self, speed, x=50, y=50, color='blue', health=100):
        super().__init__(x, y, health)
        # Auto-load defensivo: si nadie llamó load_assets() todavía, lo hacemos
        # ahora. Idealmente main.py lo llama explícitamente tras set_mode.
        if Enemy.COLOR is None:
            Enemy.load_assets()
        self.ship_img, self.bullet_img = Enemy.COLOR[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.speed = speed
        self.color = color

    def move(self):
        self.y += self.speed

    # FIX: screen_width como parámetro en vez de leer un global WIDTH.
    def create(self, amount, screen_width):
        enemies = []
        colors = list(Enemy.COLOR.keys())
        for _ in range(amount):
            color = random.choice(colors)
            sprite_w = Enemy.COLOR[color][0].get_width()
            x = random.randrange(20, screen_width - sprite_w - 20)
            y = random.randrange(-1000, -100)
            enemies.append(Enemy(self.speed, x=x, y=y, color=color))
        return enemies

    def increase_speed(self):
        self.speed *= 1.02
