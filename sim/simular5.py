"""Nivel de puzle: enemigos débiles con dados fijos, se activan al acercarse; hay que limpiar y salir (fila superior).
Uso: python3 sim/simular5.py [partidas]
Los héroes juegan con la IA sencilla (sin Mago). El dado negro no genera enemigos: solo cuenta los rellenos de bolsa.
"""
import random, sys
from collections import Counter
import simular as base
import simular3 as m3
from simular2 import FLOJO, FUERTE, COLS

AGGRO = 7
# (clase, x, y)
NIVEL = [("f", 1, 5), ("f", 3, 4), ("f", 5, 5), ("f", 7, 4), ("f", 2, 2), ("f", 6, 2), ("F", 4, 3), ("F", 5, 1)]
FIJOS = {"f": [4], "F": [5]}          # dados rojos fijos de ataque
TIPOS = {"f": (FLOJO, 4), "F": (FUERTE, 2)}   # (atributos/vida/arma, movilidad)


class Game5(m3.Game3):
    def __init__(s, nivel=NIVEL, **kw):
        super().__init__(foes0=0, spawn_table=lambda v: None, **kw)
        for k, x, y in nivel:
            (stats, hp, w), mv = TIPOS[k]
            u = base.Unit(1, len([v for v in s.units if v.side == 1]), hp, stats)
            u.weapon, u.x, u.y, u.move, u.dist, u.cls = w, x, y, mv, 1, "e"
            u.fixed, u.active = FIJOS[k], False
            s.units.append(u)

    def go_exit(s, u):
        budget = sum(u.dice["y"]) + u.move
        seen = s.bfs(u, budget)
        seen[(u.x, u.y)] = 0
        dest = min(seen, key=lambda c: (c[1], seen[c]))
        k = seen[dest]
        if k > 0:
            need = k - u.move
            if need > 0 and u.dice["y"]:
                s.spend(u, "y", s.pick_sum(list(u.dice["y"]), need) or list(u.dice["y"]))
            u.x, u.y = dest

    def turn(s, side):
        if side == 0:
            s.place(0, s.draw(0))
            if s.alive(1):
                for u in sorted(s.alive(0), key=lambda u: s.dist((u.x, u.y), (s.nearest_enemy(u).x, s.nearest_enemy(u).y))):
                    if s.alive(1):
                        s.act(u)
            else:
                for u in s.alive(0):
                    s.free_step = u.move
                    s.go_exit(u)
            for u in s.alive(0):
                for c in COLS:
                    u.dice[c] = [min(6, v + 1) for v in u.dice[c]]
        else:
            heroes = s.alive(0)
            for u in s.alive(1):
                if not u.active and heroes and min(s.dist((u.x, u.y), (h.x, h.y)) for h in heroes) <= AGGRO:
                    u.active = True
                if u.active and s.alive(0):
                    u.dice["r"] = list(u.fixed)
                    s.act(u)

    def play(s, max_rounds=40):
        for rnd in range(1, max_rounds + 1):
            s.turn(0)
            if not s.alive(1) and all(u.y == 0 for u in s.alive(0)):
                return "gana", rnd
            s.turn(1)
            if not s.alive(0):
                return "pierde", rnd
        return "tiempo", max_rounds


def run(n, **kw):
    res = Counter(); rounds = []; tot = Counter()
    for i in range(n):
        g = Game5(rng=random.Random(i), **kw)
        r, rnd = g.play()
        res[r] += 1
        if r == "gana":
            rounds.append(rnd)
        tot["rellenos"] += g.blacks[0]
        tot["ko"] += sum(1 for u in g.units if u.side == 0 and u.ko)
        tot["kills"] += g.kills
    rounds.sort()
    return {"gana_%": round(100 * res["gana"] / n, 1), "pierde_%": round(100 * res["pierde"] / n, 1),
            "sin_acabar_%": round(100 * res["tiempo"] / n, 1),
            "rondas_mediana_si_gana": rounds[len(rounds) // 2] if rounds else "-",
            "rondas_p10_p90": (rounds[len(rounds) // 10], rounds[9 * len(rounds) // 10]) if rounds else "-",
            "rellenos_de_bolsa_media": round(tot["rellenos"] / n, 1),
            "heroes_inconscientes_media": round(tot["ko"] / n, 2),
            "enemigos_derrotados_media": round(tot["kills"] / n, 1)}


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    for name, kw in [("2 Guerreros + 2 Arqueros, robar 1-2 (adaptativo)", dict(party=list("ggaa"), draw_policy="adapt")),
                     ("2 Guerreros + 2 Arqueros, robar siempre 2", dict(party=list("ggaa"))),
                     ("2 Guerreros + 2 Arqueros, robar siempre 1", dict(party=list("ggaa"), draw_policy="uno")),
                     ("4 Guerreros, robar 1-2 (adaptativo)", dict(party=list("gggg"), draw_policy="adapt"))]:
        print(f"\n== {name} ({n} partidas, máx. 40 rondas) ==")
        for k, v in run(n, **kw).items():
            print(f"  {k}: {v}")
