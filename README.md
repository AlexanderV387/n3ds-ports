# n3ds-ports

Ports de juegos clásicos a la **New Nintendo 3DS**, optimizados para aprovechar lo que casi ningún port usa: C-stick, ZL/ZR, pantalla táctil, giroscopio y los núcleos y la caché extra de la New 3DS.

El objetivo es aprender C/C++, render y optimización con poca RAM, y dejar trabajo verificable: código, mediciones de antes y después y un devlog técnico por proyecto.

## Por qué existe

La 3DS, a diferencia de la DS, casi no tuvo shooters ni juegos occidentales de ese estilo: la mayoría de su catálogo fueron aventuras y RPG. Y casi nada aprovechó la New 3DS: muchos juegos ni siquiera usaban el C-stick.

Los ports que faltaban no salían porque, para quien podía hacerlos, no compensaban cientos de horas por juegos de nicho, y la curva de aprendizaje (C y C++ en una consola, con su GPU, su memoria y sus límites) dejaba fuera a casi todos los demás. Con la ayuda de la IA ese costo bajó lo suficiente para que este proyecto sea posible.

Cada port sigue el mismo estándar, pensado para la New 3DS como debió aprovecharse:

- **C-stick para la cámara** y controles reasignables;
- **modo New 3DS siempre**: 804 MHz, caché L2 y 124 MB de RAM;
- **60 FPS** como meta;
- **la pantalla de abajo con uso real**: HUD, mapa y menús;
- **`.cia` instalable**, con su icono y banner en el menú HOME.

Todo se prueba en una New 3DS real, con logs y mediciones, antes de publicarse.

**Solo New 3DS y New 2DS XL.** Los ports no se han pensado ni probado para la Old 3DS o 2DS: ahí pueden ir muy lentos, quedarse sin memoria en mapas grandes o no arrancar.

## Estado

