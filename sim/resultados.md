# Simulaciones — 1 de noviembre de 2026

4 Guerreros (3/3/1/1, 10 de vida) contra 4 enemigos idénticos, con una IA sencilla en ambos bandos:
coloca los dados donde más sirven, avanza hacia el enemigo más cercano, ataca en cuanto está adyacente
con todos sus rojos, carga si puede, y para con el verde más bajo que sirva. Los Héroes juegan primero.
Una "ronda" = turno de Héroes + turno de Enemigos. Script: `simular.py`.

## Reglas actuales (2000 partidas)
| Métrica | Valor |
|---|---|
| Victorias Héroes / Enemigos / sin terminar (200 rondas) | 57,5% / 41,1% / 1,4% |
| Rondas por partida (mediana; 10%–90%) | 63 (41–117) |
| Turnos de personaje sin poder moverse (estando lejos del enemigo) | **53,5%** |
| Dados perdidos por no tener slot libre | 23,9% |
| Daño medio por ataque | **0,37** |
| Paradas por ataque | 0,73 |
| Ataques que son carga | 1,9% |
| Dados negros añadidos por bando y partida | 10,4 |

## Variantes (2000 partidas, salvo indicación)
| Variante | Héroes gana | Rondas (mediana) | Sin poder mover | Daño/ataque |
|---|---|---|---|---|
| Reglas actuales | 57,5% | 63 | 53,5% | 0,37 |
| B: paso básico de 1 casilla gratis | 57,9% | 69 | 5,0% | 0,34 |
| C: cualquier dado mueve 1 | 41,1% | 69 | 33,7% | 0,33 |
| B + C | 35,4% | 70 | 5,6% | 0,32 |
| B + vida 6 (1000) | 62,9% | 37 | — | 0,35 |
| B + parar solo con verde **mayor** (1000) | 61,2% | 55 | — | 0,52 |
| B + vida 6 + verde mayor (1000) | 66,1% | 30 | — | 0,54 |

## Conclusiones
1. **El bloqueo de movimiento es real**: más de la mitad de los turnos un personaje lejos del enemigo no puede moverse. El paso básico (B) lo baja al 5%.
2. **Las partidas son demasiado largas**: unas 60-70 rondas. El daño por ataque es muy bajo (0,37) porque con Defensa 3 el rojo necesita 4+ y los verdes guardados crecen hasta 5-6 y lo paran casi todo.
3. **Jugar primero da ventaja** (57-66%), y crece cuanto más corto es el combate.
4. La carga casi nunca ocurre: un solo slot morado y un solo amarillo hacen difícil reunir morado 5+, amarillo y rojo a la vez.
5. Los resultados de C dependen mucho de la IA (gasta verdes para moverse), así que no son fiables.

Limitaciones: la IA es simple (ataca siempre que puede, no guarda rojos para que crezcan, no se agrupa), así que los números son orientativos.

## Enemigos más débiles (todas con paso básico de 1 casilla; 600-1000 partidas)
Héroes: 4 Guerreros 3/3/1/1, vida 10 (40 de vida en total).

| Enemigos | Héroes gana | Rondas (mediana; 10%–90%) | Héroes inconscientes | Vida de héroes al final |
|---|---|---|---|---|
| 4 iguales (3/3/1/1, vida 10) | 58% | 69 (45–128) | — | — |
| 4 de 2/2/1/1, vida 10 | 100% | 30 (25–38) | 0,14 | 33 |
| 4 de 2/2/1/1, vida 6 | 100% | 19 (15–23) | 0,01 | 36 |
| 4 de 2/1/1/1, vida 5 | 100% | 11 (9–12) | 0,01 | 37 |
| 6 de 2/2/1/1, vida 6 | 86% | 39 (28–64) | 1,2 | 21 |
| 8 de 2/1/1/1, vida 5 | 83% | 28 (21–40) | 1,5 | 16 |
| 8 de 2/2/1/1, vida 6 | 1% | 26 (19–38) | 4,0 | 0 |
| 10 de 2/1/1/1, vida 5 | 0% | 20 (14–36) | 3,8 | 1 |

Conclusiones:
- Con 4 enemigos débiles los héroes ganan siempre y casi sin daño: la partida pierde tensión.
- La fuerza de un bando depende sobre todo de **cuántos dados saca por turno** (2 por personaje vivo). Más enemigos = más dados, y eso pesa más que sus atributos.
- La zona interesante está en **6-8 enemigos débiles**: los héroes ganan el 83-86% pero pierden más o menos la mitad de su vida y 1-2 personajes. Entre 6 y 8 enemigos de 2/2/1/1 el equilibrio cambia muy deprisa.

