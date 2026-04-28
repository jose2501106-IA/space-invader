import pygame


class Game:
    def __init__(self, font, FPS, lives, window, screen_width, screen_height,
                 bullets=0, clock=None):
        self.font = font
        self.FPS = FPS
        self.lives = lives
        self.window = window
        self.WIDTH = screen_width
        # FIX: usar HEIGHT (los .md originales escriben HEIGTH con typo).
        self.HEIGHT = screen_height
        self.bullets = bullets
        self.clock = clock or pygame.time.Clock()
        self.level = 1

        # Cargamos los assets en __init__ (no a nivel de módulo) para que
        # pygame.init() y set_mode ya hayan corrido cuando esto se ejecute.
        self.bullet_image = pygame.image.load('img/bullet_image.png').convert_alpha()

        # Récord histórico desde puntajes.txt (Fase 7).
        registros = self.leer_registros('puntajes.txt')
        if registros:
            self.jugador, self.max_pun = registros[0]
        else:
            self.jugador = None
            self.max_pun = 0

    @staticmethod
    def leer_registros(nombre_archivo):
        """Lee puntajes.txt → top 5 (nombre, int) ordenado desc.

        Robusto a:
        - archivo inexistente → []
        - líneas vacías o malformadas → skip con warning
        - "nombre, puntuación" con espacios variables (strip)
        - nombres con comas raras (rsplit con maxsplit=1)
        """
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
        except FileNotFoundError:
            print(f'[warn] no se encontró {nombre_archivo}, sin récords previos')
            return []

        registros = []
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            try:
                # FIX: el archivo real usa "nombre, puntuación" con espacio,
                # por eso strip() en cada parte. rsplit(',', 1) protege
                # contra nombres con comas.
                nombre, score = linea.rsplit(',', 1)
                registros.append((nombre.strip(), int(score.strip())))
            except ValueError:
                print(f'[warn] línea ignorada en {nombre_archivo}: {linea!r}')

        registros.sort(key=lambda t: t[1], reverse=True)
        return registros[:5]

    # FIX: el original tenía un mini-loop interno bloqueante mezclado con la
    # lógica de detección. Ahora over() solo decide si el juego terminó;
    # show_game_over_screen() se encarga de la presentación.
    def over(self):
        return self.lives <= 0

    def show_game_over_screen(self):
        label = self.font.render('GAME OVER', True, (255, 255, 255))
        pos = (
            self.WIDTH / 2 - label.get_width() / 2,
            self.HEIGHT / 2 - label.get_height() / 2,
        )
        # Pintamos el label sobre la ÚLTIMA frame del juego (no limpiamos
        # el fondo) durante FPS*3 frames. event.pump() mantiene la ventana
        # respondiendo en macOS.
        for _ in range(self.FPS * 3):
            self.clock.tick(self.FPS)
            pygame.event.pump()
            self.window.blit(label, pos)
            pygame.display.update()

    def reload_bullet(self, bullet):
        self.bullets = bullet

    def draw_HUD(self):
        lives_label = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        level_label = self.font.render(f'Level: {self.level}', True, (255, 255, 255))
        self.window.blit(lives_label, (10, 10))
        self.window.blit(
            level_label,
            (self.WIDTH - level_label.get_width() - 10, 10),
        )

        bw = self.bullet_image.get_width()
        bh = self.bullet_image.get_height()
        for i in range(self.bullets):
            self.window.blit(
                self.bullet_image,
                (self.WIDTH - (i + 1) * (bw + 4) - 6,
                 self.HEIGHT - bh - 10),
            )
