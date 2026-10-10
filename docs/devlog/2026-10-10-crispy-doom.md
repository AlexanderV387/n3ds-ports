# 2026-10-10: Crispy Doom en 3DS

## Por qué

[Crispy Doom](https://github.com/fabiangreffrath/crispy-doom) es Chocolate Doom (fiel al ejecutable original de DOS) con pantalla ancha, límites ampliados y opciones modernas. Un mismo código fuente trae Doom, Heretic, Hexen y Strife. Fork: [AlexanderV387/crispy-doom](https://github.com/AlexanderV387/crispy-doom), rama `n3ds`.

## Compilar

devkitPro no tiene SDL2 para 3DS en sus paquetes, aunque SDL lo soporta oficialmente desde 2.24. `tools/3ds/build-deps.sh` compila SDL2 2.30.9 y SDL2_mixer 2.8.0 (solo WAVE: la música de Doom es MIDI y la toca la emulación OPL del propio Crispy) y les aplica los parches de `tools/3ds/patches/`. El módulo `src/n3ds.c` concentra lo propio de la 3DS: arranque, log, presentación, opciones y errores.

## De pantalla negra a jugable

| Problema | Causa | Solución |
|---|---|---|
| Pantalla negra al iniciar | La zona de memoria de Doom tomaba toda la RAM libre y SDL ya no podía reservar nada | Zona de 16 MB y comprobar que queden 16 MB libres |
| Pantalla negra, otra vez: ni menú ni música | **Bug de SDL 2.30.9 en 3DS:** `SDL_CondWaitTimeout` espera con el `LightLock` interno del `RecursiveLock` del mutex. El hilo que avisa incrementa el contador del mutex y nunca lo suelta: el detector del chip OPL (`OPL_Delay`) esperaba para siempre | Parche `sdl-cond-recursive-mutex.patch`: guardar y restaurar `thread_tag` y `counter` alrededor de la espera. Además, `OPL_Delay` se rinde a los 3 segundos |
| Ningún botón respondía | `I_InitJoystick` se salía porque la configuración no tenía GUID de mando | Leer los botones con libctru |
| Sin música | La conversión MUS→MIDI escribía `/tmp/doom.mid`, y la 3DS no tiene `/tmp` | Convertir en memoria y leerla con `fmemopen` |
| Música "pixeleada" | 22050 Hz | 44100 Hz: el hilo de audio tiene el tercer núcleo para él solo |
| START abría y cerraba el menú sin parar | El menú repite los botones mantenidos | Solo cuenta cuando se presiona |

## El arranque: de 20 a 1,3 segundos

Cada línea del log lleva los milisegundos desde el inicio, y eso señaló cada espera:

| Paso | Costo | Solución |
|---|---|---|
| Leer el WAD por partes de la SD | Varios segundos | Leerlo completo a la memoria de una vez (si quedan 8 MB libres) |
| Tabla de translucidez | Calculada en cada arranque | Guardarla en la SD con un hash de la paleta |
| Efectos de sonido | Conversión con `SDL_BuildAudioCVT` | La expansión genérica de Crispy, mucho más rápida |
| Buscar packs de música | 1,5 s probando cada nombre conocido con cada extensión | Solo si la carpeta tiene algún archivo. El primer intento no funcionó: el propio juego escribe un `README.txt` ahí |
| `startup_delay` | 1 s fijo para que los monitores cambien de modo | Nada en la 3DS |

## La pantalla de abajo

- **Barra de estado:** con la vista completa (tamaño 11, el predeterminado en 3DS) va abajo. Se dibuja con el propio `ST_Drawer` del juego en un búfer aparte (cambiando `I_VideoBuffer` y volviendo a ponerlo), y se copian sus 320x32.
- **Automapa:** con las funciones del automapa original. `AM_DrawBottom` guarda las variables del automapa (ventana, escala, búfer, ancho), dibuja paredes, jugador y cosas centrado en el jugador, y las restaura. Solo muestra lo que el jugador vio, como el automapa.
- **Zoom:** botones + y − en una esquina del mapa (un toque acerca un cuarto; mantenerlo sigue acercando). La zona de los botones queda reservada: el giro con la pantalla táctil no empieza ahí, así que ambos conviven.
- Se actualiza 30 veces por segundo; la de arriba, 60.

## 47 FPS → 57: componer en otro núcleo

Con la vista completa y la pantalla de abajo, los combates bajaban a 47 FPS. Convertir el cuadro de 8 bits a color, estirar 200 filas a 240 mezclándolas y girarlo para el framebuffer costaba unos 3 ms de los 16,7 de cada cuadro.

Ahora el hilo del juego copia el cuadro (80 KB) y entrega la conversión a un hilo en el **núcleo del sistema (1)**, con hasta el 80% de su tiempo (`APT_SetAppCpuTimeLimit`). Ese hilo compone las dos pantallas, las intercambia y espera el vblank mientras el juego ya dibuja el siguiente cuadro. El juego solo espera si el otro hilo no terminó, así que el ritmo lo sigue marcando la pantalla. Resultado: el peor momento baja a 57. El contador muestra los tres números: FPS, ms del juego y ms de la composición.

La resolución alta (800x400 promediada a 400x240) sigue en 25-31 ms por cuadro (30 FPS). Repartir el dibujo 3D entre núcleos queda como opción experimental.

## Controles

Doom asigna un solo botón por acción (`joyb_fire`…). Para que una acción tenga varios botones (R y ZR disparan), cada acción es un **botón virtual**: el bit *i* del mando se enciende si se presiona cualquiera de los botones de la 3DS asignados a la acción *i*. A, B y START viajan aparte como ellos mismos, así que los menús siempre usan A/B aunque se reasignen.

- Página "Buttons": A sobre una fila espera el botón nuevo; un botón es de una sola acción; presionar uno que la acción ya tiene lo quita; START cancela.
- Correr: mantener, presionar una vez (hasta detenerse) o el Circle Pad a fondo.
- C-stick: gira (doble stick) o se mueve de lado (clásico).
- Giro con la pantalla táctil: se envía como movimiento de mouse, que el motor aplica cada cuadro sin el tope de giro de los mandos.
- Se apagó el "doble toque de strafe = usar" de Doom: con L abría puertas sin querer.

## HOME y la SD

- La configuración se guarda al abrir el menú HOME (`APTHOOK_ONSUSPEND`) y no se vuelve a escribir si se cierra desde ahí.
- La configuración, las partidas y el log se escriben encima de los archivos existentes y se recortan al final: escribir un archivo nuevo a veces tarda segundos en la SD.
- La Old 3DS se detecta (`APT_CheckNew3DS`): compone en el núcleo del juego, mezcla el audio a 22050 Hz y no permite la resolución alta. No se ha probado en una.
