# Investigación: motor de la familia ZDoom en la New 3DS

**Objetivo:** correr los mods más modernos posibles (Brutal Doom, mods de GZDoom con DECORATE y ZScript, juegos completos como Harmony o Chex Quest 3) con el mejor rendimiento posible. Donde no alcance, se sacrifican cosas, pero de forma visible y como opción.

DSDA-Doom sigue siendo el port para Doom clásico y para los mods Boom, MBF y MBF21: es más rápido y más fiel. Este motor sería un complemento, para lo que DSDA no puede correr.

## Lo que ya existe en la 3DS

### Legend of Doom 3DS (EstebanPdN)

- [Repositorio](https://github.com/EstebanPdN/legend-of-doom-3ds). Es GZDoom **4.7.1** en la New 3DS, publicado como v1.0 y con licencia GPL v3.
- Solo corre un juego: Legend of Doom, una conversión de Zelda en primera persona, sobre Freedoom 2.
- Dibuja el mundo **por software**. La GPU (PICA200) solo escala la imagen terminada. Juega a 320x192 por defecto, con una escala de 50 a 100%.
- Su primera medición en consola fue de **6,2 FPS** a 320x200, todo por CPU. Hubo un intento de GPU con NovaGL (una capa GLES 1.x sobre citro3d), que quedó como experimento.
- Ya resuelve, entre otras cosas:
  - el audio (OpenAL Soft sobre NDSP);
  - ZMusic;
  - la pantalla de abajo;
  - el teclado de la 3DS;
  - los volcados de diagnóstico.
- También lo hizo con ayuda de IA (Codex y Claude Code), y lo explica en su repositorio.

### El fork de tinaut1986

- [Repositorio](https://github.com/tinaut1986/legend-of-doom-3ds). Usa la misma base, GZDoom 4.7.1, y sigue activo (v0.3.1, octubre de 2026).
- **Tiene un renderizador por GPU propio para el mundo** ("a renderer of our own fed by the swrenderer's visibility"). Aprovecha la visibilidad del renderizador por software de GZDoom y le pasa la geometría al PICA200.
- Sus mediciones en una New 3DS (`docs/gpu-renderer-design.md`):

  | Mapa | Mundo | FPS | Vista 3D |
  |---|---|---|---|
  | MAP01 (mundo abierto) | CPU (software) | 27,8 | 22,9 ms |
  | MAP01 | **GPU** | **60,3** | **6,7 ms** |
  | MAP02 (mazmorra) | CPU | 38,2 | 19,8 ms |
  | MAP02 | **GPU** | **105** | **4,3 ms** |

- Además: 3D estereoscópico, Old 3DS (en beta) y una arena de memoria para bloques grandes. Este último punto resolvió cierres por falta de memoria.
- **Le falta**, según su propio documento: portales, alineación de texturas en pendientes, texturas animadas y que se desplazan (sin probar) y otros detalles. Lo hicieron para Legend of Doom, no para cualquier mod.
- El código específico de 3DS está en `src/common/platform/3ds/`: 117 archivos tocados, unas 500 marcas `__3DS__`. La parte propia de Legend of Doom (pantalla de abajo estilo NES, rutas, datos fijos en `build.sh`) es pequeña y separable.

### Lo que dicen sus mediciones del costo de la lógica

- La lógica del juego (35 tics por segundo, ZScript incluido) va siempre en un solo núcleo; GZDoom no la reparte.
- En Legend of Doom cuesta **5,5 ms por tic** en el mapa abierto, con muchos actores y ZScript, y 1 ms en una mazmorra.
- **Brutal Doom** crea muchísimos más objetos: sangre, vísceras, casquillos, cuerpos. En peleas grandes, la lógica será el límite, más que el dibujo.
- Si un tic pasa de 28,5 ms, el juego entero se vuelve lento, no solo el dibujo.

### Memoria

- En la 2DS (52 MB de heap), Legend of Doom usaba unos 41 MB en el título y 44 MB en MAP01.
- Arrancar GZDoom deja unos 150.000 bloques pequeños (10 MB): el ZScript compilado, los nombres y los menús.
- La New 3DS tiene unos 124 MB: hay margen, pero los mods grandes (Brutal Doom con sus sonidos y sprites) hay que medirlos.

## Qué motor elegir

| Opción | Mods que corre | Ventaja | Problema |
|---|---|---|---|
| **GZDoom 4.7.1** (base de los ports de Legend of Doom) | DECORATE y ZScript hasta 4.7 (2021): Brutal Doom v20b y v21, la mayoría de los mods clásicos de GZDoom | Ya corre en la New 3DS, con audio, memoria y GPU resueltos | Los mods que piden funciones posteriores a 4.7 no cargan |
| **GZDoom o LZDoom 4.14** (2025) | Los más modernos | Más compatibilidad | Port desde cero (semanas más); se puede llevar el código 3DS de los ports de Legend of Doom |
| **ZDoom 2.8 o Zandronum** | Solo DECORATE (sin ZScript) | Más ligero | Quedan fuera muchos mods modernos; código viejo, con sonido FMOD que hay que reemplazar |

**Recomendación:** empezar con **GZDoom 4.7.1, a partir del fork de tinaut1986**, que es el más avanzado (GPU a 60 FPS), y generalizarlo:

1. Cargar cualquier IWAD y cualquier mod desde la SD, con nuestro selector de juegos y mods.
2. Aplicar el estándar de controles del proyecto y nuestra pantalla de abajo (HUD, mapa, botones de armas).
3. Completar el renderizador por GPU con lo que piden los mods generales: portales, pendientes, texturas animadas y que se desplazan.
4. Medir con los mods objetivo. Si muchos piden un GZDoom más nuevo, pasar a 4.14 llevando todo el trabajo de 3DS.

Es GPL v3, así que se puede derivar acreditando a EstebanPdN, a tinaut1986 y a los autores de GZDoom. Conviene **avisarles o proponerles colaborar**: ellos también usan IA y están activos.

## Lo que se sacrificaría, si hace falta (todo como opción)

- **Resolución del mundo:** con la GPU, debería ir a 400x240 o al modo ancho. Si no, una escala como la de Legend of Doom.
- **Efectos de OpenGL moderno:** luces dinámicas de GLDEFS, bloom, shaders personalizados y posprocesado. El PICA200 no tiene shaders de fragmentos. Algunas luces se podrían imitar.
- **Modelos 3D y vóxeles:** apagados al principio.
- **Sangre, vísceras y cuerpos:** un límite de cuántos quedan y que desaparezcan antes. Brutal Doom ya trae opciones para eso.
- **FPS:** 60 como meta. En mods pesados, **30 estables** es más honesto que 60 a saltos.

## Mods y juegos de prueba

| Prueba | Por qué |
|---|---|
| Doom II o Freedoom 2 solos | La base: rendimiento del motor sin mods |
| Brutal Doom v21 y v20b | La razón principal; lógica pesada |
| Global Friendly Marines | El mod que pidió la comunidad |
| Harmony (versión para GZDoom) y Chex Quest 3 | Juegos completos y gratis |
| Un mod de solo DECORATE ligero | Para separar el costo de ZScript del de los gráficos |

## Primer paso propuesto

Compilar el fork de tinaut1986 tal cual, cambiar los datos fijos de Legend of Doom por `doom2.wad` (o `freedoom2.wad`) más un mod, y medir en la consola:

- FPS y tiempo por tic, quieto y en una pelea;
- memoria libre al cargar;
- qué se ve mal con el renderizador por GPU (portales, cielos, texturas).

Con esos números se decide si seguir con 4.7.1, cuánto falta en la GPU y qué hay que sacrificar.
