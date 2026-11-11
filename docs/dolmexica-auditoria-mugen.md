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
| Cada máquina de estados corre **una vez por tic**: andar, agacharse, levantarse o saltar (cambios del motor) se aplican tras el estado -1 y el nuevo estado corre una sola vez; los cambios hechos después de los estados (aterrizar, cubrirse, levantarse del suelo, golpes) no quitan el tic siguiente | `actionPrepare`/`actionRun` y `stateChange2` de Ikemen | el cambio corría todo otra vez (-3, -2, -1 dos veces, el estado nuevo dos veces) y **el tic siguiente no corría**: un botón pulsado justo después de agacharse o de empezar a andar se perdía; aterrizar o cubrirse duraba un tic más | `dolmexica` (este commit) | prueba `Juggle` con botones: la palma de Kung Fu Man (`~D, DF, F, y`) sale con la `y` 3 tics después de `F`; antes solo en el mismo tic |
| Juggle (ver la fila de pendientes, ahora hecho) | `hitPrecheck`, `addId` de Ikemen | una sola cuenta para todos, se restaba en cada golpe mirado | `dolmexica` | prueba `Juggle` (la palma cuesta 4, una vez; vuelve a 15 al levantarse) |
| La **energía es del jugador raíz**: `Power`, `PowerAdd`, `PowerSet` y la energía que dan o quitan los golpes de un helper son de su jugador; no cambia tras acabar la ronda | `powerOwner`, `setPower` de Ikemen | cada helper tenía la suya y la escribía en la barra del jugador: el nivel bajaba y subía en cada golpe, con su sonido ("bong", `level1.snd = 21,0` de `fight.def`) | `dolmexica` | Felicia contra Apocalypse: 32 subidas de nivel en un combate, ahora 3 |
| (3DS) Dos sonidos en "cualquier canal libre" en el mismo tic van a canales distintos | — (fallo del port) | el DSP da un canal por libre hasta su siguiente fotograma: el segundo sonido cortaba al primero (registro de la consola: el sonido de nivel y la voz de Apocalypse en el canal 23 en el primer tic) | prism | revisado en el registro de la prueba 72 |
| `MoveContact`, `MoveHit`, `MoveGuarded`, `MoveReversed` valen 1 en el tic siguiente al contacto y suben desde ahí, también si el atacante no tiene pausa | `mctime` de Ikemen (sube después de los estados) | los golpes se detectan al empezar el tic y el contador subía antes de los estados: con `pausetime = 0` el atacante ya veía 2 y nunca 1. Los misiles de Apocalypse explotan con `MoveContact = 1`: golpeaban y se quedaban hasta el fin de la ronda, más con cada super (40 a la vez) | `5725fc9` | `JumpedOver` con Apocalypse: el misil pasa a su explosión y desaparece; Kung Fu Man y Felicia sin cambios en el censo. Antes lo di por "igual en MUGEN" leyendo el código sin mirarlo en un combate: error |
| Cruzar a Apocalypse con el triple salto de Wonder Woman, y que al girarse se "desarme": **igual en MUGEN 1.1** (Wine, con posiciones vía `DisplayToClipboard`): pasa por encima, no se gira en su estado 9000 hasta cambiar de estado con control, y entonces su torso se refleja y sus partes no | — | sin cambio (es el personaje) | — | capturas de MUGEN y del simulador en la misma situación |
| `ModifyExplod` con solo `sprpriority` (u `ontop`) no mueve el explod | `modifyExplod` de Ikemen | lo recolocaba por su `postype`: el suelo de Galactus subía con él en su intro y quedaba 22 más bajo en la ronda 1 que en las demás | `57df996` | capturas de MUGEN (rondas 1 y 2) y del simulador |
| A igual `sprpriority`, todo personaje (y helper) se dibuja sobre todo explod, también los del otro jugador | `explodCueDraw` tras `charList.cueDraw` en Ikemen | el desfase del jugador 2 era mayor que el de los explods: el suelo de Galactus (-3) tapaba al jugador 1 KO (5150, -3) | `57df996` | ídem |
| `Redirección, AnimElem = n, op t` (y `TimeMod`, `HitDefAttr`) se leen igual con o sin espacios | MUGEN | el lector de `.def` devuelve las líneas con comas sin espacios y la palabra antes de `=` incluía la redirección: la línea se leía como lista, siempre verdadera. El brazo de Galactus se quedaba en su pose alzada: el puño iba solo (la "muñeca" desaparecía) | `b66a370` | capturas de MUGEN y del simulador del golpe al suelo y del rayo de la mano; 10 personajes usan la forma |
| El golpeado entra **una vez** en su estado de recibir golpe | `hitDetection` de Ikemen | tras cada golpe se volvía a poner (pensado solo para `p1stateno`): lo de su tiempo 0 se hacía dos veces; el puño de Galactus creaba dos "Damage Check" y su cuerpo, que espera uno, no recibía el daño | `3fefe4a` | jab de Kung Fu Man a Galactus: 67, igual que MUGEN 1.1 |
| El daño de un golpe a un helper es **de su propia vida**, y solo si queda en un estado de recibir golpe | `lifeAdd` sobre el golpeado en Ikemen | iba a la vida del jugador raíz: los personajes cuyas piezas reciben y pasan el daño (Galactus) lo recibían doble | `3fefe4a` | ídem |
| `LifeAdd` escalado por defensa se redondea (mínimo 1) | `lifeAdd` de Ikemen | se truncaba (Galactus 66, MUGEN 67) | `3fefe4a` | ídem |
| Los valores de vida, ataque y defensa de los 18 personajes se leen como en sus archivos; la fórmula de daño es la de MUGEN | — | correcto | — | jab de Kung Fu Man: Felicia 23, Lei-lei 26, Galactus 67 en Dolmexica y en MUGEN 1.1 |
| Un nuevo `Clsn1Default`/`Clsn2Default` dentro de una acción **reemplaza** las cajas por defecto; un `Clsn1`/`Clsn2` propio (también con 0 cajas) es el juego completo de ese cuadro | `readAnimation` de Ikemen | las cajas por defecto se sumaban: el rayo de Galactus conservaba una caja junto al puño y seguía golpeando de cerca (Kung Fu Man atrapado, ~430 de daño). Cambia 315 animaciones de 11 personajes (Onslaught 133, Kitana 110, Lei-lei 21, Psylocke 17, Wonder Woman 9, Chun-Li Neo 8, Apocalypse 7, Morrigan 6…) | prism `27df0a0` | rayo en MUGEN 1.1: 192 de daño y se libera a ~151 de distancia; simulador: 180 y ~140. Probado también con el empuje del helper "Push Check" desactivado en MUGEN: no influye |
| `EnvColor` cubre toda la pantalla | MUGEN | en la 3DS solo cubría el centro 4:3: en las hipers de Felicia se veían el escenario y su retrato a los lados | `6996f59` | simulador con el margen de la 3DS (`-DDOLMEXICA_TEST_SIDE_MARGIN=80`, `N3DS_SIM_SIDE_MARGIN=40`) |
| Lo que espera fuera de la pantalla 4:3 no se ve en los lados de la 3DS; lo que cubre la pantalla cubre también los lados | pantalla ancha de la 3DS | el contador de combo ("111", "Rush!") se veía en los bordes toda la pelea; `start.x` no se escalaba; las escenas de intros y finales se recortaban a la ventana 4:3 | `eb0d218` | prueba `ScreenTour` en el simulador con margen (`-DDOLMEXICA_TEST_SIDE_MARGIN=80`, `N3DS_SIM_SIDE_MARGIN=40`); los fundidos del simulador no llevan el margen (en la 3DS sí) |
| Destellos de pantalla completa sobre los lados de la 3DS: explods siempre; chispas de golpe, helpers y proyectiles solo si la animación suma o resta colores | pantalla ancha de la 3DS | las chispas de Onslaught y las grandes de los CvS no se estiraban; los rayos de los ojos de Galactus (helper, sin mezcla) sí y se deformaban | prism `1a72a5f`, `eb2e515` | CPU contra CPU nivel 8 de los 18 personajes con `N3DS_SIM_TRACE_UNSTRETCHED` (lo de tamaño pantalla que quedó sin estirar) |
| `postype = front`: el lado de la pantalla hacia el que mira el jugador (derecho si mira a la derecha, izquierdo si no), la x sin invertir | `Explod.setPos` de Ikemen ("even in version 1.1") | se medía desde el borde de pantalla del jugador (media pantalla de más) e invertía la x: la máscara de New Kyouki (111333/99999) salía media pantalla a la izquierda | `a3f3edd` | capturas de MUGEN 1.1 con Kyouki como P1 y P2 (copia que entra en 111333 con un botón) |
| Una `SuperPause`/`Pause` llamada con otra activa la reinicia con sus valores | `setSuperPauseTime`/`setPauseTime` de Ikemen | la cortaba: la 4200 de Kyouki llama una por tick durante 86 ticks y el rival atrapado no quedaba congelado | `3c3a204` | traza por tick en MUGEN 1.1 (estado y vida del rival vía `DisplayToClipboard` de una copia de Kyouki) |
| `p2defmul` de cada `SuperPause` se multiplica sobre quien está recibiendo golpe (movetype H) | Ikemen ("stacks… Mugen does the same") | se asignaba: el proyectil final de la 4200 (999) hacía 800 por golpe; en MUGEN ~1 | `3c3a204` | ídem: 97 de daño en MUGEN |
| Un proyectil que sobrevive a un golpe tiene su pausa de golpe (`pausetime` del atacante); su `removetime` y `misstime` no corren mientras tanto | `Projectile.tick` de Ikemen | los proyectiles nunca pausaban: el de la 26000 de Kyouki duraba 100 ticks en vez de ~195 | `3c3a204` | ídem |
| El KO de un jugador (vida 0) se aplica al empezar su siguiente actualización; hasta entonces `Alive` = 1; si está recibiendo golpe en un estado ajeno se queda en él | `actionFinish` de Ikemen | moría al instante (estado 5080): la 8904 de Kyouki no podía ponerlo en su 5175 (`enemy, alive = 1`) | `3c3a204` | ídem: rival en 5175 con vida 0 en MUGEN |
| Un `.def` que termina en `clave =` sin nada más | — (fallo de lectura) | leía un byte fuera del archivo (Mileena) | prism `5e79918` | simulador con ASan |

