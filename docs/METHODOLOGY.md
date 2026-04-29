# Metodología de desarrollo de Space Invader Hybridge

## Resumen

Este proyecto es un clon completo de Space Invaders en Python + pygame-ce
construido en 14 fases iterativas. Lo interesante no es el juego en sí
—es un proyecto educativo de OO— sino el **proceso** con el que fue
construido: planning detallado por fase, validación a tres capas antes
de cada commit, y trazabilidad completa de bugs detectados.

La metodología importa porque define el delta entre "código que funciona
en mi máquina" y "código auditable y mantenible por otra persona". El
diferenciador principal de este proyecto es el **ciclo de validación a
tres capas** (smoke automatizado + verificación sintética + validación
visual humana) que se aplicó antes de cada uno de los 17 commits del
historial. De los 16 bugs totales detectados durante el desarrollo
(12 originales del material + 4 introducidos en el proceso), **0
llegaron a producción**: todos fueron atrapados antes del commit
correspondiente.

## Los 6 principios

### 1. Planning antes de codear

Cada fase arranca con un brief escrito en lenguaje natural que define:
entregables concretos, criterios de validación, commit propuesto, y
notas de scope cerrado. Ningún código se escribe sin un plan claro.

**Ejemplo concreto** (Fase 11 — refactor mayor a menú como entry point):

> Reorganización de la estructura: sacar de `main()` todo lo que es
> setup global de pygame. Movelos a una función `setup_pygame()` que se
> llama UNA sola vez al inicio del archivo. Renombrar `main()` a
> `iniciar_juego()`. Esta función contiene SOLO la lógica del game loop
> (lo que está adentro del while running). Debe retornar normalmente al
> terminar (no hacer pygame.quit() ni sys.exit() — la app sigue viva
> tras game over).

Ese párrafo, escrito 5 minutos antes de tocar código, evita la deriva
y acota qué exactamente está en juego. Sin él, los refactors se
expanden silenciosamente.

### 2. Validación a 3 capas

Antes de cada commit, el código pasa por tres filtros:

1. **Smoke test headless** — `SDL_VIDEODRIVER=dummy python main.py`
   con kill tras 3 segundos. Detecta tracebacks, errores de import y
   crashes al boot sin necesidad de display. Es el chequeo más barato
   y atrapa el 80% de los problemas.

2. **Verificación sintética** — `assert`s específicos sobre estado
   interno: tamaños de Surface, valores de atributos, output de
   funciones puras. Estos viven en `tests/` (suite pytest con 26
   tests) y también se ejecutan ad-hoc por fase para confirmar que el
   contrato de cada nueva clase es el esperado antes de wirearla al
   resto.

3. **Validación visual humana** — el desarrollador prueba manualmente
   cada fase antes de aprobar el commit. Esto atrapa bugs que ningún
   test automático puede ver: un logo solapando un título, un layout
   con columnas que se pisan, un sonido que se desincroniza con la
   pausa de música. La capa más costosa pero la más necesaria.

### 3. Commits granulares

Una fase = un commit, con mensaje descriptivo en formato
`feat(phase-N): título corto` + cuerpo explicando los 3-5 cambios
puntuales. El historial completo está en `git log --oneline` y permite
revertir o auditar cualquier paso del proceso sin arqueología.

### 4. Documentación inline de bugs corregidos

Cada bug del material original o edge case descubierto durante
implementación queda marcado con un comentario `# FIX:` adyacente al
código que lo resuelve. La tabla de "Bugs corregidos" del README se
deriva 100% de esos comentarios. Resultado: el código mismo cuenta su
propia historia, sin necesidad de bucear en commits ni en notas
separadas.

### 5. Callbacks por constructor para arquitectura

La capa de UI (5 clases de menú + pantalla de input de récord) usa
**callbacks pasados por constructor** en lugar de singletons o
referencias globales. `MenuPuntajes(window, back_mtd=lambda: None)` es
testable en aislamiento: podés pasar cualquier callable. Y el call
stack de Python unwindea naturalmente cuando el usuario navega de
vuelta, sin necesidad de event buses ni state machines.

