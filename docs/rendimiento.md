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
