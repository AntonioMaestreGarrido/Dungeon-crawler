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
