# 🚀 Prompt inicial para Claude Code

> Copia y pega TODO el contenido de la sección "PROMPT" abajo en tu primer mensaje a Claude Code.

---

## PROMPT

Hola Claude Code. Vamos a construir un proyecto llamado **Space Invader** en Python + Pygame, en macOS.

**Antes de tocar nada, hace esto en orden:**

1. Lee el archivo `CLAUDE.md` que hay en la raíz del proyecto. Tiene el brief completo: arquitectura, clases, bugs conocidos en los docs, plan por fases y la definición de "terminado". Tomá ese archivo como tu fuente de verdad.

2. Lee los 5 archivos en `docs/` en este orden: `01_interfaces.md`, `02_pantalla_de_juego.md`, `03_enemigos.md`, `04_proyectiles.md`, `05_jugador.md`. Son la guía pedagógica del curso. Úsalos como referencia, pero **siempre** corregí los bugs listados en `CLAUDE.md` cuando aparezcan.

3. Después de leer todo, devuélveme:
   - Un resumen en 5-8 líneas de lo que entendiste.
   - El plan de la **Fase 0** (setup) con los pasos exactos que vas a ejecutar.
   - Una lista de las preguntas que tengas (si las tenés) antes de arrancar.

**Reglas de trabajo durante todo el proyecto:**

- Trabajamos por fases (0 a 5). No saltes a la siguiente sin que yo te lo confirme.
- Antes de cada fase: leé el `.md` correspondiente y contame qué vas a hacer.
- Después de cada fase: corré `python main.py` (o un script de prueba si todavía no hay `main.py`) y reportame el resultado real, incluyendo errores si los hay.
- Hacé `git commit` al final de cada fase con un mensaje descriptivo. Si no hay repo todavía, inicializalo en la Fase 0.
- Si encontrás un bug en los `.md`, **corregilo** y dejá un comentario `# FIX: ...` corto en el código.
- Mantené `requirements.txt` actualizado.
- Si necesitás instalar algo, usá el venv del proyecto (`.venv/`).

**Sobre los assets** (imágenes en `img/`):
- Si la carpeta `img/` ya tiene los PNG necesarios, usalos.
- Si NO están, generá placeholders programáticos con `pygame.Surface` + `pygame.draw` y guardalos como PNG con los nombres exactos que pide el proyecto (`player_image.png`, `bullet_image.png`, `enemy_blue_image.png`, etc.). Hacelo en un script aparte llamado `generate_placeholders.py` para que el usuario después pueda reemplazar las imágenes sin tocar el código del juego.

Cuando termines de leer y me confirmes el plan de la Fase 0, te doy luz verde para arrancar.

---

## Plan de fases (resumen para tu referencia)

- **Fase 0 — Setup**: venv, requirements, estructura, .gitignore, README, assets, commit inicial.
- **Fase 1 — Ship + Game + ventana**: `ShipClass.py`, `GameClass.py`, ventana abre, HUD funciona, QUIT funciona.
- **Fase 2 — Bullet + Enemy**: `BulletClass.py`, `EnemyClass.py`, enemigos caen.
- **Fase 3 — Player**: `PlayerClass.py`, movimiento, disparo, cooldowns.
- **Fase 4 — Drawing + main**: `DrawingClass.py`, `main.py`, juego ensamblado.
- **Fase 5 — Colisiones, niveles, polish**: `player.hit`, oleadas, GAME OVER, README final.
