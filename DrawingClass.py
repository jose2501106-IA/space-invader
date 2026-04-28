import pygame


class Drawing:
    BACKGROUND = None

    @classmethod
    def load_assets(cls):
        if cls.BACKGROUND is not None:
            return
        # convert() (sin alpha) — el fondo es opaco y rinde más rápido así.
        cls.BACKGROUND = pygame.image.load('img/background.png').convert()

    def __init__(self, window):
        self.window = window
        # Auto-load defensivo: idealmente main.py llamó load_assets() tras
        # set_mode, pero si no, lo hacemos ahora.
        if Drawing.BACKGROUND is None:
            Drawing.load_assets()

    def drawing(self, game, player, enemies, FPS):
        # a) fondo
        self.window.blit(Drawing.BACKGROUND, (0, 0))

        # b) enemigos — copia con [:] para evitar mutación durante el iter
        for enemy in enemies[:]:
            enemy.draw(self.window)

        # c) jugador
        player.draw(self.window)

        # d) balas en vuelo (también las mueve internamente)
        player.fire(self.window)

        # e) HUD por encima de todo
        game.draw_HUD()

        # f) flip
        pygame.display.update()
