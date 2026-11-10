# Auditoría de Dolmexica frente a MUGEN 1.1

Objetivo: que nuestra versión de Dolmexica se comporte como MUGEN 1.1, regla por regla, para que no queden "fisuras" como la de Apocalypse (que se desarmaba al saltarle por encima).

## Método

- **Lista de comprobación:** las notas del código de Ikemen GO que describen un comportamiento de MUGEN ("In Mugen...", "Mugen behavior..."), unas 300 en `char.go`, `bytecode.go`, `system.go`, `stage.go`, `compiler.go`. Ikemen está hecho para imitar a MUGEN y anota cada rareza que copia. Se descargan de raw.githubusercontent.com/ikemen-engine/Ikemen-GO.
- **Referencias directas:** la documentación de MUGEN 1.1 (`docs/sctrls.html`, `cns.html`, `trigger.html`), su `common1.cns`, y MUGEN 1.1 ejecutándose con Wine para comparar capturas (`dolmexicainfinite/tools/mugen-shots.sh`).
- **Cada cambio con una prueba** en PC (`Makefile.linux`) o en el simulador de la 3DS (`Makefile.sim`, con AddressSanitizer), y con la prueba de cierres de los 18 personajes.

## Estado por bloques

| Bloque | Estado |
|---|---|
| 1. Movimiento, giro, empuje, ataduras, límites | hecho |
| 2. Helpers | hecho (queda 1 punto) |
| 3. Golpes y proyectiles | en curso |
| 4. Explods, pausas y rondas | pendiente |

## Corregido

| Regla de MUGEN | Fuente | Dolmexica tenía | Commit | Comprobado con |
|---|---|---|---|---|
| Dos jugadores se empujan si sus cajas de tamaño se solapan **también en altura** (cada uno con su `height`) **y** sus Clsn2 se tocan; tener helpers pegados no lo impide | `pushDetection` de Ikemen | solo miraba la altura del propio jugador, y un jugador con helpers pegados no empujaba | `03f3716` | `JumpedOver`: Kung Fu Man ya no cruza a Apocalypse (`height = 300`); igual en MUGEN con Wine |
| Andar: adelante **o** atrás (no los dos); atrás no cuenta en distancia de guardia; frenar no necesita control; `NoWalk` solo impide empezar | `actionPrepare` de Ikemen | andaba con las dos direcciones y frenaba solo con control | `a710212` | guion de botones: las dos direcciones frenan |
| Agacharse desde andar para en seco (salvo desde correr) | `actionPrepare` de Ikemen | deslizaba | `a710212` | x se queda fija al agacharse |
| Un bucle de cambios de estado en un tic se corta ("stuck in loop") | `changeStateEx`, `MaxLoop` de Ikemen | recursión sin fin: Lei-lei agotaba la pila | `a710212` | simulador con ASan: Lei-lei sin errores |
| Empuje de esquina: se carga solo si el rival ya estaba en la esquina; desplaza al atacante ×0,7 por tic; no en superpausa; por defecto 0 si el ataque es **aéreo**, si no 1,3 × `guard.velocity` | `checkCornerPush` (modo heredado) de Ikemen; `sctrls.html` | miraba la letra equivocada del `attr` (0 para todo golpe normal), excluía especiales/supers/agarres y empujaba unas 3 veces más | `97e6586` | patada de Kung Fu Man en la esquina: retrocede 23 px (la suma de MUGEN), antes ~80 |
| Si el que agarra (`TargetBind`) recibe un golpe o desaparece, el agarrado cae (5050); el tiempo corre con la pausa del que agarra | `update` de Ikemen | solo soltaba si desaparecía | `f45ec16` | agarre de Kung Fu Man |
| Un jugador atado al rival puede salir de la pantalla (la atadura va después del límite) | nota de Ikemen en `update` | lo devolvía a la pantalla | `f45ec16` | agarre en la esquina: el rival sale un momento y vuelve |
| `ID` es el número único de MUGEN (56 y 57, cada helper el siguiente, se reinicia por partida); `PlayerID`/`PlayerIDExist` buscan en **todos**, también el rival | `initPlayerID`, `newCharId` de Ikemen | `ID` era el id del helper (0 los personajes) y `PlayerID` solo buscaba en los propios helpers | `1ca6773` | prueba `UniqueIDs` (Kung Fu Man contra Galactus) |
| `HitBy`/`NotHitBy`: el tipo de estado es el **real del atacante** (el del `attr` solo para proyectiles); `NotHitBy` bloquea si coincide el estado **o** el tipo de ataque; `HitBy` deja pasar solo si coinciden **los dos**; una clase sola (N, S, H/A) son sus tres tipos | `attrCheck`, `checkHitBySlot`, `attrMask` de Ikemen | `HitBy` aceptaba cualquiera de las dos partes: los helpers "solo proyectiles" (Kitana, Psylocke, Wonder Woman, Mileena, Morrigan, Neo Chun-Li) recibían todo | `818d814` | censo de Kitana; la intención de los autores (Chun-Li llama "NotHitBy" a su `HitBy value = SCA`) |
| Un `.def` que termina en `clave =` sin nada más | — (fallo de lectura) | leía un byte fuera del archivo (Mileena) | prism `5e79918` | simulador con ASan |

