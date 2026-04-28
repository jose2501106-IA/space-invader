# Space Invader 👾☄️ — Brief del Proyecto

> Este archivo le da contexto persistente a Claude Code. Léelo siempre antes de actuar.

## 🎯 Objetivo

Construir un clon de **Space Invaders** en **Python + Pygame** con arquitectura orientada a objetos, siguiendo la estructura modular definida en los 5 documentos `.md` del curso (carpeta `docs/`).

## 🛠️ Stack y entorno

- **Python 3.10+** (este proyecto se está desarrollando con Python 3.14)
- **pygame-ce** (Community Edition, fork drop-in compatible de pygame). Se usa `pygame-ce` en lugar de `pygame` porque pygame original aún no tiene wheels para Python 3.14. **El código sigue siendo `import pygame`** — solo cambia el nombre del paquete en `pip install` y en `requirements.txt`. NO mezclar ambos paquetes en el mismo entorno.
- **macOS** — todos los comandos deben ser compatibles con zsh/bash en macOS
- **Entorno virtual** en `.venv/` (siempre activarlo antes de instalar o ejecutar)
- **Resolución** del juego: 800×600
- **FPS objetivo**: 60

## 📁 Estructura final esperada

```
space-invader/
├── .venv/                     # Entorno virtual (no versionar)
├── docs/                      # Los 5 .md del curso (referencia)
│   ├── 01_interfaces.md
│   ├── 02_pantalla_de_juego.md
│   ├── 03_enemigos.md
│   ├── 04_proyectiles.md
│   └── 05_jugador.md
├── img/                       # Sprites del juego
│   ├── background.png
│   ├── player_image.png
│   ├── bullet_image.png
│   ├── enemy_blue_image.png
│   ├── enemy_green_image.png
│   ├── enemy_purple_image.png
│   ├── shot_blue.png
│   ├── shot_green.png
│   └── shot_purple.png
├── ShipClass.py               # Clase base
├── EnemyClass.py              # Hereda de Ship
├── PlayerClass.py             # Hereda de Ship
├── BulletClass.py
├── GameClass.py
├── DrawingClass.py
├── main.py                    # Punto de entrada
├── requirements.txt
├── .gitignore
├── README.md
└── CLAUDE.md                  # Este archivo
```

## 🧱 Arquitectura de clases

### `ShipClass.Ship` (base)
Atributos: `x`, `y`, `health=100`, `ship_img=None`, `bullet_img=None`, `bullet_cooldown_counter=0`, `bullets=[]`, `fired_bullets=[]`, `cool_down=120`.
Métodos: `__init__`, `draw(window)`, `get_width()`, `get_height()`.

### `EnemyClass.Enemy(Ship)`
Variable de clase `COLOR` con dict mapeando `'blue'/'green'/'purple'` a tuplas `(ship_img, bullet_img)`.
Constructor: `__init__(self, speed, x=50, y=50, color='blue', health=100)` — llama a `super().__init__(x, y, health)`, asigna `ship_img`/`bullet_img` desde `COLOR[color]`, crea `mask` y guarda `speed` (⚠️ los .md tienen typo `spped`, hay que escribir `speed`).
Métodos: `move()` (suma `speed` a `y`), `create(amount)` (genera lista de N enemigos en X aleatoria entre 20 y `WIDTH - sprite_width - 20`, Y aleatoria entre -1000 y -100, color aleatorio), `increase_speed()` (multiplica `speed` por 1.02).

### `BulletClass.Bullet`
Constructor: `__init__(self, x, y, img)` — guarda coordenadas, imagen y crea `mask = pygame.mask.from_surface(img)`.
Métodos: `draw(window)`, `move(speed)` (suma a `y`), `collision(obj)` (pixel-perfect con offset `(x - obj.x - 30, y - obj.y - 20)` y `mask.overlap`).

### `PlayerClass.Player(Ship)`
Constructor: `__init__(self, x, y, x_speed, y_speed, health=100)` — `super().__init__`, guarda velocidades, asigna `PLAYER_IMAGE` y `BULLET_IMAGE`, `bullet_speed=-10`, `max_health=health`, `mask`, `creation_cooldown_counter=0`, `max_amount_bullets=3`, reinicia `bullets=[]`, `bullet_cooldown_counter=0`.
Métodos:
- `move()` — WASD y flechas, con límites de pantalla (los .md tienen paréntesis mal cerrados: corrige a `if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 0:` etc.).
- `increase_speed()` — sube velocidades hasta tope (10 horizontal, 8 vertical) y reduce `cool_down` por 0.9 si > 25.
- `create_bullets()` — añade `Bullet` a `self.bullets` si hay menos del máximo y el contador está en 0; limpia balas que salieron por arriba (y ≤ -40) de `fired_bullets`.
- `cooldown()` — gestiona los dos contadores (reinicia cuando llegan al límite, incrementa si > 0).
- `fire(window)` — con SPACE + bala disponible + cooldown=0, posiciona la última bala centrada sobre la nave, la mueve a `fired_bullets`, activa cooldowns; luego mueve y dibuja todas las disparadas.
- `hit(enemy)` — chequea colisión de balas disparadas con un enemigo.

