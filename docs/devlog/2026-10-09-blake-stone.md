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

## Pendiente

- Probar en hardware: ¿arranca?, ¿FPS? Pisos y techos con textura pesan más que en Wolfenstein.
- Resto del estándar de controles: HUD abajo, modos de correr, toque en la pantalla de abajo, giro táctil, sensibilidad.
- Arte propio (ícono y banner) y activar Actions en el fork para el `.cia`.
