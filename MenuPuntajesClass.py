import sys

import pygame

from GameClass import Game


class MenuPuntajes:
    """Pantalla de visualización del top 5 histórico.

    No abre ventana propia: recibe la existente. Loop propio en `ejecutar()`
    con un único `pygame.event.get()` por frame (convención de menús).
    """

    MENU_FONDO = None

    @classmethod
    def load_assets(cls):
        if cls.MENU_FONDO is not None:
            return
        try:
            cls.MENU_FONDO = pygame.image.load('img/menu_fondo.jpg').convert()
        except (pygame.error, FileNotFoundError) as e:
            print(f'[warn] no se pudo cargar img/menu_fondo.jpg: {e}')
            try:
                cls.MENU_FONDO = pygame.image.load('img/background.png').convert()
            except (pygame.error, FileNotFoundError) as e2:
                print(f'[warn] tampoco se pudo cargar fallback img/background.png: {e2}')
                cls.MENU_FONDO = None

    def __init__(self, window, back_mtd):
        self.window = window
        self.back_mtd = back_mtd

        # Auto-load defensivo.
        if MenuPuntajes.MENU_FONDO is None:
            MenuPuntajes.load_assets()

        # Fondo escalado una sola vez (cacheado).
        if MenuPuntajes.MENU_FONDO is not None:
            self._bg_scaled = pygame.transform.scale(
                MenuPuntajes.MENU_FONDO,
                (self.window.get_width(), self.window.get_height()),
            )
        else:
            self._bg_scaled = None

        # Fuentes.
        self.font_titulo = pygame.font.SysFont('comicsans', 48)
        self.font_subtitulo = pygame.font.SysFont('comicsans', 36)
        self.font_record = pygame.font.SysFont('comicsans', 42)
        self.font_item = pygame.font.SysFont('comicsans', 36)
        self.font_vacio = pygame.font.SysFont('comicsans', 36)
        self.font_back = pygame.font.SysFont('comicsans', 36)

        # Botón "<" arriba a la izquierda.
        self.back_rect = pygame.Rect(20, 20, 50, 50)

    @staticmethod
    def cargar_puntajes(archivo):
        """Wrapper sobre Game.leer_registros para mantener acoplamiento
        explícito (esta pantalla puede mañana querer un orden distinto o
        un cap distinto sin tocar Game)."""
        return Game.leer_registros(archivo)

    def _draw(self, puntajes):
        # Fondo
        if self._bg_scaled is not None:
            self.window.blit(self._bg_scaled, (0, 0))
        else:
            self.window.fill((0, 0, 0))

        w = self.window.get_width()
        h = self.window.get_height()

        # Título
        titulo = self.font_titulo.render(
            'Mejores Puntajes', True, (255, 255, 255))
        self.window.blit(titulo, (w // 2 - titulo.get_width() // 2, 50))

        # Subtítulo
        subtit = self.font_subtitulo.render('Space Invader', True, (255, 255, 255))
        self.window.blit(subtit, (w // 2 - subtit.get_width() // 2, 120))

        # Lista o estado vacío
        if not puntajes:
            vacio = self.font_vacio.render(
                'Aún no hay registros', True, (220, 60, 60))
            self.window.blit(
                vacio, (w // 2 - vacio.get_width() // 2, h // 2))
        else:
            y = 220
            for i, (nombre, score) in enumerate(puntajes):
                texto = f'{i + 1}. {nombre}: {score}'
                if i == 0:
                    label = self.font_record.render(texto, True, (255, 255, 255))
                else:
                    label = self.font_item.render(texto, True, (255, 80, 80))
                self.window.blit(
                    label, (w // 2 - label.get_width() // 2, y))
                y += 60

        # Botón "<"
        pygame.draw.rect(self.window, (200, 200, 200), self.back_rect)
        pygame.draw.rect(self.window, (255, 255, 255), self.back_rect, 2)
        back_lbl = self.font_back.render('<', True, (0, 0, 0))
        self.window.blit(
            back_lbl,
            (
                self.back_rect.centerx - back_lbl.get_width() // 2,
                self.back_rect.centery - back_lbl.get_height() // 2,
            ),
        )

        pygame.display.update()

    def ejecutar(self):
        # Carga fresca al abrir: si el jugador acaba de batir récord en otra
        # pantalla, queremos verlo reflejado.
        puntajes = self.cargar_puntajes('puntajes.txt')

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.back_mtd()
                        return

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_rect.collidepoint(event.pos):
                        self.back_mtd()
                        return

            self._draw(puntajes)
