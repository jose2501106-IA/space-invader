import sys
import webbrowser

import pygame


class MenuAcercaDe:
    """Pantalla 'Acerca De': descripción del juego + link a Hybridge.

    Reusa la ventana existente. Loop propio en `ejecutar()` con un único
    `pygame.event.get()` por frame.
    """

    MENU_FONDO = None

    HYBRIDGE_URL = 'https://hybridge.education'

    DESCRIPCION = (
        '¡Explora la galaxia y aprende Programación Orientada a Objetos! '
        'Cada nave, cada disparo, todo es un objeto interactivo. '
        'Únete a esta experiencia divertida y educativa en este cruce '
        'de juego y aprendizaje. ¡Prepárate para salvar el universo!'
    )

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

        if MenuAcercaDe.MENU_FONDO is None:
            MenuAcercaDe.load_assets()

        if MenuAcercaDe.MENU_FONDO is not None:
            self._bg_scaled = pygame.transform.scale(
                MenuAcercaDe.MENU_FONDO,
                (self.window.get_width(), self.window.get_height()),
            )
        else:
            self._bg_scaled = None

        # Fuentes (creadas acá, no por frame).
        self.font_titulo = pygame.font.SysFont('comicsans', 48)
        self.font_subtitulo = pygame.font.SysFont('comicsans', 36)
        self.font_contenido = pygame.font.SysFont('comicsans', 28)
        self.font_enlace = pygame.font.SysFont('comicsans', 28)
        self.font_boton = pygame.font.SysFont('comicsans', 36)

        # Botón "<" arriba-izquierda.
        self.back_rect = pygame.Rect(20, 20, 50, 50)

        # Pre-wrap de la descripción para no recalcular por frame.
        self._lineas_descripcion = self._wrap_text(
            MenuAcercaDe.DESCRIPCION,
            self.window.get_width() - 100,
        )

        # rect del enlace: lo seteamos al primer _draw() (depende del
        # tamaño renderizado del label). Lo dejamos como Rect vacío para
        # que el chequeo de clic en el primer frame no falle.
        self.enlace_rect = pygame.Rect(0, 0, 0, 0)

    def _wrap_text(self, texto, max_width):
        """Devuelve una lista de líneas, cada una <= max_width píxeles.

        Splitea por palabras (split()). Si una palabra individual es más
        larga que max_width, la deja en su propia línea sin trocearla
        (no hacemos hyphenation).
        """
        palabras = texto.split()
        if not palabras:
            return []

        lineas = []
        actual = palabras[0]
        for palabra in palabras[1:]:
            tentativa = f'{actual} {palabra}'
            if self.font_contenido.size(tentativa)[0] <= max_width:
                actual = tentativa
            else:
                lineas.append(actual)
                actual = palabra
        lineas.append(actual)
        return lineas

    def _draw(self):
        # Fondo
        if self._bg_scaled is not None:
            self.window.blit(self._bg_scaled, (0, 0))
        else:
            self.window.fill((0, 0, 0))

        w = self.window.get_width()

        # Título
        titulo = self.font_titulo.render('Acerca De', True, (255, 255, 255))
        self.window.blit(titulo, (w // 2 - titulo.get_width() // 2, 50))

        # Subtítulo
        subtit = self.font_subtitulo.render(
            'Space Invader Hybridge', True, (255, 255, 255))
        self.window.blit(subtit, (w // 2 - subtit.get_width() // 2, 120))

        # Contenido wrappeado, espaciado vertical = altura de la fuente
        y = 200
        line_height = self.font_contenido.get_height()
        for linea in self._lineas_descripcion:
            label = self.font_contenido.render(linea, True, (255, 255, 255))
            self.window.blit(label, (w // 2 - label.get_width() // 2, y))
            y += line_height

        # Enlace clickeable (rojo, como el playground original).
        enlace_lbl = self.font_enlace.render(
            '¡Haz clic aquí para visitar Hybridge!', True, (255, 0, 0))
        enlace_pos = (w // 2 - enlace_lbl.get_width() // 2, 510)
        self.window.blit(enlace_lbl, enlace_pos)
        # Actualizamos el rect cada frame (cheap) por si la fuente difiere
        # entre sistemas. Así garantizamos collidepoint correcto siempre.
        self.enlace_rect = pygame.Rect(
            enlace_pos[0], enlace_pos[1],
            enlace_lbl.get_width(), enlace_lbl.get_height(),
        )

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
                    # Enlace: abre el navegador y SE QUEDA en la pantalla.
                    if self.enlace_rect.collidepoint(event.pos):
                        try:
                            webbrowser.open(MenuAcercaDe.HYBRIDGE_URL)
                        except Exception as e:
                            print(f'[warn] no se pudo abrir navegador: {e}')

            self._draw()
