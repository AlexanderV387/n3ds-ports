# Investigación: un motor compatible con MUGEN en la New 3DS

Objetivo: jugar contenido de MUGEN (personajes, escenarios, screenpacks) en la New 3DS lo más parecido posible a la versión de PC, dentro de los límites de la consola.

## Conclusión

Es viable. El camino recomendado es **portar Dolmexica Infinite** (C++, licencia MIT), que ya corre en Dreamcast y PS Vita, escribiendo una capa para la 3DS en su biblioteca base, **Prism**. **Ikemen GO** (licencia MIT) sirve como referencia de comportamiento para acercarse a MUGEN donde Dolmexica se aparta.

No se encontró ningún port de MUGEN para 3DS. Los antecedentes en portátiles son el MUGEN de PSP (InfinityCat, cerrado, compatibilidad limitada) y Dolmexica Infinite en Vita (en desarrollo).

## Opciones

| Opción | Lenguaje | Plataformas | Compatibilidad | Trabajo para la 3DS |
|---|---|---|---|---|
| **Dolmexica Infinite + Prism** | C++ | Windows, Web, Dreamcast, Vita (en desarrollo) | WinMUGEN a 1.1b; sin equipos (teams) | Una capa de plataforma nueva (~3.000 a 4.000 líneas) |
| **Ikemen GO** | Go + Lua | PC, Android, iOS (OpenGL 3.3 / GLES 3.2 / Vulkan) | La más cercana a MUGEN 1.1b | No se puede portar: Go no corre en la 3DS. Reescribirlo en C++ son unas 80.000 líneas de lógica |
| **Motor propio** | C/C++ | — | La que logremos | Años, con Ikemen GO como guía |

### Dolmexica Infinite (recomendado)

- Repositorios: `CaptainDreamcast/DolmexicaInfinite` (~51.000 líneas) y `CaptainDreamcast/prism` (~25.000), los dos con licencia MIT y activos (versión 1.8, septiembre de 2026).
- Toda la parte de MUGEN (SFF v1 y v2, AIR, CNS, CMD, SND, DEF, fuentes, escenarios, screenpacks, modos arcade, versus, entrenamiento, supervivencia) ya está en C++ portable.
- Prism separa la plataforma en archivos pequeños: dibujo, texturas, entrada, sonido, archivos, hilos y sistema. La capa de Dreamcast suma unas 2.900 líneas y la de Vita unas 2.200. La de 3DS sería parecida: dibujo y texturas con citro3d, sonido con ndsp, entrada con hid y archivos en la SD.
- La API de dibujo es de sprites con transformaciones (escala, rotación, color, transparencia, modos de mezcla), lo que encaja con citro3d.
- Los sprites grandes ya se parten en trozos (la Dreamcast, como la 3DS, admite texturas de hasta 1024 píxeles de lado).
- Dolmexica tiene un formato "precargado" de sprites, pensado para cargar rápido en la Dreamcast.

**Lo que le falta respecto a MUGEN** (según su documentación):

- Equipos (Simul, Turns, Tag) y sus triggers.
- Bancos de fuentes: los cambia por colores fijos.
- `RemapPal` solo con `source = 1,1`, y no en helpers ni proyectiles.
- En Dreamcast faltan además las estelas (afterimages), la mezcla por resta, las sombras de color y los efectos de inversión e intensidad de color. En la 3DS sí se pueden hacer con el GPU.

Para acercarlo a PC habría que recuperar esto tomando como referencia Ikemen GO, empezando por las estelas, la resta y los efectos de color, que en la 3DS son directos. Los equipos irían en una fase propia.

### Ikemen GO (como referencia)

- `ikemen-engine/Ikemen-GO`, MIT. Unas 134.000 líneas de Go: `bytecode.go` (17.000), `char.go` (15.000), `compiler*.go` (16.000), `system.go`, `fightscreen.go` y `motif.go` (las pantallas, unas 20.000), más los renderizadores.
- Traduce el CNS a un bytecode al cargar: es la técnica que conviene para que la lógica de los personajes sea rápida en el ARM11.
- Los estados comunes los escribe en su propio lenguaje (ZSS), y las pantallas y menús en Lua.
- Pide OpenGL 3.3 o Vulkan con shaders. La 3DS no tiene shaders de fragmento, así que su renderizador no sirve; su lógica, sí como guía.

## La 3DS frente al contenido de MUGEN

