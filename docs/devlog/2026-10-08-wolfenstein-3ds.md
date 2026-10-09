# 2026-10-08: Wolfenstein 3D en New 3DS

Primer port completo del proyecto: [wolf4sdl-3ds](https://github.com/AlexanderV387/wolf4sdl-3ds), rama `n3ds`, sobre el port de hax0kartik.

## Qué se hizo

- Compilación en GitHub Actions de cuatro versiones (Wolfenstein completo y shareware, Spear of Destiny completo y demo), cada una en `.3dsx` y `.cia`. Spear of Destiny salió casi gratis: solo cambian las opciones al compilar (`SPEAR`, `SPEARDEMO`, `GOODTIMES`).
- Arte propio para ícono y banner (hecho con IA).
- Sin la pantalla de memoria de DOS al arrancar.
- Controles de New 3DS: doble stick, tres modos de correr, botones reasignables y menús con A / B / START.
- HUD en la pantalla de abajo en pantalla completa, con posición configurable.
- Toque en la pantalla táctil para apagar o encender la de abajo.

Corre fluido en la New 3DS. El estándar de controles quedó en [`controles-fps.md`](../controles-fps.md) para los próximos FPS.

## Problemas que aparecieron al probar en la consola

| Problema | Causa | Solución |
|---|---|---|
| START aceptaba y A volvía en los menús | SDL 1.2 para 3DS numera START como botón 0 y A como 1 | Leer los botones directo con libctru |
| Lo asignado en el menú no hacía nada | Los controles del juego estaban fijos en el código | Tabla de asignaciones usada por el juego |
| Stick a fondo más rápido que correr | Inclinación convertida directo en velocidad, sin `tics` | Escalar a caminar/correr y multiplicar por `tics` |
| Se cerraba al asignar un botón | Texto de ayuda más ancho que la ventana (`US_CPrintLine`) | Textos más cortos |
| Las opciones cambiaban sin parar | El menú volvía a leer A mientras seguía presionado | Esperar a que se suelte A |
| HOME congelaba la consola | La sesión de `gsp::Lcd` quedaba abierta todo el juego | Abrirla solo para cada cambio de brillo |
| B + A cerraba el juego | B en el menú principal abría "salir" | Solo "Quit" sale; B vuelve al juego |
| HUD congelado abajo | La partida mostraba cada cuadro por otro camino que no actualizaba la pantalla de abajo | Todos los cuadros pasan por `N3DS_Flip` |
| Girar con el táctil era lentísimo | El tope de giro por cuadro (pensado para teclas y sticks) cortaba los deslizamientos rápidos | Sumar el giro táctil después del tope, con su propia velocidad (1-10) |

## Qué aprendí

- Lo que dice una librería no basta: el orden de los botones de SDL, el vsync y el HOME solo se descubrieron en la consola.
- En un motor viejo hay varios caminos para lo mismo (mostrar un cuadro): hay que encontrarlos todos.
- Probar con alguien que juega de verdad encuentra cosas que el código no muestra, como la velocidad del stick o el B + A accidental.
- Los servicios del sistema de la 3DS se comparten con el menú HOME: no hay que dejarlos abiertos.

## Estado final

Port dado por terminado el 8 de octubre de 2026, con todo probado en New 3DS: doble stick, giro con la pantalla táctil (con velocidad propia), tres modos de correr, botones reasignables, HUD abajo con posición configurable, HOME y salida segura del menú.

## Release

Publicado como [v1.0.0](https://github.com/AlexanderV387/wolf4sdl-3ds/releases/tag/v1.0.0) con los 8 archivos (`.cia` y `.3dsx` de las cuatro versiones). Para publicar otra versión: cambiar `VERSION` y hacer un commit con `[release]` en el mensaje; GitHub crea la etiqueta (desde este entorno no se pueden subir etiquetas).

## v1.1.0 (9 de octubre)

- Selector de misiones de Spear of Destiny: un `.cia` no puede pasar `--mission`, así que las expansiones (`*.sd2`, `*.sd3`) eran inalcanzables. Si la carpeta tiene más de una misión, un menú de texto de libctru en la pantalla de arriba deja elegir antes de que arranque SDL.
- Aclaración: los archivos `.SOD` son el juego completo; `.SDM` es la demo; `.SD2` y `.SD3` son expansiones que se vendían aparte. Steam trae solo `.SOD`.

## v1.2.0 a v1.3.1 (9 de octubre)

- **Un solo `.cia` para todos los juegos (`wolf4sdl-all`).** Wolf4SDL elige el juego al compilar (`#ifdef SPEAR`), así que no se puede cambiar en tiempo de ejecución. Solución: compilar las cuatro variantes, renombrar con `objcopy --redefine-syms` todos los símbolos globales que define cada una (`main` → `w3d_main`, `sod_main`…) y enlazarlas juntas con un menú de libctru que solo muestra los juegos cuyos datos están en la SD. Cada variante ocupa ~300 KB; el combinado pesa 1,5 MB. Los `.cia` separados se mantienen.
- **Quit vuelve al menú de juegos** en el combinado: `aptSetChainloaderToSelf()` hace que la aplicación se reinicie al salir, así cada juego se cierra limpio. Solo en `.cia` y con más de un juego.
- **Menús y pantallas de SoD descentrados.** El port original centra el menú en la pantalla de 400x240, pero el fondo de SoD (una imagen de 320x200), su título (dos imágenes) y los créditos se dibujaban en la esquina. Ahora están centrados; el fondo del menú se repite para llenar los bordes.
- Arte propio (IA) para SoD y para el combinado.

**Lección:** al portar a otra resolución, hay que revisar cada coordenada fija (`VWB_DrawPic (0,0,…)`, `112`, `60`…). El port original ajustó lo que se veía en Wolfenstein, pero no lo que solo usa Spear of Destiny.

## v1.4.0: lo aprendido en Blake Stone (9 de octubre)

- **60 FPS.** No tenía la doble espera de Blake Stone, pero sí el mismo fondo: `CalcTics` dormía hasta el siguiente tic de 70 Hz y SDL 1.2 presenta desde su propio hilo, así que nada sincronizaba el juego con la pantalla. Corría a 70 y la pantalla mostraba 60 de esos cuadros de forma desigual. Ahora `N3DS_Flip` espera el vblank (salvo al cerrar desde HOME) y `CalcTics` ya no duerme.
- **Mapa en la pantalla de abajo.** El original no tiene mapa. El motor marca en `spotvis` las casillas que se ven en cada cuadro (y lo borra al siguiente); el port las acumula en un arreglo propio que se limpia al empezar cada nivel. Paredes y puertas aparecen cuando se vio una casilla vecina. Con la vista a pantalla completa va junto a la barra de estado; con una vista más pequeña ocupa toda la pantalla de abajo. Se guarda en la configuración (opción y contador de FPS) detrás de los campos anteriores; las configuraciones viejas quedan con mapa y estadísticas arriba.
- **Guardar sin esperas.** Las partidas se borraban y se creaban de nuevo (`unlink` + `fopen "wb"`), y el selector reescribía `last-game.txt` en cada arranque: lo mismo que congelaba Blake Stone 8 segundos. Ahora se escriben encima (`"r+b"`) y se recortan al final con `ftruncate`.

## Estado

Probado en New 3DS: Wolfenstein 3D, Spear of Destiny y el `.cia` combinado (v1.4.0: mapa, 60 FPS y guardado probados).

## Pendiente

- Probar el shareware y la demo de SoD en hardware.
- Guardar lo explorado en las partidas (al cargar, el mapa empieza vacío).
- Siguiente: Chocolate Doom (su automapa irá a la pantalla de abajo).
