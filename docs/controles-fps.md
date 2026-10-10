# Estándar de controles para FPS en New 3DS

Lo que definimos al portar Wolfenstein 3D (wolf4sdl-3ds, rama `n3ds`) y que se aplica a todos los FPS del proyecto: Chocolate Doom (Doom, Heretic, Hexen), Quake y los que vengan. Así todos se sienten igual y el código se reutiliza.

## Menús: distribución Nintendo

| Botón | Acción |
|---|---|
| A | Aceptar |
| B | Volver |
| START | Salir del menú de una vez y volver al juego (o al título) |
| Cruceta / Circle Pad | Moverse por el menú |

- Salir del juego solo con la opción "Quit". B en el menú principal cierra el menú (vuelve al juego o al título), igual que START; nunca lleva a "Quit": un B + A accidental cerraba el juego y se perdía el progreso. En los demás menús, B regresa al anterior.

- Leer los botones directo con libctru (`hidKeysHeld`), no a través de SDL. SDL 1.2 para 3DS numera START como botón 0 y A como botón 1, y eso invierte aceptar y volver.
- Al abrir y al cerrar el menú, esperar a que se suelte START; si no, el mismo toque lo vuelve a abrir o cerrar.

## Movimiento

**Doble stick (predeterminado, se puede apagar):**
- Circle Pad: avanzar/retroceder y moverse de lado (*strafe*).
- C-stick: girar la cámara.
- Modo clásico opcional: el Circle Pad avanza y gira, como el original.
- Giro con la pantalla táctil (opcional, para 3DS sin C-stick): deslizar a izquierda o derecha gira, con su propia velocidad (1-10). Se suma **después** del tope de giro por cuadro del motor: ese tope es para teclas y sticks y cortaba los deslizamientos rápidos. Si el motor tiene mouse (Doom), mandarlo como movimiento de mouse: ya se aplica cada cuadro y sin tope. Con esta opción activa, el toque no apaga la pantalla de abajo durante la partida, y un deslizamiento que empieza en los botones de la pantalla de abajo (el zoom del mapa) no gira: los dos conviven.

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
- Si el motor permite un solo botón por acción (Doom: `joyb_fire`…), cada acción se vuelve un **botón virtual**: su bit se enciende si se presiona cualquiera de los botones de 3DS asignados a ella. A, B y START se mandan aparte como ellos mismos, para que los menús usen siempre A/B aunque se reasignen.
- Quitar atajos del motor que estorban con mando, como el "doble toque de strafe = usar" de Doom (L abría puertas).

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
- Pantalla de abajo: **estadísticas (HUD) y mapa juntos.** Es la filosofía de todos los FPS de este tipo:
  - Con la vista a pantalla completa, el HUD (vida, munición, cara, llaves) y el mapa comparten la pantalla de abajo. Estadísticas arriba del mapa por defecto; una opción del menú las pone abajo.
  - Con una vista más pequeña, el HUD vuelve a la pantalla de arriba como en el original y el mapa ocupa toda la de abajo.
  - El mapa se ve desde el inicio de la partida, con cualquier tamaño de vista; solo lo esconde su opción del menú. Sin mapa, el HUD puede ir arriba, en medio o abajo de la pantalla inferior.
  - El mapa muestra solo lo que el jugador ya vio, centrado en él, con su dirección: pisos, paredes y puertas en colores distintos. Botones **+** y **−** en una esquina para el zoom (un toque acerca un cuarto; mantenerlo sigue acercando), guardado en la configuración. Si el juego trae su propio mapa (Blake Stone, el automapa de Doom), se usa ese; si no lo trae (Wolfenstein), se agrega uno como extra opcional, a partir de lo que el motor marca como visible en cada cuadro.
  - En Wolfenstein el HUD se dibuja cada cuadro con las funciones originales de la barra de estado en una superficie aparte; en Blake Stone se copian 1:1 las filas de la interfaz de 320x200. En Doom, la barra y el automapa se dibujan con sus propias funciones en otro búfer, guardando y restaurando el estado del automapa.
  - La pantalla de abajo basta a 30 cuadros por segundo.
