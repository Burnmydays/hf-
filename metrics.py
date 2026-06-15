"""
MO§ES SigRank — metric engine.
Four raw integers in, full ledger out. No circular dependencies.
Every formula verified in session docs 023/024/025.
Optional cost: pass a `cost_usd` (from ccusage) to get Avg $/1M.
"""
import math

# default per-1M prices (USD) — Claude Sonnet-class, used only if no cost given
DEFAULT_PRICES = {"input": 3.0, "output": 15.0, "cache_read": 0.30, "cache_create": 3.75}

def compute(i, o, cw, cr, cost_usd=None, prices=None):
    """i=input, o=output, cw=cache_create, cr=cache_read (raw integers).
    cost_usd: total $ for the window (ccusage provides it) -> Avg $/1M.
    prices: optional per-1M price dict to compute cost when cost_usd is None."""
    i = max(i, 0); o = max(o, 0); cw = max(cw, 0); cr = max(cr, 0)
    cache = cw + cr
    total = i + o + cache
    safe_i = i if i > 0 else 1

    snr        = o / (i + o) if (i + o) > 0 else 0.0
    velocity   = o / safe_i
    leverage   = cr / safe_i
    yield_     = (cr / safe_i) * (o / safe_i)

    if cw > 0 and o > 0 and i > 0 and cr > 0:
        transmission = o / i
        commitment   = cw / o
        reuse        = cr / cw
        dev10x       = math.log10(transmission * commitment * reuse)
        cascade_str  = f"{transmission:.1f}\u00d7{commitment:.1f}\u00d7{reuse:.1f}"
    else:
        transmission = commitment = reuse = dev10x = None
        cascade_str  = "\u2014"

    op_ratio = f"{cache/safe_i:.0f}:1:{o/safe_i:.1f}"
    efficiency = ((cache + o) / safe_i) / 4.0

    # Avg cost per 1M tokens (blended across all states)
    if cost_usd is None:
        p = prices or DEFAULT_PRICES
        cost_usd = (i*p["input"] + o*p["output"] + cr*p["cache_read"]
                    + cw*p["cache_create"]) / 1_000_000
        cost_estimated = prices is None  # default prices => estimate
    else:
        cost_estimated = False
    avg_cost_1m = (cost_usd / (total / 1_000_000)) if total > 0 else 0.0

    V = math.log10(total) if total > 0 else 0.0
    comp = {
        "input":  100*i/total  if total else 0,
        "output": 100*o/total  if total else 0,
        "create": 100*cw/total if total else 0,
        "read":   100*cr/total if total else 0,
    }

    return {
        "raw": {"input": i, "output": o, "cache_create": cw, "cache_read": cr},
        "snr": snr, "dev10x": dev10x, "op_ratio": op_ratio,
        "velocity": velocity, "leverage": leverage, "efficiency": efficiency,
        "yield": yield_,
        "avg_cost_1m": avg_cost_1m, "cost_usd": cost_usd, "cost_estimated": cost_estimated,
        "cascade_str": cascade_str,
        "transmission": transmission, "commitment": commitment, "reuse": reuse,
        "V": V, "composition": comp, "total": total,
        "non_compounding": cw == 0,
    }

# seed corpus + hardcoded fallback for db.load_operators() (do NOT delete — safety net).
# Cost provenance: SEED rows carry only the four token integers, so the board's
# $/1M is a list-price recompute (~) for ALL rows. MO§ES happens to reproduce its
# verified ccusage cost ($0.527); the 6 wild operators have no real cost data.
# Real blended cost only appears on the live ccusage paste path (cost_usd passed in).
SEED = {
    "MO§ES (ccusage)": (1_251_211, 11_296_121, 128_196_310, 2_555_179_769),
    "vincentkoc":  (6_600_000_000, 342_700_000, 223_700_000, 195_000_000_000),
    "MapleEve":    (34_800_000_000, 2_800_000_000, 550_100_000, 794_600_000_000),
    "kzquandary":  (118_400_000_000, 5_900_000_000, 0, 1_066_000_000_000),
    "iamtheavoc1": (989_500_000_000, 1_272_000_000_000, 0, 4_524_000_000_000),
    "Nepomuk5665": (4_037_000_000_000, 1_259_000_000_000, 96_300_000_000, 1_658_000_000_000),
    "cexll":       (67_700_000_000, 64_000_000_000, 217_800_000, 36_900_000_000),
}

if __name__ == "__main__":
    for name,(i,o,cw,cr) in SEED.items():
        m = compute(i,o,cw,cr)
        d = f"{m['dev10x']:.2f}" if m['dev10x'] is not None else "—"
        print(f"{name:18} SNR {m['snr']:.3f}  10xDEV {d:>6}  "
              f"vel {m['velocity']:.2f}  lev {m['leverage']:.1f}  "
              f"$/1M {m['avg_cost_1m']:.3f}  Y {m['yield']:.2f}")
