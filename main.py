import random
import sys

import pygame

from DrawingClass import Drawing
from EnemyClass import Enemy
from GameClass import Game
from MenuAcercaDeClass import MenuAcercaDe
from MenuInstruccionesClass import MenuInstrucciones
from MenuPrincipalClass import MenuPrincipal
from MenuPuntajesClass import MenuPuntajes
from PantallaNombreClass import PantallaNombre
from PlayerClass import Player

WIDTH, HEIGHT = 800, 600
FPS = 60
ENEMY_INITIAL_SPEED = 2
ENEMY_COUNT = 5

# Globales seteados por setup_pygame() y consumidos por las funciones de
# flujo (iniciar_juego, iniciar_puntajes, ...). Es la forma más simple de
# mantener una sola ventana viva durante toda la sesión.
window = None
explosion_sound = None
win_sound = None


def start_music():
    """Inicia la música de fondo en loop. Si falla, loguea y sigue."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/background_song.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f'[warn] no se pudo iniciar la música: {e}')


def load_sfx(path, volume=0.6):
    """Carga un Sound. Devuelve None si falla, así el caller filtra con `if`."""
    try:
        s = pygame.mixer.Sound(path)
        s.set_volume(volume)
        return s
    except (pygame.error, FileNotFoundError) as e:
        print(f'[warn] no se pudo cargar {path}: {e}')
        return None


def setup_pygame():
    """Inicialización única (Fase 11): pygame, ventana, ícono, caption,
    música y SFX. Se llama UNA sola vez desde el entry point. El resto
    del flujo (juego y menús) reusa los globales que setea esta función.
    """
    global window, explosion_sound, win_sound
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    icon = pygame.image.load('img/title_icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Space Invader')

    start_music()
    explosion_sound = load_sfx('sounds/explosion.wav', volume=0.5)
    win_sound = load_sfx('sounds/ganar.mp3', volume=0.7)


def spawn_wave(level):
    """Genera una nueva oleada para el nivel dado. Escalado leve a propósito.
    Nivel 1 arranca a speed puro (2.0); los siguientes escalan ×1.1 por nivel.
    """
    speed = ENEMY_INITIAL_SPEED * (1.1 ** (level - 1))
    count = ENEMY_COUNT + level - 1
    return Enemy(speed).create(count, WIDTH)


def _build_pause_overlay():
    """Surface SRCALPHA con velo negro semi-transparente + textos de pausa.
    Se construye una sola vez por entrada al sub-loop (no por frame)."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    font_title = pygame.font.SysFont('comicsans', 80)
    font_hint = pygame.font.SysFont('comicsans', 28)
    font_esc = pygame.font.SysFont('comicsans', 24)

    title = font_title.render('PAUSA', True, (255, 255, 255))
    overlay.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50),
    )
    hint = font_hint.render('Presiona P para continuar', True, (200, 200, 200))
    overlay.blit(
        hint,
        (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 30),
    )
    esc = font_esc.render('ESC vuelve al menú principal', True, (180, 180, 180))
    overlay.blit(
        esc,
        (WIDTH // 2 - esc.get_width() // 2, HEIGHT // 2 + 70),
    )
    return overlay


def _pause_loop(drawing, game, player, enemies, puntaje, overlay):
    """Sub-loop bloqueante de pausa. Devuelve:
       'resume' → seguir jugando (P presionado)
       'menu'   → salir al menú principal (ESC presionado)
    Maneja QUIT también (cierra app)."""
    pygame.mixer.music.pause()
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)  # 30 FPS basta estando pausado.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.music.unpause()
                    return 'resume'
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.unpause()
                    return 'menu'

        # Re-renderiza el último frame congelado y le superpone el overlay.
        drawing.drawing(game, player, enemies, FPS, puntaje)
        window.blit(overlay, (0, 0))
        pygame.display.update()


