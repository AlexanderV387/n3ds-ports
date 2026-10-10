# n3ds-ports

Ports de juegos clásicos a la **New Nintendo 3DS**, optimizados para aprovechar lo que casi ningún port usa: C-stick, ZL/ZR, pantalla táctil, giroscopio y los núcleos y la caché extra de la New 3DS.

El objetivo es aprender C/C++, render y optimización con poca RAM, y dejar trabajo verificable: código, mediciones de antes y después y un devlog técnico por proyecto.

## Estado

| Proyecto | Repo | Estado |
|---|---|---|
| Hola mundo (devkitPro + SDL2) | [`hello-world/`](hello-world/) | Funciona en New 3DS: 59,8 FPS estables con vsync |
| Wolfenstein 3D y Spear of Destiny | [wolf4sdl-3ds](https://github.com/AlexanderV387/wolf4sdl-3ds) (rama `n3ds`) | Terminado ([v1.4.1](https://github.com/AlexanderV387/wolf4sdl-3ds/releases/tag/v1.4.1)): 60 FPS, doble stick, giro táctil, botones reasignables, HUD y mapa abajo, todos los juegos en un `.cia` con menú |
| Blake Stone (Aliens of Gold, Planet Strike) | [bstone](https://github.com/AlexanderV387/bstone) (rama `n3ds`) | [v1.0.4](https://github.com/AlexanderV387/bstone/releases/tag/n3ds-v1.0.4): 60 FPS, HUD y mapa abajo, vista 3D a pantalla completa, `.cia` |
| Crispy Doom (Doom, Doom II, Final Doom, Freedoom) | [crispy-doom](https://github.com/AlexanderV387/crispy-doom) (rama `n3ds`) | [n3ds-v1.0.0](https://github.com/AlexanderV387/crispy-doom/releases/tag/n3ds-v1.0.0): 60 FPS (mínimo 57; Freedoom 54), barra de estado y automapa con zoom abajo, botones reasignables, giro táctil, selector de juego y mods, `.cia` ([devlog](docs/devlog/2026-10-10-crispy-doom.md)). Base de Heretic, Hexen y Strife |
| DSDA-Doom (mods Boom/MBF/MBF21, Heretic, Hexen) | Pendiente | Siguiente: el port principal para mods |
| Duke Nukem 3D | Pendiente | Siguiente |
| Motor compatible con MUGEN | Pendiente | Después de Duke Nukem 3D |

## Plan

1. **Crispy Doom** ([1.0.0](https://github.com/AlexanderV387/crispy-doom/releases/tag/n3ds-v1.0.0)): Doom como era en DOS, en pantalla ancha, con los mods del formato original y de límites ampliados. Queda como la base de **Strife** y de **Hexen** (completo en Crispy). Ya existe [PrBoom+ para 3DS](https://db.universal-team.net/3ds/prboom) (Voxel), con OpenGL, 3D estereoscópico y mods Boom/MBF; este port apunta al estándar del proyecto (pantalla de abajo, controles) y a 60 FPS.
2. **DSDA-Doom:** el port principal para mods: Doom con todos los formatos (original, Boom, MBF, MBF21, UMAPINFO, UDMF), Heretic y mods de Hexen. Sucesor de PrBoom+. Primera etapa por software, sin su OpenGL (2.0 con shaders, que la GPU de la 3DS no tiene), reutilizando la capa de 3DS de Crispy.
3. **La GPU para mostrar la imagen** (citro3d), como módulo compartido para todos los ports: libera el núcleo 1, que hoy compone las pantallas (~3 ms por cuadro).
4. **Dibujo repartido entre dos núcleos**, para la alta resolución a 60 FPS (hoy 25-31 ms por cuadro, 30 FPS) en Crispy y DSDA-Doom. Opción experimental.
5. **DSDA-Doom con la GPU de la 3DS:** un renderizador nativo con citro3d (texturas a color, luz por vértice y la niebla del hardware), como opción experimental: resolución nativa, cámara real y 3D estereoscópico.
6. **Duke Nukem 3D:** ya hay ports (EDuke3D, dn3ds); el nuestro aplicaría el estándar. Su renderizador Polymost (OpenGL antiguo) es el candidato más realista para dibujar con la GPU.
7. **Motor compatible con MUGEN:** MUGEN es cerrado y Ikemen GO está en Go con OpenGL, así que es otro tipo de proyecto, más grande.
8. **Largo plazo:**
   - **Brutal Doom:** necesita un motor de la familia ZDoom (DECORATE o ZScript; ningún port Boom/MBF lo corre). Investigar ZDoom 2.8 con Brutal Doom v20; probablemente lento en peleas grandes.
   - Return to Castle Wolfenstein y Enemy Territory.

Todos los FPS siguen el [estándar de controles](docs/controles-fps.md): 60 FPS, HUD y mapa en la pantalla de abajo, doble stick y botones reasignables.

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