### 6. Iteración en fases con scope cerrado

Cada fase tiene scope explícito y no se permite expansión sin
flagearla. Si durante la implementación aparece un bug o un edge case
que no está en el brief, se documenta y se decide: (a) arreglar acá
y mencionar en el reporte, o (b) anotar para una fase futura. Nunca
se mezclan refactors no pedidos en un commit de feature.

## Las 14 fases del proyecto

| # | Fase | Tipo |
|---|------|------|
| 0 | Setup inicial (venv, requirements, estructura, assets, .gitignore) | Base |
| 1 | `Ship` + `Game` + ventana abre con HUD funcional | Base |
| 2 | `Bullet` + `Enemy` (3 colores, oleadas aleatorias) | Base |
| 3 | `Player` (movimiento WASD/flechas, disparo, cooldowns) | Base |
| 4 | `Drawing` encapsula el render pipeline | Base |
| 5 | Colisiones, sistema de niveles, GAME OVER, música, README inicial | Base |
| 6 | Setup de assets nuevos (sounds/, puntajes.txt, menú imgs) + bonus gameplay | Expansión |
| 7 | Sistema de puntaje (Points HUD, lectura de récords, sonidos kill/win) | Expansión |
| 8 | `PantallaNombre` para input al batir récord (con hardening de newline) | Expansión |
| 9 | `MenuPuntajes` (top 5 leído de archivo) | Expansión |
| 10 | `MenuAcercaDe` con link clickeable a Hybridge | Expansión |
| 11 | `MenuPrincipal` como entry point + flujo completo de navegación | Expansión |
| 12 | Pantalla de pausa con tecla P | Polish |
| 13 | `MenuInstrucciones` con todos los controles del juego | Polish |

## Métricas del proceso

- **17+ commits en `main`**, todos con validación previa.
- **12 bugs del material original** detectados y corregidos
  (typo `spped`, paréntesis mal cerrados en `move()`, `WIDTH`/`HEIGHT`
  como globales, listas de clase compartidas, etc).
- **4 bugs descubiertos durante el proceso** (no presentes en el
  material): conflicto de teclas WASD vs `K_a`, fusión de líneas en
  `puntajes.txt` por falta de newline final, solapamiento del logo
  Hybridge sobre el título del menú principal, solapamiento de
  columnas de teclas/descripciones en MenuInstrucciones.
- **0 bugs llegaron a producción**: todos fueron atrapados antes del
  commit correspondiente gracias al ciclo plan → implementar →
  smoke + sintética → validación visual → commit.
- **26 tests automatizados** en `tests/` cubren parser de récords,
  hardening de append-write, atributos de instancia, ciclo de vida
  de balas y velocidades de naves.

## Lecciones aprendidas

### El git diff es la última línea de defensa

Durante la validación de Fase 8 (`PantallaNombre` + persistencia),
revisamos el `git diff` antes del commit y notamos algo extraño en
`puntajes.txt`: la línea histórica de `Andrés Díaz, 55` aparecía
fusionada con el nuevo registro `pepe,58`, formando
`Andrés Díaz, 55pepe,58`. La causa era que el archivo del playground
no terminaba en `\n`, y el método de append escribía
`contenido + '\n'` solo después. Ningún test automático ni smoke
hubiera detectado eso porque `rsplit(',', 1)` parseaba la línea
fusionada sin error (con un nombre inventado). Lección: **el
ojo humano sobre el diff atrapa lo que el código pasa por alto**.

### La validación visual humana detecta bugs invisibles a los tests

