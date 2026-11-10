# Hechos verificados de la 3DS (para Catequilla)

Cada hecho dice **de dónde sale**. Antes de afirmar algo sobre una API de libctru o citro3d que no esté aquí, léelo en el código fuente local (`~/work/refs/citro3d`, `~/work/refs/libctru`) y cita archivo y línea. Si no lo encuentras, dilo como **hipótesis**, nunca como hecho.

Versiones leídas: citro3d `9f21cf7` (oct. 2023, la que trae devkitPro 3ds-dev), libctru `62b7c42` (nov. 2025).

Cuando se compruebe un hecho nuevo, se añade aquí con su fuente. Si uno resulta falso, se tacha y se explica por qué.

## citro3d: fotogramas

| # | Hecho | Fuente |
|---|---|---|
| F1 | `C3D_FrameBegin(flags)` devuelve `false` **sin hacer nada** si el fotograma anterior no se cerró (`inFrame` sigue activo). | `citro3d/source/renderqueue.c`, `C3D_FrameBegin` |
| F2 | Con `C3D_FRAME_SYNCDRAW`, primero espera a que pasen las vblank de **las dos** pantallas (`C3D_FrameSync`). Después espera a que la cola de la GPU termine: para siempre, o nada si va con `C3D_FRAME_NONBLOCK` (devuelve `false` si sigue ocupada). | ídem, `C3D_FrameBegin` y `C3D_FrameSync` |
| F3 | `C3D_FrameEnd(flags)`: `flags` son **opciones de la lista de comandos GX** (se pasan a `C3D_FrameSplit`), **no un tiempo de espera**. `C3D_FrameEnd(-1)` no espera nada. | ídem, `C3D_FrameEnd` |
| F4 | `C3D_FrameEnd` pone `inFrame = false` **antes** de enviar el trabajo (`gxCmdQueueRun`, asíncrono). Que retorne no significa que la GPU terminó. | ídem |
| F5 | `C3D_FrameEnd` vacía la caché de **toda** la memoria lineal salvo que se pase `GX_CMDLIST_FLUSH`. | ídem |
| F6 | `C3D_FrameDrawOn(target)` pone el viewport al tamaño completo del render target. | ídem, `C3D_FrameDrawOn` |
| F7 | La cola GX de citro3d tiene 32 entradas. `C3D_DEFAULT_CMDBUF_SIZE` es `0x40000` (256 KB). | `citro3d/source/base.c` (`maxEntries = 32`), `include/c3d/base.h` |
| F8 | Si el buffer de comandos de la GPU se llena, libctru hace `svcBreak(USERBREAK_PANIC)`: **un cierre, no un cuelgue**. | `libctru/source/gpu/gpu.c`, `GPUCMD_AddInternal` |
| F9 | Una cola de GPU que no termina en 2 s (120 vblanks) mientras `C3D_FrameBegin(…NONBLOCK)` sigue devolviendo `false` = **la GPU no terminó el fotograma anterior**. Un fotograma normal tarda mucho menos de 1/60 s. | F2 + medición en las pruebas 16 a 23 |
| F10 | Esperar `gspWaitForP3D()` después de `C3D_FrameEnd` **no prueba nada por sí solo**: citro3d gestiona la cola con su propio manejador de eventos y la espera puede no volver aunque la GPU haya avanzado. No usarlo como diagnóstico. | `libctru/include/3ds/services/gspgpu.h`; prueba 19b ambigua |

## citro3d: dibujo

| # | Hecho | Fuente |
|---|---|---|
| D1 | `BufInfo_Add` admite como máximo 12 buffers (devuelve `-1`) y devuelve `-2` si los vértices **no están en memoria que la GPU pueda leer** (dirección física por debajo de `0x18000000`, por ejemplo memoria de `malloc`). | `citro3d/source/buffers.c` |
| D2 | `C3D_DrawElements` **no dibuja nada, sin avisar,** si los índices no están en memoria lineal o VRAM. | `citro3d/source/drawElements.c` |
| D3 | Tipos de índice: `C3D_UNSIGNED_BYTE = 0`, `C3D_UNSIGNED_SHORT = 1`. No hay índices de 32 bits. | `citro3d/include/c3d/base.h` |
| D4 | `AttrInfo` admite 12 atributos. `AttrInfo_AddLoader`/`AddFixed` devuelven el **número de atributo**, y la permutación del buffer lista números de atributo, no registros del shader. | `citro3d/source/attribs.c` |
| D5 | En la permutación de un buffer, `0xC`–`0xF` son 4, 8, 12 y 16 bytes de relleno. | registros de la GPU en 3dbrew (`GPUREG_ATTRIBBUFFERi_CONFIG`); usado en `c3d_renderstate.cpp`. Pendiente de citar con enlace exacto |
| D6 | **No verificado:** que el PICA200 se cuelgue si la permutación no cubre todo el stride. Es una hipótesis (prueba 17); no hay fuente. El relleno hasta el stride se añadió por si acaso. | — |

