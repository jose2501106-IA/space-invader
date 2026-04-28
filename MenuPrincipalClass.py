import sys

import pygame


class MenuPrincipal:
    """Menú principal: entry point del juego post-Fase 11.

    3 opciones: Iniciar juego / Puntajes / Acerca de. Navegación con
    flechas ↑↓ + Enter. Loop propio en `mostrar()` con un único
    `pygame.event.get()` por frame (convención de menús).
    """

    MENU_FONDO = None
    HYBRIDGE_LOGO = None

    @classmethod
    def load_assets(cls):
        if cls.MENU_FONDO is None:
            try:
                cls.MENU_FONDO = pygame.image.load('img/menu_fondo.jpg').convert()
            except (pygame.error, FileNotFoundError) as e:
                print(f'[warn] no se pudo cargar img/menu_fondo.jpg: {e}')
                try:
                    cls.MENU_FONDO = pygame.image.load('img/background.png').convert()
                except (pygame.error, FileNotFoundError) as e2:
                    print(f'[warn] tampoco se pudo cargar fallback img/background.png: {e2}')
                    cls.MENU_FONDO = None
        if cls.HYBRIDGE_LOGO is None:
            try:
                # convert_alpha() porque el .gif puede tener transparencia.
                cls.HYBRIDGE_LOGO = pygame.image.load('img/hybridge.gif').convert_alpha()
            except (pygame.error, FileNotFoundError) as e:
                print(f'[warn] no se pudo cargar img/hybridge.gif: {e}')
                cls.HYBRIDGE_LOGO = None

    def __init__(self, window, init_game_mtd, init_score_mtd, init_about_mtd):
        self.window = window
        self.init_game_mtd = init_game_mtd
        self.init_score_mtd = init_score_mtd
        self.init_about_mtd = init_about_mtd

        if MenuPrincipal.MENU_FONDO is None or MenuPrincipal.HYBRIDGE_LOGO is None:
            MenuPrincipal.load_assets()

        # Pre-escalado de fondo y logo (cacheados, no se recalculan por frame).
        if MenuPrincipal.MENU_FONDO is not None:
            self._bg_scaled = pygame.transform.scale(
                MenuPrincipal.MENU_FONDO,
                (self.window.get_width(), self.window.get_height()),
            )
        else:
            self._bg_scaled = None

        if MenuPrincipal.HYBRIDGE_LOGO is not None:
            self._logo_scaled = pygame.transform.scale(
                MenuPrincipal.HYBRIDGE_LOGO, (80, 80))
        else:
            self._logo_scaled = None

        # Fuentes (creadas acá, no por frame).
        self.font_titulo = pygame.font.SysFont('comicsans', 64)
        self.font_subtitulo = pygame.font.SysFont('comicsans', 36)
        self.font_opciones = pygame.font.SysFont('comicsans', 32)

        self.opciones = ['Iniciar juego', 'Puntajes', 'Acerca de']
        self.opcion_seleccionada = 0

    def _draw(self):
        # Fondo
        if self._bg_scaled is not None:
            self.window.blit(self._bg_scaled, (0, 0))
        else:
            self.window.fill((0, 0, 0))

        w = self.window.get_width()

        # Layout en píxeles absolutos (no en función de h//4) para asegurar
        # que el logo no ocluya el título ni el subtítulo. Verificado:
        # título 64px (80→144), subtítulo 36px (150→186), logo 80px
        # (200→280), opciones desde y=340 con espaciado 70px.

        # Título
        titulo = self.font_titulo.render('Space Invader', True, (255, 255, 255))
        self.window.blit(titulo, (w // 2 - titulo.get_width() // 2, 80))

        # Subtítulo
        subtit = self.font_subtitulo.render('Hybridge', True, (255, 255, 255))
        self.window.blit(subtit, (w // 2 - subtit.get_width() // 2, 150))

        # Logo (80×80, centrado)
        if self._logo_scaled is not None:
            self.window.blit(
                self._logo_scaled,
                (w // 2 - self._logo_scaled.get_width() // 2, 200),
            )

        # Opciones — empiezan en y=340, espaciado de 70px entre ítems.
        y_base = 340
        item_height = 70
        for i, opcion in enumerate(self.opciones):
            label = self.font_opciones.render(opcion, True, (255, 255, 255))
            x = w // 2 - label.get_width() // 2
            y = y_base + i * item_height
            self.window.blit(label, (x, y))

            # Selector rojo (border-only) sobre la opción seleccionada.
            if i == self.opcion_seleccionada:
                rect = pygame.Rect(0, 0, 300, 50)
                rect.centerx = w // 2
                rect.centery = y + label.get_height() // 2
                pygame.draw.rect(self.window, (255, 0, 0), rect, 2)

        pygame.display.update()

    def mostrar(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # ESC en el menú principal cierra la app (convención).
                        # En el resto de pantallas, ESC = back al menú.
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_UP:
                        self.opcion_seleccionada = (self.opcion_seleccionada - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        self.opcion_seleccionada = (self.opcion_seleccionada + 1) % 3
                    elif event.key == pygame.K_RETURN:
                        # Después de la llamada NO hacemos return: el while
                        # sigue y volvemos a renderizar el menú al regresar.
                        if self.opcion_seleccionada == 0:
                            self.init_game_mtd()
                        elif self.opcion_seleccionada == 1:
                            self.init_score_mtd()
                        elif self.opcion_seleccionada == 2:
                            self.init_about_mtd()

            self._draw()
