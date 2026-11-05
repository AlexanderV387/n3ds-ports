# Instalación de los ports terminados

Cómo instalar cada port, dónde van los archivos del juego en la SD y qué archivos se han probado de verdad en una New 3DS.

Ningún port trae los archivos del juego: cada persona usa su propia copia (o la versión gratuita, cuando existe).

## Método de instalación (igual en todos)

Cada release trae dos archivos; basta con uno:

| Archivo | Cómo se usa |
|---|---|
| `.cia` | Se instala con **FBI** y aparece en el menú HOME, con su icono y banner |
| `.3dsx` | Se copia a `/3ds/` en la SD y se abre desde el **Homebrew Launcher** |

Los dos usan la misma carpeta de datos. Se pueden tener instalados a la vez.

Al arrancar, si hay más de un juego (o mods), un menú deja elegir. Si hay solo uno, entra directo. En el `.cia`, salir del juego vuelve a ese menú.

La configuración, las partidas guardadas y el log se guardan en la misma carpeta del juego.

## Wolfenstein 3D y Spear of Destiny (Wolf4SDL)

Release: [wolf4sdl-3ds](https://github.com/AlexanderV387/wolf4sdl-3ds/releases). Archivos: `wolf4sdl-all.cia` o `wolf4sdl-all.3dsx` (todos los juegos en uno).

| Juego | Archivos | Carpeta en la SD |
|---|---|---|
| Wolfenstein 3D v1.4 (Steam, GOG) | `*.wl6` | `/3ds/wolf4sdl/wolf3d/` |
| Wolfenstein 3D shareware v1.4 (gratis) | `*.wl1` | `/3ds/wolf4sdl/wolf3d/` |
| Spear of Destiny (Steam, GOG) | `*.sod` | `/3ds/wolf4sdl/sod/` |
| Misiones 2 y 3 de Spear of Destiny | `*.sd2`, `*.sd3` | `/3ds/wolf4sdl/sod/` |
| Demo de Spear of Destiny (gratis) | `*.sdm` | `/3ds/wolf4sdl/sod/` |

**Probado en hardware:**

- Wolfenstein 3D, datos de Steam.
- Spear of Destiny.

**Sin probar:** el shareware, la demo de Spear of Destiny y las misiones 2 y 3.

## Blake Stone: Aliens of Gold y Planet Strike (BStone)

Release: [bstone](https://github.com/AlexanderV387/bstone/releases). Archivos: `bstone.cia` o `bstone.3dsx`.

Todo va en `/3ds/bstone/`:

| Juego | Archivos |
|---|---|
| Aliens of Gold shareware (gratis) | `*.BS1` |
| Aliens of Gold completo (Steam, GOG) | `*.BS6` |
| Planet Strike (Steam, GOG) | `*.VSI` |

**Probado en hardware:**

- Planet Strike.
- Aliens of Gold shareware v3.0.

**Sin probar:** Aliens of Gold completo (`*.BS6`).

## Crispy Doom y Crispy Strife

Release: [crispy-doom](https://github.com/AlexanderV387/crispy-doom/releases). Archivos: `crispy-doom.cia`/`.3dsx` y `crispy-strife.cia`/`.3dsx`.

| Juego | Archivos | Carpeta en la SD |
|---|---|---|
| The Ultimate Doom | `doom.wad` | `/3ds/crispy-doom/` |
| Doom shareware (gratis) | `doom1.wad` | `/3ds/crispy-doom/` |
| Doom II | `doom2.wad` | `/3ds/crispy-doom/` |
| Final Doom | `plutonia.wad`, `tnt.wad` | `/3ds/crispy-doom/` |
| [Freedoom](https://freedoom.github.io/) (gratis) | `freedoom1.wad`, `freedoom2.wad`, `freedm.wad` | `/3ds/crispy-doom/` |
| Otros | `chex.wad`, `hacx.wad`, `rekkrsa.wad` | `/3ds/crispy-doom/` |
| Mods | `.wad`, `.deh`, `.bex` | `/3ds/crispy-doom/mods/` |
| Strife (Veteran Edition de Steam o GOG) | `strife1.wad` y `voices.wad` | `/3ds/crispy-strife/` |

Crispy Doom corre mods vanilla y limit-removing. Los mods Boom/MBF van en DSDA-Doom.

**Probado en hardware:**

- IWADs: `doom1.wad`, `doom2.wad`, `freedoom1.wad` y `freedoom2.wad`.
- Strife: `strife1.wad` y `voices.wad`, de GOG.
- Mods:
  - D4V (`D4V.wad`, `D4V.deh`, más `D4V-3_HELLST.deh` y `D4V-3_REAPER.deh`);
  - `SD21.wad` con `SD21-BloodPatch.wad`;
  - `eviternity.wad`, `nuts.wad`, `nuts3.wad`, `planisf2.wad` y `frozent.wad`;
  - `d2spfx20.wad` con `d2dehfix.deh`;
  - `mensajes-espanol.bex`.

**Sin probar:** `doom.wad`, Final Doom, `freedm.wad`, Chex Quest, HACX y REKKR.

## DSDA-Doom, Heretic y Hexen

Release: [dsda-doom](https://github.com/AlexanderV387/dsda-doom/releases). Son tres títulos, cada uno con su carpeta:

| Archivo | Carpeta en la SD | Mods en |
|---|---|---|
| `dsda-doom.cia` o `dsda-doom.3dsx` | `/3ds/dsda-doom/` | `/3ds/dsda-doom/mods/` |
| `heretic.cia` | `/3ds/heretic/` | `/3ds/heretic/mods/` |
| `hexen.cia` | `/3ds/hexen/` | `/3ds/hexen/mods/` |

Los mods pueden ser `.wad`, `.deh`, `.bex` o `.zip`. El `.cia` (o `.3dsx`) de DSDA-Doom también juega Heretic y Hexen si sus archivos están en `/3ds/dsda-doom/`; ahí sus mods van en `/3ds/dsda-doom/mods/heretic/` y `/3ds/dsda-doom/mods/hexen/`.

Si la carpeta de mods está vacía (o los mods están en otra carpeta), no aparece la pantalla de mods: después de elegir el juego, arranca directo.

**DSDA-Doom:** los mismos IWADs que Crispy Doom (tabla de arriba), más mods Boom, MBF, MBF21 y UMAPINFO.

**Heretic**, en `/3ds/heretic/`:

| Juego | Archivos |
|---|---|
| Heretic (registrado o Shadow of the Serpent Riders) | `heretic.wad` |
| Heretic shareware (gratis) | `heretic1.wad` |
| Enhanced Maps (remaster de 2025) | `heretic.wad` y `heretic_ex.wad` |
| Faith Renewed (remaster de 2025) | `heretic.wad` y `heretic_fr.wad` |

**Hexen**, en `/3ds/hexen/`:

| Juego | Archivos |
|---|---|
| Hexen | `hexen.wad` |
| Deathkings of the Dark Citadel | `hexen.wad` y `hexdd.wad` |
| Hexen, Enhanced Maps (remaster de 2025) | `hexen.wad` y `hexen_ex.wad` |
| Deathkings, Enhanced Maps (remaster de 2025) | `hexen.wad` y `hexdd_ex.wad` |
| Vestiges of Grandeur (remaster de 2025) | `hexen.wad` y `hexen_vog.wad` |

Los archivos del remaster (Heretic + Hexen de Nightdive, Steam o GOG) se copian de su carpeta de instalación.

**Probado en hardware:**

- **DSDA-Doom:**
  - los mismos IWADs y mods que en Crispy Doom;
  - Eviternity con `freedoom2.wad`.
- **Heretic:**
  - `heretic.wad` y `heretic1.wad` (shareware);
  - `heretic_ex.wad` y `heretic_fr.wad`, del remaster de GOG;
  - el mod `HTIC_V12_2.zip`.
- **Hexen:** `hexen.wad`, `hexdd.wad`, `hexen_ex.wad`, `hexdd_ex.wad` y `hexen_vog.wad`, del remaster de GOG.

**Sin probar:** Final Doom, Chex Quest, HACX y REKKR en DSDA-Doom.

## Duke Nukem 3D (EDuke32)

Release: [NBlood](https://github.com/AlexanderV387/NBlood/releases). Archivos: `duke3d.cia` o `eduke32.3dsx`.

| Juego | Archivo | Carpeta en la SD |
|---|---|---|
| Duke Nukem 3D shareware 1.3d (gratis, episodio 1) | `DUKE3D.GRP` | `/3ds/eduke32/` |
| Duke Nukem 3D completo, Atomic Edition o World Tour | `DUKE3D.GRP` | `/3ds/eduke32/` |

**Probado en hardware:** solo el shareware 1.3d (`DUKE3D.GRP` de `3dduke13SW.zip`).

**Sin probar:** el juego completo, Atomic Edition y World Tour. Corren en EDuke32 en PC, pero partes pueden no funcionar en la 3DS.

**Problema conocido:** guardar partida es muy lento. Está anotado y sin investigar.