## Dos slots amarillos (Agilidad 2) — 800 partidas
| Variante | Sin poder mover | Héroes gana | Rondas (mediana) |
|---|---|---|---|
| Agilidad 1, sin paso, vs iguales | 53,6% | 56% | 62 |
| Agilidad 1 + paso básico, vs iguales | 5,3% | 57% | 70 |
| Agilidad 2, sin paso, vs iguales (Agilidad 2) | 50,3% | 58% | 65 |
| Agilidad 2 + paso, vs iguales (Agilidad 2) | 4,1% | 52% | 67 |
| Agilidad 1 + paso, vs 6 de 2/2/1/1 vida 6 | 7,9% | 86% | 39 |
| Agilidad 2, sin paso, vs 6 débiles | 50,7% | 75% | 42 |
| Agilidad 2 + paso, vs 6 débiles | 12,0% | 74% | 42 |

Con Agilidad 2 salen ~1,8 amarillos por turno para 4 héroes: más slots dejan guardar, pero no crean más amarillos.
Además diluyen la bolsa (menos rojos y verdes) y los héroes rinden peor contra 6 enemigos débiles.

## Amarillos de uno en uno (máximo 1 amarillo por personaje y turno) — vs 6 de 2/2/1/1 vida 6, 800 partidas
| Variante | Sin poder mover | Héroes gana | Rondas (mediana) |
|---|---|---|---|
| Agilidad 1, sin límite | 51,0% | 86% | 38 |
| Agilidad 2, sin límite | 50,7% | 75% | 42 |
| Agilidad 2, de uno en uno | 48,3% | 79% | 40 |
| Agilidad 1 + paso básico | 7,9% | 86% | 39 |
| Agilidad 2 de uno en uno + paso | 9,8% | 77% | 41 |

Repartir los amarillos en el tiempo apenas ayuda: el límite es cuántos amarillos salen de la bolsa, no cómo se gastan.

## Dado fijo de movilidad (d6 propio por personaje, fuera de la bolsa) — 800 partidas
| Variante | Sin poder mover | Héroes gana | Rondas (mediana) |
|---|---|---|---|
| vs 6 débiles, sin nada | 51,0% | 86% | 38 |
| vs 6 débiles, paso básico 1 | 7,9% | 86% | 39 |
| vs 6 débiles, dado fijo | 3,0% | 84% | 39 |
| vs 4 iguales, dado fijo | 1,5% | 55% | 71 |

## Dado fijo con valor fijo (movimiento base sin tirar) — vs 6 débiles, 800 partidas
| Valor | Sin poder mover | Héroes gana | Rondas (mediana) |
|---|---|---|---|
| 1 | 7,9% | 86% | 39 |
| 2 | 6,5% | 81% | 41 |
| 3 | 3,8% | 82% | 41 |
| 4 | 1,7% | 86% | 39 |

## Armadura de 1 solo en los héroes — vs 6 de 2/2/1/1 vida 6 (con dado de movilidad), 800 partidas
| Tipo de armadura | Héroes gana | Rondas (mediana) | Vida de héroes al final | Héroes inconscientes |
|---|---|---|---|---|
| Sin armadura | 84% | 39 | 21,7 | 1,2 |
| Umbral: el rojo debe superar Defensa + 1 | 100% | 34 | 33,0 | 0,15 |
| Absorbe 1 herida por ataque | 100% | 34 | 37,2 | 0 |
| Reduce 1 por impacto (mínimo 1) | 97% | 36 | 27,7 | 0,5 |

Con el daño actual (0,4 heridas por ataque), una armadura de 1 es muy fuerte: hay que dársela con cuentagotas.

## Armadura en espejo (4 Guerreros 3/3/1/1 contra 4 iguales, movilidad fija 2 en ambos bandos, 800 partidas)
Armadura 1 en **ambos** bandos, para valorar sin sesgo.
| Variante | Héroes gana | Rondas (mediana; 10%–90%) | Sin terminar (200 rondas) |
|---|---|---|---|
| Sin armadura | 55% | 70 (45–135) | 2% |
| Umbral (rojo debe superar Defensa + 1) | 38% | 153 (84–200) | 31% |
| Reduce 1 por impacto (mínimo 1) | 46% | 113 (77–195) | 9% |
| Absorbe 1 herida por ataque | 11% | 200 (174–200) | 81% |