## Comprobado igual que MUGEN (sin cambios)

- Giro automático en cada tic: solo el personaje base, en los estados 0, 11, 20 y 52 (este al acabar la animación), con control o con la ronda terminada (`Ikemen`, bucle de comandos).
- Giro al cambiar de estado con control, de pie o agachado (regla no documentada de MUGEN, `changeStateEx` de Ikemen).
- Andar, saltar y agacharse desde cualquier estado de pie con control (tutorial 3 de MUGEN, Ikemen).
- Helpers borrados al empezar cada ronda; `NumHelper` no cuenta los destruidos en ese tic; `NumHelper(0)` cuenta todos; `IsHelper(-1)` da falso; `keyctrl` decide si el helper ejecuta el estado -1.
- No se vuelve a atar tras un empuje (mejora propia de Ikemen que MUGEN no tiene).
- `BindToRoot`/`BindToParent` con tiempo 1: coloca al atado y lo suelta en el tic siguiente.

## Diferencias encontradas, pendientes

| Regla de MUGEN | Fuente | Dolmexica | Por qué espera |
|---|---|---|---|
| Juggle: puntos por atacante (empiezan en su `airjuggle`); se comprueban si el atacante ya tiene al rival como objetivo, aunque esté de pie; un rival que aún no es objetivo siempre se puede golpear (los proyectiles siempre se comprueban); el coste es el `juggle` del estado, una vez por estado (o el `air.juggle` de cada proyectil), y se resta solo si el golpe entra sobre un rival que caía antes o después | `hitPrecheck`, `addId`, `exitTarget` de Ikemen | solo comprueba si el rival cae o está tumbado, resta en cada golpe mirado (entre o no) y una sola cuenta para todos | escrito, falta una prueba dirigida (después de la 72) |
| Un helper `helpertype = player` empuja y es empujado como un jugador | `pushDetection` y `CSF_playerpush` de Ikemen | los helpers nunca empujan | afecta al helper de New Kyouki; hacerlo con prueba propia |
| Guardia: los estados de guardia de `common1.cns` conservan el control; Ikemen empieza la guardia en la misma cadena que andar/saltar | `common1.cns`; `actionPrepare` de Ikemen | la guardia se resuelve aparte, tras los estados | revisar el momento exacto con capturas de MUGEN |

## Sin verificar todavía

- El oscurecimiento en superpausa: en MUGEN depende de `ownpal` (el helper sin paleta propia se oscurece con su padre). Dolmexica dibuja una capa oscura. Hace falta capturar un super en MUGEN.
- El orden de dibujo de un helper nuevo (MUGEN puede reutilizar el de uno borrado; Ikemen tampoco lo copia).
- La distancia a un rival mientras se está atado (Ikemen la corrige con la posición del que ata).

## Otros hallazgos

- **Psylocke contra Psylocke no recibe ningún golpe en 2 minutos** (censo), ya antes de estos cambios. Revisar su IA o sus `NotHitBy`.
- **El barrido de Kung Fu Man (abajo + `b`, estado 440) no conecta** en las pruebas con botones guionados, ni pegado al rival; pasa igual antes de estos cambios. Investigar.
- **El `hitflag` `P`** (Poison Ivy usa `mafdp`) Ikemen lo acepta; Dolmexica avisa y lo ignora. Averiguar qué hace en MUGEN.
