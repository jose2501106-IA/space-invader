"""Tests del append-write hardenizado de PantallaNombre + estado inicial."""
from PantallaNombreClass import PantallaNombre


def test_escribir_en_archivo_nuevo(tmp_path):
    archivo = tmp_path / 'puntajes.txt'

    PantallaNombre.escribir_en_archivo(str(archivo), 'Foo,42')

    assert archivo.read_bytes() == b'Foo,42\n'


def test_escribir_en_archivo_append(tmp_path):
    archivo = tmp_path / 'puntajes.txt'
    archivo.write_bytes(b'Foo,42\n')

    PantallaNombre.escribir_en_archivo(str(archivo), 'Bar,99')

    assert archivo.read_bytes() == b'Foo,42\nBar,99\n'


def test_escribir_en_archivo_hardening_sin_newline(tmp_path):
    """Regresión Fase 8: archivo sin \\n final no debe fusionar la última línea."""
    archivo = tmp_path / 'puntajes.txt'
    archivo.write_bytes(b'Foo,42')  # SIN newline final

    PantallaNombre.escribir_en_archivo(str(archivo), 'Bar,99')

    assert archivo.read_bytes() == b'Foo,42\nBar,99\n'
    # Y específicamente NO tiene la fusión:
    assert b'Foo,42Bar' not in archivo.read_bytes()


def test_escribir_en_archivo_vacio_preexistente(tmp_path):
    archivo = tmp_path / 'puntajes.txt'
    archivo.write_bytes(b'')

    PantallaNombre.escribir_en_archivo(str(archivo), 'Foo,42')

    assert archivo.read_bytes() == b'Foo,42\n'


def test_escribir_en_archivo_unicode(tmp_path):
    archivo = tmp_path / 'puntajes.txt'

    PantallaNombre.escribir_en_archivo(str(archivo), 'María Torres,55')

    contenido = archivo.read_text(encoding='utf-8')
    assert contenido == 'María Torres,55\n'
    # Round-trip parseable.
    nombre, score = contenido.strip().rsplit(',', 1)
    assert nombre == 'María Torres'
    assert int(score) == 55


def test_escribir_en_archivo_multiples_appends(tmp_path):
    archivo = tmp_path / 'puntajes.txt'

    for i in range(5):
        PantallaNombre.escribir_en_archivo(str(archivo), f'P{i},{i * 10}')

    contenido = archivo.read_text(encoding='utf-8')
    lineas = contenido.split('\n')
    # 5 líneas + 1 vacía al final por el \n final.
    assert lineas == ['P0,0', 'P1,10', 'P2,20', 'P3,30', 'P4,40', '']
    assert contenido.endswith('\n')


def test_pantalla_nombre_init_state(pygame_window):
    pn = PantallaNombre(pygame_window, puntaje=99, finish_mtd=lambda: None)

    assert pn.texto_input == ''
    # Autofocus aplicado en Fase 8 — el usuario no debe clickear para tipear.
    assert pn.input_active is True
    assert pn.puntaje == 99
