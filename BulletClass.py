import pygame


class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, speed):
        self.y += speed

    def collision(self, obj):
        # NOTA: los offsets (-30, -20) vienen tal cual de los .md del curso
        # y asumen un tamaño de sprite concreto. Cuando integremos colisiones
        # reales en Fase 5 puede que necesiten ajuste fino según los sprites
        # finales (ancho/alto de bala vs. nave).
        offset = (int(self.x - obj.x - 30), int(self.y - obj.y - 20))
        return self.mask.overlap(obj.mask, offset)
