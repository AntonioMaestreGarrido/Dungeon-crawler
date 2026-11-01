"""Simulador con las reglas de noviembre: daño = margen + arma, dado de movilidad fijo,
carga con morado 5+ y amarillo 5+, y el dado negro hace aparecer enemigos.
Uso: python3 sim/simular2.py [partidas]
Supuestos: los dados negros solo entran en la bolsa de los héroes; el enemigo aparece en una
casilla libre del borde del mapa y actúa en el siguiente turno enemigo; la partida sigue aunque
no queden enemigos (llegarán más) y dura como máximo `max_rounds` rondas.
"""
import random, sys
from collections import Counter
import simular as base
from simular import Game, Unit, COLS

FLOJO = ({"r": 2, "g": 1, "y": 1, "p": 1}, 5, 0)    # atributos, vida, bono de arma
FUERTE = ({"r": 3, "g": 2, "y": 1, "p": 1}, 10, 1)
HEROE = ({"r": 3, "g": 3, "y": 1, "p": 1}, 10, 2)
# clase: atributos, vida, bono de arma, movilidad fija, distancia
CLASES = {
    "g": ({"r": 3, "g": 3, "y": 1, "p": 1}, 10, 2, 2, 1),
    "a": ({"r": 1, "g": 1, "y": 2, "p": 3}, 8, 1, 3, 5),
}


class Game2(Game):
    def __init__(s, hero_hp=10, foes0=4, foe0=FLOJO, rng=None, black_returns=True, spawn_table=None, draw_policy='dos', party=None, hp_bonus=0, flojo_move=2):
        super().__init__(free_step=2, rng=rng, hp=hero_hp, dmg_mode="margen", foes=0)
        s.units = []
        for i, cl in enumerate(party or ["g"] * 4):
            st, hp0, w, mv, dist = CLASES[cl]
            u = Unit(0, i, hp0 + hp_bonus if party else hero_hp, st)
            u.weapon, u.move, u.dist, u.cls = w, mv, dist, cl
            s.units.append(u)
        s.bag = [[], []]
        for u in s.units:
            for c in COLS:
                s.bag[0] += [c] * (u.stats[c] + 1)
        s.disc = [[], []]
        s.draw_policy = draw_policy
        s.flojo_move = flojo_move
        s.black_returns = black_returns
        s.spawn_table = spawn_table or (lambda v: FLOJO if v <= 3 else FUERTE)
        s.spawned = 0
        s.kills = 0
        for _ in range(foes0):
            s.spawn_unit(*foe0)

    def spawn_unit(s, stats, hp, weapon):
        used = s.occ()
        n = base.N
        cells = [(x, y) for x in range(n) for y in range(n)
                 if (x in (0, n - 1) or y in (0, n - 1)) and (x, y) not in used]
        if not cells:
            return
        x, y = s.rng.choice(cells)
        u = Unit(1, len([v for v in s.units if v.side == 1]), hp, stats)
        u.weapon, u.x, u.y = weapon, x, y
        u.move, u.dist, u.cls = (s.flojo_move if stats is FLOJO[0] else 2), 1, 'e'
        s.units.append(u)
        for c in COLS:
            s.bag[1] += [c] * (u.stats[c] + 1)

    def draw(s, side):
        out = []
        if side == 0 and s.draw_policy != 'dos':
            n = 0
            for u in s.alive(0):
                free = sum(max(0, u.stats[c] - len(u.dice[c])) for c in COLS)
                n += 1 if (s.draw_policy == 'uno' or free < 4) else 2
        else:
            n = 2 * len(s.alive(side))
        for _ in range(n):
            if not s.bag[side]:
                if not s.disc[side]:
                    break
                s.bag[side], s.disc[side] = s.disc[side], []
                if side == 0:
                    s.bag[0].append("k"); s.blacks[0] += 1
            c = s.bag[side].pop(s.rng.randrange(len(s.bag[side])))
            out.append((c, s.rng.randint(1, 6)))
        return out

    def place(s, side, pool):
        rest = []
        for c, v in pool:
            if c == "k":
                if s.black_returns:
                    s.disc[side].append("k")
                s.spawned += 1 if s.spawn_table(v) else 0
                kind = s.spawn_table(v)
                if kind:
                    s.spawn_unit(*kind)
                else:
                    s.st['negros_sin_efecto'] += 1
            else:
                rest.append((c, v))
        super().place(side, rest)

    def attack(s, att, tgt, reds, charge):
        reds = sorted(reds, reverse=True)
        s.st["ataques"] += 1
        defense = tgt.stats["g"]
        dmg = 0
        for r in reds:
            if r <= defense:
                continue
            greens = sorted(v for v in tgt.dice["g"] if v >= r)
            if greens:
                s.spend(tgt, "g", [greens[0]]); s.st["paradas"] += 1
                continue
            dmg += (r - defense) + att.weapon
        dmg *= 2 if charge else 1
        s.st["cargas"] += charge
        s.st["dano"] += dmg
        s.st["dano_" + att.cls] += dmg
        tgt.hp -= dmg
        if tgt.hp <= 0:
            tgt.hp, tgt.ko = 0, True
            tgt.x = tgt.y = -9
            if tgt.side == 1:
                s.kills += 1

    def act(s, u):
        if u.ko:
            return
        # carga: morado 5+ y amarillo 5+
        if (u.dice["p"] and max(u.dice["p"]) >= 5 and u.dice["y"] and max(u.dice["y"]) >= 5
                and u.dice["r"] and not s.adjacent_enemies(u)):
            top = max(u.dice["y"])
            budget = top + sum(v for v in u.dice["y"]) - top + s.free_step
            best = None
            for e in s.alive(1 - u.side):
                seen = s.bfs(u, budget, (e.x, e.y))
                for p, k in seen.items():
                    if k > 0 and s.dist(p, (e.x, e.y)) == 1 and (best is None or k < best[0]):
                        best = (k, p, e)
            if best:
                k, p, e = best
                s.spend(u, "y", [top])
                need = k - top - s.free_step
                if need > 0:
                    s.spend(u, "y", s.pick_sum(list(u.dice["y"]), need) or list(u.dice["y"]))
                s.spend(u, "p", [max(u.dice["p"])])
                u.x, u.y = p
                reds = list(u.dice["r"]); s.spend(u, "r", reds)
                s.attack(u, e, reds, True)
                return
        super().act(u)

    def play(s, max_rounds=80):
        for rnd in range(1, max_rounds + 1):
            for side in (0, 1):
                s.turn(side)
                if not s.alive(0):
                    return 1, rnd
        return None, max_rounds


