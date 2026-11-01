"""Enemigos que persiguen a los arqueros. Uso: python3 sim/simular4.py [partidas]
Los enemigos no cargan en ninguna variante, para comparar en igualdad: 'cerca' va al héroe más próximo,
'arqueros' va al arquero más próximo (si hay alguno consciente) y ataca a un arquero adyacente antes que a otros.
"""
import random, sys
from collections import Counter
import simular2 as m2
import simular3 as m3
from simular2 import FLOJO, FUERTE


class Game4(m3.Game3):
    def __init__(s, chase="cerca", **kw):
        super().__init__(**kw)
        s.chase = chase

    def act(s, u):
        if u.ko or u.side == 0:
            return m3.Game3.act(s, u)
        s.free_step = u.move
        heroes = s.alive(0)
        if not heroes:
            return
        arch = [h for h in heroes if h.cls == "a"]
        goals = arch if (s.chase == "arqueros" and arch) else heroes

        def pref(adj):
            if s.chase == "arqueros":
                a = [h for h in adj if h.cls == "a"]
                if a:
                    return a
            return adj
        adj = s.adjacent_enemies(u)
        if not adj:
            budget = sum(u.dice["y"]) + u.move
            seen = s.bfs(u, budget)
            seen[(u.x, u.y)] = 0
            dest = min(seen, key=lambda c: (min(s.dist(c, (g.x, g.y)) for g in goals), seen[c]))
            k = seen[dest]
            if k > 0:
                need = k - u.move
                if need > 0 and u.dice["y"]:
                    s.spend(u, "y", s.pick_sum(list(u.dice["y"]), need) or list(u.dice["y"]))
                u.x, u.y = dest
            adj = s.adjacent_enemies(u)
        if adj and u.dice["r"]:
            tgt = min(pref(adj), key=lambda e: e.hp)
            reds = list(u.dice["r"]); s.spend(u, "r", reds)
            s.attack(u, tgt, reds, False)


def run(n, **kw):
    out = Counter(); fall = []; tot = Counter()
    for i in range(n):
        g = Game4(rng=random.Random(i), **kw)
        w, r = g.play()
        out["caen" if w == 1 else "sobreviven"] += 1
        if w == 1:
            fall.append(r)
        tot["aparecidos"] += g.spawned; tot["bajas"] += g.kills
        tot["ko_g"] += sum(1 for u in g.units if u.cls == "g" and u.ko)
        tot["ko_a"] += sum(1 for u in g.units if u.cls == "a" and u.ko)
    fall.sort()
    return {"sobreviven_%": round(100 * out["sobreviven"] / n, 1),
            "caen_ronda_mediana": fall[len(fall) // 2] if fall else "-",
            "enemigos_derrotados": round(tot["bajas"] / n, 1),
            "guerreros_ko": round(tot["ko_g"] / n, 2), "arqueros_ko": round(tot["ko_a"] / n, 2)}


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    t56 = lambda v: FLOJO if v == 5 else (FUERTE if v == 6 else None)
    for tname, tab in [("negro: solo 5-6", t56), ("negro: 1-3 flojo, 4-6 fuerte", None)]:
        for chase, fm in (("cerca", 2), ("cerca", 4), ("arqueros", 4)):
            kw = dict(party=list("gggaa"), draw_policy="adapt", chase=chase, flojo_move=fm)
            if tab:
                kw["spawn_table"] = tab
            print(f"\n== 3G+2A, {tname}, flojo con movilidad {fm}, enemigos van a: {chase} ({n} partidas) ==")
            for k, v in run(n, **kw).items():
                print(f"  {k}: {v}")
