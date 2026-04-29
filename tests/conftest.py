"""Shared pytest setup.

Establece SDL en modo dummy ANTES de importar pygame, e inicializa la ventana
una sola vez por sesión. El proyecto requiere `set_mode()` para que
`convert_alpha()` funcione, así que el fixture es session-scoped + autouse.
"""
import os

# Setear ANTES de importar pygame, no después.
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

import pygame  # noqa: E402  — imports después de env setup, intencional
import pytest  # noqa: E402


@pytest.fixture(scope='session', autouse=True)
def pygame_window():
    """Inicializa pygame + ventana dummy. Reusado por toda la sesión."""
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    yield window
    pygame.quit()