def run(n, **kw):
    out = Counter(); fall = []; tot = Counter()
    for i in range(n):
        g = Game2(rng=random.Random(i), **kw)
        w, r = g.play()
        out["caen" if w == 1 else "sobreviven"] += 1
        if w == 1:
            fall.append(r)
        tot["aparecidos"] += g.spawned
        tot["bajas"] += g.kills
        tot["vida"] += sum(u.hp for u in g.units if u.side == 0)
        tot["heroes_ko"] += sum(1 for u in g.units if u.side == 0 and u.ko)
        tot["dano"] += g.st["dano"]; tot["ataques"] += g.st["ataques"]; tot["cargas"] += g.st["cargas"]
        tot["alive_enemy"] += len(g.alive(1))
    fall.sort()
    return {
        "heroes_sobreviven_%": round(100 * out["sobreviven"] / n, 1),
        "ronda_en_que_caen_mediana": fall[len(fall) // 2] if fall else "-",
        "enemigos_aparecidos": round(tot["aparecidos"] / n, 1),
        "enemigos_derrotados": round(tot["bajas"] / n, 1),
        "enemigos_vivos_al_final": round(tot["alive_enemy"] / n, 1),
        "heroes_inconscientes": round(tot["heroes_ko"] / n, 2),
        "dano_por_ataque": round(tot["dano"] / max(1, tot["ataques"]), 2),
        "cargas_por_partida": round(tot["cargas"] / n, 2),
    }


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    t56 = lambda v: FLOJO if v == 5 else (FUERTE if v == 6 else None)
    for name, kw in [("Robar 2 por personaje (fijo), 1-3 flojo 4-6 fuerte", dict(hero_hp=15)),
                     ("Robar 1-2 (adaptativo), 1-3 flojo 4-6 fuerte", dict(hero_hp=15, draw_policy='adapt')),
                     ("Robar siempre 1, 1-3 flojo 4-6 fuerte", dict(hero_hp=15, draw_policy='uno')),
                     ("Robar 2 (fijo), solo 5 y 6", dict(hero_hp=15, spawn_table=t56)),
                     ("Robar 1-2 (adaptativo), solo 5 y 6", dict(hero_hp=15, spawn_table=t56, draw_policy='adapt')),
                     ("Robar siempre 1, solo 5 y 6", dict(hero_hp=15, spawn_table=t56, draw_policy='uno'))]:
        print(f"\n== {name} ({n} partidas, 80 rondas) ==")
        for k, v in run(n, **kw).items():
            print(f"  {k}: {v}")