| Tema | Situación | Plan |
|---|---|---|
| Resolución | WinMUGEN 320x240; MUGEN 1.0 640x480; 1.1 HD 1280x720 | 320x240 cabe casi exacto en los 400x240 de arriba. El de 640x480 se reduce a la mitad de alto y en el modo ancho (800x240) conserva el detalle a lo ancho. El HD se reduce |
| Paletas | Los sprites SFF v1 y muchos v2 son de 8 bits con paleta; MUGEN cambia paletas en vivo (colores del personaje, `RemapPal`, PalFX) | El GPU de la 3DS no tiene texturas con paleta: cada sprite se convierte a color directo con su paleta al subirlo, y se rehace si la paleta cambia. Los efectos de color (suma, multiplicación, inversión, destello) van en los combinadores de color del GPU |
| Mezclas | Normal, suma, resta, suma con alfa | Todas en el GPU de la 3DS, incluida la resta |
| Memoria | 124 MB para el juego (modo New 3DS), 6 MB de VRAM | Personajes clásicos: decenas de MB entre los dos, sin problema. Personajes HD con sprites de 32 bits pueden no caber de a dos: cargar sprites cuando hacen falta y liberar los que no se usan |
| CPU | ARM11 a 804 MHz | La lógica CNS de dos personajes a 60 FPS es razonable con bytecode. Jefes con cientos de helpers o IA muy pesada pueden ir lentos |
| Sonido | WAV en SND; música en MP3, OGG, MIDI | ndsp para los efectos; OGG y MP3 con bibliotecas pequeñas (tremor, libmad). MIDI más adelante |
| Controles | 6 botones (a, b, c, x, y, z) + start | Y=x, X=y, R=z, B=a, A=b, ZR=c (reasignables). Circle Pad y cruceta para moverse |
| Pantalla de abajo | — | Lista de movimientos del personaje, datos del modo entrenamiento, menú táctil; según el estándar del proyecto |

## Fases

1. **Capa de 3DS para Prism:** dibujo y texturas en citro3d (con la conversión de paletas), entrada, sonido, archivos y sistema. Meta: el título de Dolmexica en la 3DS.
2. **Kung Fu Man contra Kung Fu Man** en un escenario, a 60 FPS (Kung Fu Man es el personaje de referencia de MUGEN). Medir CPU, GPU y memoria con el log, como en los otros ports.
3. **Pantallas completas:** selección, versus, barras de vida, fuentes y screenpacks de 320x240 y 640x480; modo ancho 800x240 para el contenido de 640.
4. **Sonido y música.**
5. **Acercarlo a PC:** estelas, resta, efectos de color, `RemapPal` completo, bancos de fuentes y luego equipos, con Ikemen GO como referencia.
6. **Compatibilidad:** probar personajes y escenarios populares de cada época (WinMUGEN, 1.0, 1.1) y anotar qué funciona, como se hizo con los mods de DSDA.
7. **Estándar del proyecto:** pantalla de abajo, botones reasignables, `.cia` con su icono y banner.

## Riesgos

- **La exactitud:** MUGEN tiene muchas rarezas sin documentar. Dolmexica prefiere el comportamiento de las versiones antiguas cuando chocan, por su enfoque en la Dreamcast; algunos personajes de 1.1 pueden comportarse distinto.
- **Personajes HD y jefes:** memoria y CPU.
- **Mantener el port al día** con Dolmexica: conviene que los cambios de la 3DS queden en la capa de plataforma y que los arreglos generales vuelvan al proyecto original como pull request.
- **Datos:** el contenido de MUGEN no se distribuye con el port; el usuario copia su carpeta (`data/`, `chars/`, `stages/`, `font/`, `sound/`). Los estados comunes (`common1.cns`) vienen con el paquete de MUGEN o con el de Dolmexica.

## Fuentes

- Dolmexica Infinite: <https://github.com/CaptainDreamcast/DolmexicaInfinite> (documentación de diferencias en `docs/differences.html`) y <https://captaindreamcast.itch.io/dolmexica-infinite>
- Prism: <https://github.com/CaptainDreamcast/prism>
- Ikemen GO: <https://github.com/ikemen-engine/Ikemen-GO>
- GameBrew, Dolmexica Infinite Vita: <https://gamebrew.org/wiki/Dolmexica_Infinite_Vita>
- MUGEN en PSP: <https://psp-archive.github.io/games/mugen-PSP.html>
