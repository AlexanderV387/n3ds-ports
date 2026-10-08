# 2026-10-08: el hola mundo en hardware real

## Qué pasó

- Actualicé la consola: Luma3DS 9.1 → 13.4 (boot9strap 1.3, sin cambios). Instalé ftpd para pasar archivos por Wi-Fi con FileZilla.
- Primera prueba en la New 3DS: **108,1 FPS / 9,25 ms**, con tearing al mover el cuadro. SDL2 para 3DS ignora `SDL_RENDERER_PRESENTVSYNC`.
- Agregamos `gspWaitForVBlank()` después de cada cuadro: **59,8 FPS / 16,71 ms, estables y sin tearing**.
- Circle Pad y START funcionan.

## Mis respuestas y correcciones

### 1. ¿Por qué marcaba ~108 FPS y qué cambió `gspWaitForVBlank()`?

**Mi respuesta:** pensé que era falta de sincronía entre CPU y GPU, o que la 3DS daba más FPS de los que la pantalla soporta y eso causaba la desincronización vertical.

**Corrección:** lo segundo es lo correcto. La pantalla se refresca a 60 Hz y el bucle dibujaba a 108. No es un tema de CPU y GPU: SDL2 en 3DS dibuja todo con la CPU. La pantalla se dibuja de arriba abajo; si la imagen cambia a mitad de ese recorrido, se ve medio cuadro de uno y medio del siguiente (tearing). `gspWaitForVBlank()` espera a que la pantalla termine de dibujarse (el VBlank), así cada vuelta del bucle coincide con un refresco.

### 2. ¿Por qué el FPS se promedia cada medio segundo?

**Mi respuesta:** pensé que debería ser por cuadro y que quizá había un desfase.

**Corrección:** no es desfase. Si se calcula en cada cuadro, el número cambia 60 veces por segundo y no se puede leer. Además, un cuadro suelto puede tardar más por casualidad; promediar ~30 cuadros reduce ese ruido.

### 3. ¿Qué pasa si quitas la zona muerta del Circle Pad?

**Mi respuesta:** pensé que la zona muerta eran los bordes que evitan que el cuadro se salga de la pantalla.

**Corrección:** eso existe y se llama *clamping* (las líneas con `box_x < 0`). La zona muerta es otra cosa: el Circle Pad casi nunca queda exactamente en el centro y da lecturas pequeñas (300, -500). La zona muerta ignora lo que esté cerca del centro (menos de 8000 de 32767). Sin ella, el cuadro se movería solo, despacio: *stick drift*.

### 4. ¿Cómo se dibuja un número con la fuente de 3x5 bits?

**Mi respuesta:** no lo sabía.

**Explicación:** cada dígito es pixel art de 3x5 guardado en binario. Cada fila es un número de 3 bits: `7` = `111` (los tres píxeles), `5` = `101` (los lados, sin el centro). `4 >> col` revisa la columna izquierda (`100`), centro (`010`) y derecha (`001`).

### 5. ¿Qué genera `ctr_create_3dsx` y qué lo diferencia de un `.cia`?

**Mi respuesta:** el `.3dsx` se abre desde el Homebrew Launcher y sirve para pruebas; pensé que el `.cia` era como un acceso directo.

**Corrección:** lo del `.3dsx` es correcto: no se instala, se copia (o se manda con 3dslink) y se ejecuta. El `.cia` no es un acceso directo: instala el programa en la consola como un título real, igual que un juego de la eShop, con ícono en el menú HOME. Para publicar un port terminado se suelen ofrecer los dos.

## Qué aprendí

- La documentación de una librería no garantiza cómo se comporta en el hardware: hay que medir.
- SDL2 en 3DS dibuja por CPU. Con un presupuesto de 16,67 ms por cuadro, eso importa para los ports.
- Historia para entrevistas: problema (tearing), medición (108 FPS), causa (vsync ignorado), solución (`gspWaitForVBlank`), resultado (59,8 estables).

## Siguiente

Chocolate Doom en 3DS: compilarlo y medir los FPS de partida.
