import os
import sys

import pygame


class PantallaNombre:
    """Pantalla de input de nombre cuando el jugador supera el récord.

    Reusa la ventana pygame existente (no abre otra). Tiene su propio loop
    en `ejecutar()` con un único `pygame.event.get()` por frame (convención
    para clases de menú — ver CLAUDE.md).
    """

    MENU_FONDO = None

    @classmethod
    def load_assets(cls):
        if cls.MENU_FONDO is not None:
            return
        # convert() — el fondo es opaco. Si menu_fondo.jpg falla, caemos al
        # background del juego para no romper la UX.
        try:
            cls.MENU_FONDO = pygame.image.load('img/menu_fondo.jpg').convert()
        except (pygame.error, FileNotFoundError) as e:
            print(f'[warn] no se pudo cargar img/menu_fondo.jpg: {e}')
            try:
                cls.MENU_FONDO = pygame.image.load('img/background.png').convert()
            except (pygame.error, FileNotFoundError) as e2:
                print(f'[warn] tampoco se pudo cargar fallback img/background.png: {e2}')
                cls.MENU_FONDO = None

    def __init__(self, window, puntaje, finish_mtd):
        self.window = window
        self.puntaje = puntaje
        self.finish_mtd = finish_mtd
        self.texto_input = ''
        # Autofocus: el usuario abrió esta pantalla con la intención clara
        # de escribir, no le hacemos clickear el input primero.
        self.input_active = True

        # Auto-load defensivo.
        if PantallaNombre.MENU_FONDO is None:
            PantallaNombre.load_assets()

        # Fondo escalado una sola vez (cacheado a tamaño de ventana).
        if PantallaNombre.MENU_FONDO is not None:
            self._bg_scaled = pygame.transform.scale(
                PantallaNombre.MENU_FONDO,
                (self.window.get_width(), self.window.get_height()),
            )
        else:
            self._bg_scaled = None

        # Fuentes (creadas acá, no a nivel de módulo).
        self.font_titulo = pygame.font.SysFont('comicsans', 28)
        self.font_subtitulo = pygame.font.SysFont('comicsans', 36)
        self.font_puntaje = pygame.font.SysFont('comicsans', 40)
        self.font_input = pygame.font.SysFont('comicsans', 30)
        self.font_boton = pygame.font.SysFont('comicsans', 30)
        self.font_error = pygame.font.SysFont('comicsans', 24)

        # Geometría.
        self.input_rect = pygame.Rect(200, 250, 400, 50)
        self.button_rect = pygame.Rect(300, 350, 200, 50)

        # Estado del overlay de error (mensaje + ms hasta cuándo mostrarlo).
        self.error_msg = ''
        self.error_until_ms = 0

        # Cap de longitud del nombre.
        self.MAX_LEN = 20

    @staticmethod
    def escribir_en_archivo(nombre_archivo, contenido):
        """Append-only. Crea el archivo si no existe.

        FIX: el flujo original chequeaba existencia + abría con 'w' o 'a'.
        Modo 'a' ya cubre ambos casos (crea si no existe, agrega si sí).

        FIX (hardening): el puntajes.txt del playground viene SIN newline
        final, y un usuario puede editarlo a mano y olvidar el '\\n'. Si
        appendeamos crudo, fusionamos la última línea con la nueva
        (ej: 'Andrés, 55' + 'pepe,58\\n' → 'Andrés, 55pepe,58\\n').
        Antes del append, si el archivo no termina en '\\n', lo prependemos.
        """
        try:
            needs_newline = False
            if os.path.exists(nombre_archivo):
                with open(nombre_archivo, 'rb') as f:
                    try:
                        f.seek(-1, os.SEEK_END)
                        last_byte = f.read(1)
                        needs_newline = last_byte != b'\n'
                    except OSError:
                        # Archivo vacío: seek(-1) falla.
                        needs_newline = False

            with open(nombre_archivo, 'a', encoding='utf-8') as f:
                if needs_newline:
                    f.write('\n')
                f.write(contenido + '\n')
        except PermissionError as e:
            print(f'[warn] sin permiso para escribir {nombre_archivo}: {e}')
        except Exception as e:
            print(f'[warn] error escribiendo {nombre_archivo}: {e}')

    def _try_save(self):
        """Devuelve True si guardó. Si no, deja un error visible 2s."""
        nombre = self.texto_input.strip()
        if not nombre:
            self.error_msg = 'Ingresa al menos 1 carácter'
            self.error_until_ms = pygame.time.get_ticks() + 2000
            return False
        # Cap de longitud + sanitizar comas: el parser usa rsplit(',', 1)
        # así que UNA coma no rompe, pero un nombre con comas confunde a
        # cualquier lector ingenuo. Las cambiamos por espacio.
        nombre = nombre[: self.MAX_LEN].replace(',', ' ')
        PantallaNombre.escribir_en_archivo(
            'puntajes.txt', f'{nombre},{self.puntaje}')
        return True

    def _draw(self):
        # Fondo
        if self._bg_scaled is not None:
            self.window.blit(self._bg_scaled, (0, 0))
        else:
            self.window.fill((0, 0, 0))

        w = self.window.get_width()

        # Título
        titulo = self.font_titulo.render(
            '¡Felicidades! Superaste el récord. Ingresa tu nombre',
            True, (255, 255, 255))
        self.window.blit(titulo, (w // 2 - titulo.get_width() // 2, 50))

        # Subtítulo
        subtit = self.font_subtitulo.render('Space Invader', True, (255, 255, 255))
        self.window.blit(subtit, (w // 2 - subtit.get_width() // 2, 100))

        # Puntaje grande arriba del input
        score_lbl = self.font_puntaje.render(
            f'Puntaje: {self.puntaje}', True, (255, 220, 0))
        self.window.blit(score_lbl, (w // 2 - score_lbl.get_width() // 2, 180))

        # Caja de input
        border_color = (255, 255, 255) if self.input_active else (128, 128, 128)
        pygame.draw.rect(self.window, (30, 30, 30), self.input_rect)
        pygame.draw.rect(self.window, border_color, self.input_rect, 2)
        text_surf = self.font_input.render(self.texto_input, True, (255, 255, 255))
        self.window.blit(
            text_surf, (self.input_rect.x + 10, self.input_rect.y + 10))

        # Botón Aceptar
        pygame.draw.rect(self.window, (200, 200, 200), self.button_rect)
        pygame.draw.rect(self.window, (255, 255, 255), self.button_rect, 2)
        btn_lbl = self.font_boton.render('Aceptar', True, (0, 0, 0))
        self.window.blit(
            btn_lbl,
            (
                self.button_rect.centerx - btn_lbl.get_width() // 2,
                self.button_rect.centery - btn_lbl.get_height() // 2,
            ),
        )

        # Overlay de error (si activo)
        if self.error_msg and pygame.time.get_ticks() < self.error_until_ms:
            err_lbl = self.font_error.render(self.error_msg, True, (255, 50, 50))
            self.window.blit(
                err_lbl,
                (
                    w // 2 - err_lbl.get_width() // 2,
                    self.input_rect.bottom + 10,
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
                        # Cancelar y volver al flujo que invocó esta pantalla.
                        self.finish_mtd()
                        return
                    if self.input_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.texto_input = self.texto_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            # Atajo de submit: equivalente a clic en Aceptar.
                            if self._try_save():
                                self.finish_mtd()
                                return
                        else:
                            ch = event.unicode
                            if (ch and ch.isprintable()
                                    and len(self.texto_input) < self.MAX_LEN):
                                self.texto_input += ch

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    if self.input_rect.collidepoint(pos):
                        self.input_active = True
                    elif self.button_rect.collidepoint(pos):
                        if self._try_save():
                            self.finish_mtd()
                            return
                    else:
                        self.input_active = False

            self._draw()
