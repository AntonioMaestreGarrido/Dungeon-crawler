# Dungeon crawler (juego de mesa) — Reglas en construcción

_Documento vivo. Se va completando paso a paso._

## 0. Objetivo del juego
- Es un **puzle**: se trata de resolver cada mazmorra con los dados que tocan y los mínimos recursos.
- Los **enemigos son débiles y predecibles**.
- Se gana **limpiando la mazmorra y saliendo de ella**.
- Consecuencias a decidir: el dado negro deja de generar enemigos al azar, los enemigos pasan a tener dados fijos y comportamiento visible, y el reloj (rellenado de la bolsa) pasa a ser el límite de turnos del puzle. Pendiente de confirmar con Antonio.

## 1. Personajes
- Cada personaje empieza con **10 puntos de vida** (en el futuro variarán según el personaje). El daño recibido quita puntos de vida.
- Al llegar a **0** el personaje queda **inconsciente**.
- Cada jugador controla **4 personajes**.
- Cada personaje tiene 4 atributos: **Ataque, Defensa, Agilidad, Especial**.
- Cada atributo vale entre **1 y 3**.

## 2. Colores
| Atributo | Color |
|---|---|
| Ataque | Rojo |
| Defensa | Verde |
| Agilidad | Amarillo |
| Especial | Morado |

## 3. Slots
- El **valor del atributo es el número de slots**: cuántos dados de ese color puede acumular el personaje en su hoja.
  - Ejemplo: Ataque 3 → puede tener hasta 3 dados rojos.
- Los personajes empiezan **sin dados** en sus slots.

## 4. Bolsa del jugador
- **Un dado del color correspondiente por cada slot** (la suma de los atributos de cada personaje).
- **Más 4 dados fijos por personaje, uno de cada color.**
- Ejemplo: un personaje con Ataque 3, Defensa 2, Agilidad 1, Especial 2 aporta 3+1 rojos, 2+1 verdes, 1+1 amarillos y 2+1 morados = 12 dados.

## 5. Núcleo del juego: el turno
1. **Sacar y tirar**: al inicio del turno se sacan de la bolsa **entre 1 y 2 dados por personaje vivo** (a elegir por el jugador; mínimo 1 por personaje) y se tiran. Robar menos retrasa el rellenado de la bolsa y la llegada del dado negro.
2. **Repartir**: se reparten entre los personajes, colocándolos con su valor en los slots de su color.
   - Un dado que no cabe en ningún slot libre **se pierde**: va a descartes junto con los gastados y vuelve a la bolsa en el siguiente relleno.
3. **Acciones**: los dados acumulados se **gastan o se guardan** para hacer acciones.

### Regla general: los dados guardados crecen
- Cada turno, **todo dado que no se ha usado sube 1 punto** su valor.
- Se aplica **al final del turno** de su dueño.
- **Tope en 6**: un dado en 6 se queda en 6.

### Especial (dado morado)
- Su efecto **depende del personaje**: cada uno tiene su propia habilidad especial.
  - Ejemplos: arquero → ataque a distancia; mago → magia.
- Las habilidades concretas se definirán con cada personaje.

## 6. Rellenar la bolsa y el dado negro
**Concepto clave: acumular frente a vaciar la bolsa.**
- Guardar dados en las hojas **los hace crecer** (+1 por turno), pero **saca dados de la circulación**: la bolsa se vacía antes, se rellena antes y entra antes el siguiente dado negro (más enemigos).
- Gastar los dados los devuelve a descartes y alarga el tiempo entre rellenos, pero se pierde su crecimiento.
- El jugador decide en cada turno cuánto invierte en poder y cuánto en tiempo.
- Cuando la bolsa se vacía, **se rellena solo con los dados gastados y perdidos** (los guardados en las hojas se quedan donde están).
- En cada relleno se **añade un dado negro nuevo**: se van acumulando.
- **Efecto del dado negro: aparece un enemigo.** Al sacarlo y tirarlo, su valor decide el tipo:
  - **1-3: enemigo flojo y rápido** (movilidad 4).
  - **4-6: enemigo fuerte.**
- El enemigo aparece en una **casilla libre del borde del mapa**.
- Por confirmar: qué atributos tienen flojo y fuerte (borrador: flojo rápido 2/1/1/1 vida 5, arma +0, movilidad 4; fuerte 3/2/1/1 vida 10, arma +1, movilidad 2), si actúa el turno en que aparece, y si el dado negro vuelve con el siguiente relleno y se acumula (ver simulación) o sale del juego.

