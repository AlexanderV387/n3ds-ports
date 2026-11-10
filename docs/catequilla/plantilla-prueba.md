# Plantilla de prueba (para Catequilla)

Cada prueba en consola cuesta tiempo del dueño: hay que copiarla a la SD, probarla, sacar el log y pasarlo. Antes de escribir código, rellena esta plantilla y muéstrasela. **Si los dos resultados posibles no se distinguen en el log, la prueba no se hace.**

```markdown
## Prueba NN

**Pregunta:** <una sola pregunta, de sí o no>

**Lo que ya sabemos (con la prueba que lo mostró):**
- ...

**Hipótesis A:** <...>
- Si A es cierta, el log mostrará: <líneas concretas>
**Hipótesis B:** <...>
- Si B es cierta, el log mostrará: <líneas concretas>
(Hasta 3 hipótesis. Cada una con un resultado distinto.)

**Única variable que cambia:** <qué se toca, en qué archivo y función>
(Quitar o cambiar algo, como un dibujo, un estado o una función, informa más que añadir marcadores.)

**Pasadas en la consola** (cada una con su log; el dueño renombra log.txt a log-A.txt, log-B.txt...):
| Pasada | Archivos de control en sdmc:/3ds/gzdoom/ | Qué mirar en pantalla |
|---|---|---|
| A | ninguno | ... |
| B | ... | ... |

**Marcadores que se quedan:** los de la pregunta abierta. **Marcadores que se quitan:** los de preguntas ya respondidas.

**Cómo se compila:** `platform/3ds/docker-build-test.sh NN` (nada a mano).

**Autocomprobación** (obligatoria, ver abajo): tabla de diferencias entre pasadas y las 5 preguntas, respondidas.
```

## Autocomprobación antes de enseñar la plantilla

Responde por escrito, dentro de la plantilla. Si alguna respuesta es "no" o "no sé", la plantilla no está lista.

1. **Tabla de diferencias.** Para cada par de pasadas que vas a comparar, haz una tabla con **todo** lo que cambia entre ellas: shader, valores de los uniformes, vértices (coordenadas y z), atributos (cuántos, cuáles fijos y qué registro), estado (blend, depth, combinadores), textura y llamada de dibujo. Para llenarla, lee el código de los **dos caminos**, no solo el que escribiste. Si cambia más de una fila, la prueba no aísla una sola variable: o separas las filas en pasadas distintas, o la conclusión solo podrá nombrar el conjunto ("el shader o sus datos").
2. **¿Cada hipótesis predice algo distinto en el log?** Escribe la línea `[C3D]` concreta que saldría bajo cada una. Si dos hipótesis dan el mismo log, no las distingue esta prueba.
3. **¿Lo que dices que se verá en pantalla puede verse?** Comprueba el color final con los datos reales: qué registro de entrada lee el shader y qué valor le llega. Un triángulo negro sobre fondo negro "no se ve" aunque funcione. Si la pantalla no es fiable, el criterio es el log.
4. **¿Se resuelve en una sola compilación?** Si sabes de antemano que harán falta más pruebas para separar hipótesis ("para distinguir B de C haría falta la 28"), mete esas variantes **en esta**: un interruptor por variante, una pasada por variante. Cada compilación y cada ronda en la consola cuestan más que una pasada extra.
5. **¿Cada afirmación sobre una API tiene su fuente** (archivo y línea en `~/work/refs/`, o `hechos-3ds.md`)?

## Al concluir: no digas más de lo que se cambió

La conclusión solo puede nombrar lo que cambió entre las pasadas, según la tabla de diferencias. Si cambiaron cuatro cosas a la vez, la conclusión es "una de estas cuatro", no la que te parece más probable. Escribe la más probable como **hipótesis para la siguiente prueba**, no como hecho en "Lo que sabemos".

## Al recibir los logs

1. `python3 ~/work/3ds-ports/n3ds-ports/tools/catequilla/analiza-log.py log-A.txt pruebas/NN/uzdoom-pruebaNN.elf`, para cada log.
2. Comprueba que la línea `Test:` del log diga **NN**. Si no, el dueño probó otra versión: avísale antes de analizar nada.
3. Compara con lo que la plantilla decía para cada hipótesis. Escribe cuál queda descartada y por qué, con las líneas del log.
4. Si el resultado no encaja con ninguna hipótesis, dilo así. No fuerces una explicación.
5. Actualiza `platform/3ds/STATUS.md`: la tabla de pruebas, lo que ya sabemos y la pregunta siguiente.

## Errores que ya pasaron (no repetir)

- **Prueba 26:** la pasada con el shader de `simple_tri` cambió a la vez el shader, la matriz (identidad frente a `Mtx_OrthoTilt`), los vértices (z −0,5 en recorte frente a z 0,5 en píxeles) y los atributos (2 fijos frente a 1). Se escribió "el shader del motor es el culpable": la conclusión correcta era "el shader o sus datos". La tabla de diferencias lo habría mostrado.
- **Propuesta 27 (primera versión):** el shader intermedio leía el color de `v1`, pero ese camino pone la textura (0,0,0,0) en `v1`: el triángulo saldría negro aunque funcionara, y la pantalla habría engañado. Además dejaba hipótesis sin separar "para la 28".

- **Prueba 22:** "saltar el fotograma 0" movió el mismo dibujo al fotograma 1, y se concluyó que "no depende de lo que se dibuja". Antes de concluir, pregúntate: ¿la variable cambió de verdad, o solo de sitio?
- **Pruebas 18 a 20:** seis pruebas midiendo *cuándo* falla, sin cambiar *qué* se dibuja. Si dos pruebas seguidas confirman lo mismo, la siguiente debe quitar o cambiar algo.
- **Prueba 24:** se quitaron los marcadores de la pregunta abierta y el log no sirvió para nada.
- **Prueba 17:** el plan acordado (4 pasadas con interruptores) nunca se pidió. El plan de `STATUS.md` se cumple o se abandona por escrito.