## Sistema y archivos

| # | Hecho | Fuente |
|---|---|---|
| S1 | `fopen("sdmc:/…")` funciona: libctru monta la SD (`archiveMountSdmc`) al arrancar. | `libctru/source/system/appInit.c` |
| S2 | `fflush` **no** escribe en la tarjeta: libctru solo pide `FS_WRITE_FLUSH` si el archivo se abrió con `O_SYNC`. Para que sobreviva a un apagado hace falta `fsync` (llama a `FSFILE_Flush`). | `libctru/source/archive_dev.c` (`archive_write`, `archive_fsync`) |
| S3 | Un `.3dsx` empieza con los bytes `3DSX`, y su cabecera extendida (en `0x20`: posición y tamaño del SMDH, posición de la RomFS) apunta al SMDH (icono y título, empieza con `SMDH`) y a la RomFS. En un `.3dsx` la RomFS es la imagen de nivel 3, que empieza con su tamaño de cabecera, `0x28`; `IVFC` solo aparece en la RomFS de un CIA. **Un ELF renombrado no es un `.3dsx`**: empieza con `\x7fELF` y la consola no lo abre bien. Lo crea `3dsxtool` (con `--smdh` y `--romfs`). | `libctru/source/romfs_dev.c`; comprobado en el `.3dsx` de la prueba 25; `platform/3ds/tools/check-3dsx.py` lo verifica |
| S4 | UZDoom busca sus datos en `romfs:/data/uzdoom.pk3` y `romfs:/data/game_support.pk3`: deben ir en la carpeta `data/` de la RomFS, no en la raíz. | `i_main_3ds.cpp` |
| S5 | No hay `dlopen`, `mmap`, `termios`, `uname` ni `getpwuid`. | experiencia de los ports |

## devkitARM y compilación

| # | Hecho | Fuente |
|---|---|---|
| C1 | `int32_t` es `long`, no `int`. El proyecto lo corrige con `-U__INT32_TYPE__ -D__INT32_TYPE__=int` (cada `-U` antes de su `-D`, como opciones). | `CMakeLists.txt` |
| C2 | Los `enum` sin tipo ocupan 1 byte si caben. Los que el motor lee como `int` llevan `: int`. **No** usar `-fno-short-enums` en todo: rompe las estructuras de libctru y citro3d. | port de UZDoom, prueba 6 |
| C3 | devkitPro **no tiene paquete de SDL2 para 3DS** (`3ds-sdl` es SDL 1.2). Se compila con `platform/3ds/build-sdl2-3ds.sh`. | `pacman -Ss sdl2`, 8 nov. 2026 |
| C5 | En el PC de Alex el servidor de devkitPro responde `403` al instalador (`install-devkitpro-pacman`, también con `curl` y otro user agent). Se usa la imagen `devkitpro/devkitarm` de Docker Hub, que sí baja. | 10 nov. 2026 |
| C4 | Compilar desde Windows (MSYS2) un repo que vive en WSL obliga a copiar a `C:` y a traducir rutas: fue la causa de las pruebas 17 y 19 inválidas. Se compila en Ubuntu (WSL). | sesión de las pruebas 17 a 24 |

## Memoria de la New 3DS

| # | Hecho | Fuente |
|---|---|---|
| M1 | Con 124 MB para la app, libctru reparte 72 MB de heap y 32 MB de memoria lineal (lo único que lee la GPU, junto con los 6 MB de VRAM). | `log.txt` (`[mem] start`) |
| M2 | La fragmentación puede impedir una reserva grande aunque haya memoria libre en total. | ports anteriores (Dolmexica) |
