# 2026-10-09: Blake Stone (BStone) en 3DS

## Por qué

Blake Stone usa una versión ampliada del motor de Wolfenstein (pisos y techos con textura, terminales, mapa). [BStone](https://github.com/bibendovsky/bstone) es el port moderno: C++14, CMake y SDL2, con renderizadores OpenGL y Vulkan además del de software. Fork: [AlexanderV387/bstone](https://github.com/AlexanderV387/bstone), rama `n3ds`.

## Lo que hubo que cambiar para compilar

| Error | Causa | Solución |
|---|---|---|
| `std::max(long, int)` | En ARM, `int32_t` es `long`, no `int` | Dar el tipo explícito |
| `ftruncate` no declarada | newlib solo la declara en modo GNU (`-std=gnu++14`) | `CXX_EXTENSIONS ON` para la 3DS |
| `flock`, `dlfcn.h`, `umask`, `pipe`, `execle` | La 3DS no tiene bloqueo de archivos, librerías dinámicas ni procesos | Versiones vacías para la 3DS |
| `-ldl` | El toolchain de la 3DS no tiene libdl | No enlazarla |
| 3dsxtool: "ELF has no symbol table" | BStone quita los símbolos en Release | No quitarlos en la 3DS |

SDL2 viene incluido en BStone (2.32), y esa versión ya trae soporte de 3DS: no hubo que compilarlo aparte.

## El reloj del juego

El original suma los *ticks* (70 por segundo) desde un hilo que duerme entre tick y tick. En la 3DS, los hilos del mismo núcleo **no se interrumpen entre sí**: el hilo del reloj solo corre cuando el principal se bloquea o duerme. Y el juego tiene bucles como `while (TimeCount - lasttimecount < tics) {}` que esperan sin dormir: el reloj nunca avanzaría y el juego se congelaría.

Solución: en la 3DS, los ticks se calculan con el tiempo transcurrido (`steady_clock`) más un desfase para `set_ticks` y `subtract_ticks`. Sin hilo. Por lo mismo, el registro (log) se escribe sin hilo aparte.

## Controles

Los botones de la 3DS se agregaron como códigos de tecla (`sc_n3ds_a`…). Así el menú de reasignar de BStone funciona tal cual y la configuración los guarda por nombre (`3ds_r`). En los menús, A también es Enter/Sí y B es Escape/No; en el juego solo son sus propios botones. Circle Pad para avanzar y moverse de lado (con el *strafe* analógico que ya traía BStone) y C-stick para girar.

## En hardware: de no arrancar a 60 FPS

| Problema | Causa | Solución |
|---|---|---|
| Volvía al Homebrew Launcher sin mensaje | Error al iniciar y la 3DS no tiene ventanas de mensaje | Mostrar el error en la pantalla de arriba; pila de 1 MB |
| "Content not found" | newlib declara `F_OFD_SETLK` pero los bloqueos de archivo siempre fallan: no se abría ningún archivo | Bloqueos vacíos en la 3DS |
| "No relative mode implementation" | SDL no tiene modo relativo del mouse en la 3DS | Omitirlo |
| Data abort (Alignment) después del título | Cabeceras de las animaciones leídas con casts sobre un búfer de bytes desalineado; GCC usó `ldm/stm` | `memcpy` |
| Rígido, ~20-30 FPS | El renderizador por software de SDL (escalar, mezclar, rotar) y sin vsync | Componer en una pasada directo al framebuffer y esperar el vsync |
| 40 FPS con 7 ms de trabajo | El motor dormía hasta su tic de 70 Hz y luego se esperaba el vsync de 60 Hz | Solo el vsync marca el ritmo: **60 FPS** |
| Cierre de 9 segundos | Los récords se escribían dato por dato a la SD, dos veces | Escribirlos de una vez |
| Cortes de audio | Hilo de audio en el núcleo del sistema con 30% | Tercer núcleo del New 3DS |

Lo más valioso: medir. Los números en la pantalla de abajo mostraron que el juego casi no costaba nada y que el problema eran esperas, no cálculo.

## Release 1.0.0

Publicado como [n3ds-v1.0.0](https://github.com/AlexanderV387/bstone/releases/tag/n3ds-v1.0.0) (`.cia` y `.3dsx`). Además de lo anterior:

- **Pantalla de abajo:** barra de estado, mapa de lo explorado (centrado en el jugador) y barra de zona, copiadas 1:1 de la interfaz de 320x200; la vista 3D ocupa toda la pantalla de arriba. El orden de las barras se puede intercambiar, y el diseño original sigue como opción.
- **Diagonales lentas:** el Circle Pad es circular (en diagonal cada eje llega a ~70%) y BStone usaba solo la parte frontal del movimiento al desplazarse de lado. Zona muerta radial y longitud completa del movimiento.
- **Cierre lento desde HOME:** el juego esperaba el vsync de pantallas que ya no eran suyas. Con `aptShouldClose()` deja de esperar.
- Un solo `.cia` para los tres juegos: BStone detecta el juego al arrancar; con más de uno, menú propio (y Quit vuelve a él en el `.cia`).

## Pendiente

- Probar el HUD y el mapa en la pantalla de abajo.
- `.cia` (activar Actions en el fork), arte propio y release.
- Revisar en Wolfenstein si tiene la misma doble espera (tic + vsync).
- Arte propio (ícono y banner) y activar Actions en el fork para el `.cia`.