## 7. Acciones
### Mover (dado amarillo, Agilidad)
- Gastar un dado amarillo permite **mover tantas casillas como su valor**.
- Solo movimiento **ortogonal** (sin diagonales).
- Se pueden gastar **varios amarillos a la vez** y sumar sus valores.
- Se puede mover **menos** de lo que marca el dado (por confirmar).
- **Dado fijo de movilidad**: cada personaje tiene un dado amarillo propio que **no va a la bolsa** y **no se tira**: tiene un **valor fijo según el personaje** (p. ej. Guerrero 2, un pícaro 4). 
  - **A todos los efectos es un dado amarillo** que está disponible cada turno y **nunca se tira**: se suma a otros amarillos y sirve también para la carga.
  - Si se usa, vuelve a estar disponible el turno siguiente; no ocupa slot, no va a la bolsa ni crece.
  - Como los enemigos son idénticos a los personajes, también lo tienen.
  - Valor del Guerrero: **2**.
  - Simulación (vs 6 enemigos débiles): con valor 1-4 los turnos sin poder moverse bajan del 51% al 2-8%, sin cambiar el equilibrio.
- **No** se puede atravesar a aliados ni a enemigos.

### Atacar (dado rojo, Ataque)
- Se gastan uno o varios dados rojos contra un enemigo a la **distancia** del arma del personaje (ver abajo).
- **Valor de distancia** (propio de cada personaje/arma):
  - **Distancia 1**: cuerpo a cuerpo, solo a un enemigo **adyacente** (ortogonal, como el movimiento; por confirmar si cuenta la diagonal).
  - **Distancia N ≥ 2**: ataque a distancia, a un objetivo **a entre 2 y N casillas** (pasos ortogonales), **en cualquier dirección** y **nunca adyacente**.
- Un dado rojo **impacta** si su valor **supera** la Defensa del objetivo.
- **Daño de cada dado que impacta = margen + bono de arma.**
  - **Margen** = valor del dado − Defensa del objetivo (con Defensa 3: un 4 hace 1, un 5 hace 2, un 6 hace 3).
  - **Bono de arma** = valor fijo propio de cada personaje, que **se suma a cada dado que impacta** (p. ej. espada +0, martillo +1).
  - Bono de arma del Guerrero: **+2**.
- Con d6: contra Defensa 1 impacta con 2+ (83%), Defensa 2 con 3+ (67%), Defensa 3 con 4+ (50%).
- Decisión consciente: Defensa 1 es frágil a propósito.
- Pendiente de decidir: crítico propio por personaje, tope de daño por impacto, y ajustar la vida (con este daño, la vida de 10 a 15 podría ser razonable).

### Parar (dado verde, Defensa) — reacción
- Se usa **en el turno del rival**, cuando te atacan.
- Gastar un dado verde **anula un dado rojo** atacante de valor **igual o menor**.

### Orden de resolución de un ataque
1. El atacante gasta sus rojos y los muestra.
2. El defensor puede gastar verdes; cada uno anula un rojo de valor igual o menor.
3. Cada rojo no parado que **supere la Defensa** del objetivo causa su daño (margen + bono de arma).

## 8. Personajes

### Guerrero
- **Ataque 3 · Defensa 3 · Agilidad 1 · Especial 1**
- Aporta a la bolsa: 4 rojos, 4 verdes, 2 amarillos, 2 morados (12 dados).
- Arma: bono **+2** por dado que impacta. Distancia **1** (cuerpo a cuerpo). Movilidad fija: 2.
- Vida: 10.
- **Carga** (habilidad morada): requiere **a la vez** un **dado morado de 5 o 6** y un **dado amarillo de 5 o más**.
- Se gastan el **morado**, el **amarillo** (moverse) y **rojo** (atacar) para cargar contra un enemigo.
- El **amarillo** da el recorrido de la carga: tantas casillas como su valor (se pueden sumar más amarillos).
- El recorrido puede ser cualquiera **sin retroceder**: ningún paso puede alejarle del objetivo.
- Es una jugada **rara y fuerte** a propósito: exige guardar varios turnos un morado y un amarillo altos.
- La carga hace **doble daño**: el daño de cada rojo que impacta se **duplica**.
- Los verdes del defensor **pueden parar** los rojos de una carga como en un ataque normal.

