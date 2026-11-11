# Auditoría de Catequilla (pruebas 8 a 24 de UZDoom)

Análisis de la conversación exportada de Catequilla (`ses_e4c66a90…`, 7–9 nov. 2026, unas 70 h) y de sus commits en `gzdoom-3ds`. El objetivo es que sea la mejor herramienta posible para ports de 3DS: medir qué falló, por qué, qué lo arregla y cómo comprobar que mejoró. Las cifras salen del archivo exportado. Los porcentajes de impacto son estimaciones.

Qué es Catequilla y cómo está montada: OpenCode + Ollama con Qwen3.6 27B (Q4_K_M, 65K de contexto) en una RTX 3070 de 8 GB, dentro de WSL. El modelo no cabe entero en la GPU: unas 3,4 palabras (tokens) por segundo.

## 1. Cifras

| Medida | Valor | Lectura |
|---|---|---|
| Pruebas en consola (9 a 24) | ~16 en ~70 h | ~4,4 h por prueba |
| Tiempo generando texto | ~30 h | lento por el hardware |
| Tokens de entrada procesados | ~3 millones | cada acción relee la conversación |
| Llamadas a herramientas | 1.767 | |
| …copias y rutas entre WSL y `C:` | 382 (22 %) | coste de compilar desde Windows |
| …compilar y empaquetar | 194 (~5 h) | |
| …internet | 140, 59 fallidas | sin las fuentes en el disco |
| …subagentes buscando | 8 llamadas, ~4 h | ídem |
| Compactaciones | 51 | pierde contexto cada ~1,4 h |
| Mensajes de Alex que eran correcciones | 42 de 106 (40 %) | dependía de un supervisor |
| Mensajes con el agente "build" en vez de "catequilla" | 1.698 de 1.734 | casi nunca trabajó con su perfil |

## 2. Pruebas: válidas y útiles

| Prueba | ¿Válida? | ¿Aportó algo nuevo? |
|---|---|---|
| 9–10 | sí | sí, en parte |
| 11–12 | sí | **sí** (fallo de `I_Rumble`) |
| 13 | sí | **sí** (`Init complete`) |
| 14–15 | sí | sí (dentro de `C3D_FrameBegin`) |
| 16 | sí | sí |
| 17 (1.ª) | **no** (ELF renombrado a `.3dsx`) | no |
| 17 (2.ª) | sí | sí (cuelgue de GPU) |
| 18 | sí | poco |
| 19 | **no** (archivos viejos) | no |
| 19b | sí | ambiguo |
| 20 | dudosa | no |
| 21–22 | sí | sí, pero mal interpretada |
| 23 | **no** (rompió el arranque) | no |
| 23b | sí | no |
| 24 | sí, sin marcadores | no |

Unas 4 pruebas no eran válidas y unas 5 o 6 repitieron lo ya sabido. Desde la 17, la pregunta decisiva (¿se cuelga si no se dibuja nada?) no se hizo.

## 3. Errores, causa y arreglo

| Tipo | Casos | Causa | Arreglo |
|---|---|---|---|
| A. Pruebas inválidas por el build | 17, 19 (¿20, 24?) | copias a mano a `C:`, rutas MSYS2, empaquetado a mano sin comprobar, binario sin número de prueba | compilar en Ubuntu con `build-test.sh` (comprueba el 3DSX y lleva prueba y commit en el binario) |
| B. Afirmaciones falsas | ELF = 3DSX; `FrameEnd(0)` = tiempo de espera; `fopen` no abre `sdmc:/`; `C3D_GetCommandQueue` | sin las fuentes, completa con lo que suena bien | fuentes en `~/work/refs/`, `hechos-3ds.md`, regla de citar archivo y línea |
| C. Lógica de las pruebas | prueba 22 | no escribe antes qué resultado espera bajo cada hipótesis | `plantilla-prueba.md` obligatoria |
| D. Medir alrededor | 18–20, 23 | sus reglas premiaban medir y frenaban proponer | objetivo: descartar hipótesis; quitar o cambiar algo antes que añadir marcadores |
| E. No cumplir el plan | interruptores de la 17 | el plan vivía solo en el chat | `STATUS.md` con el plan; se cumple o se abandona por escrito |
| F. Olvidos | 51 compactaciones | una conversación de 70 h | una conversación por prueba; herramientas que resumen (`analiza-log.py`) |
| G. Logs inútiles | cortes en sitios distintos; 24 sin marcadores | `fflush` no escribe en la SD; marcadores borrados | `fsync`; esperar 60 s; no quitar los marcadores de la pregunta abierta |
| H. Configuración | agente "build", `presence_penalty` 1,5, `catequilla.md` con un modelo de 4B | — | corregido el 10 nov. 2026 |

