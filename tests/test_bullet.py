"""Tests de Bullet (creación, movimiento) + ciclo de vida vía Player."""
import pygame

from BulletClass import Bullet
from PlayerClass import Player


def _bullet_img():
    """Surface chica con alpha — sirve para crear Bullet sin assets reales."""
    surf = pygame.Surface((10, 20), pygame.SRCALPHA)
    surf.fill((255, 255, 255, 255))
    return surf


def test_bullet_creates_with_position(pygame_window):
    bullet = Bullet(x=42, y=100, img=_bullet_img())

    assert bullet.x == 42
    assert bullet.y == 100
    assert bullet.img is not None
    # mask se construye en __init__ — confirmamos que existe y es del tamaño.
    assert bullet.mask.get_size() == (10, 20)


def test_bullet_move_negativo_disminuye_y(pygame_window):
    """Bala de player: speed negativo → la bala sube."""
    bullet = Bullet(x=0, y=300, img=_bullet_img())

    bullet.move(-10)

    assert bullet.y == 290


def test_bullet_move_positivo_aumenta_y(pygame_window):
    """Bala con speed positivo (ej: enemigos hipotéticos) → baja."""
    bullet = Bullet(x=0, y=300, img=_bullet_img())

    bullet.move(5)

    assert bullet.y == 305


def test_player_descarta_balas_arriba(pygame_window):
    """Regresión: balas con y <= -40 deben ser limpiadas en create_bullets()."""
    Player.load_assets()
    player = Player(x=400, y=500, x_speed=5, y_speed=5)

    arriba = Bullet(x=0, y=-50, img=_bullet_img())
    player.fired_bullets = [arriba]

    player.create_bullets()

    assert arriba not in player.fired_bullets


def test_player_mantiene_balas_en_pantalla(pygame_window):
    """Balas con y > -40 (en pantalla o cerca del borde) deben permanecer."""
    Player.load_assets()
    player = Player(x=400, y=500, x_speed=5, y_speed=5)

    en_pantalla = Bullet(x=0, y=300, img=_bullet_img())
    cerca_borde = Bullet(x=0, y=-30, img=_bullet_img())
    player.fired_bullets = [en_pantalla, cerca_borde]

    player.create_bullets()

    assert en_pantalla in player.fired_bullets
    assert cerca_borde in player.fired_bullets
