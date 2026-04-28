import sys

import pygame


class MenuInstrucciones:
    """Pantalla de instrucciones: lista los controles del juego en dos
    columnas (tecla → descripción) + breve explicación del gameplay.

    Reusa la ventana existente. Loop propio en `ejecutar()` con un único
    `pygame.event.get()` por frame.
    """

    MENU_FONDO = None

    # Lista de pares (tecla, descripción). Orden = orden de render.
    CONTROLES = [
        ('WASD / Flechas', 'Mover la nave'),
        ('SPACE', 'Disparar (máx 3 balas en vuelo)'),
        ('P', 'Pausar / reanudar el juego'),
        ('ESC (en juego)', 'Volver al menú principal'),
        ('ESC (en menú)', 'Cerrar la aplicación'),
        ('X de la ventana', 'Cerrar la aplicación'),
    ]

    COMO_JUGAR = [
        'Destruí enemigos disparándoles para subir tu puntaje.',
        'Cada 3 niveles ganás +1 vida y +1 bala máxima.',
        'Si superás el récord, podrás guardar tu nombre.',
    ]

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

        if MenuInstrucciones.MENU_FONDO is None:
            MenuInstrucciones.load_assets()

        if MenuInstrucciones.MENU_FONDO is not None:
            self._bg_scaled = pygame.transform.scale(
                MenuInstrucciones.MENU_FONDO,
                (self.window.get_width(), self.window.get_height()),
            )
        else:
            self._bg_scaled = None

        # Fuentes
        self.font_titulo = pygame.font.SysFont('comicsans', 48)
        self.font_subtitulo = pygame.font.SysFont('comicsans', 36)
        # Bold para la columna de teclas (más fácil de escanear). Tamaños
        # achicados respecto del primer intento para que la columna izquierda
        # no se solape con la derecha en filas largas como "ESC (en juego)".
        self.font_label = pygame.font.SysFont('comicsans', 24, bold=True)
        self.font_desc = pygame.font.SysFont('comicsans', 22)
        self.font_boton = pygame.font.SysFont('comicsans', 36)
        self.font_como = pygame.font.SysFont('comicsans', 22)

        # Botón "<" arriba-izquierda.
        self.back_rect = pygame.Rect(20, 20, 50, 50)

    def _draw(self):
        # Fondo
        if self._bg_scaled is not None:
            self.window.blit(self._bg_scaled, (0, 0))
        else:
            self.window.fill((0, 0, 0))

        w = self.window.get_width()

        # Título
        titulo = self.font_titulo.render('Instrucciones', True, (255, 255, 255))
        self.window.blit(titulo, (w // 2 - titulo.get_width() // 2, 40))

        # Subtítulo
        subtit = self.font_subtitulo.render('Space Invader', True, (255, 255, 255))
        self.window.blit(subtit, (w // 2 - subtit.get_width() // 2, 95))

        # Lista de controles en 2 columnas. Columna izquierda x=80 (teclas
        # en bold 24, máx ~280px), derecha x=380 (descripciones en 22, máx
        # ~710px). Gap de ~100px entre columnas garantiza no overlap.
        y = 160
        for tecla, desc in MenuInstrucciones.CONTROLES:
            tecla_lbl = self.font_label.render(tecla, True, (255, 255, 255))
            desc_lbl = self.font_desc.render(desc, True, (220, 220, 220))
            self.window.blit(tecla_lbl, (80, y))
            self.window.blit(desc_lbl, (380, y))
            y += 45

        # Sección "Cómo jugar" desde y=480, líneas centradas.
        y = 480
        for linea in MenuInstrucciones.COMO_JUGAR:
            label = self.font_como.render(linea, True, (180, 180, 180))
            self.window.blit(label, (w // 2 - label.get_width() // 2, y))
            y += 28

        # Botón "<"
        pygame.draw.rect(self.window, (200, 200, 200), self.back_rect)
        pygame.draw.rect(self.window, (255, 255, 255), self.back_rect, 2)
        back_lbl = self.font_boton.render('<', True, (0, 0, 0))
        self.window.blit(
            back_lbl,
            (
                self.back_rect.centerx - back_lbl.get_width() // 2,
                self.back_rect.centery - back_lbl.get_height() // 2,
            ),
        )

        pygame.display.update()

    def ejecutar(self):
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

            self._draw()