## Armadura solo en los héroes, enemigos idénticos sin armadura (4 vs 4 de 3/3/1/1, movilidad fija 2, 1000 partidas)
| Armadura 1 en los héroes | Héroes gana | Enemigos gana | Rondas (mediana) |
|---|---|---|---|
| Sin armadura (referencia) | 54% | 44% | 70 |
| Umbral (rojo > Defensa + 1) | 96,5% | 2,3% | 57 |
| Reduce 1 por impacto (mínimo 1) | 84% | 13,5% | 69 |
| Absorbe 1 herida por ataque | 99,8% | 0% | 56 |

Armadura 1 vale más que cualquier otro cambio probado: un personaje con armadura 1 contra uno idéntico sin ella gana casi siempre.

## Daño por impacto: 1 frente a margen (rojo − Defensa) — espejo 4v4 de 3/3/1/1, movilidad fija 2, 800 partidas
| Daño | Vida | Daño medio por ataque | Rondas (mediana; 10%–90%) | Héroes gana |
|---|---|---|---|---|
| 1 por impacto | 10 | 0,33 | 70 (45–135) | 55% |
| Margen | 10 | 0,72 | 32 (22–53) | 64% |
| Margen | 15 | 0,70 | 50 (32–88) | 58% |
| Margen | 20 | 0,70 | 66 (45–123) | 54% |

Armadura 1 solo en los héroes con daño = margen y vida 15: los héroes ganan el 99,5% (sin armadura, 58,5%). La armadura sigue siendo muy dominante.

## Reglas de noviembre (daño = margen + arma, movilidad fija 2, carga con morado 5+ y amarillo 5+, el dado negro hace aparecer un enemigo)
Script: `simular2.py`. 300 partidas, 80 rondas como máximo, 4 héroes (3/3/1/1, arma +2) contra 4 enemigos flojos iniciales.
Flojo: 2/1/1/1, vida 5, arma +0 (1-3). Fuerte: 3/2/1/1, vida 10, arma +1 (4-6). Aparecen en el borde del mapa y actúan en el siguiente turno enemigo.
Solo la bolsa de los héroes recibe dados negros.

| Variante | Héroes sobreviven | Ronda en que caen (mediana) | Enemigos aparecidos | Derrotados |
|---|---|---|---|---|
| Los negros vuelven y se acumulan, vida 10 | 0% | 37 | 33 | 25 |
| Los negros vuelven y se acumulan, vida 15 | 0% | 38 | 35 | 24 |
| Los negros vuelven y se acumulan, vida 20 | 0% | 40 | 37 | 25 |
| El negro sale del juego al usarse, vida 10 | 100% | — | 35 | 39 |
| El negro sale del juego al usarse, vida 15 | 100% | — | 35 | 39 |

Observaciones:
- La IA acumula dados en las hojas (hasta 32 de los 48), así que solo circulan unos 16 y **la bolsa se rellena cada ~2 rondas**. Cada relleno añade un negro: aparece un enemigo cada ~2 rondas, y si los negros vuelven y se acumulan, el ritmo sube sin parar.
- Con el daño actual (margen + arma +2, ×2 en carga) un enemigo flojo (vida 5) muere de un golpe: el daño medio por ataque es 6 y las cargas son frecuentes (~9 por partida).
- Hay un punto medio sin probar: por ejemplo, un máximo de negros en la bolsa.

## Solo 5 y 6 del dado negro añaden enemigos (5 = flojo, 6 = fuerte; 1-4 sin efecto) — 300 partidas, 80 rondas
Mismas reglas que la tabla anterior (los negros vuelven y se acumulan).

| Variante | Héroes sobreviven | Ronda en que caen (mediana) | Enemigos aparecidos | Derrotados | Cargas por partida |
|---|---|---|---|---|---|
| 1-3 flojo, 4-6 fuerte, vida 15 | 0% | 38 | 35 | 24 | 8,7 |
| Solo 5 y 6, vida 10 | 19% | 66 | 41 | 36 | 16,5 |
| Solo 5 y 6, vida 15 | 21% | 68 | 43 | 37 | 16,5 |
| Solo 5 y 6, vida 20 | 26% | 69 | 45 | 37 | 16,6 |

Casi se duplica la supervivencia en rondas (de 38 a ~67), pero los héroes siguen cayendo el ~75-80% de las veces: como los negros se acumulan, el ritmo sigue subiendo con cada relleno.
