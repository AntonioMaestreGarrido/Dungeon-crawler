"""Simulador con Guerreros y Arqueros (valor de distancia). Uso: python3 sim/simular3.py [partidas]
Arquero: dispara con rojos y morados a objetivos a 2..5 casillas (cualquier dirección, sin bloqueo);
se aleja de los enemigos adyacentes y busca una casilla desde la que disparar.
"""
import random, sys
from collections import Counter
import simular2 as m2
from simular2 import Game2, FLOJO, FUERTE
from simular import Game


class Game3(Game2):
    def dist_to(s, u, e):
        return s.dist((u.x, u.y), (e.x, e.y))

    def act(s, u):
        if u.ko:
            return
        s.free_step = u.move
        if u.cls != "a":
            return Game2.act(s, u)
        enemies = s.alive(1 - u.side)
        if not enemies:
            return
        # moverse a la mejor casilla para disparar
        budget = sum(u.dice["y"]) + u.move
        seen = s.bfs(u, budget)
        seen[(u.x, u.y)] = 0

        def score(cell):
            ds = [s.dist(cell, (e.x, e.y)) for e in enemies]
            inrange = [d for d in ds if 2 <= d <= u.dist]
            adj = sum(1 for d in ds if d == 1)
            near2 = sum(1 for d in ds if d <= 2)
            return (-adj, bool(inrange), -near2, -min(ds) if min(ds) > u.dist else 0, -seen[cell])
        dest = max(seen, key=score)
        k = seen[dest]
        if k > 0:
            need = k - u.move
            if need > 0 and u.dice["y"]:
                s.spend(u, "y", s.pick_sum(list(u.dice["y"]), need) or list(u.dice["y"]))
            u.x, u.y = dest
        targets = [e for e in enemies if 2 <= s.dist_to(u, e) <= u.dist]
        dice = list(u.dice["p"]) + list(u.dice["r"])
        if targets and dice:
            tgt = min(targets, key=lambda e: e.hp)
            s.spend(u, "p", list(u.dice["p"]))
            s.spend(u, "r", list(u.dice["r"]))
            s.attack(u, tgt, dice, False)


def run(n, **kw):
    out = Counter(); fall = []; tot = Counter()
    for i in range(n):
        g = Game3(rng=random.Random(i), **kw)
        w, r = g.play()
        out["caen" if w == 1 else "sobreviven"] += 1
        if w == 1:
            fall.append(r)
        tot["aparecidos"] += g.spawned
        tot["bajas"] += g.kills
        tot["heroes_ko"] += sum(1 for u in g.units if u.side == 0 and u.ko)
        tot["ko_g"] += sum(1 for u in g.units if u.cls == "g" and u.ko)
        tot["ko_a"] += sum(1 for u in g.units if u.cls == "a" and u.ko)
        tot["dano_g"] += g.st["dano_g"]; tot["dano_a"] += g.st["dano_a"]
        tot["cargas"] += g.st["cargas"]
    fall.sort()
    dg, da = tot["dano_g"], tot["dano_a"]
    return {
        "sobreviven_%": round(100 * out["sobreviven"] / n, 1),
        "caen_ronda_mediana": fall[len(fall) // 2] if fall else "-",
        "enemigos_aparecidos": round(tot["aparecidos"] / n, 1),
        "enemigos_derrotados": round(tot["bajas"] / n, 1),
        "heroes_inconscientes": round(tot["heroes_ko"] / n, 2),
        "guerreros_ko": round(tot["ko_g"] / n, 2),
        "arqueros_ko": round(tot["ko_a"] / n, 2),
        "reparto_daño_arqueros_%": round(100 * da / max(1, dg + da), 1),
    }


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    t56 = lambda v: FLOJO if v == 5 else (FUERTE if v == 6 else None)
    base = dict(spawn_table=t56, draw_policy="adapt")
    for name, kw in [("4 Guerreros (vida 10)", dict(base, party=list("gggg"))),
                     ("5 Guerreros (vida 10)", dict(base, party=list("ggggg"))),
                     ("3 Guerreros + 2 Arqueros (vida 10 y 8)", dict(base, party=list("gggaa"))),
                     ("3 Guerreros + 2 Arqueros (vida 15 y 12)", dict(base, party=list("gggaa"), hp_bonus=5)),
                     ("2 Guerreros + 3 Arqueros (vida 10 y 8)", dict(base, party=list("ggaaa")))]:
        print(f"\n== {name} ({n} partidas, 80 rondas) ==")
        for k, v in run(n, **kw).items():
            print(f"  {k}: {v}")
