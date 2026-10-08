# n3ds-ports

Ports de juegos clásicos a la **New Nintendo 3DS**, optimizados para aprovechar lo que casi ningún port usa: C-stick, ZL/ZR, pantalla táctil, giroscopio y los núcleos y la caché extra de la New 3DS.

El objetivo es aprender C/C++, render y optimización con poca RAM, y dejar trabajo verificable: código, mediciones de antes y después y un devlog técnico por proyecto.

## Estado

| Proyecto | Repo | Estado |
|---|---|---|
| Hola mundo (devkitPro + SDL2) | [`hello-world/`](hello-world/) | Funciona en New 3DS: 59,8 FPS estables con vsync |
| Wolfenstein 3D y Spear of Destiny | [wolf4sdl-3ds](https://github.com/AlexanderV387/wolf4sdl-3ds) (rama `n3ds`) | Terminado: doble stick, giro táctil, botones reasignables, HUD abajo, `.cia` |
| Chocolate Doom (Doom, Heretic, Hexen) | Fork propio, pendiente | No iniciado |
| Motor compatible con MUGEN | Pendiente | Largo plazo |

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

Para empaquetar cualquier port como `.cia` está [`tools/3ds/make-cia.sh`](tools/3ds/make-cia.sh), que usa makerom, bannertool y la plantilla RSF de [buildtools](https://github.com/Steveice10/buildtools) (MIT). Activa siempre los modos de New 3DS: 804 MHz, caché L2 y 124 MB de RAM.

## Reglas del proyecto

- **Rendimiento:** solo cuentan las mediciones hechas en una New 3DS real; los emuladores pueden comportarse distinto.
- **Assets:** nunca se distribuyen archivos de juegos. Cada persona aporta los suyos.
- **Licencias:** cada port conserva la licencia del proyecto base y acredita a sus autores.
- **Uso de IA:** este proyecto se desarrolla con ayuda de IA (Claude). Las partes centrales de cada port (bucle de render, memoria, bugs difíciles) se estudian y documentan a mano en el devlog.

## Licencia

El código propio de este repo se publica bajo licencia MIT (ver [`LICENSE`](LICENSE)). Los ports en repos separados mantienen la licencia de su proyecto base, normalmente GPL.
