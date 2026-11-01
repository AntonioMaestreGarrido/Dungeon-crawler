# Dungeon crawler (juego de mesa) — Reglas en construcción

_Documento vivo. Se va completando paso a paso._

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
1. **Sacar y tirar**: se sacan de la bolsa un número fijo de dados (de momento, **2 por personaje**, 8 en total) y se tiran.
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
- Cuando la bolsa se vacía, **se rellena solo con los dados gastados y perdidos** (los guardados en las hojas se quedan donde están).
- En cada relleno se **añade un dado negro nuevo**: se van acumulando.
- El efecto del dado negro está **por determinar**.

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
- Se gastan uno o varios dados rojos contra un enemigo **adyacente** (ortogonal, como el movimiento; por confirmar si cuenta la diagonal).
- Un dado rojo **impacta** si su valor **supera** la Defensa del objetivo.
- **Daño de cada dado que impacta = margen + bono de arma.**
  - **Margen** = valor del dado − Defensa del objetivo (con Defensa 3: un 4 hace 1, un 5 hace 2, un 6 hace 3).
  - **Bono de arma** = valor fijo propio de cada personaje, que **se suma a cada dado que impacta** (p. ej. espada +0, martillo +1).
  - Valor del Guerrero: por definir (propuesta: +0).
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
- Vida: 10.
- **Carga** (habilidad morada): requiere un **dado morado de 5 o 6**.
- Se gastan el **morado**, **amarillo** (moverse) y **rojo** (atacar) para cargar contra un enemigo.
- El recorrido puede ser cualquiera **sin retroceder**: ningún paso puede alejarle del objetivo.
- La carga hace **doble daño**: el daño de cada rojo que impacta se **duplica**.
- Los verdes del defensor **pueden parar** los rojos de una carga como en un ataque normal.

## 9. Mapa
- Tablero de **10x10** casillas.

## 10. Enemigos
- De momento, los enemigos son **idénticos a los personajes**: mismos atributos, mismas reglas de slots, turno y acciones.
- Usan **su propia bolsa** de dados, construida igual que la del jugador.

## Preguntas abiertas
- ¿Qué personajes hay y qué hace el morado de cada uno?
- Inconsciente: ¿qué pasa con sus dados guardados? ¿Se puede reanimar? ¿Ocupa casilla? ¿Cuándo se pierde la partida?
- ¿Cómo se alternan los turnos entre jugador y enemigos?
- ¿Qué hace el dado negro?
- ¿Para qué se usan los dados acumulados (atacar, defender, moverse) y qué hace su valor?
- ¿Qué tipo de dado es (d6 normal, caras especiales)?
- ¿Se pueden conseguir más slots durante la partida?
- ¿Cómo se colocan personajes y enemigos en el mapa al empezar?
