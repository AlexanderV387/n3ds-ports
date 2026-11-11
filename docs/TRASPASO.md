# Traspaso del proyecto n3ds-ports

Estado completo al **6 de noviembre de 2026**, para seguir el trabajo en otro entorno (local o una sesión nueva) sin releer conversaciones. Junta lo hecho, lo que está a medio hacer, lo pendiente, cómo se compila cada cosa y lo aprendido sobre la New 3DS y sobre portear.

Si una sesión nueva de Claude retoma el proyecto, que lea primero este archivo y el [README](../README.md).

---

## 1. Forma de trabajo (acuerdos con AlexanderV387)

- **Idioma:** en el chat, español, con explicaciones sencillas y 1 o 2 preguntas al final. En el código, comentarios, commits y documentación de cada fork: inglés. Los documentos de este repo (n3ds-ports) van en español.
- **Esperar siempre al log** antes de cambiar algo después de una prueba en consola. Si dice "ya te mando el log", no se toca nada hasta recibirlo.
- **Nunca poner `[release]` en un commit sin confirmación explícita:** ese texto publica una release en GitHub.
- **Créditos solo en los README**, con tono neutral: "dirección, diseño y pruebas en hardware: AlexanderV387; código escrito con Claude (IA)", más el motor original y sus autores.
- **Uso de IA declarado abiertamente** en los README y en Reddit (`AI disclosure: AI was used`).
- **Las pruebas se entregan numeradas**, por ejemplo `dolmexica-prueba71.3dsx`, `gzdoom-prueba03`, `uzdoom-prueba08.3dsx`.
- **Varios arreglos por entrega** cuando se pueda, en vez de uno por prueba.
- **Al comparar con el original** (MUGEN 1.0/1.1, Ikemen GO, el juego en PC), se arregla el motor, nunca el contenido (personajes, mods).
- **No tocar `pull-on-heart-prototype`** (repo ajeno al proyecto).
- **Commits** con estas dos líneas finales, sin nombres de modelo en el texto:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: <enlace de la sesión>
  ```
- **Probado en hardware real:** una New 3DS con Luma3DS 13.4 (Rosalina 2.4.3), con el Homebrew Launcher abierto desde Rosalina. Para el audio hace falta `sdmc:/3ds/dspfirm.cdc` (se vuelca desde Rosalina: Miscellaneous options → Dump DSP firmware).

---

## 2. Repositorios

| Repo | Rama de trabajo | Qué es |
|---|---|---|
| [n3ds-ports](https://github.com/AlexanderV387/n3ds-ports) | `main` | Este repo: plan, catálogo, estándar de controles, rendimiento, devlog, investigaciones, guía de instalación, herramientas de empaquetado (`tools/3ds/`) |
| [wolf4sdl-3ds](https://github.com/AlexanderV387/wolf4sdl-3ds) | `n3ds` | Wolfenstein 3D y Spear of Destiny (Wolf4SDL) |
| [bstone](https://github.com/AlexanderV387/bstone) | `n3ds` | Blake Stone: Aliens of Gold y Planet Strike |
| [crispy-doom](https://github.com/AlexanderV387/crispy-doom) | `n3ds` | Crispy Doom y Crispy Strife |
| [dsda-doom](https://github.com/AlexanderV387/dsda-doom) | `n3ds` | DSDA-Doom, más los `.cia` de Heretic y Hexen |
| [NBlood](https://github.com/AlexanderV387/NBlood) | `n3ds` | Duke Nukem 3D (EDuke32); más adelante Blood, Redneck, Shadow Warrior, Exhumed |
| [dolmexicainfinite](https://github.com/AlexanderV387/dolmexicainfinite) | `n3ds` | Motor compatible con MUGEN (Dolmexica Infinite) |
| [prism](https://github.com/AlexanderV387/prism) | `n3ds` | La librería de Dolmexica, con la capa 3DS y el simulador `n3dssim` |
| [gzdoom-3ds](https://github.com/AlexanderV387/gzdoom-3ds) | `n3ds` y `uzdoom-3ds` | Fork del port de Legend of Doom de tinaut1986. `n3ds`: GZDoom 4.7.1 general. `uzdoom-3ds`: UZDoom 4.15 con backend 100% GPU (en curso) |

### Versiones publicadas y IDs de título

| Port | Última release | `.cia` (unique ID) | Carpeta en la SD |
|---|---|---|---|
| Wolf4SDL | v1.7.0 | `wolf4sdl-all.cia` (y variantes 0xF3D50–0xF3D54) | `/3ds/wolf4sdl/wolf3d/`, `/3ds/wolf4sdl/sod/` |
| BStone | n3ds-v1.3.0 | `bstone.cia` (0xF3D55) | `/3ds/bstone/` |
| Crispy Doom / Strife | n3ds-v1.1.0 | `crispy-doom.cia`, `crispy-strife.cia` (0xF3D56, 0xF3D57) | `/3ds/crispy-doom/`, `/3ds/crispy-strife/` |
| DSDA-Doom | n3ds-dsda-doom-v1.1.0 | `dsda-doom.cia` (0xF3D58) | `/3ds/dsda-doom/` |
| Heretic | n3ds-heretic-v1.1.0 | `heretic.cia` (0xF3D59) | `/3ds/heretic/` |
| Hexen | n3ds-hexen-v1.1.0 | `hexen.cia` (0xF3D5A) | `/3ds/hexen/` |
| Duke Nukem 3D | n3ds-duke3d-v1.0.0 | `duke3d.cia` (0xF3D5B) | `/3ds/eduke32/` |
| GZDoom / UZDoom | sin release | reservado 0xF3D5C | `/3ds/gzdoom/` |
| Dolmexica (MUGEN) | sin release | `3ds/app.rsf` | `/3ds/dolmexica/` |

Cada port usa un unique ID distinto: el siguiente libre es **0xF3D5D**. La guía para jugadores (instalación, rutas, archivos originales y qué se probó) está en [`instalacion.md`](instalacion.md).

### Cómo se publica

En los forks, un commit en `n3ds` cuyo mensaje contiene `[release]` dispara el workflow de GitHub Actions (`.github/workflows/n3ds.yml` o `build.yml`). Ese workflow compila, arma el `.cia` y el `.3dsx`, y crea la release con las notas de `tools/3ds/release/.../RELEASE_NOTES.md`, `n3ds/RELEASE_NOTES.md` o `RELEASE_NOTES.md`. **Solo con confirmación del dueño.**

---

## 3. Cómo se compila cada cosa

### Requisitos generales

- **devkitPro** con `3ds-dev` (devkitARM, libctru, citro3d, citro2d) y las portlibs que pida cada port (`3ds-sdl`, `3ds-sdl_mixer`, `3ds-libvorbisidec`...). En Windows hay instalador; en Linux, `dkp-pacman`.
- **Alternativa con Docker:** la imagen `devkitpro/devkitarm` es la que usa GitHub Actions. [`tools/3ds/build-local.sh`](../tools/3ds/build-local.sh) la envuelve. En las sesiones en la nube se usó Docker porque los servidores de paquetes de devkitPro bloquean esas máquinas.
- **Para los `.cia`:** `makerom` y `bannertool`. [`tools/3ds/make-cia.sh`](../tools/3ds/make-cia.sh) arma el `.cia` siempre en modo New 3DS (804 MHz, L2, 124 MB). Los forks traen su copia en `tools/3ds/`.

### Por port

| Port | Compilar |
|---|---|
| Wolf4SDL | `make TARGET=wolf4sdl-all BUILD=build-all` (ver la matriz de variantes en `.github/workflows/build.yml`) |
| BStone | `cmake -S . -B build-3ds -DCMAKE_TOOLCHAIN_FILE=$DEVKITPRO/cmake/3DS.cmake -DCMAKE_BUILD_TYPE=Release ...` (flags completos en `.github/workflows/n3ds.yml`) |
| Crispy Doom/Strife | `sh tools/3ds/build-deps.sh`, luego `sh tools/3ds/build.sh --target crispy-doom_3dsx` y `--target crispy-strife_3dsx` |
| DSDA-Doom / Heretic / Hexen | `sh tools/3ds/build-deps.sh`, luego `sh tools/3ds/build.sh` (los tres `.cia` salen del mismo ejecutable) |
| Duke (NBlood) | `sh tools/3ds/build-deps.sh`, luego `sh tools/3ds/build.sh` |
| Dolmexica | primero prism: `make -f Makefile.3ds -j` en `prism/`; luego `make -f Makefile.3ds -j` en `dolmexicainfinite/` (busca prism en `../prism`). Sale `dolmexica.3dsx`; el `.cia`, con `3ds/make-cia.sh` |
| Simulador de prism | `make -f Makefile.n3dssim -j` en `prism/`: el código de texturas de la 3DS sobre una GPU y una memoria lineal simuladas, en Linux, con AddressSanitizer. Variables: `N3DS_SIM_SHOT=frames`, `N3DS_SIM_SHOT_DIR`, `N3DS_SIM_SHOT_LIST` (guardan imágenes PPM de los fotogramas) |
| GZDoom 4.7.1 (`gzdoom-3ds`, rama `n3ds`) | `./platform/3ds/build.sh hardware-hybrid`. Descarga y parchea SDL2, ZMusic, OpenAL Soft (NDSP), NovaGL, Freedoom y Legend of Doom. Sin `libsdl2-dev` en el host: `SDL2DIR=<sdl2 del host estático>`. Con `LOD3DS_FULL_MUSIC=1` se salta la conversión de música (ffmpeg) |
| UZDoom (`gzdoom-3ds`, rama `uzdoom-3ds`) | `platform/3ds/build.sh` (ver [su README](https://github.com/AlexanderV387/gzdoom-3ds/blob/uzdoom-3ds/platform/3ds/README.md)): herramientas del host, compilación 3DS y `.3dsx` con los datos del motor dentro |

**Pruebas de Dolmexica en PC** (desde el 10 nov. 2026, en el repo):
- `make -f Makefile.linux -j` (rápido, sin dibujar) y `make -f Makefile.sim -j` (sobre `prism/bin_n3dssim`: texturas de la 3DS simuladas, ASan, dibuja). Con g++ 13 o más nuevo, prism necesita `CXX="g++ -include cstdint"`.
- Se corren desde una carpeta que tenga `assets/` (datos de Dolmexica 1.8 y los personajes en `assets/chars/<nombre>/<nombre>.def`). En PC las rutas del `.def` deben ir con `/`; `DOLMEXICA_ALLOW_MINUS=1` acepta archivos con `-` (Galactus, Onslaught).
- Pruebas útiles (`--gtest_filter=`): `CrashTest.CharacterCrashTest` (con `DOLMEXICA_ASSET_FILTER`), `EntityCensusTest.MirrorMatchCensus`, `ContinueHelperTest.HelpersAfterContinue` (árbol de helpers antes y después del "Continue?"), `ContinueHelperTest.MissingHelpers` (helpers que faltan, `DOLMEXICA_WATCH_IDS`), `ContinueHelperTest.JumpedOver` (cruzar al rival; con `DOLMEXICA_VERSUS=1` y `PRISM_LINUX_SCRIPT="360:right;420:up,right;..."` se pulsan botones del jugador 1).
- **MUGEN 1.1 de referencia en Linux:** Wine + `Xvfb :99` + `dolmexicainfinite/tools/mugen-shots.sh` (capturas de una pelea; con xdotool se controlan los dos jugadores). El código de Ikemen GO (`src/char.go`) se baja de raw.githubusercontent.com para citar reglas.

---

## 4. Estado de cada proyecto

### Terminados y publicados

| Proyecto | Estado | Pendientes |
|---|---|---|
| **Wolf4SDL** | v1.7.0: 60 FPS a 800x240, doble stick, giro táctil, HUD y mapa con zoom abajo, teclado y armas táctiles, un `.cia` con selector de juegos y misiones de Spear | Auto Fire (opción); barra de estado arriba (opción clásica); probar shareware, demo de SoD y misiones 2 y 3 |
| **BStone** | n3ds-v1.3.0: 60 FPS a 800x240, HUD y mapa abajo, vista 3D a pantalla completa | Volver a poner la barra arriba como opción (se quitó en 1.2.0); Auto Fire; probar Aliens of Gold completo |
| **Crispy Doom / Strife** | n3ds-v1.1.0: 60 FPS (mínimo 57; Freedoom 54), selector de juego y mods, Strife con voces e inventario táctil | Quitar la posición "en medio" de la barra de estado; dibujo repartido en dos núcleos (tarea 9); barra arriba como opción |
| **DSDA-Doom / Heretic / Hexen** | v1.1.0: GPU (capa `pgl`, OpenGL sobre citro3d) a 800x240, selector de campañas y complementos, remaster de Heretic y Hexen | Versión **1.2**, con lo pedido en Reddit: giroscopio, selector gráfico con letra grande, botones avanzados (doble toque, mantener, shift), aviso de carpeta `mods/` vacía, aviso de GZDoom más claro, ocultar el inventario de Heretic/Hexen en Doom. Además: inventario táctil en Heretic y Hexen; pulir la GPU (luz, cielo, tinte, transición); el fallo de profundidad con niebla a 800x240 (tarea 41); nodebuilder para mapas sin nodes (ZDBSP); optimizar las hordas (~10 FPS en E1M9 de Faith Renewed y MAP07 de Vestiges) |
| **Duke Nukem 3D** | n3ds-duke3d-v1.0.0: software o GPU (Polymost sobre `pgl`), barra, mapa, teclado y armas abajo. Solo probado con el shareware 1.3d | **Guardar partida es muy lento** (sin investigar); estándar FPS completo (tarea 32); presentación propia en el núcleo 1 (tarea 30); probar el juego completo, Atomic y World Tour |

### Estándar común para los FPS, pendiente en todos

En [`controles-fps.md`](controles-fps.md):
- apuntar con el giroscopio (opción);
- botones avanzados;
- selector gráfico;
- modo 800x240 como estándar en todos;
- barra de estado arriba como opción clásica.

### Motor compatible con MUGEN (Dolmexica Infinite): a medio camino

- **Última prueba entregada: `dolmexica-prueba79.3dsx`** (11 nov. 2026, dolmexicainfinite `eb0d218`, prism `1d749be`; md5 del `.elf.xz` `d2371bd204aacab2f6cfc9d9b438d0ef`). La 78 más la pantalla ancha revisada pantalla por pantalla (título, selección, intro, VS, pelea, KO, continuar; prueba `ScreenTour` con el simulador y su margen de 3DS): el contador de combo ya no se ve en los bordes cuando espera fuera de la pantalla 4:3, y las intros/finales con imágenes del tamaño de la pantalla se estiran a todo el ancho. Fundidos, oscurecido de súper, pausa, resultados y fondos de menús ya cubrían todo el ancho.
- Prueba 78 (11 nov. 2026, dolmexicainfinite `6996f59`, prism `572912d`; md5 del `.elf.xz` `6f96971e6a96c743737e4f924e27eb4e`). `EnvColor` cubre también los lados de la pantalla ancha (el oscurecido de las hipers de Felicia dejaba ver el escenario); la selección de personajes ya no busca un escenario "random" por cada personaje ni lee las paletas de un SFF v2 una por una (los retratos de Kitana, Chun-Li Neo, Psylocke y Chun-Li costaban ~3 s); `log.txt` se vacía al arrancar. Comparado con MUGEN 1.1 sin cambios: la IA de New Kyouki (repite su súper 100001 contra Apocalypse también allí) y el punto ciego de Galactus. Pendiente propuesto: leer de la SD las pistas largas dentro de los `.snd` (Kyouki y Onslaught: ~20 MB de memoria lineal) y repartir mejor el heap entre los dos luchadores (Kyouki contra Onslaught: 55-62 % de cuadros dibujados, 7000 sprites releídos de la SD).
- Prueba 77 (11 nov. 2026, dolmexicainfinite `3fefe4a`, prism `27df0a0`; md5 del `.elf.xz` `68879be35f1f2003265dee936f989000`). Cajas de colisión de los `.air` como MUGEN: un nuevo `ClsnNDefault` reemplaza las cajas por defecto anteriores (antes se sumaban). Arregla el rayo de la mano de Galactus (Kung Fu Man recibe 180 y queda tumbado, MUGEN 1.1: 192) y cambia 315 animaciones de 11 personajes (Onslaught 133, Kitana 110, Lei-lei 21, Psylocke 17…). Siguiente fase: escenarios.
- Prueba 76 (10 nov. 2026, dolmexicainfinite `3fefe4a`, prism `e078393`; md5 del `.elf.xz` `518eac94d67ed2400fe857d20aa2e864`). Daño como MUGEN: un golpe pone el estado de recibir una sola vez, el daño a un helper es suyo, `LifeAdd` redondeado; comprobado con MUGEN 1.1.
- Prueba 75 (10 nov. 2026, dolmexicainfinite `b66a370`, prism `e078393`; md5 del `.elf.xz` `cecc9e1f3860318bb54250fe16aa592e`). Galactus: el suelo igual en todas las rondas y el KO delante de él; el brazo sigue al puño (la muñeca ya no desaparece; el rayo sale de la mano). La causa del brazo afecta a 10 personajes (`Redirección, AnimElem = n, op t` se leía mal). Apocalypse desarmándose al cruzarlo con Wonder Woman: igual en MUGEN 1.1.
- Prueba 74 (10 nov. 2026, dolmexicainfinite `5725fc9`, prism `f6e05af`; md5 del `.elf.xz` `49d28d8687d821eb88b37cd8df94e0c1`). La 73 más `MoveContact` como MUGEN: los misiles de Apocalypse se quedaban hasta el fin de la ronda.
- Prueba 73 (10 nov. 2026, dolmexicainfinite `3627684`, prism `f6e05af`; md5 del `.elf.xz` `b4ebe24135d4fa5dd612123e7ca51294`). Responde al informe de la 72: el cierre por memoria tras varios combates (las tablas de paletas propias y de texturas devuelven su sitio entre combates), los botones que se perdían justo después de agacharse, levantarse o empezar a andar (cada personaje corre sus estados una vez por tic, como Ikemen/MUGEN), el "bong" al dar o recibir golpes (era el sonido de subir de nivel la barra de energía: los helpers tenían energía propia; en MUGEN es la del jugador), dos sonidos del mismo tic que se cortaban en la 3DS (posible causa de que Felicia no grite al perder) y el juggle por atacante. Detalle en [`dolmexica-auditoria-mugen.md`](dolmexica-auditoria-mugen.md).
- Prueba 72 (10 nov. 2026, dolmexicainfinite `818d814`, prism `5e79918`; md5 del `.elf.xz` `a83df306b2e06438ba8a847efbdc4afc`): primera tanda de la auditoría frente a MUGEN 1.1 (empuje, andar, esquina, agarres, IDs, `HitBy`/`NotHitBy`, Mileena, Lei-lei). Informe: Felicia lenta, misiles de Apocalypse, "bong", Galactus (suelo, muñeca, rayo, se le puede cruzar), esferas de Onslaught, daño, fondos azules de MvC recortados en pantalla ancha, cierre por memoria.
- **Funciona:** carga personajes y escenarios desde `sdmc:/3ds/dolmexica/` (autodetección en `chars/`), menú de pausa con START, `compat-log.txt` por personaje, vista 4:3 automática para jefes grandes. Además, muchas reglas de MUGEN/Ikemen implementadas y verificadas contra MUGEN 1.0/1.1:
  - helpers sin animación hasta que su estado la pone;
  - comparación de strings sin mayúsculas;
  - temporizadores de NotHitBy/HitBy;
  - `fall.defence_up`;
  - Trans de un tic;
  - límites del escenario en pantalla ancha;
  - giro automático como Ikemen;
  - prioridades de sprite de más de ±10;
  - BindToParent/Root con tiempo -1;
  - proyectiles de helpers destruidos;
  - la bandera de guardia;
  - **el empuje entre personajes (prueba 72):** se empujan si sus cajas de tamaño se solapan también en altura (cada una con su `height`) y sus Clsn2 se tocan, como `pushDetection` de Ikemen. Un personaje con helpers pegados (`BindToParent`) ya empuja; solo un agarre (el rival atado) lo apaga. Antes, Kung Fu Man le saltaba por encima a Apocalypse (`height = 300`), Apocalypse se giraba al empezar a caminar (regla no documentada de MUGEN, ver `changeStateEx` de Ikemen) y su torso (el propio personaje, animación 0) se reflejaba mientras sus partes (helpers sin `facing`) no: "se desarmaba". Comprobado con `JumpedOver` y en MUGEN 1.1 con Wine (allí Kung Fu Man no logra pasar).
- **Pendientes concretos:**
  - **Galactus:** la mano desaparece después de "continuar" (arcade). No se reproduce en PC ni en el simulador con Kung Fu Man (el puño, helper 4, se vuelve a crear y se dibuja). El dueño cree que jugaba con New Kyouki: probar con él (memoria de texturas).
  - **Onslaught:** los 4 orbes eléctricos no conectan.
  - **Abyss se ve invisible:** el `abyss.sff` de la SD del dueño está cortado (786 KB de 9.314.266). Hay que volver a copiarlo. El motor ya avisa de SFF cortados.
  - **Memoria de texturas** para personajes grandes (CvS, POTS, HD) (tarea 50).
  - **Música** MP3/OGG y modos solo CPU (tarea 44).
  - **Selección de personajes en la pantalla de abajo** (idea, tarea 51).
- **Verificado que no son fallos** (MUGEN se comporta igual):
  - la muñeca de Galactus sale de pantalla;
  - la ultimate de Kyouki no conecta contra Galactus;
  - Apocalypse solo recibe daño en la cabeza;
  - el daño de Onslaught es el del arcade;
  - Galactus resiste mucho (life 4000, defence 300);
  - dos "Watchers" de Galactus a la vez (su estado 5900 crea uno y su intro 190 otro);
  - Poison Ivy entra en estados que no tiene (230, 430, 1400) y pide animaciones que no existen (155, 455, 701, 723);
  - las bolas de cañón de Apocalypse (helpers 700/701) se quedan flotando sobre un rival tumbado (`hitflag = MAF` y `var(21)` nunca vuelve a 0);
  - Onslaught y Wonder Woman (triple salto) sí pueden pasar por encima de Apocalypse: Onslaught no tiene Clsn2 al caminar y Wonder Woman va más alta que la Clsn2 de él.
- **Para publicar un avance en Reddit:** Harley Quinn (de Ax, del "Batman 2021 fullgame") contra Poison Ivy (de Mr.Giang), en el escenario por defecto de MUGEN (Elecbyte). El borrador del post y la respuesta para el bot están en la conversación anterior; el autor de Dolmexica es Josh Tari (CaptainDreamcast), licencia MIT.

### Motor ZDoom: GZDoom 4.7.1 y UZDoom, en curso (lo último en lo que se trabajaba)

**Decisión del dueño: ir por el camino difícil**, UZDoom con renderizado 100% GPU. La meta mínima es un motor 4.13 o más nuevo, para correr **H-Doom**, que necesita `MissileChanceMult` (aparece en 4.14). Investigación completa en [`investigacion-zdoom.md`](investigacion-zdoom.md).

**Rama `n3ds` de gzdoom-3ds** (GZDoom 4.7.1, a partir de tinaut1986/legend-of-doom-3ds):
- Carga el IWAD desde `/3ds/gzdoom/` (con `iwad.txt` para elegir) y todos los mods de `/3ds/gzdoom/mods/`.
- Restaurados los actores de Heretic, Hexen y Strife, que Legend of Doom quitaba para la Old 3DS.
- Los datos del motor van dentro del `.3dsx`.
- **En consola llegó a jugar MAP01 con `doom2.wad`.**
- H-Doom no carga: pide GZDoom 4.13+.
- Todavía tiene la pantalla de abajo, los controles y la animación de carga (Trifuerza) de Legend of Doom, y el icono de Doomguy. El `CLAUDE.md` es el de tinaut1986: hay que reemplazarlo.

**Rama `uzdoom-3ds`** (UZDoom de noviembre de 2026, que prepara la 4.15, con el historial completo de UZDoom):
- Capa de plataforma 3DS propia y un **backend de video citro3d** para el hwrenderer de UZDoom: el "100% GPU". Detalle de cambios en [`platform/3ds/README.md`](https://github.com/AlexanderV387/gzdoom-3ds/blob/uzdoom-3ds/platform/3ds/README.md).
- **Avance en consola, prueba a prueba:**

| Prueba | Resultado | Arreglo |
|---|---|---|
| 1 | No encontraba el IWAD | `sdmc:/` y `romfs:/` cuentan como rutas completas |
| 2 a 4 | Sin memoria en `Texman.Init` | Diagnóstico de memoria en el log |
| 5 | Fuentes TrueType chinas, japonesas y coreanas: atlas de 16 MB | Se saltan en la 3DS y se quitan del paquete |
| 6 | Fuentes hex (Unifont, 57.000 glifos): ~45 MB | Solo latino, griego, cirílico y símbolos |
| 7 | 12 errores de ZScript: los `enum` ocupan 1 byte en ARM | `: int` en esos `enum` |
| 8 | **"Init complete"**, el backend se inicializa, y luego se agota la memoria al dibujar el título: la lista 2D no se vaciaba | `Update()` dibuja y vacía el 2D; los buffers y texturas se liberan un fotograma después |
| 8 (resultado) | El dueño dijo "no funcionó todavía", **sin mandar log** | — |

- **Lo inmediato:**
  1. Pedir o leer el `log.txt` de la prueba 8 y una foto de la pantalla de arriba.
  2. Lograr la primera imagen: orientación (inclinación de 90°), profundidad y colores se escribieron sin verlos.
  3. Después: líneas del automapa; niebla y luz por distancia (con la tabla de niebla del PICA, como en DSDA); portales (rango de profundidad); sonido (traer OpenAL Soft/NDSP de la rama `n3ds`); controles 3DS y pantalla de abajo; empaquetado `.cia`.
  4. Revisar el aviso de UZDoom sobre "artefactos visuales en 32 bits" ([foro](https://forum.zdoom.org/viewtopic.php?f=7&t=75673)) cuando el mundo se dibuje.
- **Memoria medida:** heap de 72 MB y memoria lineal de 32 MB en un `.3dsx`. Después de ZScript quedan ~49 MB en uso. ZScript compila en ~6,6 s.
- **Para H-Doom después:** la carga es muy lenta (en GZDoom 4.7.1 tardó unos 2 min 45 s solo en el gestor de texturas). Convendrá un índice guardado la primera vez.
- **Alternativa si UZDoom se atasca:** LZDoom 4.14 conserva el renderizador por CPU (softpoly) que usa la base de tinaut1986. Lo aprendido en UZDoom sirve igual.

---

## 5. Roadmap (orden acordado)

1. ~~Crispy Doom~~ ✔ · 2. ~~DSDA-Doom, Heretic, Hexen~~ ✔ · 3. ~~Duke Nukem 3D~~ ✔
4. **MUGEN** (Dolmexica): en curso.
5. **Plugin de Luma3DS para el C-stick:** Kid Icarus: Uprising primero (el C-stick imita el arrastre del lápiz), luego Ocarina of Time 3D. Un solo plugin con un archivo de configuración por juego. Para juegos de DS haría falta parchear TWL_FIRM (ver TWPatch): investigación aparte, con Metroid Prime Hunters como meta.
6. **Blood, Redneck Rampage, Shadow Warrior, Exhumed** (repo NBlood): heredan casi todo de Duke.
7. **Motor de beat 'em ups** (probablemente OpenBOR), con Final Fight Ladies como juego de prueba. Antes, confirmar en qué motor está hecho y si ya existe un OpenBOR para 3DS. Se publica solo el motor.
8. **Serious Sam** (Serious Engine 1, GPL desde 2016).
9. **Motor de la familia ZDoom**, que se adelantó y está en curso: H-Doom, Brutal Doom, Global Friendly Marines, Harmony, Chex Quest 3. Postal 2 queda descartado (Unreal Engine 2 cerrado); Postal 1 está liberado, como alternativa.
10. **PS1 con la GPU** (renderizador citro3d para PCSX ReARMed).
11. **Arcades 3D basados en PS1** (Namco System 11, Capcom ZN).
12. **N64** (N64Recomp, GoldenEye, Donkey Kong 64).
13. **Largo plazo:** Return to Castle Wolfenstein, Enemy Territory, Sonic Robo Blast 2 versión 2.2 (ya hay un port viejo de la 2.1: derrekr/srb2_3ds).

**Ideas anotadas:**
- **Budokai Tenkaichi 3:** otra persona mostró un port desde la decompilación, a 20–30 FPS y con el código privado. Ver si lo publica antes de empezar algo propio.
- **Postal 1.**
- **Pruebas con variantes como norma** en todos los ports (tarea 40).

---

## 6. Comunidad (Reddit r/3dshomebrew)

- Etiqueta **"New Homebrew"**, nunca "AI FREE". El AutoModerator pide en cada post una respuesta con: participación, experiencia ("software engineering student, beginner in game programming and game engine architecture") y uso de IA. Se responde en cada post.
- Orden de publicación acordado: Wolfenstein 3D, Blake Stone, Strife, DSDA-Doom, Heretic, Hexen y Duke, uno cada 3–4 días. Luego, quizá el avance de MUGEN.
- **Comentarios recibidos (DSDA-Doom, cosmos10040):**
  - pidió giroscopio, selector gráfico, LZDoom/Zandronum y botones avanzados;
  - no encontraba la carpeta `mods/`;
  - el mod Global Friendly Marines es de GZDoom (por eso salió el aviso);
  - dijo que corre mejor y con más luz que el "Doom Launcher".
  - Todo quedó anotado para la 1.2.
- Preguntaron por un "Sonic the Hedgehog 3D": era SRB2, motor derivado de Doom, no Build. Y por la Old 3DS: no está planeada.

---

## 7. Lo aprendido sobre la New 3DS

### CPU y memoria
- **ARM11 MPCore.** La New 3DS corre a 804 MHz con caché L2 (`osSetSpeedupEnable(true)`). El núcleo 0 es de la app; el núcleo 2 se puede usar en la New 3DS para un hilo de trabajo; el 1 lo comparte el sistema.
- **Modo de 124 MB:** el `.cia` lo pide en su RSF. Un `.3dsx` abierto desde Rosalina en una New 3DS también recibió 124 MB.
- **Cómo reparte libctru por defecto** (`__system_allocateHeaps`): si sobran más de 24 MB, la memoria lineal se lleva 32 MB y el heap lo demás. Con 124 MB: **72 MB de heap y 32 MB lineales**. En el modo de 64 MB, el heap queda en ~28 MB. Se puede ajustar con `__ctru_heap_size` y `__ctru_linear_heap_size`, o con un crt0 propio, como hizo tinaut1986.
- **La memoria lineal** es la única que lee la GPU: vértices, texturas y buffers de comandos. VRAM: 6 MB.
- **La fragmentación del heap tumba juegos aunque haya memoria libre:** en Dolmexica hubo 46 MB libres sin un bloque de 3 MB. Ayudan las arenas o pilas propias, las reservas al inicio, y liberar antes de volver a pedir.

### GPU (PICA200)
- **Shaders solo de vértices** (lenguaje de picasso, `.v.pica`). Los fragmentos usan **6 etapas fijas de combinadores (TEV)**, con prueba de alfa, mezcla, stencil, profundidad y **niebla por tabla**: sirve para imitar la luz por distancia del software de Doom.
- **Texturas** de lados potencia de 2 entre 8 y 1024, en baldosas de 8x8 en orden Morton. La fila 0 de memoria es t=0. Si el original no es potencia de 2, se reescala; así la repetición sigue funcionando.
- **Índices de 16 bits como máximo:** los de 32 bits hay que convertirlos en cada dibujo, con base en el índice mínimo. No dibuja líneas ni puntos: hay que convertirlos en quads.
- **La pantalla de arriba es un framebuffer de 240x400 girado 90°.** La matriz de proyección lleva la inclinación (como `Mtx_OrthoTilt` de citro3d: x' = y, y' = −x) y la profundidad va en [−w, 0]. El viewport y el scissor de OpenGL (400x240, origen abajo a la izquierda) se traducen así: `C3D_SetViewport(y, 400−x−w, h, w)`.
- **Modo ancho de 800x240** (`gfxSetWide`): es la resolución estándar del proyecto en la pantalla de arriba.
- **La GPU lee los datos un fotograma tarde:** lo que se libera durante un fotograma debe liberarse al empezar el siguiente. `C3D_FRAME_SYNCDRAW` espera al fotograma anterior.
- **Limpiar la caché** (`GSPGPU_FlushDataCache`, `C3D_TexFlush`) antes de que la GPU lea lo que escribió la CPU.

### Sistema y SD
- **La SD es lenta:** escribir el log línea a línea cuesta. Conviene usar un buffer y cerrarlo bien, o volcar solo cuando hay error. Duke tarda mucho en guardar partida.
- **Las rutas son `sdmc:/...` y `romfs:/...`**: los motores de PC creen que una ruta completa empieza con `/`. Hay que enseñarles estas dos.
- **El `.3dsx` puede llevar su propia RomFS** (`3dsxtool --romfs`): así el `.3dsx` y el `.cia` son un solo archivo con los datos del motor.
- **No hay `dlopen`, `mmap`, terminal (`termios`), `uname` ni usuarios (`getpwuid`).** Se ponen versiones vacías o alternativas.
- **El audio** con NDSP necesita `dspfirm.cdc`. OpenAL Soft tiene un backend NDSP (en la rama `n3ds` de gzdoom-3ds).
- **Los errores** se muestran con el diálogo del sistema (`errorInit`/`errorText`/`errorDisp`) y se escriben en un `fatal.log`.
- **Los volcados de Luma** (`/luma/dumps/arm11/*.dmp`) traen la dirección del cierre. `arm-none-eabi-addr2line -f -C -e juego.elf <direcciones>` la traduce a funciones: **guardar el `.elf` de cada prueba**.

### Compilador (devkitARM)
- **`int32_t` es `long`, no `int`:** rompe sobrecargas, serializadores y la VM de ZScript en motores de PC. La solución global: `-U__INT32_TYPE__ -D__INT32_TYPE__=int` (y lo mismo para `UINT32` y `LEAST32`), como **opciones** (cada `-U` antes de su `-D`), no como definiciones. libctru, citro3d y SDL son C y no se ven afectados.
- **Los `enum` ocupan lo mínimo** (1 byte si sus valores caben): es lo normal en ARM EABI para bare-metal. No usar `-fno-short-enums` en todo, porque cambia las estructuras de libctru y citro3d. Mejor `enum X : int` en los que se leen como `int`: la VM, los serializadores, `(int&)`.
- **newlib esconde `strdup`, `strcasecmp` y otras** sin `_GNU_SOURCE` o las extensiones GNU (`-std=gnu++20`).
- **ARMv6K no tiene** CRC32 de ARMv8, NEON ni `sys/auxv.h`: desactivar esas rutas en librerías como lzma.

---

## 8. Lo aprendido haciendo ports

- **Medir en la consola, no en emuladores.** Cada prueba numerada lleva un log con etapas, la memoria en uso y los tiempos. Pedir siempre el log antes de tocar nada.
- **Instrumentar en vez de adivinar.** Cuando falla la memoria, anotar los pedidos grandes con la traza de quién los hizo (`_Unwind_Backtrace` + addr2line) y la memoria en uso por línea del log. Así salieron, en dos pruebas, las fuentes TrueType, las fuentes hex y la lista 2D.
- **Comparar con una referencia:** MUGEN 1.0/1.1 e Ikemen GO para Dolmexica, el renderizado por software para la GPU de DSDA, el juego en PC para los demás. Si el original hace lo mismo, no es un fallo.
- **Simulador en PC cuando se puede:** el `n3dssim` de prism encontró en PC fallos de memoria del código de texturas de la 3DS, con AddressSanitizer, y genera capturas de fotogramas.
- **Variantes:** mandar varias versiones de un mismo arreglo en una prueba ahorra idas y vueltas (sobre todo en sensibilidad y rendimiento).
- **Las capas de traducción sirven para varios motores:** `pgl` (OpenGL sobre citro3d) se escribió para DSDA y la reusó Duke (Polymost). El backend citro3d de UZDoom sigue la misma idea, pero para el hwrenderer de GZDoom.
- **Los motores de PC traen cosas pensadas para escritorio** que en la 3DS se comen la memoria: buffers de 64 MB, fuentes de todos los idiomas, lanzadores con ventanas, depuradores y librerías como abseil. Hay que buscarlas y recortarlas solo en la 3DS (`#ifdef __3DS__`), sin cambiar el comportamiento en PC.
- **60 FPS:**
  - presentar sin doble espera (el arreglo de Wolf4SDL);
  - dibujar en otro núcleo cuando el motor lo permite;
  - en los mapas con hordas, el límite suele ser la lógica, no el dibujo.
- **Estándar de cada port:** C-stick para la cámara, modo New 3DS, 60 FPS como meta, pantalla de abajo con uso real (HUD, mapa, botones de armas, teclado) y `.cia` con icono y banner. Detalle en [`controles-fps.md`](controles-fps.md).
- **Licencias:** cada port conserva la de su motor (GPL en casi todos; Dolmexica es MIT). Nunca se distribuyen datos de juegos.
- **Antes de empezar un port, buscar si ya existe uno:** Legend of Doom 3DS (EstebanPdN) y su fork (tinaut1986) ahorraron semanas en GZDoom. Si alguien ya lo hizo, conviene construir encima, acreditarlo, y considerar colaborar.

---

## 9. Lista de tareas abiertas (resumen)

| # | Tarea | Estado |
|---|---|---|
| 63 | UZDoom 4.15 con backend 100% GPU: primera imagen (prueba 8) | **en curso, lo último** |
| 62 | GZDoom 4.7.1: pantalla de abajo, controles, icono y carga propios | en curso |
| 43, 50, 52 | MUGEN: capa 3DS de prism, memoria de texturas, pendientes de pruebas | en curso |
| 44 | MUGEN: música y modos solo CPU | pendiente |
| 51 | MUGEN: selección de personajes en la pantalla de abajo | idea |
| 61 | Todos los FPS: giroscopio, selector gráfico, botones avanzados (DSDA 1.2 primero) | pendiente |
| 17, 41 | DSDA GPU: pulir; profundidad con niebla a 800x240 | en curso |
| 19, 25, 27 | DSDA: nodebuilder; dibujo en otro núcleo; inventario táctil en Heretic/Hexen | pendiente |
| 28, 30, 32, 60 | Duke: presentación propia, estándar FPS, guardado lento | pendiente |
| 9 | Crispy Doom: dibujo en dos núcleos | pendiente |
| 15, 26, 39, 40 | Auto Fire; barra arriba como opción; 800x240 en todos; pruebas con variantes como norma | pendiente |
| 21 | Idea: Budokai Tenkaichi 3 | en espera |

---

## 10. Para retomar en local

1. Instalar devkitPro (o Docker con `devkitpro/devkitarm`), git y CMake.
2. Clonar los repos de la sección 2 y cambiar a su rama de trabajo.
3. Para UZDoom: `git clone https://github.com/AlexanderV387/gzdoom-3ds`, `git checkout uzdoom-3ds` y `platform/3ds/build.sh`.
4. Abrir Claude Code dentro del repo y pedirle que lea este archivo y el README de `platform/3ds/`. Así no hace falta repetir el contexto.
5. **Ahorro de tokens:** compilar y probar sin la IA, y llamarla con el log y la foto ya listos, una tarea concreta por sesión.

---

## 11. Para la IA que retome el proyecto: dónde quedó y cómo se trabajaba

Esta sección es para la próxima IA (Catequilla u otra). Junta el punto exacto donde quedó el trabajo con Claude, la metodología que funcionó, los prompts para arrancar y lo que hay que hacer primero.

> **Actualización 10 nov. 2026:** UZDoom siguió con Catequilla hasta la prueba 24. El estado vigente está en `platform/3ds/STATUS.md` de la rama `uzdoom-3ds-test25` de gzdoom-3ds, y la forma de trabajar con Catequilla en [`catequilla/`](catequilla/) y [`catequilla-auditoria.md`](catequilla-auditoria.md). Lo de abajo describe el punto del 6 de noviembre.

### 11.1 Punto exacto donde quedó (6 de noviembre de 2026)

| Repo | Rama | Último commit | Qué hay ahí |
|---|---|---|---|
| gzdoom-3ds | `uzdoom-3ds` | `50bf5d04a` "3DS: build script and notes" (antes: `5511d6bb6`, el arreglo de la prueba 8) | UZDoom con backend citro3d. **Aquí se estaba trabajando.** |
| gzdoom-3ds | `n3ds` | `8c46f24c4` "Engine data inside the 3DSX..." | GZDoom 4.7.1; jugó MAP01 de Doom II en consola |
| dolmexicainfinite | `n3ds` | `6d04d18` "Auto-turn as MUGEN; sprite priorities past 10..." | MUGEN; es la prueba 71 |
| prism | `n3ds` | `ac46ada` "3DS simulation: pictures of chosen frames" | Librería de Dolmexica y simulador |
| n3ds-ports | `main` | este traspaso | Documentación |

**La tarea en curso:** UZDoom, prueba 8 (`uzdoom-prueba08.3dsx`). Se esperaba ver por primera vez la pantalla de título dibujada por la GPU. El dueño dijo "no funcionó todavía", sin decir si se cerró o quedó en negro, y **no llegó el log**. Lo primero es pedir:

1. `sdmc:/3ds/gzdoom/log.txt` (y `fatal.log` si existe);
2. una foto de las dos pantallas;
3. si hay volcado de Luma (`/luma/dumps/arm11/`), el `.dmp` más reciente.

**El `.elf` de la prueba 8** (`uzdoom-prueba08.elf`, md5 `01872fd02b49cbc65ba9c764ac6c18fd`) se le entregó al dueño comprimido (`uzdoom-prueba08.elf.xz`), porque el entorno en la nube donde se compiló se pierde. Sin ese archivo no se pueden traducir las direcciones del log o del volcado de la prueba 8. Si se perdió: recompilar el mismo commit no garantiza las mismas direcciones, así que conviene hacer una prueba 9 con más diagnóstico (11.5) en lugar de insistir con la 8.

### 11.2 El ciclo de trabajo que funcionó

1. **El dueño prueba en la consola** y avisa: "salió esto, ya te mando el log". **Desde ese momento no se toca nada** hasta que llega el log, aunque la foto ya parezca explicar el fallo.
2. **Leer el log completo**, no solo el final:
   - las últimas líneas dicen dónde se paró;
   - la columna de memoria (cada línea empieza con `[KB en uso]`) dice si se estaba agotando;
   - las líneas de reservas grandes traen la traza de quién las pidió.
3. **Encontrar la causa con pruebas, no con intuición:**
   - `addr2line` sobre el `.elf` de esa misma prueba;
   - buscar en el código del motor el mensaje del log;
   - comparar con la referencia: el motor en PC, MUGEN 1.0/1.1, el render por software.

   Antes de cambiar nada, decir la hipótesis y la evidencia.
4. **Arreglar el motor, nunca el contenido.**
   - Cada cambio va protegido para la 3DS (`#ifdef __3DS__` o en `platform/3ds/`), para que en PC no cambie nada.
   - **Varios arreglos por prueba.**
   - **Agregar diagnóstico para el siguiente fallo probable**, para que, si algo falla, el próximo log ya diga por qué. Así salieron las fuentes TrueType, las hex y la lista 2D en una prueba cada una.
5. **Compilar y numerar:**
   - `<port>-pruebaNN.3dsx` (solo el 3dsx cuando los datos van en la RomFS: no hace falta mandar un zip);
   - **guardar `<port>-pruebaNN.elf` fuera del entorno temporal.**
6. **Explicar al dueño en español sencillo:**
   - qué falló;
   - qué se cambió;
   - qué tiene que mirar en la prueba;
   - y terminar con 1 o 2 preguntas.
7. **Commit y push** a la rama de trabajo:
   - mensaje en inglés con las líneas de atribución;
   - la documentación se actualiza en el mismo cambio (README de `platform/3ds/`, este traspaso);
   - **nunca `[release]` sin que el dueño lo confirme.**

### 11.3 Prompts para arrancar con la nueva IA

**Al empezar una sesión:**
> Lee `n3ds-ports/docs/TRASPASO.md` (todo, en especial la sección 11) y `gzdoom-3ds/platform/3ds/README.md` en la rama `uzdoom-3ds`. Háblame en español y escribe el código y los commits en inglés. No cambies nada después de una prueba hasta que te mande el log. Dime en qué punto estamos y qué me vas a pedir primero.

**Al reportar una prueba:**
> Prueba NN de <port>. Pasó esto: <qué se ve, en qué momento, si se cerró o quedó congelado>. Adjunto `log.txt`, `fatal.log` (si hay), foto de las dos pantallas y el `.dmp` de Luma (si hay). Busca la causa con el log antes de proponer cambios; si necesitas traducir direcciones usa el `.elf` de esa prueba.

**Al pedir algo nuevo:**
> Quiero <función>. Antes de programar, dime cómo lo hacen el motor original o los otros ports del proyecto, qué archivos tocarías y cómo lo voy a probar en la consola.

**Al cerrar una sesión:**
> Actualiza `docs/TRASPASO.md` (estado, la tabla de pruebas, lo pendiente) y el README del port, haz commit y push. Dime qué prueba me toca hacer y qué tengo que mandarte.

### 11.4 Cómo leer los logs de UZDoom

- **`log.txt`:** cada línea empieza con la memoria del heap en uso, en KB, por ejemplo `[48933] ...`. El heap es de 72 MB (~73.700 KB): si la cifra se acerca a eso, el fallo es de memoria.
- **Líneas `C3D: ...`:** son del backend.
  - `C3D: backend ready, N KB of linear memory free`: la GPU se inicializó.
  - `C3D: lines and points are not drawn yet`: normal por ahora.
  - `C3D: no memory for a WxH texture`: falta memoria lineal.
- **Reservas de 1 MB o más:** salen con su tamaño y una lista de direcciones (las llamadas). Las reservas que fallan salen siempre. Se traducen así:
  ```sh
  arm-none-eabi-addr2line -f -C -e uzdoom-pruebaNN.elf 0x00123456 0x00234567 ...
  ```
- **`Init complete`:** el motor terminó de arrancar. Lo que pase después es el primer fotograma y el bucle del juego.
- **`fatal.log`:** el texto del error fatal, el mismo que mostró el diálogo del sistema.
- **Volcado de Luma (`.dmp`):** trae el PC (dónde se cerró) y el LR (desde dónde se llamó). Se traducen con el mismo `addr2line`.

### 11.5 Plan para la prueba 9 de UZDoom: lograr la primera imagen

**Paso 0, con el log de la prueba 8 en la mano:** decidir en qué caso estamos.

| Lo que muestra el log o la consola | Qué hacer |
|---|---|
| Se cierra con error o volcado | `addr2line` con el `.elf` de la prueba 8. Seguir la traza |
| La memoria sube sin parar en cada línea | Algo sigue creciendo por fotograma: mirar las reservas grandes y sus llamadas |
| No se cierra, pantalla de arriba negra | Ver "Pantalla negra" abajo |
| Se ve algo, pero girado, en espejo o con colores cambiados | Ver "Imagen rara" abajo |

**Pantalla negra.** Separar las dos mitades del camino con diagnóstico en la prueba 9:

1. **¿Funciona la presentación?** En `C3DFrameBuffer::ScreenBegin` (`c3d_framebuffer.cpp`), limpiar con magenta (`0xff00ffff`) en lugar de negro (`0x000000ff`).
   - Si la pantalla sale magenta, la salida a la pantalla funciona y el problema está en los dibujos.
   - Si sigue negra, el problema está en `C3D_RenderTargetSetOutput` o `C3D_FrameEnd`, o el bucle nunca llama a `Update()`.
2. **¿Llegan los dibujos?** Durante los 3 primeros fotogramas, escribir en el log:
   - cuántas veces se llamó a `Update()`;
   - cuántos `Draw`/`DrawIndexed` hubo y **cuántos salieron antes de dibujar, y por qué**: sin vertex buffer, `attrIndex[0] < 0`, `hi - lo > 0xffff` o el anillo de índices lleno (`c3d_renderstate.cpp`, `DrawIndexed`);
   - los argumentos de `SetViewport`;
   - las 4 filas de la matriz `mvp` del primer dibujo;
   - **la posición del primer vértice transformada en la CPU.** Tiene que quedar con x e y entre −w y w, y z entre −w y 0. Si queda fuera, la GPU la recorta y no se ve nada.
3. **Triángulo de prueba:** si existe `sdmc:/3ds/gzdoom/c3d-test.txt`, dibujar en `Update()` un triángulo fijo sin textura, con matriz identidad y color de vértice fijo. Esto prueba el shader, los atributos y los combinadores sin el motor de por medio.
4. **Texturas:** escribir en el log las primeras 20 texturas creadas (tamaño y nombre) en `C3DHardwareTexture::CreateTexture`.

**Sospechosos ya vistos en el código** (revisar antes de la prueba 9):

- **La matriz 2D llega por `C3DDataBuffer::BindRange`** (`c3d_buffers.cpp`), que guarda un puntero en `mHwUniforms`.
  - Si el motor nunca llama a `BindRange` con `VIEWPOINT_BINDINGPOINT`, `ApplyMatrices` usa la identidad. Las coordenadas 2D en píxeles (0..400) quedarían fuera de pantalla: negro total.
  - Comprobarlo en el log: ¿`mHwUniforms` es nulo en el primer dibujo?
- **Las limpiezas a mitad de fotograma:** `C3DRenderState::Clear` usa `C3D_RenderTargetClear`, que en citro3d es un `GX_MemoryFill` en la cola de GX. La lista de dibujos del fotograma se envía recién en `C3D_FrameEnd`, así que **una limpieza a mitad de fotograma se ejecuta antes que todos los dibujos de ese fotograma**, no en su lugar. Para el 2D no importa (solo limpia la profundidad). Para el mundo 3D sí: hará falta `C3D_FrameSplit(0)` antes de limpiar.
- **La luz por software:** `mLightParms[3]` lo pone `SetSoftLightLevel` solo en los dibujos 2D indexados (`hw_draw2d.cpp`). En `SetupAttributes` multiplica el color. Si queda en 0 de un dibujo anterior, todo lo siguiente sale negro. Comprobar que vuelva a −1.
- **Profundidad:** la tabla `{GPU_GREATER, GPU_GEQUAL, GPU_ALWAYS}` supone profundidad invertida (el PICA guarda −z/w). Por ahora no importa, porque el 2D dibuja sin prueba de profundidad. Hay que verificarlo cuando se dibuje el mundo.
- **El formato del vértice 2D:** 24 bytes, con posición `Float3` en 0, coordenadas de textura `Float2` en 12 y color `Byte4` en 20 (`v_2ddrawer.cpp`). Coincide con los loaders de `SetupAttributes` (sin relleno). El color ya llega como R,G,B,A porque `Draw2D` lo invierte en la primera pasada.

**Imagen rara.**

| Síntoma | Dónde se arregla |
|---|---|
| Girada 90° o en espejo | Signos de `u[0]`/`u[1]` en `ApplyMatrices` y las fórmulas de `SetViewport`/`SetScissor` (`c3d_renderstate.cpp`). Hoy: x' = y, y' = −x, como `Mtx_OrthoTilt` |
| Rojo y azul cambiados | El empaquetado `R<<24 \| G<<16 \| B<<8 \| A` en `CreateTexture` (`c3d_hwtexture.cpp`) o el intercambio BGRA→RGBA de `Draw2D` |
| Texturas boca abajo | El orden de filas en `CreateTexture` (comentario "t = 0 is the first row in memory") |
| Pantalla de 240 de ancho, estirada | `C3D_RenderTargetCreate(240, 400, ...)` y `DISPLAY_TRANSFER_FLAGS` (`c3d_framebuffer.cpp`) |

**Después de la primera imagen**, en este orden:
1. menús y consola (2D completo);
2. el mundo 3D en MAP01 (profundidad, cielo, sprites);
3. líneas del automapa, convertidas en quads;
4. luz por distancia con la tabla de niebla del PICA;
5. sonido (traer OpenAL Soft/NDSP de la rama `n3ds`);
6. controles 3DS y pantalla de abajo;
7. el `.cia` (unique ID 0xF3D5C);
8. H-Doom.

### 11.6 Lo que sirve de los otros trabajos con GPU (DSDA y Duke)

- La capa `pgl` (OpenGL sobre citro3d) de DSDA-Doom y NBlood resolvió los mismos problemas:
  - la inclinación de la pantalla;
  - los índices de 16 bits;
  - las texturas en baldosas;
  - la niebla con tabla;
  - las limpiezas.

  Ante una duda sobre citro3d, mirar cómo lo hizo `pgl` en el repo de DSDA. El backend de UZDoom no usa `pgl`, porque el hwrenderer de UZDoom ya está separado del API gráfico.
- **Método que funcionó en DSDA:**
  - comparar con el render por software, captura a captura;
  - activar una función a la vez (primero sin texturas, luego con texturas, luego mezcla, luego niebla);
  - una prueba con variantes cuando algo depende del gusto (brillo, niebla).

### 11.7 Errores que ya se cometieron (para no repetirlos)

- **Perder archivos del entorno temporal:** los Makefiles del simulador de Dolmexica y los `.elf` de las pruebas. Todo script o ayuda que se use más de una vez va al repo. Los `.elf`, a una carpeta local fuera de git.
- **Ponerle `-U` después de `-D`** a los tipos de 32 bits: rompe `_intsup.h`. Van juntos en `add_compile_options`, primero `-U`.
- **`-fno-short-enums` en todo el proyecto:** rompe las estructuras de libctru y citro3d. Mejor `: int` en los `enum` que hacen falta.
- **Subir un clon superficial (`--depth`)** a GitHub: lo rechaza. Hay que hacer `git fetch --unshallow` primero.
- **Mandar al dueño un zip entero** cuando el `.3dsx` ya lleva los datos: basta el `.3dsx`.
- **Confiar en Azahar (emulador)** para memoria o velocidad: solo sirve para la lógica.
- **El `CLAUDE.md` de la rama `n3ds` de gzdoom-3ds es el de tinaut1986:** sus reglas de git (repos, ramas `release/*`, títulos) **no aplican** a este proyecto. Reemplazarlo cuando se trabaje ahí.

### 11.8 Materiales que acompañan este traspaso

- `TRASPASO-n3ds-ports.pdf` y `.docx`: este documento.
- `uzdoom-prueba08.elf.xz`: el ejecutable con símbolos de la prueba 8, para traducir su log o su volcado (descomprimir con `xz -d`).
- En GitHub: el código y los README de cada port (sección 2). `gzdoom-3ds/platform/3ds/build.sh` (rama `uzdoom-3ds`) compila UZDoom con un solo comando.