## 4. Lo que hizo bien

- Encontró y arregló el cierre de `I_Rumble`, y bajó la memoria de la pantalla de carga.
- Sigue bien un plan concreto con archivo y línea.
- Reconoce sus errores y comprueba binarios (`strings`, la cabecera del `.3dsx`).
- Separa hechos de hipótesis cuando se lo exige el formato.

## 5. Sin medir todavía

- El efecto de `presence_penalty` (1,5 → 0): habría que comparar la misma tarea corta con cada valor.
- Si los cortes de log eran por `fsync` o por apagar pronto: lo aclarará la prueba 25.

## 6. Metas para las próximas 5 pruebas

| Medida | Antes | Meta |
|---|---|---|
| Pruebas válidas | ~75 % | 100 % |
| Pruebas que aportan algo nuevo | ~50 % | ≥ 80 % |
| Correcciones de Alex por prueba | ~2,6 | ≤ 1 |
| Horas por prueba (sin contar la consola) | ~4 | ≤ 1,5 |
| Afirmaciones sobre APIs sin fuente | frecuentes | 0 |

Al cerrar cada prueba se anota en `STATUS.md`. Después de la quinta se compara con esta tabla.

## 7. Qué se cambió (10 nov. 2026)

- `docs/catequilla/AGENTS.md`: instrucciones nuevas, cortas, con el estado fuera.
- `docs/catequilla/hechos-3ds.md`: hechos comprobados en el código de citro3d y libctru.
- `docs/catequilla/plantilla-prueba.md`: plantilla y errores ya vistos.
- `docs/catequilla/arranque.md`: cómo ponerla en marcha.
- `tools/catequilla/analiza-log.py`: resumen del log y direcciones traducidas.
- En `gzdoom-3ds`, rama `uzdoom-3ds-test25`:
  - `platform/3ds/build-test.sh`, `build-sdl2-3ds.sh` y `tools/check-3dsx.py`;
  - `STATUS.md`;
  - el log con `fsync`;
  - el módulo `c3d_diag` con los interruptores de la prueba 25;
  - fuera los marcadores de las pruebas 13, 14 y 21 del motor.

## 8. Seguimiento (nuevo método)

| Prueba | ¿Válida? | ¿Aportó algo nuevo? | Correcciones de Claude | Errores de razonamiento |
|---|---|---|---|---|
| 25 (diseñada por Claude) | sí | sí: el dibujo cuelga; no la textura ni los buffers del motor | — | análisis de Catequilla: PICA "con shader de fragmento"; "el estado se hereda"; HOME "abre una consola"; afirmar sin pruebas que el texto en ruso no afecta |
| 26 | sí | sí: **primera imagen** (triángulo de `simple_tri`) | 1 ronda (pequeña) | conclusión mayor que lo que se cambió (shader + matriz + vértices + atributos) |
| 27 (propuesta) | — | — | 1 ronda | color leído del registro equivocado (triángulo invisible); hipótesis sin separar dejadas "para la 28" |
| 27 (2.ª propuesta, con autocomprobación) | — | — | 1 ronda (pequeña) | **aciertos:** tabla de diferencias correcta, color comprobado, una sola compilación. **Fallos:** no separó código de datos (todas las variantes con los datos del motor, aunque se le había sugerido); una frase técnica inventada ("mul vía texmat") |