### `GameClass.Game`
Carga `BULLET_IMAGE` desde `img/bullet_image.png` al importar el módulo.
Constructor: `__init__(self, font, FPS, lives, window, screen_width, screen_height, bullets=0, clock=None)` — usa `clock or pygame.time.Clock()`, guarda `WIDTH`, `HEIGHT` (⚠️ los .md escriben `HEIGTH` con typo, **usa `HEIGHT` correcto** y mantén consistencia), `level=1`, `count=0`.
Métodos:
- `escape()` — devuelve True si hay evento `QUIT` en la cola, False si no. ⚠️ Cuidado: este método consume eventos; no lo llames junto con otro `pygame.event.get()` en el mismo frame.
- `over()` — si `lives <= 0`, dibuja "GAME OVER" centrado durante ~3 segundos y devuelve True; si no, False.
- `reload_bullet(bullet)` — actualiza `self.bullets`.
- `draw_HUD()` — render de "Lives: N" arriba-izquierda, "Level: N" arriba-derecha, e iconos de balas en la esquina inferior derecha.

### `DrawingClass.Drawing`
Carga `BACKGROUND` desde `img/background.png` al importar.
Constructor recibe `window`. Método `drawing(game, player, enemies, FPS)` que dibuja en orden: fondo → `player.fire(window)` → enemigos → `player.draw(window)` → `game.draw_HUD()` → `pygame.display.update()`.

## 🎮 Bucle principal (main.py)

1. `pygame.init()`, crear window 800×600, `pygame.display.set_caption("Space Invader")`.
2. Cargar font con `pygame.font.SysFont('comicsans', 30)`.
3. Crear instancias: `Game`, `Player(WIDTH/2, HEIGHT-100, 5, 5)`, `enemies = Enemy(2).create(5)`, `Drawing(window)`.
4. `while running:` con `clock.tick(FPS)`:
   - Manejo de eventos (un solo `pygame.event.get()` por frame; salir con `QUIT`).
   - `player.create_bullets()`, `player.cooldown()`, `player.move()`.
   - Para cada enemigo: `move()`, comprobar colisión con balas del jugador (`player.hit(enemy)` → eliminar enemigo + sumar puntos); si llega al fondo → restar vida y reposicionar.
   - Si lista de enemigos vacía → `level += 1`, `player.increase_speed()`, generar nueva oleada.
   - `drawing.drawing(game, player, enemies, FPS)`.
   - Si `game.over()` → break.
5. `pygame.quit()`, `sys.exit()`.

## 🐛 Bugs conocidos en los .md (corregir al implementar)

1. **Paréntesis mal cerrados** en `Player.move()`: `if (keys[pygame.K_UP] and (self.y > 0):` debe ser `if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 0:`.
2. **Typo `spped`** en `Enemy.__init__` → debe ser `speed`.
3. **`Player.create_bullets`** tiene un loop sobre `self.fired_bullets` que limpia balas viejas — está bien pero asegurarse que `fired_bullets` exista (lo hereda de `Ship`).
4. **`HEIGTH` vs `HEIGHT`** — los .md mezclan ambos. Usar `HEIGHT` consistentemente.
5. **`Game.escape()` y `pygame.event.get()`** — si se llama dos veces por frame se pierden eventos. En `main.py` hay que centralizar el manejo de eventos.
6. **`Game.over()`** tiene `if self.count == self.FPS*3` — usar `>=` para evitar carrera.
7. **`Player.hit()`** original devuelve dentro del loop en la primera iteración → no es correcto. Implementar para que recorra todas las balas y devuelva la primera colisión real, eliminando la bala que impactó.
8. **`Drawing.drawing`** debe llamar a `player.fire(self.window)` y `player.draw(self.window)` (los .md lo aclaran al final del doc 5).

## 📦 Assets

Las imágenes deben estar en `img/`. Si el usuario aún no las tiene, **generar placeholders programáticos** con `pygame.Surface` + `pygame.draw` y guardarlos como PNG en `img/` con los nombres correctos. Esto desbloquea el desarrollo y luego el usuario reemplaza por sprites reales sin tocar el código.

## 🚦 Plan por fases

