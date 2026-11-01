"""Simulador de partidas del dungeon crawler con las reglas de docs/reglas.md.

Ambos bandos son 4 Guerreros (Ataque 3, Defensa 3, Agilidad 1, Especial 1, 10 de vida)
controlados por una IA sencilla. Uso: python3 sim/simular.py [partidas]
"""
import random, sys
from collections import deque, Counter

N = 10
COLS = "rgyp"
STATS = {"r": 3, "g": 3, "y": 1, "p": 1}


class Unit:
    def __init__(s, side, i, hp=10, stats=None):
        s.side, s.i = side, i
        s.hp = hp
        s.stats = dict(stats or STATS)
        s.x, s.y = 3 + i, (0 if side else 9)
        s.ko = False
        s.dice = {c: [] for c in COLS}


class Game:
    def __init__(s, free_step=0, any_die_move=False, rng=None, hp=10, strict_parry=False, foe_stats=None, foe_hp=None, foes=4, hero_stats=None, one_yellow=False, fixed_move_die=False):
        s.rng = rng or random.Random()
        s.free_step, s.any_die_move, s.strict_parry = free_step, any_die_move, strict_parry
        s.one_yellow = one_yellow
        s.fixed_move_die = fixed_move_die
        s.units = [Unit(0, i, hp, hero_stats) for i in range(4)] + [Unit(1, i, foe_hp or hp, foe_stats) for i in range(foes)]
        s.bag = [[], []]
        for u in s.units:
            for c in COLS:
                s.bag[u.side] += [c] * (u.stats[c] + 1)
        s.disc = [[], []]
        s.blacks = [0, 0]
        st = Counter()
        s.st = st

    # --- utilidades ---
    def alive(s, side):
        return [u for u in s.units if u.side == side and not u.ko]

    def occ(s):
        return {(u.x, u.y) for u in s.units if not u.ko}

    @staticmethod
    def dist(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def nearest_enemy(s, u):
        es = s.alive(1 - u.side)
        return min(es, key=lambda e: s.dist((u.x, u.y), (e.x, e.y))) if es else None

    def bfs(s, u, maxd, target=None):
        """Casillas alcanzables -> pasos. Con target: cada paso se acerca (carga)."""
        occ = s.occ()
        start = (u.x, u.y)
        seen = {start: 0}
        q = deque([start])
        while q:
            p = q.popleft()
            k = seen[p]
            if k == maxd:
                continue
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (p[0] + d[0], p[1] + d[1])
                if not (0 <= n[0] < N and 0 <= n[1] < N) or n in seen or n in occ:
                    continue
                if target and s.dist(n, target) >= s.dist(p, target):
                    continue
                seen[n] = k + 1
                q.append(n)
        return seen

    @staticmethod
    def pick_sum(dice, need):
        """Subconjunto más barato de dados cuya suma >= need (pocos dados, fuerza bruta)."""
        best = None
        n = len(dice)
        for m in range(1, 1 << n):
            sub = [dice[i] for i in range(n) if m >> i & 1]
            t = sum(d for d in sub)
            if t >= need and (best is None or (t, len(sub)) < (sum(best), len(best))):
                best = sub
        return best

    def spend(s, u, c, vals):
        for v in vals:
            u.dice[c].remove(v)
            s.disc[u.side].append(c)

    # --- turno ---
    def draw(s, side):
        out = []
        for _ in range(2 * len(s.alive(side))):
            if not s.bag[side]:
                if not s.disc[side]:
                    break
                s.bag[side], s.disc[side] = s.disc[side], []
                s.bag[side].append("k")
                s.blacks[side] += 1
            c = s.bag[side].pop(s.rng.randrange(len(s.bag[side])))
            out.append((c, s.rng.randint(1, 6)))
        return out

    def place(s, side, pool):
        us = s.alive(side)
        for c, v in sorted(pool, key=lambda d: -d[1]):
            s.st["dados_sacados"] += 1
            if c == "k":
                s.st["negros_sacados"] += 1
                s.disc[side].append(c)
                continue
            cand = [u for u in us if len(u.dice[c]) < u.stats[c]]
            if not cand:
                s.st["dados_perdidos"] += 1
                s.disc[side].append(c)
                continue

            def key(u):
                e = s.nearest_enemy(u)
                d = s.dist((u.x, u.y), (e.x, e.y)) if e else 0
                return -d if c == "y" else d  # amarillos al más lejano, resto al más cercano
            min(cand, key=key).dice[c].append(v)

    def attack(s, att, tgt, reds, charge):
        reds = sorted(reds, reverse=True)
        s.st["ataques"] += 1
        s.st["cargas"] += charge
        defense = tgt.stats["g"]
        hits = 0
        for r in reds:
            if r <= defense:
                continue
            greens = sorted(v for v in tgt.dice["g"] if (v > r if s.strict_parry else v >= r))
            if greens:
                s.spend(tgt, "g", [greens[0]])
                s.st["paradas"] += 1
                continue
            hits += 1
        dmg = hits * (2 if charge else 1)
        s.st["dano"] += dmg
        tgt.hp -= dmg
        if tgt.hp <= 0:
            tgt.hp, tgt.ko = 0, True
            tgt.x = tgt.y = -9

    def adjacent_enemies(s, u):
        return [e for e in s.alive(1 - u.side) if s.dist((u.x, u.y), (e.x, e.y)) == 1]

    def act(s, u):
        if u.ko:
            return
        # 1) carga
        if u.dice["p"] and max(u.dice["p"]) >= 5 and u.dice["r"] and u.dice["y"] and not s.adjacent_enemies(u):
            ysum = sum(u.dice["y"])
            best = None
            for e in s.alive(1 - u.side):
                seen = s.bfs(u, ysum, (e.x, e.y))
                for p, k in seen.items():
                    if k > 0 and s.dist(p, (e.x, e.y)) == 1 and (best is None or k < best[0]):
                        best = (k, p, e)
            if best:
                k, p, e = best
                s.spend(u, "y", s.pick_sum(list(u.dice["y"]), k))
                s.spend(u, "p", [max(u.dice["p"])])
                u.x, u.y = p
                reds = list(u.dice["r"])
                s.spend(u, "r", reds)
                s.attack(u, e, reds, True)
                s.st["turnos_mov"] += 1
                return
        # 2) mover hacia el enemigo si no está adyacente
        adj = s.adjacent_enemies(u)
        if not adj:
            budget_dice = sorted(u.dice["y"])
            if s.one_yellow and budget_dice:
                budget_dice = [max(budget_dice)]  # solo un amarillo por turno: el más alto
            extra = list(u.dice["r"] + u.dice["g"]) if s.any_die_move else []
            free = s.free_step + (s.rng.randint(1, 6) if s.fixed_move_die else 0)
            total = sum(budget_dice) + free + len(extra)
            if total == 0:
                s.st["bloqueado"] += 1
            else:
                seen = s.bfs(u, total)
                es = s.alive(1 - u.side)
                def score(p):
                    return (min(s.dist(p, (e.x, e.y)) for e in es), seen[p])
                dest = min(seen, key=score)
                k = seen[dest]
                if k > 0:
                    need = k - free
                    if need > 0 and budget_dice:
                        sub = s.pick_sum(budget_dice, need) or budget_dice
                        s.spend(u, "y", sub)
                        need -= sum(sub)
                    while need > 0 and s.any_die_move:
                        c = "g" if u.dice["g"] else "r"
                        s.spend(u, c, [min(u.dice[c])])
                        need -= 1
                    u.x, u.y = dest
                    s.st["turnos_mov"] += 1
                else:
                    s.st["bloqueado"] += 1
            adj = s.adjacent_enemies(u)
        # 3) atacar
        if adj and u.dice["r"]:
            tgt = min(adj, key=lambda e: e.hp)
            reds = list(u.dice["r"])
            s.spend(u, "r", reds)
            s.attack(u, tgt, reds, False)

    def turn(s, side):
        s.place(side, s.draw(side))
        for u in sorted(s.alive(side), key=lambda u: s.dist((u.x, u.y), (s.nearest_enemy(u).x, s.nearest_enemy(u).y)) if s.nearest_enemy(u) else 0):
            if s.alive(1 - side):
                s.act(u)
        for u in s.alive(side):
            for c in COLS:
                u.dice[c] = [min(6, v + 1) for v in u.dice[c]]

    def play(s, max_rounds=200):
        for rnd in range(1, max_rounds + 1):
            for side in (0, 1):
                s.turn(side)
                if not s.alive(1 - side):
                    return side, rnd
        return None, max_rounds


def run(n, **kw):
    res = Counter()
    rounds = []
    tot = Counter()
    for i in range(n):
        g = Game(rng=random.Random(i), **kw)
        w, r = g.play()
        res[w] += 1
        rounds.append(r)
        tot += g.st
        tot["negros"] += sum(g.blacks)
        tot["heroes_ko"] += sum(1 for u in g.units if u.side == 0 and u.ko)
        tot["vida_heroes"] += sum(u.hp for u in g.units if u.side == 0)
    rounds.sort()
    pct = lambda a, b: 100 * a / b if b else 0
    return {
        "victorias_heroes_%": round(pct(res[0], n), 1),
        "victorias_enemigos_%": round(pct(res[1], n), 1),
        "sin_terminar_%": round(pct(res[None], n), 1),
        "rondas_media": round(sum(rounds) / n, 1),
        "rondas_mediana": rounds[n // 2],
        "rondas_p10_p90": (rounds[n // 10], rounds[9 * n // 10]),
        "turnos_personaje_sin_poder_mover_%": round(pct(tot["bloqueado"], tot["bloqueado"] + tot["turnos_mov"]), 1),
        "dados_perdidos_%": round(pct(tot["dados_perdidos"], tot["dados_sacados"]), 1),
        "dano_medio_por_ataque": round(tot["dano"] / max(1, tot["ataques"]), 2),
        "paradas_por_ataque": round(tot["paradas"] / max(1, tot["ataques"]), 2),
        "cargas_%_de_ataques": round(pct(tot["cargas"], tot["ataques"]), 1),
        "heroes_inconscientes_media": round(tot["heroes_ko"] / n, 2),
        "vida_heroes_restante_media": round(tot["vida_heroes"] / n, 1),
        "dados_negros_por_bando": round(tot["negros"] / n / 2, 1),
    }


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    for name, kw in [("Reglas actuales", {}),
                     ("B: paso básico de 1 casilla", {"free_step": 1}),
                     ("C: cualquier dado mueve 1", {"any_die_move": True}),
                     ("B + C", {"free_step": 1, "any_die_move": True}),
                     ("B + vida 6", {"free_step": 1, "hp": 6}),
                     ("B + parar solo con verde mayor", {"free_step": 1, "strict_parry": True}),
                     ("B + vida 6 + parar con verde mayor", {"free_step": 1, "hp": 6, "strict_parry": True})]:
        print(f"\n== {name} ({n} partidas) ==")
        for k, v in run(n, **kw).items():
            print(f"  {k}: {v}")
