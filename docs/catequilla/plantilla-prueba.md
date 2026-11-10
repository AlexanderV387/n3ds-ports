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
```

## Al recibir los logs

1. `python3 ~/work/3ds-ports/n3ds-ports/tools/catequilla/analiza-log.py log-A.txt pruebas/NN/uzdoom-pruebaNN.elf`, para cada log.
2. Comprueba que la línea `Test:` del log diga **NN**. Si no, el dueño probó otra versión: avísale antes de analizar nada.
3. Compara con lo que la plantilla decía para cada hipótesis. Escribe cuál queda descartada y por qué, con las líneas del log.
4. Si el resultado no encaja con ninguna hipótesis, dilo así. No fuerces una explicación.
5. Actualiza `platform/3ds/STATUS.md`: la tabla de pruebas, lo que ya sabemos y la pregunta siguiente.

## Errores que ya pasaron (no repetir)

- **Prueba 22:** "saltar el fotograma 0" movió el mismo dibujo al fotograma 1, y se concluyó que "no depende de lo que se dibuja". Antes de concluir, pregúntate: ¿la variable cambió de verdad, o solo de sitio?
- **Pruebas 18 a 20:** seis pruebas midiendo *cuándo* falla, sin cambiar *qué* se dibuja. Si dos pruebas seguidas confirman lo mismo, la siguiente debe quitar o cambiar algo.
- **Prueba 24:** se quitaron los marcadores de la pregunta abierta y el log no sirvió para nada.
- **Prueba 17:** el plan acordado (4 pasadas con interruptores) nunca se pidió. El plan de `STATUS.md` se cumple o se abandona por escrito.
