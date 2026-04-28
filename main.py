import random
import sys

import pygame

from GameClass import Game
from EnemyClass import Enemy
from PlayerClass import Player
from DrawingClass import Drawing


WIDTH, HEIGHT = 800, 600
FPS = 60
ENEMY_INITIAL_SPEED = 2
ENEMY_COUNT = 5


def start_music():
    """Inicia la música de fondo en loop. Si falla, loguea y sigue."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f'[warn] no se pudo iniciar la música: {e}')


def spawn_wave(level):
    """Genera una nueva oleada para el nivel dado. Escalado leve a propósito.
    Nivel 1 arranca a speed puro (2.0); los siguientes escalan ×1.1 por nivel.
    """
    speed = ENEMY_INITIAL_SPEED * (1.1 ** (level - 1))
    count = ENEMY_COUNT + level - 1
    return Enemy(speed).create(count, WIDTH)


def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    icon = pygame.image.load('img/title_icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Space Invader')

    start_music()

    font = pygame.font.SysFont('comicsans', 30)

    Enemy.load_assets()
    Player.load_assets()
    Drawing.load_assets()

    game = Game(font, FPS, lives=5, window=window,
                screen_width=WIDTH, screen_height=HEIGHT, bullets=3)

    player = Player(
        x=WIDTH / 2 - Player.PLAYER_IMAGE.get_width() / 2,
        y=HEIGHT - 100,
        x_speed=5,
        y_speed=5,
    )

    enemies = spawn_wave(game.level)

    drawing = Drawing(window)

    running = True
    while running:
        # a) tick
        game.clock.tick(FPS)

        # b) eventos (un solo event.get() por frame)
        events = pygame.event.get()
        if game.escape(events):
            running = False
            break

        # c-e) lógica del jugador
        player.create_bullets()
        player.cooldown()
        player.move(WIDTH, HEIGHT)

        # f) enemigos: mover y respawnear si salen por abajo
        for enemy in enemies:
            enemy.move()
            if enemy.y > HEIGHT:
                enemy.y = random.randrange(-1000, -100)

        # g) colisiones — recorremos inverso para poder remover sin romper
        #    iteración. Combinamos bala→enemy y enemy→player en un solo paso.
        for i in range(len(enemies) - 1, -1, -1):
            enemy = enemies[i]
            # Bala → enemigo: hit() ya remueve la bala internamente.
            if player.hit(enemy):
                enemies.pop(i)
                continue
            # Enemigo → jugador: pixel-perfect con offset relativo.
            offset = (int(enemy.x - player.x), int(enemy.y - player.y))
            if player.mask.overlap(enemy.mask, offset):
                game.lives -= 1
                enemies.pop(i)

        # h) game over (chequeo no bloqueante)
        if game.over():
            # un último frame con el estado actual y luego la pantalla GO
            drawing.drawing(game, player, enemies, FPS)
            game.show_game_over_screen()
            break

        # i) fin de oleada → subir nivel y regenerar
        if not enemies:
            game.level += 1
            player.increase_speed()
            enemies = spawn_wave(game.level)

        # j) render encapsulado (fondo, enemigos, player, balas, HUD, flip)
        drawing.drawing(game, player, enemies, FPS)

    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