## Comprobado igual que MUGEN (sin cambios)

- **IA de New Kyouki** (CPU contra CPU, nivel 4, contando sus súper/hiper con una copia instrumentada): contra Galactus, Onslaught y Apocalypse elige lo mismo en MUGEN 1.1 y en Dolmexica; contra Apocalypse repite el súper 100001 (29 veces en MUGEN, 26 aquí), no le hace daño y pierde en los dos. Sus hipers (8900 y otras) piden condiciones (vida del rival <= 230, rival no de pie): es su IA, no el motor.
- **Punto ciego de Galactus:** en MUGEN 1.1 Kung Fu Man pegado a él (entre el puño y el cuerpo) pasa 80 s perdiendo 8 de vida; en Dolmexica tampoco recibe daño. Quieto en su esquina, Galactus lo derrota en ~30 s en MUGEN y ~20 s aquí.


- Giro automático en cada tic: solo el personaje base, en los estados 0, 11, 20 y 52 (este al acabar la animación), con control o con la ronda terminada (`Ikemen`, bucle de comandos).
- Giro al cambiar de estado con control, de pie o agachado (regla no documentada de MUGEN, `changeStateEx` de Ikemen).
- Andar, saltar y agacharse desde cualquier estado de pie con control (tutorial 3 de MUGEN, Ikemen).
- Helpers borrados al empezar cada ronda; `NumHelper` no cuenta los destruidos en ese tic; `NumHelper(0)` cuenta todos; `IsHelper(-1)` da falso; `keyctrl` decide si el helper ejecuta el estado -1.
- No se vuelve a atar tras un empuje (mejora propia de Ikemen que MUGEN no tiene).
- `BindToRoot`/`BindToParent` con tiempo 1: coloca al atado y lo suelta en el tic siguiente.