En Fase 11, después de wirear `MenuPrincipal` con todos sus
callbacks, el smoke test pasaba y la verificación sintética también.
Pero al abrirlo en pantalla, el logo de Hybridge estaba pintado
encima del título "Space Invader" y del subtítulo. Era un layout
calculado en función de `h // 4 + offset`, y los offsets eran muy
chicos para la altura real de las fuentes en macOS. **Ningún test
unitario hubiera detectado eso** porque las coordenadas eran
matemáticamente "correctas". El mismo patrón se repitió en Fase 13
con la columna de teclas de MenuInstrucciones pisando las
descripciones.

### Los caracteres invisibles existen

Al mover capturas de pantalla del Desktop al repo, los `mv` con
nombres tipeados a mano fallaban con "No such file or directory". El
diagnóstico con `xxd` reveló que macOS usa **U+202F (NARROW NO-BREAK
SPACE)** entre la hora y "p.m." en los nombres de screenshots, no un
espacio normal U+0020. Visualmente idénticos, distintos en bytes.
Solución: globs por timestamp único (`Screenshot*5.05.06*.png`)
matchean cualquier caracter incluyendo el U+202F. Lección: **antes de
tipear filenames de macOS con espacios y horarios, usá globs o
verificá con `xxd`; nunca asumas que los espacios visibles son
U+0020**.

### Las pausas pidiendo confirmación protegen contra asunciones equivocadas

En el flujo de mover capturas al proyecto, hubo un mensaje en el
que se pidió confirmación antes de ejecutar 7 `mv`. Esa pausa quedó
sin respuesta — el siguiente turno asumió que el move había
sucedido. Resultado: el README terminó referenciando archivos
inexistentes, y GitHub mostraba links azules en lugar de imágenes.
La pausa fue lo correcto; lo que faltó fue verificar el estado real
con `ls screenshots/` antes de seguir. Lección: **si pediste
confirmación y la respuesta no llegó, NO asumas que se hizo —
verificá**.

### Refactorear el código muerto al detectar el cambio de contrato

En Fase 11, al separar QUIT (cierra app) de ESC (vuelve al menú) en
el game loop, `Game.escape()` —que mezclaba ambos en un único bool—
quedó sin uso. La tentación es dejarlo "por si acaso". Lo correcto
fue eliminarlo del código junto con cualquier referencia residual,
y documentarlo en el commit de la fase. **Código muerto es deuda
técnica silenciosa**; cuando un cambio de contrato deja una API sin
usar, removerla es parte del refactor, no una limpieza posterior.

## Cómo replicar este proceso en otros proyectos

**1. Armá un brief persistente del proyecto.** En la raíz del repo,
creá un `CLAUDE.md` (o equivalente) que describa: objetivo, stack y
entorno, estructura final esperada, arquitectura de clases, bugs
conocidos del material original, plan por fases, definición de
"terminado", y cómo trabajar con el agente. Este archivo se carga al
inicio de cada sesión y le da contexto a Claude Code sin que tengas
que repetirlo. Cuando el proyecto evoluciona, actualizá el brief —
es la fuente de verdad.

**2. Escribí prompts de fase con estructura repetible.** Cada brief
de fase tiene: (a) entregables concretos numerados, (b) reglas
duras (ej: "NO mockees la base de datos", "escribir comentarios
`# FIX:` en bugs corregidos"), (c) criterios de validación
explícitos (smoke + sintética + qué valida visualmente el humano),
(d) commit propuesto con título + cuerpo, (e) regla de no-commit
hasta validación visual aprobada. La estructura repetida elimina
ambigüedad y da al agente un patrón mental claro.

**3. Establecé el ritual de validación.** Antes de cada commit,
ejecutá los tres filtros en orden: smoke test (más barato),
sintética (assertions específicas), validación visual (el humano
prueba la feature). Si algo falla en cualquier capa, se diagnostica
antes de avanzar. La regla más importante: **ningún commit sin las
tres capas pasadas**. El costo es modesto (5-10 minutos por fase),
el beneficio es que el historial nunca tiene commits "rotos" que
después haya que revertir o parchar.
