"""Tests del parser y constructor de Game (récords persistentes)."""
import pygame

from GameClass import Game


def _write(path, content):
    """Helper: escribe `content` en `path` con encoding utf-8."""
    path.write_text(content, encoding='utf-8')


def test_leer_registros_archivo_valido(tmp_path):
    archivo = tmp_path / 'puntajes.txt'
    _write(archivo, 'Pepe,50\nAna,30\nLuis,40\nMaria,20\nJuan,10\n')

    recs = Game.leer_registros(str(archivo))

    assert len(recs) == 5
    for nombre, score in recs:
        assert isinstance(nombre, str)
        assert isinstance(score, int)


def test_leer_registros_archivo_inexistente(tmp_path):
    archivo = tmp_path / 'no_existe.txt'

    recs = Game.leer_registros(str(archivo))

    assert recs == []


def test_leer_registros_linea_malformada(tmp_path):
    archivo = tmp_path / 'puntajes.txt'
    contenido = (
        'Bueno,50\n'
        'linea_sin_coma\n'
        'Otro,abc\n'
        '\n'
        'Bueno2,30\n'
    )
    _write(archivo, contenido)

    recs = Game.leer_registros(str(archivo))

    assert recs == [('Bueno', 50), ('Bueno2', 30)]


def test_leer_registros_formato_con_espacio(tmp_path):
    archivo = tmp_path / 'puntajes.txt'
    _write(archivo, 'Pepe, 50\nAna, 30\n')

    recs = Game.leer_registros(str(archivo))

    assert recs == [('Pepe', 50), ('Ana', 30)]


def test_leer_registros_top_5(tmp_path):
    archivo = tmp_path / 'puntajes.txt'
    contenido = '\n'.join(f'P{i},{i * 10}' for i in range(1, 9)) + '\n'
    _write(archivo, contenido)

    recs = Game.leer_registros(str(archivo))

    assert len(recs) == 5
    assert recs[0] == ('P8', 80)
    assert recs[-1] == ('P4', 40)


def test_leer_registros_utf8(tmp_path):
    archivo = tmp_path / 'puntajes.txt'
    _write(archivo, 'Andrés,55\nMaría,42\n')

    recs = Game.leer_registros(str(archivo))

    nombres = [n for n, _ in recs]
    assert 'Andrés' in nombres
    assert 'María' in nombres


def test_leer_registros_orden_descendente(tmp_path):
    archivo = tmp_path / 'puntajes.txt'
    _write(archivo, 'Bajo,10\nAlto,90\nMedio,50\n')

    recs = Game.leer_registros(str(archivo))

    scores = [s for _, s in recs]
    assert scores == sorted(scores, reverse=True)
    assert recs[0] == ('Alto', 90)


def test_leer_registros_archivo_vacio(tmp_path):
    archivo = tmp_path / 'puntajes.txt'
    archivo.write_text('', encoding='utf-8')

    recs = Game.leer_registros(str(archivo))

    assert recs == []


def test_game_init_max_pun(monkeypatch, pygame_window):
    monkeypatch.setattr(
        Game, 'leer_registros',
        staticmethod(lambda _path: [('Andrés', 99), ('Otro', 50)]),
    )

    font = pygame.font.SysFont('comicsans', 30)
    game = Game(font, 60, lives=5, window=pygame_window,
                screen_width=800, screen_height=600, bullets=3)

    assert game.max_pun == 99
    assert game.jugador == 'Andrés'


def test_game_init_sin_puntajes(monkeypatch, pygame_window):
    monkeypatch.setattr(
        Game, 'leer_registros', staticmethod(lambda _path: []))

    font = pygame.font.SysFont('comicsans', 30)
    game = Game(font, 60, lives=5, window=pygame_window,
                screen_width=800, screen_height=600, bullets=3)

    assert game.max_pun == 0
    assert game.jugador is None