## Diferencias encontradas, pendientes

| Regla de MUGEN | Fuente | Dolmexica | Por qué espera |
|---|---|---|---|
| Un helper `helpertype = player` empuja y es empujado como un jugador | `pushDetection` y `CSF_playerpush` de Ikemen | los helpers nunca empujan | afecta al helper de New Kyouki; hacerlo con prueba propia |
| Guardia: los estados de guardia de `common1.cns` conservan el control; Ikemen empieza la guardia en la misma cadena que andar/saltar | `common1.cns`; `actionPrepare` de Ikemen | la guardia se resuelve aparte, tras los estados | revisar el momento exacto con capturas de MUGEN |

## Sin verificar todavía

- El modo rápido de pruebas (`Makefile.linux`, sin dibujar) no detecta golpes de algunos helpers: medir con el simulador (`Makefile.sim`).

- `StopSnd channel = -1`: Ikemen (como MUGEN) para solo los sonidos de los personajes; Dolmexica para todos, también el locutor. En la 3DS hace falta separar los canales libres de personajes y de sistema.
- Daño de cada personaje: la fórmula es la de Ikemen (daño × ataque × `attack`/100 ÷ defensa); falta comparar un mismo golpe en MUGEN 1.1.

- El oscurecimiento en superpausa: en MUGEN depende de `ownpal` (el helper sin paleta propia se oscurece con su padre). Dolmexica dibuja una capa oscura. Hace falta capturar un super en MUGEN.
- El orden de dibujo de un helper nuevo (MUGEN puede reutilizar el de uno borrado; Ikemen tampoco lo copia).
- La distancia a un rival mientras se está atado (Ikemen la corrige con la posición del que ata).

## Otros hallazgos

- **Psylocke contra Psylocke no recibe ningún golpe en 2 minutos** (censo), ya antes de estos cambios. Revisar su IA o sus `NotHitBy`.
- **El barrido de Kung Fu Man (abajo + `b`, estado 440) no conecta** en las pruebas con botones guionados, ni pegado al rival; pasa igual antes de estos cambios. Investigar.
- **El `hitflag` `P`** (Poison Ivy usa `mafdp`) Ikemen lo acepta; Dolmexica avisa y lo ignora. Averiguar qué hace en MUGEN.
