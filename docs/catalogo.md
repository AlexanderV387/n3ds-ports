# Catálogo de ports

Ideas ordenadas por dificultad. Antes de empezar cualquiera, buscar en GBAtemp y GitHub si ya hay un port en curso.

Investigación del 7 de octubre de 2026; las listas consultadas no son exhaustivas.

## Nivel 1: base ya existente o SDL puro

| Juego | Base posible | Estado |
|---|---|---|
| Doom, Heretic, Hexen, Strife (y mods del formato original) | Crispy Doom | En curso |
| Mods de Doom en formato Boom/MBF | Woof! | Largo plazo |
| Doom 64 | Por definir | Pendiente |
| Dune II | Por definir | Pendiente |
| Half-Life: Opposing Force y Blue Shift | Xash3DS | Probar primero sobre el port existente |

## Nivel 2: más trabajo

| Juego | Estado |
|---|---|
| Command & Conquer: Tiberian Dawn | Pendiente (código GPL de EA, Vanilla-Conquer) |
| Command & Conquer: Red Alert | Pendiente (código GPL de EA, Vanilla-Conquer) |
| Warcraft II | Pendiente |
| Fallout 2 | Pendiente |
| Tomb Raider II | Pendiente |
| Tomb Raider III | Pendiente |
| OpenBOR 3DS (mejorar el port existente) | Pendiente |
| Bugdom 2 | Pendiente |
| Otto Matic | Pendiente |
| Hexen II | Pendiente |

## Nivel 3: retos grandes

Heretic II, Jedi Outcast, Jedi Academy, Return to Castle Wolfenstein, Serious Sam, Brutal Doom (necesita un motor de la familia ZDoom), Brutal Doom Lite, Nanosaur 2, Silent Hill, MediEvil, Driver 2, Blood Omen, Banjo-Kazooie, Diddy Kong Racing y Perfect Dark.

## Nivel 4: largo plazo

1. **Motor compatible con MUGEN (prioridad).** No es un port, porque MUGEN es cerrado: hay que escribir un motor compatible, con Ikemen GO como referencia (revisar su licencia antes). Meta: 60 fps con dos personajes y efectos usando contenido convertido con una herramienta de PC que aligere sprites y paletas. El motor no distribuye contenido de terceros.
2. Age of Empires II
3. Age of Mythology
4. Juego tipo Dragon Ball 3D (no hay código ni decompilación conocidos, sería un juego propio)
5. Donkey Kong 64: como GoldenEye, por su decompilación (revisar en qué va), no por emulación.
6. Dinosaur Planet
7. **PS1 con la GPU de la 3DS.** Un renderizador con citro3d para PCSX ReARMed: hoy dibuja por software (Unai) y muchos juegos ya van a 60 en New 3DS, pero los pesados no. Lo aprendido con la GPU en DSDA-Doom sirve aquí. Su renderizador serviría también para los arcades 3D basados en el hardware de PS1: Namco System 11 (Tekken, Tekken 2, Soul Edge) y Capcom ZN-1/ZN-2 (Street Fighter EX), aunque cada placa necesita además su propio emulador (CPU, sonido, protecciones).
8. **GoldenEye 007, nativo.** Su decompilación llegó al 100% en 2026 y ya hay ports de PC; Perfect Dark (mismo motor) está decompilado y tiene port de PC (fgsfds). El camino es un port nativo como el de Super Mario 64 en 3DS (30 fps), con los gráficos de N64 traducidos a citro3d, no un emulador: emular el N64 completo no alcanza en la 3DS.
9. **N64Recomp en 3DS (experimento).** [N64Recomp](https://github.com/N64Recomp/N64Recomp) (Mr-Wiseguy, MIT) traduce la ROM completa a C de una vez, sin decompilarla a mano; en PC dibuja con RT64 (Direct3D 12/Vulkan). Para la 3DS faltaría: un renderizador de las listas de dibujo del N64 con citro3d (el mismo de GoldenEye), el audio y el ajuste por juego. Primero medir con un juego ya recompilado si el ARM11 llega a 30 fps.

## Lo que ya existe en 3DS

Estos juegos ya tienen port, así que no conviene repetirlos salvo para mejorarlos:

| Juego | Proyecto |
|---|---|
| GTA III, Vice City, Liberty City Stories | re3, reVC, reLCS (solo New 3DS) |
| Fallout 1 | Fallout 1 CE 3DS (MrHuu), proof of concept |
| Half-Life | Xash3DS |
| Quake 1, 2 y 3 | ctrQuake, Quake2CTR, ioQuake3DS |
| Duke Nukem 3D | EDuke3D, dn3ds |
| Shadow Warrior | JFShadowWarrior (MrHuu), en desarrollo |
| Doom | PrBoom+ 3DS (Voxel; PrBoom+ 2.6.66, OpenGL con 3D estereoscópico, mods Boom/MBF; no cubre Heretic ni Hexen) |
| Diablo | DevilutionX 3DS, Devil-3Ds |
| Super Mario 64 | Port basado en la decompilación, 30 fps |
| Mario Kart 64 | EstebanPdN |
| Bugdom | Basado en el port de Jorio |
| Nanosaur 2 | ColemanCDA, en Swift, en desarrollo |
| OpenBOR | MrHuu, v0.0.6 (2022), cuelgues y carga lenta |
| Tomb Raider 1 | OpenLara 3DS |

## Descartados

| Juego | Motivo |
|---|---|
| Mina the Hollower | Juego comercial nuevo (Yacht Club Games, 2025) sin código abierto ni decompilación: no hay base para portarlo |

## Riesgo legal por tipo de base

- **Motor con licencia libre (GPL, BSD):** lo más seguro. Con GPL hay que publicar el código de las modificaciones.
- **Licencias con límites:** por ejemplo, Fallout 1 CE usa Sustainable Use License, que limita el uso comercial.
- **Decompilaciones de juegos comerciales:** lo más delicado, sobre todo con propiedad intelectual de Nintendo (Donkey Kong 64, juegos de Rare).
- **Assets:** nunca se distribuyen.

Esto es orientación general, no asesoría legal. Manda la licencia de cada repositorio.