def iniciar_juego():
    """Game loop. Retorna naturalmente al terminar (game over o ESC), para
    que mostrar_menu_principal() siga su loop al recibir el control.

    FIX (Fase 11): ESC ya NO cierra la app — solo termina el game loop y
    vuelve al menú. QUIT (cerrar la ventana) sigue cerrando la app entera.
    Antes Game.escape(events) mezclaba ambos en un bool; ahora chequeamos
    los eventos a mano para diferenciarlos.
    """
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
    puntaje = 0

    # Overlay de pausa pre-construido (SRCALPHA + textos). Una sola vez.
    pause_overlay = _build_pause_overlay()

    running = True
    while running:
        game.clock.tick(FPS)

        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                running = False
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_p:
                # Sub-loop bloqueante. Devuelve 'resume' o 'menu'.
                resultado = _pause_loop(
                    drawing, game, player, enemies, puntaje, pause_overlay)
                if resultado == 'menu':
                    running = False
        if not running:
            break

        # c-e) lógica del jugador
        player.create_bullets()
        game.reload_bullet(len(player.bullets))
        player.cooldown()
        player.move(WIDTH, HEIGHT)

        # f) enemigos
        for enemy in enemies:
            enemy.move()
            if enemy.y > HEIGHT:
                enemy.y = random.randrange(-1000, -100)

        # g) colisiones
        for i in range(len(enemies) - 1, -1, -1):
            enemy = enemies[i]
            if player.hit(enemy):
                enemies.pop(i)
                puntaje += 1
                if explosion_sound:
                    explosion_sound.play()
                continue
            offset = (int(enemy.x - player.x), int(enemy.y - player.y))
            if player.mask.overlap(enemy.mask, offset):
                game.lives -= 1
                enemies.pop(i)

        # h) game over
        if game.over():
            if puntaje > game.max_pun:
                if win_sound:
                    win_sound.play()
                print(f'[NEW RECORD] {puntaje} > {game.max_pun}')
                pygame.mixer.music.pause()
                # finish_mtd como no-op: tras Aceptar, PantallaNombre retorna
                # naturalmente y caemos al show_game_over_screen() de abajo.
                # Después, este iniciar_juego() retorna y MenuPrincipal sigue
                # vivo en su propio loop (unwinding limpio, sin recursión).
                PantallaNombre(window, puntaje, finish_mtd=lambda: None).ejecutar()
                pygame.mixer.music.unpause()
            drawing.drawing(game, player, enemies, FPS, puntaje)
            game.show_game_over_screen()
            return

        # i) fin de oleada
        if not enemies:
            game.level += 1
            player.increase_speed()
            # BALANCE: caps 10 balas / 6 vidas.
            if game.level % 3 == 0:
                if player.max_amount_bullets < 10:
                    player.max_amount_bullets += 1
                if game.lives < 6:
                    game.lives += 1
            enemies = spawn_wave(game.level)

        # j) render
        drawing.drawing(game, player, enemies, FPS, puntaje)

    # Salida vía ESC: retorno limpio al caller (mostrar_menu_principal).


def iniciar_instrucciones():
    """Abre MenuInstrucciones desde el menú principal. back_mtd no-op:
    el unwinding natural devuelve el control al loop de MenuPrincipal."""
    MenuInstrucciones(window, back_mtd=lambda: None).ejecutar()


def iniciar_puntajes():
    """Abre MenuPuntajes desde el menú principal. back_mtd no-op: el
    unwinding natural devuelve el control al loop de MenuPrincipal."""
    MenuPuntajes(window, back_mtd=lambda: None).ejecutar()


def iniciar_acerca_de():
    """Abre MenuAcercaDe desde el menú principal. back_mtd no-op: el
    unwinding natural devuelve el control al loop de MenuPrincipal."""
    MenuAcercaDe(window, back_mtd=lambda: None).ejecutar()


def mostrar_menu_principal():
    """Punto de entrada al flujo: crea MenuPrincipal y entra a su loop.

    Las referencias circulares (este menú apunta a iniciar_juego/_puntajes/
    _acerca_de y esos a su vez apuntan acá vía back_mtd) se resuelven solas
    porque Python evalúa los nombres en runtime, no al definirlos.
    """
    MenuPrincipal(
        window,
        init_game_mtd=iniciar_juego,
        init_instructions_mtd=iniciar_instrucciones,
        init_score_mtd=iniciar_puntajes,
        init_about_mtd=iniciar_acerca_de,
    ).mostrar()


if __name__ == '__main__':
    setup_pygame()
    mostrar_menu_principal()
