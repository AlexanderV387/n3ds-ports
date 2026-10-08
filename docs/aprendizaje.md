# Plan de aprendizaje

Cada paso deja una habilidad concreta y una forma de comprobarla.

| Paso | Qué se aprende | Cómo comprobarlo | Hecho |
|---|---|---|---|
| Hola mundo con devkitPro y SDL2 | Toolchain, bucle principal, entrada | Corre en la consola y muestra los FPS | [ ] |
| Chocolate Doom en 3DS | C, arquitectura de un motor clásico, render por columnas | FPS antes y después; demos que se reproducen igual | [ ] |
| Controles y pantalla táctil | Entrada e interfaz | Mapeo documentado y probado en hardware | [ ] |
| Render multihilo | Concurrencia y perfilado | ms por cuadro antes y después de cada cambio | [ ] |
| Heretic y Hexen | Reutilizar un motor para varios juegos | Los tres juegos corren sobre la misma capa compartida | [ ] |
| Motor compatible con MUGEN | Formatos binarios, intérprete de scripts, diseño de motores | Cargar un personaje, mostrarlo y que camine | [ ] |

## Plan del motor base (Chocolate Doom)

1. Compilarlo en 3DS y medir los FPS de partida.
2. Mejorar controles: C-stick fluido, ZL/ZR, táctil y giroscopio.
3. Pasar HUD, automapa y menús a la pantalla de abajo.
4. Repartir el render entre los núcleos extra, midiendo cada cambio.
5. Grabar demos de referencia y comprobar que se reproducen igual tras cada cambio.
6. Extraer una capa compartida de controles, HUD y guardado para Heretic, Hexen y Doom 64.

## Reglas para aprender de verdad

- Explicar con mis propias palabras cómo funciona el componente central antes de darlo por cerrado.
- Arreglar al menos un bug por mi cuenta en cada proyecto.
- Apuntar en [`rendimiento.md`](rendimiento.md) qué cambio mejoró el rendimiento y por qué.

## Preguntas para entender el hola mundo

Responderlas en el devlog antes de pasar a Chocolate Doom:

1. ¿Qué hace `SDL_RENDERER_PRESENTVSYNC` y por qué el contador se queda en unos 60 FPS?
2. ¿Por qué el FPS se promedia cada medio segundo en lugar de calcularse en cada cuadro?
3. ¿Qué pasa si quitas la zona muerta del Circle Pad?
4. ¿Cómo se dibuja un número con la fuente de 3x5 bits? Explica la operación `4 >> col`.
5. ¿Qué archivo genera `ctr_create_3dsx` y qué lo diferencia de un `.cia`?
