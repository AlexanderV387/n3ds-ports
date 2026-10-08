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

## Pendiente

- Probar Spear of Destiny y el shareware (solo se probó Wolfenstein completo).
- Siguiente port: Chocolate Doom (Doom, Heretic, Hexen), con este mismo estándar de controles.
