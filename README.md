# Space Invader 👾☄️

Clon de **Space Invaders** en Python + pygame-ce, construido como proyecto de
curso con arquitectura modular orientada a objetos. El jugador defiende la
parte inferior de la pantalla disparando contra oleadas de enemigos que caen;
cada nivel sube la velocidad y la cantidad de enemigos, hasta que el jugador
se queda sin vidas.

<!-- TODO: insertar capturas de pantalla -->

## 🎮 Controles
- **Mover**: `WASD` o flechas (`↑ ← ↓ →`).
- **Disparar**: `SPACE` (máximo 3 balas en vuelo, con cooldown).
- **Salir**: `ESC` o cerrar la ventana.

## 🛠️ Requisitos
- Python 3.10+ (probado en 3.14).
- [pygame-ce](https://pyga.me/) (drop-in compatible con `pygame`; soporta Python 3.14).

## 🚀 Cómo correr
```bash
git clone <este-repo>
cd space-invader
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows
pip install -r requirements.txt
python main.py
```

## 📁 Estructura del proyecto
```
space-invader/
├── ShipClass.py        # clase base
├── EnemyClass.py       # Enemy(Ship) — 3 colores, oleadas escaladas
├── PlayerClass.py      # Player(Ship) — movimiento, disparo, hit()
├── BulletClass.py      # Bullet con mask pixel-perfect
├── GameClass.py        # HUD, lives/level, escape, game over screen
├── DrawingClass.py     # pipeline de render (fondo + capas + flip)
├── main.py             # punto de entrada, loop principal, música
├── img/                # sprites (player, enemigos, balas, fondo, ícono)
├── music.mp3           # música de fondo
├── docs/               # referencia (los .md del curso viven en Drive)
├── requirements.txt
├── README.md
└── CLAUDE.md           # brief del proyecto para Claude Code
```

## 🐛 Bugs conocidos del material original corregidos

Durante la implementación se encontraron y corrigieron los siguientes bugs
en los `.md` del curso. Cada corrección está marcada con `# FIX: ...` en el
código:

| # | Archivo | Bug original | Corrección |
|---|---------|--------------|------------|
| 1 | `EnemyClass.py` | typo `spped` en `__init__` | renombrado a `speed` |
| 2 | `PlayerClass.py` | paréntesis mal cerrados en `move()` | reagrupados correctamente |
| 3 | `EnemyClass.py` / `PlayerClass.py` | `WIDTH`/`HEIGHT` como globales | parámetros `screen_width`/`screen_height` |
| 4 | `GameClass.py` | typo `HEIGTH` mezclado con `HEIGHT` | siempre `HEIGHT` |
| 5 | `GameClass.py` | `Game.escape()` consumía eventos por su cuenta | recibe la lista `events` desde `main` |
| 6 | `GameClass.py` | `over()` con `==` (carrera de frames) | refactor: `over()` no bloquea, `show_game_over_screen()` aparte |
| 7 | `PlayerClass.py` | `hit()` retornaba en la primera iteración | recorre todas las balas, remueve solo la que impacta |
| 8 | `ShipClass.py` | `bullets`/`fired_bullets` como variables de clase | atributos de instancia para evitar listas compartidas |

## 📦 Créditos
- Motor: [pygame-ce 2.5.7](https://pyga.me/) — fork comunitario de pygame.
- Sprites y música: material original del curso.
- Implementación: basada en los 5 documentos del curso, con `CLAUDE.md` como
  fuente de verdad para arquitectura y plan por fases.