- Todos los caminos que muestran un cuadro deben actualizar la pantalla de abajo (en Wolfenstein, `N3DS_Flip` en lugar de `SDL_Flip`). La partida usaba su propio blit + flip y el HUD se quedaba congelado.
- Un toque en la pantalla táctil apaga o enciende la de abajo (ahorra batería), en cualquier momento: título, menús y juego. Con el HUD o el mapa visibles el toque no la apaga, y si estaba apagada se enciende sola al aparecer.
- **Abrir `gsp::Lcd` solo alrededor de cada cambio de brillo** (`gspLcdInit` → `GSPLCD_PowerOn/OffBacklight` → `gspLcdExit`). Dejar la sesión abierta todo el juego congeló la consola al presionar HOME en Wolfenstein: el menú HOME necesita ese mismo servicio.
- Con `aptHook`, encender la pantalla de abajo al ir a HOME, al dormir y al salir, y volver a apagarla al regresar si estaba apagada. También con `atexit`.
- En SDL 1.2 para 3DS, `SDL_DUALSCR` con una superficie de 400×480 da las dos pantallas: filas 0-239 arriba y 240-479 abajo (se ven las columnas 40-359, 1:1). Sin consola de texto: `consoleDebugInit(debugDevice_NULL)`.
- Quitar pantallas de PC sin sentido en la consola, como la verificación de memoria de DOS.

## Rendimiento

- **El ritmo lo marca solo el refresco de la pantalla (60 Hz).** Los motores de id cuentan el tiempo en tics de 70 Hz y duermen hasta el siguiente: con el vsync encima, las dos esperas se desfasan (Blake Stone quedaba en 40 FPS); sin vsync, el juego corre a 70 y la pantalla muestra 60 de esos cuadros de forma desigual (Wolfenstein, porque SDL 1.2 presenta desde su propio hilo). En ambos casos: no dormir hasta el tic, esperar el vblank en el hilo del juego y calcular los tics con el tiempo transcurrido.

- **Objetivo: 60 FPS sin sacrificar calidad; mínimo aceptable, 30.** Se mide en hardware con un contador pequeño en una esquina de la pantalla de abajo (opción, apagado por defecto): cuadros por segundo y milisegundos por cuadro.
- Medir antes de optimizar: separar el tiempo del dibujo 3D, el de copiar a la pantalla y el resto. En Blake Stone el juego costaba ~7 ms y aun así iba a 40 FPS: el resto era espera.
- **Una sola espera por cuadro.** Si el motor duerme hasta su propio "tic" (70 Hz en los motores de id) y además se espera el vsync (60 Hz), las dos esperas se desfasan y muchos cuadros pierden un refresco (~40 FPS). En la 3DS el ritmo lo marca el vsync; el motor solo mide el tiempo transcurrido.
- SDL2 en la 3DS ignora el vsync y su renderizador por software escala, mezcla y rota con la CPU: es mejor componer la imagen y copiarla ya rotada al framebuffer (`gfxGetFramebuffer`), en bloques de 8x8 para aprovechar la caché, y esperar con `gspWaitForVBlank`.
- El hilo de audio de SDL va al núcleo del sistema con 30% de su tiempo; con música emulada (OPL) se corta. Usar el tercer núcleo del New 3DS, o subir el límite al 80%.
- **Componer las pantallas en otro núcleo.** Convertir el cuadro a color, estirarlo y girarlo costaba ~3 ms por cuadro en Doom. El hilo del juego copia el cuadro y un hilo en el núcleo 1 (`APT_SetAppCpuTimeLimit(80)`) compone, intercambia y espera el vblank; el juego solo espera si ese hilo no terminó. En Crispy Doom: de 47 a 57 FPS en el peor momento. El contador muestra los milisegundos de los dos núcleos.
- **En el `.cia`, permitir el núcleo 1:** la plantilla RSF traía `AffinityMask: 1` (solo el núcleo 0) y el hilo en el núcleo 1 no se creaba: el `.cia` bajaba a 47 FPS mientras el `.3dsx` (con los permisos del Homebrew Launcher) iba a 57-60. Ahora es `3`. El tercer núcleo (2) sí se pudo usar con `1`. Además, `MaxCpu` es el máximo del núcleo 1 que la aplicación puede pedir con `APT_SetAppCpuTimeLimit`: el bit 7 elige el modo de reparto ("multi") y el resto es el porcentaje. El valor de la plantilla, `0x9E`, es 30%: pedir 80 fallaba (`d8e05bf4`) y con 30 la composición no cabía en un cuadro (30 FPS fijos). Ahora es `0xD0` (80%). Lo explica `sysmodules/pm/source/reslimit.c` de Luma3DS. Probar siempre el `.cia` y el `.3dsx`, y que el log diga en qué núcleo corre cada hilo.
- **Detectar la Old 3DS** (`APT_CheckNew3DS`): un tercio de la velocidad y sin tercer núcleo. Bajar lo caro (resolución alta, frecuencia de audio) y no poner hilos extra en el núcleo 1, que ya tiene el audio.
- **Arranque:** el log con milisegundos en cada línea encuentra las esperas. En Crispy Doom: leer los archivos de datos completos a la memoria de una vez, guardar en la SD las tablas que se calculan en cada arranque, no buscar archivos opcionales nombre por nombre y quitar esperas fijas para monitores de PC. De ~20 s a 1,3 s.