### Arquero (borrador)
- **Ataque 1 · Defensa 1 · Agilidad 2 · Especial 3**; vida 8.
- Aporta a la bolsa: 2 rojos, 2 verdes, 3 amarillos, 4 morados (11 dados). Movilidad fija: 3. Arma (arco): bono +1, **distancia 5** (propuesta).
- **Disparo** (habilidad morada): cada **dado morado** gastado **ataca como un rojo, pero a distancia**: impacta si su valor supera la Defensa del objetivo y hace **margen + bono de arma**.
- Alcance: su **valor de distancia (5)**: objetivos **a entre 2 y 5 casillas**, en cualquier dirección y nunca adyacentes (reglas de distancia, en Atacar).
- Por confirmar: si aliados o enemigos intermedios bloquean el disparo.

### Mago (borrador)
- **Ataque 1 · Defensa 2 · Agilidad 1 · Especial 3**; vida 6.
- Aporta a la bolsa: 2 rojos, 3 verdes, 2 amarillos, 4 morados (11 dados). Movilidad fija: 2. Arma (bastón): bono +0, **distancia 3**.
- **Telequinesis** (habilidad morada): gasta un **dado morado** para **mover a un enemigo** situado a **3 casillas o menos** (puede estar adyacente), tantas casillas como el **valor del dado**, en pasos ortogonales y sin atravesar unidades.
  - Sirve para **desviar las intenciones**: apartar a un enemigo, taparle el camino, 
  - Al ser movido, el enemigo **pierde su intención de movimiento** pero **conserva la dirección de su ataque**, que parte de su nueva casilla.
- Por confirmar: si puede mover al enemigo menos casillas de las que marca el dado, y si puede mover a un aliado.

## 9. Mapa
- Tablero de **10x10** casillas.

## 10. Enemigos
### Intenciones visibles (puzle)
- **Antes de actuar, el jugador sabe lo que van a hacer los enemigos.** Al terminar el turno enemigo se **anuncian las intenciones** del siguiente: cada enemigo muestra a qué casilla se mueve y en qué dirección ataca.
- El jugador resuelve su turno **sabiendo** eso: puede eliminar a un enemigo antes de que actúe, bloquear su paso, apartarse o preparar paradas.
- Los enemigos **no tiran dados**: atacan con **dados fijos** (valores conocidos), así que el daño y las paradas se pueden calcular de antemano.
- El ataque anunciado es una **dirección relativa al enemigo**, no un héroe concreto:
  - **Golpe cuerpo a cuerpo:** hacia delante, a la casilla adyacente en esa dirección.
  - **Disparo:** en esa dirección, a lo largo de la línea y hasta su distancia, e **impacta a la primera unidad** que encuentre (aliados incluidos).
  - Si el héroe se aparta, el golpe cae en el vacío; si hay otra unidad (incluido otro enemigo), se la lleva.
- Si el enemigo es **movido** (p. ej. por la Telequinesis del Mago), **pierde su intención de movimiento** pero **conserva la dirección del ataque**, que ahora parte de su **nueva casilla**. El ataque solo se cancela si el enemigo muere.
- Se muestran con **flechas de trayectoria** sobre el mapa: una flecha por el camino de movimiento y otra con la dirección del golpe o disparo.
- Por confirmar: conducta fija de cada tipo de enemigo (hacia quién se mueve y a quién ataca) y orden en que actúan.


- Modelo anterior (a sustituir por el de puzle): enemigos idénticos a los personajes, con su propia bolsa de dados.
- Modelo de puzle (pendiente de cerrar): enemigos débiles con **dados fijos y conducta fija**, sin bolsa, e intenciones visibles (ver arriba).

## Preguntas abiertas
- Dado negro: ¿qué atributos y vida tienen flojo y fuerte? ¿Actúa el turno en que aparece? ¿Se acumulan o salen del juego?
- ¿Qué personajes hay y qué hace el morado de cada uno?
- Inconsciente: ¿qué pasa con sus dados guardados? ¿Se puede reanimar? ¿Ocupa casilla? ¿Cuándo se pierde la partida?
- ¿Cómo se alternan los turnos entre jugador y enemigos?
- ¿Para qué se usan los dados acumulados (atacar, defender, moverse) y qué hace su valor?
- ¿Qué tipo de dado es (d6 normal, caras especiales)?
- ¿Se pueden conseguir más slots durante la partida?
- ¿Cómo se colocan personajes y enemigos en el mapa al empezar?
