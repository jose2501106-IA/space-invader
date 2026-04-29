"""Tests de Ship/Enemy/Player — atributos de instancia y velocidades."""
from EnemyClass import Enemy
from PlayerClass import Player
from ShipClass import Ship


def test_ship_bullets_es_atributo_de_instancia():
    """Regresión Fase 5: bullets debe ser per-instance, no class-shared."""
    s1 = Ship(0, 0)
    s2 = Ship(100, 100)

    s1.bullets.append('marker')

    assert s2.bullets == []
    assert s1.bullets == ['marker']


def test_ship_fired_bullets_es_atributo_de_instancia():
    """Regresión Fase 5: fired_bullets debe ser per-instance."""
    s1 = Ship(0, 0)
    s2 = Ship(100, 100)

    s1.fired_bullets.append('disparo')

    assert s2.fired_bullets == []
    assert s1.fired_bullets == ['disparo']


def test_enemy_speed_es_int_positivo(pygame_window):
    Enemy.load_assets()
    enemy = Enemy(speed=2)

    assert enemy.speed > 0
    assert isinstance(enemy.speed, (int, float))


def test_player_x_speed_es_int_positivo(pygame_window):
    Player.load_assets()
    player = Player(x=400, y=500, x_speed=5, y_speed=5)

    assert player.x_speed > 0
    assert player.y_speed > 0