| 27 (resultado) y 28 (propuesta) | 27 sí | sí: **la salida `outtc0` del shader es la causa** (V0/V2 cuelgan, V1/V3/V4 no) | ninguna (Alex aprobó la 28 tal cual) | **aciertos:** conclusión ajustada a la tabla, sin exagerar; explicó bien la orientación del triángulo. **Fallos menores:** sustituyó las preguntas de la autocomprobación por otras propias y se saltó la 6 (en la 28 no dice qué significa que V0 y V2 funcionen las dos); la hipótesis C dice que el tex env "usa texcoords como en el motor real", pero en el camino del triángulo los combinadores solo usan el color de vértice |

| 28 (resultado) y 29 (propuesta) | 28 sí | sí: con `outtc0` escrito por `mov` constante funciona; con los `dp4` se cuelga; la textura no influye | 1 ronda | **aciertos:** buscó el ejemplo de citro3d y citó archivo y línea; propone un arreglo y una pasada con el dibujo real, como se le pidió. **Fallos:** de nuevo concluyó más de lo que cambió (en la 28 y en el arreglo de la 29 cambian a la vez lo que se lee y los componentes escritos); la hoja de pasadas de la 29 pone `c3d-triangle.txt` en la pasada del dibujo real, contradiciendo su propio texto |

| 29 (resultado) | 3 de 4 válidas (V1 con log incompleto) | **sí: primera pantalla de título del juego dibujada por la GPU** (V2: `dp4` con `intex` y `outtc0.zw` escrito) | 1 ronda | **aciertos:** buena separación de variables en el diseño. **Fallos:** usó la pasada inválida (V1) para concluir que basta escribir `zw`; no notó que V2 se había probado con el juego real |

| 29 (V1 repetida) | sí, log completo (esperando la carga entera) | **igual que V2**: con `outtc0.zw` escrito funciona lea el `dp4` de `r2` o de `intex`; sin `zw` (V0) se cuelga | — | se avisa a Catequilla: ahora sí puede concluir que lo necesario es escribir `zw`, **siempre que V1 y V2 se probaran con el mismo dibujo** (si una fue el triángulo y otra el juego, cambian dos filas) |

| 29 (V1 repetida) y 30 (propuesta) | sí | sí: **escribir `outtc0.zw` basta** (V1, que solo cambia eso frente al original, funciona) | ninguna de fondo (aprobada) | **aciertos:** comprobó en los logs que todas las pasadas de la 29 fueron con el juego real; tabla instrucción por instrucción; las 7 preguntas respondidas. **Detalle:** mezcla el arreglo con una limpieza de código y no contempla que, si falla, la causa pueda ser la limpieza |

**Patrón que queda:** el proceso (plantilla, una sola compilación, commit, logs completos) ya funciona sin ayuda. Lo que todavía necesita revisión externa es **el control de variables**: comprobar que solo cambia lo que dice y no concluir más de lo que se cambió. Desde el 10 nov. la plantilla obliga a una tabla de diferencias y a cinco preguntas de autocomprobación (`plantilla-prueba.md`). Meta: que las próximas propuestas lleguen sin estos dos errores. Si se repiten, el siguiente paso es un revisor automático: una segunda conversación de Catequilla, con el modo de análisis (pensando), que solo revise la plantilla contra la autocomprobación antes de enseñársela a Alex.

## 9. Límite que no arreglan las herramientas

Un modelo de 27B que corre en parte desde la RAM es lento, y en diagnósticos difíciles (como un cuelgue de GPU) necesita que un modelo grande diseñe la prueba. Cuando se atasque dos pruebas seguidas, lo indicado es llevar el resumen de `STATUS.md` a un modelo grande. Si algún día se invierte en hardware: una GPU de 24 GB para que el modelo corra entero en ella, o un modelo MoE (más rápido) para las tareas mecánicas.
