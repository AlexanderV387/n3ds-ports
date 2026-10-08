# Estándar de controles para FPS en New 3DS

Lo que definimos al portar Wolfenstein 3D (wolf4sdl-3ds, rama `n3ds`) y que se aplica a todos los FPS del proyecto: Chocolate Doom (Doom, Heretic, Hexen), Quake y los que vengan. Así todos se sienten igual y el código se reutiliza.

## Menús: distribución Nintendo

| Botón | Acción |
|---|---|
| A | Aceptar |
| B | Volver |
| START | Salir del menú de una vez y volver al juego (o al título) |
| Cruceta / Circle Pad | Moverse por el menú |

- Salir del juego solo con la opción "Quit". B en el menú principal vuelve al juego durante una partida y no hace nada en el título: un B + A accidental cerraba el juego y se perdía el progreso.

- Leer los botones directo con libctru (`hidKeysHeld`), no a través de SDL. SDL 1.2 para 3DS numera START como botón 0 y A como botón 1, y eso invierte aceptar y volver.
- Al abrir y al cerrar el menú, esperar a que se suelte START; si no, el mismo toque lo vuelve a abrir o cerrar.

## Movimiento

**Doble stick (predeterminado, se puede apagar):**
- Circle Pad: avanzar/retroceder y moverse de lado (*strafe*).
- C-stick: girar la cámara.
- Modo clásico opcional: el Circle Pad avanza y gira, como el original.

**Velocidad analógica:**
- La inclinación del stick es proporcional: a medio camino, más lento.
- Siempre multiplicada por `tics` (o el equivalente del motor), para que no dependa de los FPS.
- Error que encontramos en Wolfenstein: el stick a fondo daba ~97 unidades por cuadro, más rápido que correr con la cruceta (~82), y el botón de correr no lo afectaba.

**Tres modos de correr (opción del menú):**

| Modo | Comportamiento |
|---|---|
| Stick a fondo | La inclinación llega hasta la velocidad de correr; el botón también corre |
| Mantener botón | Corre mientras el botón está presionado (predeterminado) |
| Presionar una vez | Un toque corre a tope hasta que dejas de moverte, como el *sprint* de los FPS modernos |

Aplica igual al Circle Pad y a la cruceta.

## Botones reasignables

- Cada acción (disparar, usar/abrir, correr, strafe, arma siguiente/anterior, pausa, mapa…) se asigna a A, B, X, Y, L, R, ZL, ZR o SELECT desde el menú.
- Pantalla de asignación: una fila por acción con sus botones; A en una fila espera el botón nuevo; START cancela; fila de "restablecer".
- Un botón pertenece a una sola acción (al asignarlo se quita de la anterior); una acción puede tener varios botones.
- START y la cruceta no se reasignan: START es el menú, la cruceta mueve.
- El menú muestra nombres de botones de 3DS, nunca teclas de PC, mouse ni joystick.

Predeterminados de Wolfenstein (R dispara, como en la mayoría de los FPS):

| Botón | Acción |
|---|---|
| R, ZR | Disparar |
| A | Usar / abrir |
| B, ZL | Correr |
| X / Y | Arma siguiente / anterior |
| L | Strafe |
| SELECT | Pausa |

## Pantallas

- Pantalla de arriba: el juego.
- Pantalla de abajo: el HUD (vida, munición, cara, llaves) cuando el juego está a pantalla completa. En Wolfenstein se dibuja cada cuadro con las funciones originales de la barra de estado en una superficie aparte.
- Un toque en la pantalla táctil apaga o enciende la de abajo (ahorra batería), en cualquier momento: título, menús y juego. Con el HUD visible el toque no la apaga, y si estaba apagada se enciende sola al aparecer el HUD.
- **Abrir `gsp::Lcd` solo alrededor de cada cambio de brillo** (`gspLcdInit` → `GSPLCD_PowerOn/OffBacklight` → `gspLcdExit`). Dejar la sesión abierta todo el juego congeló la consola al presionar HOME en Wolfenstein: el menú HOME necesita ese mismo servicio.
- Con `aptHook`, encender la pantalla de abajo al ir a HOME, al dormir y al salir, y volver a apagarla al regresar si estaba apagada. También con `atexit`.
- En SDL 1.2 para 3DS, `SDL_DUALSCR` con una superficie de 400×480 da las dos pantallas: filas 0-239 arriba y 240-479 abajo (se ven las columnas 40-359, 1:1). Sin consola de texto: `consoleDebugInit(debugDevice_NULL)`.
- Quitar pantallas de PC sin sentido en la consola, como la verificación de memoria de DOS.

## Configuración guardada

- Asignaciones, doble stick y modo de correr se guardan en el archivo de configuración del juego.
- Se agregan al final del formato original, detrás de un número mágico (`0x3d50` en Wolfenstein), para que los archivos de configuración viejos sigan cargando.
- Validar al leer: valores fuera de rango vuelven al predeterminado.

## Empaquetado

- `.3dsx` y `.cia` en cada compilación (`tools/3ds/make-cia.sh`), con 804 MHz, caché L2 y 124 MB activados.
- Datos del juego en `/3ds/<port>/<juego>/`, una carpeta por juego para no mezclar configuraciones ni partidas guardadas.