| Proyecto | Repo | Estado |
|---|---|---|
| Hola mundo (devkitPro + SDL2) | [`hello-world/`](hello-world/) | Funciona en New 3DS: 59,8 FPS estables con vsync |
| Wolfenstein 3D y Spear of Destiny | [wolf4sdl-3ds](https://github.com/AlexanderV387/wolf4sdl-3ds) (rama `n3ds`) | Terminado ([v1.7.0](https://github.com/AlexanderV387/wolf4sdl-3ds/releases/tag/v1.7.0)): 60 FPS a 800x240 (el modo ancho de la pantalla de arriba), doble stick, giro táctil, botones reasignables, HUD y mapa con zoom abajo, teclado y botones de armas táctiles, todos los juegos en un `.cia` con menú |
| Blake Stone (Aliens of Gold, Planet Strike) | [bstone](https://github.com/AlexanderV387/bstone) (rama `n3ds`) | [v1.3.0](https://github.com/AlexanderV387/bstone/releases/tag/n3ds-v1.3.0): 60 FPS a 800x240, HUD y mapa con zoom abajo, teclado y botones de armas táctiles, vista 3D a pantalla completa, `.cia` |
| Crispy Doom (Doom, Doom II, Final Doom, Freedoom) | [crispy-doom](https://github.com/AlexanderV387/crispy-doom) (rama `n3ds`) | [n3ds-v1.1.0](https://github.com/AlexanderV387/crispy-doom/releases/tag/n3ds-v1.1.0): 60 FPS (mínimo 57; Freedoom 54), barra de estado y automapa con zoom abajo, botones reasignables, giro táctil, selector de juego y mods, `.cia` ([devlog](docs/devlog/2026-10-10-crispy-doom.md)). Base de Heretic, Hexen y Strife |
| Strife | [crispy-doom](https://github.com/AlexanderV387/crispy-doom) (rama `n3ds`, `crispy-strife`) | Publicado con Crispy Doom ([n3ds-v1.1.0](https://github.com/AlexanderV387/crispy-doom/releases/tag/n3ds-v1.1.0)): voces, inventario táctil, teclado en pantalla |
| DSDA-Doom (mods Boom/MBF/MBF21, DeHackEd) | [dsda-doom](https://github.com/AlexanderV387/dsda-doom) (rama `n3ds`) | [n3ds-dsda-doom-v1.1.0](https://github.com/AlexanderV387/dsda-doom/releases/tag/n3ds-dsda-doom-v1.1.0): renderizador por GPU (una capa OpenGL sobre citro3d) a 800x240, 60 FPS, selector de campañas y complementos con avisos de mods incompatibles, pantalla de abajo con barra de estado, mapa y botones de armas, `.cia` y `.3dsx`. Los mods pesados (Smooth Doom) bajan en peleas grandes |
| Heretic | [dsda-doom](https://github.com/AlexanderV387/dsda-doom) (rama `n3ds`), su propio `.cia` | [n3ds-heretic-v1.1.0](https://github.com/AlexanderV387/dsda-doom/releases/tag/n3ds-heretic-v1.1.0): shareware, completo (5 episodios) y el `heretic.wad` del remaster de Nightdive, a 60 FPS. Faith Renewed, el episodio del remaster, también; su mapa secreto (E1M9) baja a unos 10 FPS con las hordas |
| Hexen y Deathkings of the Dark Citadel | [dsda-doom](https://github.com/AlexanderV387/dsda-doom) (rama `n3ds`), su propio `.cia` | [n3ds-hexen-v1.1.0](https://github.com/AlexanderV387/dsda-doom/releases/tag/n3ds-hexen-v1.1.0): las tres clases, hubs, salto, 60 FPS (bajón breve con el Arc of Death). Vestiges of Grandeur, el episodio del remaster, y los Enhanced Maps también; el MAP07 de Vestiges baja a unos 10 FPS con las hordas |
| Duke Nukem 3D | [NBlood](https://github.com/AlexanderV387/NBlood) (rama `n3ds`), EDuke32 | [n3ds-duke3d-v1.0.0](https://github.com/AlexanderV387/NBlood/releases/tag/n3ds-duke3d-v1.0.0): renderizado por software o por GPU (Polymost sobre la capa OpenGL de DSDA-Doom, a 800x240 en el modo ancho), barra de estado, mapa, teclado y botones de armas en la pantalla de abajo, botones reasignables, giro táctil, `.cia` y `.3dsx` |
| Motor compatible con MUGEN | Pendiente | [Investigado](docs/investigacion-mugen.md): portar Dolmexica Infinite (C++, MIT) a la 3DS, con Ikemen GO como referencia |

## Plan

1. **Crispy Doom** ([1.1.0](https://github.com/AlexanderV387/crispy-doom/releases/tag/n3ds-v1.1.0)): Doom como era en DOS, en pantalla ancha, y **Strife**, el único juego del motor que DSDA-Doom no soporta. Ya existe [PrBoom+ para 3DS](https://db.universal-team.net/3ds/prboom) (Voxel), con OpenGL, 3D estereoscópico y mods Boom/MBF; este port apunta al estándar del proyecto (pantalla de abajo, controles) y a 60 FPS.
2. **DSDA-Doom, Heretic y Hexen:** el port principal para mods (original, Boom, MBF, MBF21, UMAPINFO, UDMF), con renderizador por GPU: una capa que imita OpenGL sobre citro3d. Heretic y Hexen van en sus propios `.cia`. **Faith Renewed** (Heretic) y **Vestiges of Grandeur** (Hexen), los episodios del remaster de Nightdive (2025), ya se juegan. Publicados ([DSDA-Doom](https://github.com/AlexanderV387/dsda-doom/releases/tag/n3ds-dsda-doom-v1.0.1), [Heretic](https://github.com/AlexanderV387/dsda-doom/releases/tag/n3ds-heretic-v1.0.1), [Hexen](https://github.com/AlexanderV387/dsda-doom/releases/tag/n3ds-hexen-v1.0.1)). Más adelante: optimizar los mapas con hordas (dibujo en otro núcleo, movimiento de monstruos más barato).
3. **Duke Nukem 3D** con EDuke32, tomado del repositorio de [NBlood](https://github.com/NBlood/NBlood), que trae EDuke32 completo y los demás juegos del motor Build. EDuke32 soporta World Tour (episodio 5, Incinerator, Firefly) y es el motor con más mods de Duke. Primero el renderizado por software, para que arranque y medir; luego Polymost (su modo OpenGL) sobre la capa OpenGL de DSDA-Doom, para 60 FPS. Desarrollo con el shareware (episodio 1, gratis). Ya hay ports en 3DS (EDuke3D, abandonado; dn3ds, del código de 1997); este apunta al estándar del proyecto. Un `.cia` por juego, como Heretic y Hexen. Publicado ([n3ds-duke3d-v1.0.0](https://github.com/AlexanderV387/NBlood/releases/tag/n3ds-duke3d-v1.0.0)). **En pausa hasta después de MUGEN:** Blood, Redneck Rampage, Shadow Warrior y Exhumed, del mismo repositorio; heredan casi todo lo de Duke (motor, video, controles) y cada uno lleva su pantalla de abajo, menú, armas e inventario.
4. **Motor compatible con MUGEN,** al terminar Duke ([investigación](docs/investigacion-mugen.md): portar Dolmexica Infinite, con Ikemen GO como referencia), como descanso del 3D: MUGEN es cerrado e Ikemen GO está en Go con OpenGL, así que es un motor propio, con sprites escalados, transparencias y paletas por GPU. Meta: 60 FPS con dos personajes y efectos.
5. **PS1 con la GPU:** un renderizador con citro3d para PCSX ReARMed, para los juegos pesados que hoy no llegan a 60 dibujando por software.
6. **Arcades 3D basados en PS1** (Namco System 11: Tekken, Soul Edge; Capcom ZN: Street Fighter EX): el renderizador de PS1 sirve tal cual, pero cada placa necesita su emulador (CPU, sonido, protecciones), que PCSX ReARMed no trae.
7. **N64:** primero medir si un juego recompilado con N64Recomp corre a 30 FPS en el ARM11; luego el renderizador de N64 con citro3d, para GoldenEye nativo (decompilado al 100%) o N64Recomp. Donkey Kong 64 por el camino que madure primero.
8. **Largo plazo:**
   - **Brutal Doom:** necesita un motor de la familia ZDoom (DECORATE o ZScript; ningún port Boom/MBF lo corre). Investigar ZDoom 2.8 con Brutal Doom v20; probablemente lento en peleas grandes.
   - Return to Castle Wolfenstein y Enemy Territory.

Pendientes pequeños:

- **Opción clásica** (apagada por defecto) para dejar las barras de estado en la pantalla de arriba, según el estándar: volver a ponerla en Blake Stone (se quitó en 1.2.0) y agregarla en Wolfenstein 3D, Crispy Doom y DSDA-Doom.
- **Crispy Doom:** quitar la posición en medio de la barra de estado (solo arriba o abajo), como en Wolfenstein 3D.
- **Inventario táctil** en Heretic y Hexen (DSDA-Doom), como en Strife.
- Opción **Auto Fire** (apagada por defecto) en Wolfenstein 3D y Blake Stone: que la pistola y el cuchillo disparen seguido al mantener el botón. Por defecto siguen como en DOS, un disparo por presión.

Todos los FPS siguen el [estándar de controles](docs/controles-fps.md): 60 FPS, HUD y mapa en la pantalla de abajo (el mapa se puede ocultar), doble stick, cámara táctil, botones reasignables, teclado y botones de armas táctiles, y ajustes guardados al cerrar el menú.

El catálogo completo, con 33 ideas en 4 niveles, está en [`docs/catalogo.md`](docs/catalogo.md).

## Cómo está organizado

- **Este repo** concentra el catálogo, el registro de rendimiento, el devlog y los experimentos pequeños.
- **Cada port serio vive en su propio repo**, como fork del proyecto original. Así se respeta su licencia, el historial muestra qué cambió y los arreglos útiles pueden volver al proyecto original como pull request.

```
docs/
  catalogo.md       candidatos por nivel y qué ya existe
  rendimiento.md    mediciones en hardware real, antes y después
  aprendizaje.md    plan de aprendizaje y cómo comprobar cada paso
  controles-fps.md  estándar de controles para todos los FPS del proyecto
  devlog/           una entrada por avance importante
hello-world/        primer programa: toolchain, bucle principal, entrada y FPS
tools/3ds/          empaquetado .cia reutilizable para todos los ports
```

## Compilar

Hace falta [devkitPro](https://devkitpro.org/wiki/Getting_Started) con devkitARM, libctru y SDL2 para 3DS:

```sh
dkp-pacman -S 3ds-dev
dkp-pacman -Ss sdl   # buscar el paquete de SDL2 para 3DS; si no hay, ver .github/workflows/build.yml
cd hello-world
cmake -B build -DCMAKE_TOOLCHAIN_FILE="$DEVKITPRO/cmake/3DS.cmake"
cmake --build build
```

Se genera `build/hello_n3ds.3dsx`. Cópialo a `/3ds/` en la SD y ábrelo desde el Homebrew Launcher.

GitHub Actions compila el proyecto en cada push con la imagen oficial `devkitpro/devkitarm` y deja como artefactos descargables el `.3dsx` (para el Homebrew Launcher) y el `.cia` (se instala con FBI y aparece en el menú HOME).

En las sesiones de Claude Code en la nube se compila con [`tools/3ds/build-local.sh`](tools/3ds/build-local.sh), que usa la misma imagen Docker `devkitpro/devkitarm` que GitHub Actions: los servidores de paquetes de devkitPro bloquean esas máquinas (Cloudflare), así que devkitPro no se puede instalar directo.

Para empaquetar cualquier port como `.cia` está [`tools/3ds/make-cia.sh`](tools/3ds/make-cia.sh), que usa makerom, bannertool y la plantilla RSF de [buildtools](https://github.com/Steveice10/buildtools) (MIT). Activa siempre los modos de New 3DS: 804 MHz, caché L2 y 124 MB de RAM.

## Reglas del proyecto

- **Rendimiento:** solo cuentan las mediciones hechas en una New 3DS real; los emuladores pueden comportarse distinto.
- **Assets:** nunca se distribuyen archivos de juegos. Cada persona aporta los suyos.
- **Licencias:** cada port conserva la licencia del proyecto base y acredita a sus autores.
- **Uso de IA:** este proyecto se desarrolla con ayuda de IA (Claude). Las partes centrales de cada port (bucle de render, memoria, bugs difíciles) se estudian y documentan a mano en el devlog.

## Licencia

El código propio de este repo se publica bajo licencia MIT (ver [`LICENSE`](LICENSE)). Los ports en repos separados mantienen la licencia de su proyecto base, normalmente GPL.

## Créditos

Dirección, diseño y pruebas en hardware: AlexanderV387. Código: escrito con Claude (IA). Motor original: el de cada port (Wolf4SDL, BStone, Crispy Doom, DSDA-Doom; ver su repo). El arte de iconos y banners se hizo con herramientas de IA.

El uso de IA se dice abiertamente, como pide la comunidad (Universal-DB marca los proyectos con contenido generado por IA): lo que se publica aquí se prueba en una New 3DS real, con logs y mediciones.