- **Fase 0 — Setup**: venv, requirements, estructura de carpetas, .gitignore, README, assets (reales o placeholder), commit inicial.
- **Fase 1 — Ship + Game + ventana**: `ShipClass`, `GameClass`, ventana abre, HUD muestra vidas/nivel/balas, evento QUIT funciona. Smoke test ejecutable.
- **Fase 2 — Bullet + Enemy**: enemigos caen aleatoriamente, balas se dibujan en pantalla.
- **Fase 3 — Player**: movimiento WASD/flechas, disparo con espacio, cooldowns funcionando.
- **Fase 4 — Drawing + integración**: `DrawingClass`, `main.py` ensambla todo, el juego corre.
- **Fase 5 — Colisiones, niveles y polish**: `player.hit`, `level += 1`, GAME OVER, ajuste de balance, README final.

## ✅ Definición de "terminado"

- `python main.py` desde el venv arranca el juego sin errores.
- El jugador se mueve con WASD o flechas y dispara con espacio.
- Los enemigos aparecen, caen, son destruidos al ser disparados.
- El HUD muestra vidas, nivel y balas correctamente.
- Al llegar a 0 vidas aparece "GAME OVER" 3 segundos y la ventana se cierra limpiamente.
- Todos los archivos `.py` están bien formateados (PEP8 razonable) y sin imports muertos.
- README explica cómo instalar y correr el juego.

## 🤝 Cómo trabajar conmigo (para Claude Code)

- Antes de cada fase, **lee el .md correspondiente** en `docs/` y resume al usuario lo que vas a implementar.
- Después de cada fase, **ejecuta `python main.py`** (o un script de prueba si aún no hay main) y reporta lo que ves.
- Si encuentras un bug del código original de los .md, **arréglalo** y deja un comentario `# FIX: ...` corto explicando.
- Haz **commits granulares** por fase con mensajes descriptivos.
- Si algo no está claro, **pregunta al usuario** en lugar de inventar.

## 🚀 Plan de expansión (Fases 6–11)

El proyecto base (Fases 0–5) está terminado. A partir de acá lo convertimos en
una aplicación con menús, navegación y puntajes persistentes.

| Fase | Entregable | Estado |
|------|------------|--------|
| 6 | Setup assets nuevos (sounds/, puntajes.txt, menú imgs) + bonus gameplay (HUD balas reales, +1 vida y +1 bala max cada 3 niveles) | ✅ |
| 7 | Sistema de puntaje (variable puntaje, lectura de puntajes.txt en Game, "Points: N" en HUD) + sonidos (explosion.wav, ganar.mp3) | ✅ |
| 8 | PantallaNombreClass — input al batir récord, escribe nombre,puntaje en puntajes.txt | ✅ |
| 9 | MenuPuntajesClass — top 5 leído de archivo, botón "<" volver | ✅ |
| 10 | MenuAcercaDeClass — info + link clickeable a Hybridge, botón "<" volver | ✅ |
| 11 | MenuPrincipalClass + integración total (refactor main para que el menú sea entrada) | ✅ |

## 🧱 Convenciones para las nuevas clases de menú

- Todas las clases de menú reciben `back_mtd` o callbacks por constructor
  (NO singletons, NO globales).
- Cada clase de menú vive en su propio archivo `MenuXxxClass.py`.
- TODAS usan el patrón `@classmethod load_assets()` con autoload lazy en
  `__init__`, igual que las clases del juego.
- NO incluir `pygame.init()` ni `pygame.display.set_mode()` a nivel de módulo.
  La ventana es una sola y se pasa por argumento o se reusa la misma.
- Manejo de eventos: un solo `pygame.event.get()` por frame dentro del loop
  de la clase. NO consumir eventos en métodos auxiliares.
- Todas exponen un método público para mostrarse (`ejecutar()` / `mostrar()` /
  `loop()`) que contiene su propio `while` loop.

## 🎮 Mecánicas de puntaje y persistencia

- Archivo: `puntajes.txt` en raíz del proyecto. Formato: `nombre,puntuacion\n`
  por línea.
- `Game.leer_registros(archivo)` → lista de tuplas `(nombre, puntuación)`
  ordenada desc, top 5.
- En el constructor de `Game`, leer `puntajes.txt` y guardar
  `self.max_pun` = max histórico (0 si no hay registros) y `self.jugador` =
  nombre del récord (si hay).
- Variable `puntaje` en `main()`: suma 1 por cada enemy destruido por bala
  del player.
- Al GAME OVER: si `puntaje > game.max_pun` → reproducir `ganar.mp3` + lanzar
  `PantallaNombre`. Si no → volver al menú principal.
