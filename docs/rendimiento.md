# Registro de rendimiento

Solo valen mediciones en una **New 3DS real**. Anotar cada cambio que afecte el rendimiento, aunque empeore las cosas.

Cómo medir:
- Misma escena o demo grabada, mismo tiempo de medición.
- Anotar FPS promedio y milisegundos por cuadro (a 60 fps el presupuesto es 16,67 ms; a 30 fps, 33,33 ms).
- Indicar el commit medido.

| Fecha | Proyecto | Commit | Escena | Cambio | FPS antes | FPS después | ms/cuadro antes | ms/cuadro después | Por qué cambió |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-08 | hello-world | e0e67ff | Cuadro rojo, pantalla de arriba | Primera medición (Luma 13.4) | — | 108,1 | — | 9,25 | Línea base. SDL2 ignora `SDL_RENDERER_PRESENTVSYNC` en 3DS, así que el bucle no se limita a 60 |
| 2026-10-08 | hello-world | b6b1bd3 | Cuadro rojo, pantalla de arriba | `gspWaitForVBlank()` tras cada cuadro | 108,1 | 59,8 (estable) | 9,25 | 16,71 (estable) | El bucle espera el refresco de pantalla; desaparece el tearing |
| 2026-10-09 | crispy-doom | 688e63b | Del inicio al primer cuadro | WAD leído completo a memoria, tabla de translucidez guardada, expansión de sonidos rápida | ~20 s | 3,8 s | — | — | Medido con el log con tiempos: el arranque esperaba a la SD y a cálculos repetidos |
| 2026-10-10 | crispy-doom | 3002431 | Del inicio al primer cuadro | Sin `startup_delay` ni búsqueda de packs de música | 3,8 s | 1,3 s | — | — | 1 s de espera fija para monitores y 1,5 s probando nombres de archivo en la SD |
| 2026-10-10 | crispy-doom | cfdf8a0 | E1M2, combates con imps, vista completa + mapa abajo | Componer las dos pantallas en el núcleo 1 | 47 (mínimo) | 57 (mínimo) | — | — | La conversión (~3 ms por cuadro) sale del núcleo del juego |
| 2026-10-09 | crispy-doom | 316a126 | E1M1, resolución alta (800x400 promediada) | Primera medición | — | 29-30 | — | 25-31 | El dibujo 3D a 4 veces los píxeles no cabe en 16,7 ms; pendiente repartirlo entre núcleos |
