import random
import sys

import pygame

from GameClass import Game
from EnemyClass import Enemy
from PlayerClass import Player


WIDTH, HEIGHT = 800, 600
FPS = 60
ENEMY_INITIAL_SPEED = 2
ENEMY_COUNT = 5


def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    icon = pygame.image.load('img/title_icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Space Invader')

    font = pygame.font.SysFont('comicsans', 30)

    Enemy.load_assets()
    Player.load_assets()

    game = Game(font, FPS, lives=5, window=window,
                screen_width=WIDTH, screen_height=HEIGHT, bullets=3)

    player = Player(
        x=WIDTH / 2 - Player.PLAYER_IMAGE.get_width() / 2,
        y=HEIGHT - 100,
        x_speed=5,
        y_speed=5,
    )

    enemies = Enemy(ENEMY_INITIAL_SPEED).create(ENEMY_COUNT, WIDTH)

    running = True
    while running:
        # a) tick
        game.clock.tick(FPS)

        # b) eventos (un solo event.get() por frame)
        events = pygame.event.get()
        if game.escape(events):
            running = False
            break

        # c) limpiar fondo
        window.fill((0, 0, 0))

        # d-f) lógica del jugador
        player.create_bullets()
        player.cooldown()
        player.move(WIDTH, HEIGHT)

        # g) enemigos: mover, respawn, dibujar
        for enemy in enemies:
            enemy.move()
            if enemy.y > HEIGHT:
                enemy.y = random.randrange(-1000, -100)
            enemy.draw(window)

        # h) dibujar player
        player.draw(window)

        # i) disparar (también mueve y dibuja las balas en vuelo)
        player.fire(window)

        # j) HUD encima de todo
        game.draw_HUD()

        # k) flip
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