## Configuración guardada

- Asignaciones, doble stick, modo de correr, posición del HUD y giro táctil (con su velocidad) se guardan en el archivo de configuración del juego.
- Se agregan al final del formato original, detrás de un número mágico (`0x3d50` en Wolfenstein), para que los archivos de configuración viejos sigan cargando.
- Validar al leer: valores fuera de rango vuelven al predeterminado.

## HOME y la tarjeta SD

- Cerrar desde HOME: SDL manda `SDL_QUIT` cuando `aptMainLoop()` devuelve falso. Comprobar que el juego lo procese (BStone lo ignoraba y el menú HOME esperaba para siempre). Al cerrar desde HOME no esperar el vsync ni presentar: las pantallas ya son del menú HOME.
- Guardar configuración y récords en `APTHOOK_ONSUSPEND` (al pulsar HOME) y no volver a guardar si se cierra desde ahí: con el menú HOME al frente, escribir en la SD fue mucho más lento.
- No vaciar un archivo para reescribirlo, ni escribir a un temporal y renombrarlo: escribir en un archivo recién creado o vaciado a veces tarda 8 segundos en la SD. Escribir encima del existente y recortarlo al final. Tampoco reescribir archivos que no cambian en cada arranque (el `README.txt` de los packs de música de Crispy).

## SDL2 en la 3DS

- SDL 2.30.9: `SDL_CondWaitTimeout` con un mutex de SDL se bloquea para siempre (espera con el `LightLock` interno del `RecursiveLock`). Parche en `crispy-doom/tools/3ds/patches/sdl-cond-recursive-mutex.patch`.
- No hay `/tmp`: lo que el motor escriba ahí, hacerlo en memoria (`fmemopen`) o en la carpeta del juego (`TMPDIR`).
- Pila del hilo principal: 32 KB por defecto; Doom necesita `__stacksize__` de 1 MB.

## Empaquetado

- Un `.cia` arranca **sin argumentos** (`argc` = 0); un `.3dsx` recibe su ruta como `argv[0]`. Si el port agrega opciones a la línea de comandos (por ejemplo, el juego elegido en un menú), primero hay que poner un nombre de programa. En Blake Stone, la opción se perdía y el `.cia` fallaba aunque el `.3dsx` funcionaba: probar siempre los dos.

- `.3dsx` y `.cia` en cada compilación (`tools/3ds/make-cia.sh`), con 804 MHz, caché L2 y 124 MB activados.
- Datos del juego en `/3ds/<port>/<juego>/`, una carpeta por juego para no mezclar configuraciones ni partidas guardadas.
