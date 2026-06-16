"""
MO§ES SigRank — HF/Gradio Build Small Hackathon.
Operator pastes ccusage/codex output -> ingestion -> full profile + board placement.
Board ranks by Net Volumetric Yield (Υ). Four raw integers drive everything.
"""
import gradio as gr
import html as _html
import math as _math
import re as _re
from datetime import datetime, timezone
from metrics import compute, SEED
from ingest import ingest_meta
from theme import CSS
import db
try:
    from narrate import narrate
except Exception:
    def narrate(name, m, klass): return f"**{klass}.**"

# ---------- operator corpus (Supabase if configured, else SEED) ----------
_OPS = None
def operators(force=False):
    """Cached board corpus. Reads from Supabase via db.load_operators() (which
    itself falls back to metrics.SEED if persistence is unconfigured/down).
    Cached so a page render isn't one REST call per board; force=True refreshes
    after a write so a newly-persisted row shows immediately."""
    global _OPS
    if _OPS is None or force:
        _OPS = db.load_operators()
    return _OPS

def _fmt_int(n):
    for u,d in (("T",1e12),("B",1e9),("M",1e6),("K",1e3)):
        if abs(n)>=d: return f"{n/d:.2f}{u}"
    return str(int(n))

def _fmt_cost(c):
    """Adaptive $/1M: keep sub-cent values legible instead of rounding to $0.00.
    e.g. $0.000195 -> $0.0002 (2 sig figs) rather than $0.00."""
    if c >= 1:    return f"{c:,.2f}"
    if c >= 0.01: return f"{c:.3f}"
    return f"{c:.2g}"

def _cost_str(m):
    c = m.get("avg_cost_1m")
    if not c: return "\u2014"
    mark = "~" if m.get("cost_estimated") else ""
    return f"{mark}${_fmt_cost(c)}"

# ---------- leaderboard (HTML hero, log-scaled Υ, cost column) ----------
# column label -> metrics key, used by the "Rank by" control on the board
SORT_LABELS = {"Υ yield": "yield", "SNR": "snr", "10x DEV": "dev10x",
               "velocity": "velocity", "leverage": "leverage", "$/1M": "avg_cost_1m"}

def board_html_slim(extra=None):
    """3-column mini board for the Clock Your Signal tab (SNR · 10x DEV · Υ)."""
    ops = operators()
    rows = [(n, compute(*v)) for n, v in ops.items() if not (extra and n == extra[0])]
    if extra: rows.append(extra)
    ymax = max((m["yield"] for _, m in rows), default=1) or 1
    rows.sort(key=lambda r: r[1]["yield"], reverse=True)
    out = ['<div class="moses-board">']
    out.append('<div class="mb-head" style="display:grid;grid-template-columns:28px 1fr 0.55fr 0.55fr 1.1fr;'
               'align-items:center;gap:8px;padding:8px 10px;'
               'color:#C4923A;font-size:10px;letter-spacing:0.06em;text-transform:uppercase;'
               'border-bottom:1px solid #C4923A;">'
               '<span>#</span><span>operator</span>'
               '<span style="text-align:right">SNR</span>'
               '<span style="text-align:right">10x DEV</span>'
               '<span style="text-align:right">\u03a5 yield</span></div>')
    for i, (n, m) in enumerate(rows, 1):
        y = m["yield"]; you = extra and n == extra[0]
        orders = _math.log10(ymax / y) if y > 0 else 99
        barpct = max(2, 100 * (1 - orders / 5))
        d = f"{m['dev10x']:.2f}" if m['dev10x'] is not None else "\u2014"
        rank_cls = f"mb-rank-{i}" if i <= 3 else ""
        rkey = rarity_class(m)[0]
        if you:
            cls = f"species-{rkey} you"
            row_style = "background:rgba(196,146,58,0.10);color:#E8E0CF;"
        elif i == 1:
            cls = f"species-{rkey} rank1"
            row_style = "background:rgba(196,146,58,0.12);color:#E8E0CF;"
        else:
            cls = f"species-{rkey}"
            row_style = ""
        ne = _html.escape(n)
        est_mark = "<span class='mb-est' title='estimated'>*</span>" if m.get("cost_estimated") else ""
        out.append(
            f'<div class="mb-row {cls}" style="display:grid;grid-template-columns:28px 1fr 0.55fr 0.55fr 1.1fr;'
            f'align-items:center;gap:8px;padding:7px 10px;border-bottom:1px solid #3A3324;'
            f'font-size:11px;{row_style}">'
            f'<span class="mb-rank {rank_cls}">{i}</span>'
            f'<span><b style="color:#E8E0CF">{ne}{est_mark}</b></span>'
            f'<span style="text-align:right;color:#8a7f68">{m["snr"]:.3f}</span>'
            f'<span style="text-align:right;color:#8a7f68">{d}</span>'
            f'<span class="mb-y" style="position:relative;display:flex;align-items:center;justify-content:flex-end;min-height:18px">'
            f'<span class="mb-bar" style="width:{barpct:.0f}%"></span>'
            f'<span class="mb-yval" style="position:relative;z-index:2;font-weight:700;font-size:11px;padding-right:3px">{y:,.0f}</span>'
            f'</span></div>'
        )
    out.append('</div>')
    out.append('<div class="mb-foot">\u03a5 bar is log-scaled \u00b7 volume can\'t buy rank</div>')
    return "".join(out)

def board_html(extra=None, sort_key="yield"):
    ops = operators()
    # dedup: if `extra` is already persisted, replace it so it shows once + highlighted
    rows=[(n,compute(*v)) for n,v in ops.items() if not (extra and n==extra[0])]
    if extra: rows.append(extra)
    ymax=max((m["yield"] for _,m in rows), default=1) or 1   # Υ bar always scales to Υ
    asc = sort_key == "avg_cost_1m"                          # cheapest leads for cost
    rows.sort(key=lambda r:(r[1].get(sort_key) if r[1].get(sort_key) is not None
                            else float("-inf")), reverse=not asc)
    out=['<div class="moses-board">']
    out.append('<div class="mb-head"><span class="mb-rank">#</span>'
               '<span class="mb-op">operator</span>'
               '<span class="mb-num">SNR</span><span class="mb-num">10x DEV</span>'
               '<span class="mb-num">velocity</span><span class="mb-num">leverage</span>'
               '<span class="mb-num">$/1M</span>'
               '<span class="mb-y">\u03a5 yield</span></div>')
    for i,(n,m) in enumerate(rows,1):
        y=m["yield"]; you = extra and n==extra[0]
        orders=_math.log10(ymax/y) if y>0 else 99
        barpct=max(2,100*(1-orders/5))
        d=f"{m['dev10x']:.2f}" if m['dev10x'] is not None else "\u2014"
        rank_cls = f"mb-rank-{i}" if i <= 3 else ""
        rkey = rarity_class(m)[0]
        if you:
            cls = f"mb-row species-{rkey} you"
        elif i == 1:
            cls = f"mb-row species-{rkey} rank1"
        else:
            cls = f"mb-row species-{rkey}"
        ne = _html.escape(n)
        est_mark = " <span class='mb-est' title='* structural estimation'>*</span>" if m.get("cost_estimated") else ""
        out.append(f'<div class="{cls}">'
            f'<span class="mb-rank {rank_cls}">{i}</span>'
            f'<span class="mb-op"><b>{ne}{est_mark}</b><br><span class="mb-raw">R {_fmt_int(m["raw"]["cache_read"])} \u00b7 C {_fmt_int(m["raw"]["cache_create"])} \u00b7 I {_fmt_int(m["raw"]["input"])} \u00b7 O {_fmt_int(m["raw"]["output"])}</span></span>'
            f'<span class="mb-num">{m["snr"]:.3f}</span>'
            f'<span class="mb-num">{d}</span>'
            f'<span class="mb-num">{m["velocity"]:.2f}</span>'
            f'<span class="mb-num">{m["leverage"]:,.0f}\u00d7</span>'
            f'<span class="mb-num">{_cost_str(m)}</span>'
            f'<span class="mb-y"><span class="mb-bar" style="width:{barpct:.0f}%"></span>'
            f'<span class="mb-yval">{y:,.0f}</span></span>'
            f'</div>')
    out.append('</div>')
    out.append('<div class="mb-foot">\u03a5 bar is log-scaled \u00b7 MO\u00a7ES leads the field by ~4 orders of magnitude \u00b7 $/1M blended cost (~ = list-price estimate) \u00b7 * = structural estimation \u00b7 volume can\'t buy rank</div>')
    return "".join(out)

# raw token pillars: I=input  O=output  Cw=cache-create  Cr=cache-read
_METRIC_KEY = [
    ("\u03a5 yield", "(Cache \u00b7 Output) / Input\u00b2", "the main efficiency score",
     "How well you reuse stored info (cache) to produce strong output while keeping new "
     "input low. Squaring input heavily penalizes wasted tokens \u2014 a high \u03a5 means you're "
     "getting value from smart reuse, not just throwing more data at the model."),
    ("SNR", "O / (I+O)", "signal-to-noise",
     "How much useful, meaningful output (signal) you get versus repetitive or low-value "
     "fluff (noise). Rewards clean, focused generations over long, rambling ones."),
    ("leverage", "Cr / I", "cache leverage",
     "How effectively you reuse previously computed results (cache-read) instead of "
     "recomputing from fresh input. Big \u2018free\u2019 value from smart memory \u2014 the core "
     "architectural signal that separates a compounding cache from a stateless pipe."),
    ("velocity", "O / I", "throughput",
     "Output produced per input token spent \u2014 single-pass processing speed."),
    ("10x DEV", "log\u2081\u2080(transmission \u00d7 commitment \u00d7 reuse)", "cascade velocity",
     "How efficiently the run chains steps together \u2014 the 10\u00d710\u00d720 cascade. The three "
     "factors telescope to Cr/I, so this is the cascade expressed in orders of magnitude "
     "(log\u2081\u2080 of leverage). Smoother chaining = higher."),
    ("$/1M", "blended cost / 1M tokens", "across all states",
     "Average cost per million tokens across input, output, and cache. Efficient "
     "architecture is also the cheapest. ~ = recomputed at list price."),
]

def metrics_key_html():
    """Collapsible legend for the board columns. Definitions match metrics.compute exactly."""
    rows = "".join(
        f'<div class="mk-row"><span class="mk-name">{n}</span>'
        f'<span class="mk-form">{f}</span>'
        f'<span class="mk-alias">{a}</span>'
        f'<span class="mk-desc">{d}</span></div>'
        for n, f, a, d in _METRIC_KEY
    )
    return (
        '<details class="metric-key"><summary>What do these metrics mean? '
        '<span class="mk-hint">(tap to expand)</span></summary>'
        '<div class="mk-legend">'
        '<div class="mk-note">Raw pillars: <b>I</b> input \u00b7 <b>O</b> output \u00b7 '
        '<b>Cw</b> cache-create \u00b7 <b>Cr</b> cache-read</div>'
        f'{rows}</div></details>'
    )

_STANDARD_METRICS = [
    ("Total Tokens", "Input + Output", "Raw count of everything processed. Higher = more usage."),
    ("Input Tokens", "prompt / context", "How much you feed in \u2014 often the biggest cost driver."),
    ("Output Tokens", "model generation", "How much the model writes. Longer answers cost more."),
    ("Tokens/sec \u00b7 Latency", "speed", "How fast it runs \u2014 nothing about how well."),
    ("Cost ($)", "$ per 1M tokens", "Dollars from token pricing. Counts spend, not skill."),
]
_SIGRANK_METRICS = [
    ("\u03a5 \u2014 Upsilon", "(Cache \u00d7 Output) / Input\u00b2",
     "Standard just adds Input + Output. \u03a5 squares input to punish waste while rewarding reuse (cache) and real output.",
     "Encourages tight, smart prompts instead of long ones."),
    ("Signal-to-Noise (SNR)", "Out / (In + Out)",
     "Standard counts every output token equally. SNR separates useful signal from repetitive fluff.",
     "Rewards quality, not length."),
    ("Cache Leverage", "Cache-read / Input",
     "Standard ignores reuse \u2014 every call is fresh. This measures the \u2018free\u2019 work you get from remembering prior results.",
     "Big win for systems that avoid repeating work."),
    ("Cascade Velocity", "10 \u00d7 10 \u00d7 20",
     "Standard might just time the whole run. This tracks smooth chaining of steps (10 focused ops \u2192 10 more \u2192 20\u00d7 leverage).",
     "Rewards well-designed pipelines over messy long chains."),
]
_COMPARE_ROWS = [
    ("Focus", "How much you use", "How well you use it"),
    ("Penalizes", "Nothing \u2014 bigger is often \u2018better\u2019", "Wasteful inputs, fluff, poor reuse"),
    ("Rewards", "Volume &amp; speed", "Efficiency, quality, smart architecture"),
    ("Easy to game?", "Very \u2014 just inflate prompts", "Hard \u2014 square penalty + quality checks"),
    ("Best for", "Billing &amp; raw scale", "Hackathons, governance, Build Small"),
]

def metrics_explainer_html():
    """The full 'what the metrics mean' education: SigRank vs standard token metrics,
    the thermodynamic grounding, and a side-by-side comparison."""
    std = "".join(
        f'<div class="mx-item"><div class="mx-item-head"><span class="mx-name">{n}</span>'
        f'<span class="mx-form">{f}</span></div><div class="mx-desc">{d}</div></div>'
        for n, f, d in _STANDARD_METRICS)
    sig = "".join(
        f'<div class="mx-item"><div class="mx-item-head"><span class="mx-name">{n}</span>'
        f'<span class="mx-form">{f}</span></div>'
        f'<div class="mx-vs"><b>vs standard:</b> {v}</div>'
        f'<div class="mx-result">\u2192 {r}</div></div>'
        for n, f, v, r in _SIGRANK_METRICS)
    comp = "".join(
        f'<tr><th class="mx-aspect">{a}</th><td>{s}</td><td class="mx-win">{g}</td></tr>'
        for a, s, g in _COMPARE_ROWS)
    return (
        '<div class="mx-wrap">'
        '<div class="mx-analogy">Standard token metrics are an <b>odometer</b> \u2014 they count '
        'distance (tokens used). <span class="mx-gold">SigRank is a fuel-efficiency + '
        'smart-driving score</span> \u2014 it judges how intelligently you drive.</div>'
        '<div class="mx-cols">'
        '<div class="mx-col mx-col-std"><div class="mx-col-head">Standard Token Metrics</div>'
        f'{std}<div class="mx-foot">Rewards <b>volume &amp; scale</b> \u2014 easy to track, easy to game '
        '(this is \u201ctokenmaxxing\u201d).</div></div>'
        '<div class="mx-col mx-col-sig"><div class="mx-col-head">SigRank Metrics</div>'
        f'{sig}<div class="mx-foot">Rewards <b>efficiency, quality &amp; architecture</b> \u2014 the same '
        'numbers, turned into judgment.</div></div>'
        '</div>'
        '<table class="mx-table"><thead><tr><th>Aspect</th><th>Standard</th>'
        '<th class="mx-win">SigRank</th></tr></thead><tbody>' + comp + '</tbody></table>'
        '<div class="mx-thermo"><div class="mx-thermo-h">\u25c6 Why square the input? \u2014 the thermodynamic floor</div>'
        'The metrics are grounded in <b>Landauer\u2019s principle</b>: processing or erasing information '
        'carries a real, physical energy cost (on the order of kT\u00b7ln2 per bit). Tokens aren\u2019t free \u2014 '
        'every input bit you push through has a price. SigRank takes that seriously: it rewards '
        '<b>reusing</b> what you already computed (cache) and <b>minimizing fresh input</b>, the way an '
        'efficient engine minimizes wasted heat. Squaring input in \u03a5 is that penalty made concrete.</div>'
        '<div class="mx-bottom">Bottom line: standard metrics are great for paying the bill. '
        'SigRank adds judgment \u2014 it ranks by <span class="mx-gold">cleverness, not consumption.</span> '
        'That\u2019s \u201cown your loop.\u201d</div>'
        '</div>')

# ---------- profile ----------
def classify(m):
    if m["non_compounding"]: return "Non-Compounding \u00b7 stateless pipe"
    v,l=m["velocity"],m["leverage"]
    if v>=1 and l>=100: return "Cascade Matrix \u00b7 recursive processing loop"
    if l>=10 and v<1:   return "Cache Architect \u00b7 high structural reuse"
    if v>=0.5 and l<2:  return "Converter Loop \u00b7 single-pass processing velocity"
    return "Throughput Pipe \u00b7 raw metric bandwidth"

def rarity_class(m):
    """Returns (species_key, label, trait, description).
    Quadrant Species Designation based on algorithmic efficiency vectors.
    """
    v, l = m["velocity"], m["leverage"]
    if v >= 1 and l >= 100:
        return ("cascade", "CASCADE SPECIES",
                "Compound Cascading Loop",
                "Multipliers stack across all dimensions. Transmission \u00d7 Commitment \u00d7 Reuse = Leverage. "
                "Maintains high production velocity while driving compounding architectural feedback.")
    if l >= 10 and v < 1:
        return ("architect", "CACHE ARCHITECT",
                "Persistent Context Layer",
                "Builds high-reuse caching layers. Every token commit is read across sequential loops. "
                "Holds state perfectly without requiring linear transformation velocity.")
    if v >= 0.5:
        return ("converter", "CONVERTER SPECIES",
                "Linear Volumetric Output",
                "High immediate input-to-output context conversion ratio. Maximizes localized turn processing. "
                "Token footprint does not compound or recur inside long-term retrieval networks.")
    return ("throughput", "THROUGHPUT SPECIES",
            "Volumetric Mass Transit",
            "Processes massive raw token scale across standard pipelines. Focuses on total platform load. "
            "Optimization vector is execution bandwidth rather than persistent feedback loops.")

def comp_bar_html(c):
    return (f'<div class="comp-bar">'
            f'<div class="comp-read" style="width:{c["read"]:.1f}%"></div>'
            f'<div class="comp-create" style="width:{c["create"]:.1f}%"></div>'
            f'<div class="comp-output" style="width:{c["output"]:.1f}%"></div>'
            f'<div class="comp-input" style="width:{c["input"]:.3f}%"></div>'
            f'</div>'
            f'<div style="font-size:10px;color:#8a7f68;margin-bottom:8px">'
            f'read {c["read"]:.1f}% \u00b7 create {c["create"]:.1f}% \u00b7 output {c["output"]:.1f}% \u00b7 input {c["input"]:.3f}%'
            f'</div>')

def _first_sentence(text, limit=120):
    t = _re.sub(r"[*_`>#]", "", text or "").replace("\n", " ").strip()
    parts = _re.split(r"(?<=[.!?])\s", t, maxsplit=1)
    s = parts[0] if parts else t
    if len(s) > limit:
        s = s[:limit].rstrip() + "\u2026"
    return s

def card_html(name, m, rank, total_ops, narration_text):
    archetype = classify(m).split("\u00b7")[0].strip()
    rkey, rlabel, passive, effect = rarity_class(m)
    c = m["composition"]
    parsing_mode = m.get("_parsing_mode", "")
    mode_badge = (f'<div class="sig-card-mode">* {_html.escape(parsing_mode)}</div>'
                  if parsing_mode else "")
    if m["transmission"] is not None:
        cascade = (
            f'<div class="sig-card-cascade-box">{m["transmission"]:.1f}\u00d7<small>trans</small></div>'
            f'<span class="sig-card-cascade-arrow">\u2192</span>'
            f'<div class="sig-card-cascade-box">{m["commitment"]:.1f}\u00d7<small>commit</small></div>'
            f'<span class="sig-card-cascade-arrow">\u2192</span>'
            f'<div class="sig-card-cascade-box">{m["reuse"]:.1f}\u00d7<small>reuse</small></div>'
            f'<span class="sig-card-cascade-arrow">=</span>'
            f'<div class="sig-card-cascade-box">{m["leverage"]:,.0f}\u00d7<small>leverage</small></div>'
        )
    else:
        cascade = '<div class="sig-card-cascade-box">\u2014<small>non-compounding</small></div>'
    quote = _first_sentence(narration_text)
    return (
        f'<div class="sig-card species-{rkey}">'
        '<div class="sig-card-watermark">MO\u00a7ES\u2122 SIGRANK</div>'
        f'<div class="sig-card-rarity species-{rkey}">{rlabel}</div>'
        f'<div class="sig-card-name">{name}</div>'
        f'<div class="sig-card-archetype">{archetype}</div>'
        f'<div class="sig-card-passive">Passive: {passive}</div>'
        f'<div class="sig-card-effect">{effect}</div>'
        f'{mode_badge}'
        f'<div class="sig-card-yield">{m["yield"]:,.0f}</div>'
        '<div class="sig-card-yield-label">net volumetric yield</div>'
        f'<div class="sig-card-rank">#<span>{rank}</span> of {total_ops} operators</div>'
        f'<div class="sig-card-cascade">{cascade}</div>'
        f'{comp_bar_html(c)}'
        f'<div class="sig-card-quote">{quote}</div>'
        '<div class="sig-card-footer"><span>sigrank.hf.space</span><span>\u03a5=(C\u00b7O)/I\u00b2</span></div>'
        '</div>'
    )

def profile_md(name, m, rank, total_ops, read=None):
    c=m["composition"]; r=m["raw"]
    d=f"{m['dev10x']:.3f}" if m['dev10x'] is not None else "\u2014 non-compounding (no cache_create)"
    if read is None:
        read = narrate(name, m, classify(m))
    cav = m.get("_caveat")
    cav_line = f"\n\n`\u26a0 {cav}`" if cav else ""
    cost_note = " (list-price estimate)" if m.get("cost_estimated") else " (from ccusage)"
    mode = m.get("_parsing_mode")
    mode_line = f"\n\n`* {mode}`" if mode else ""
    return f"""## OPERATOR \u00b7 {name}
ranked **#{rank}** of {total_ops} by \u03a5{cav_line}{mode_line}

> {read}

### raw ledger (the four pillars)
| | tokens |
|---|---|
| input | {r['input']:,} |
| output | {r['output']:,} |
| cache_create | {r['cache_create']:,} |
| cache_read | {r['cache_read']:,} |
| **total** | **{m['total']:,}** |

### board metrics
| metric | value | |
|---|---|---|
| SNR | {m['snr']:.3f} | output share |
| 10x DEV | {d} | amplification exponent |
| Operating Ratio | {m['op_ratio']} | vs AA 7:2:1 |
| Velocity | {m['velocity']:.3f}\u00d7 | output per input |
| Leverage | {m['leverage']:,.1f}\u00d7 | reads per human token |
| Efficiency | {m['efficiency']:,.1f}\u00d7 | vs AA baseline |
| Avg $/1M | ${_fmt_cost(m['avg_cost_1m'])} |{cost_note} |
| **\u03a5 Yield** | **{m['yield']:,.2f}** | un-gameable rank |

**cascade** \u2014 {m['cascade_str']} (transmission \u00d7 commitment \u00d7 reuse)
**scale V** \u2014 {m['V']:.2f}
"""

def _greatest_hits_html(name):
    """Render top sessions for this operator from session history."""
    history = db.load_session_history(name, limit=5)
    if not history:
        return ""
    rows = []
    for h in history:
        i = int(h.get("input", 0) or 0)
        o = int(h.get("output", 0) or 0)
        cw = int(h.get("cache_create", 0) or 0)
        cr = int(h.get("cache_read", 0) or 0)
        m = compute(i, o, cw, cr)
        ts = h.get("submitted_at", "")
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                ts = dt.strftime("%Y-%m-%d %H:%M UTC")
            except (ValueError, TypeError):
                pass
        src = h.get("source", "")
        rows.append(
            f'<tr><td>{ts}</td><td>{_fmt_int(m["yield"])}</td>'
            f'<td>{m["velocity"]:.2f}\u00d7</td><td>{m["leverage"]:,.0f}\u00d7</td>'
            f'<td>{src}</td></tr>'
        )
    return (
        '<div class="greatest-hits">'
        '<h4>Greatest Hits</h4>'
        '<table><thead><tr><th>when</th><th>\u03a5</th><th>vel</th><th>lev</th><th>source</th></tr></thead>'
        '<tbody>' + "".join(rows) + '</tbody></table>'
        '</div>'
    )

# ---------- ingestion handler ----------
def run_ingest(blob, name, request: gr.Request):
    hf_user = None
    if request:
        hf_user = getattr(request, "username", None)
    name=(name or "you").strip()[:24] or "you"
    try:
        i,o,cw,cr,meta = ingest_meta(blob or "")
    except Exception as e:
        return ("Paste your `ccusage claude --json` output, your "
                "`ccusage codex --json` output, or `ccusage --json` "
                "for all providers. You can also paste four numbers: "
                "input output cache_create cache_read.\n\n"
                f"_parser said: {e}_"), "", "", ""
    if i+o+cw+cr==0:
        return "Got zeros \u2014 check your paste.", "", "", ""
    m=compute(i,o,cw,cr, cost_usd=meta.get("cost"))
    if meta.get("estimated"):
        m["_caveat"]=meta.get("caveat")
    if meta.get("parsing_mode"):
        m["_parsing_mode"] = meta["parsing_mode"]
    # persist only if HF-authenticated + writes configured
    saved=False
    if hf_user and db.writes_enabled():
        saved=db.save_operator(name,i,o,cw,cr, cost=meta.get("cost"),
                               source=meta.get("source","manual"),
                               estimated=bool(meta.get("estimated")),
                               caveat=meta.get("caveat"),
                               hf_user=hf_user)
    base=operators(force=saved)
    rows=[(nn,compute(*vv)) for nn,vv in base.items() if nn!=name]+[(name,m)]
    rows.sort(key=lambda r:r[1]['yield'],reverse=True)
    rank=next(idx for idx,(nn,_) in enumerate(rows,1) if nn==name)
    read = narrate(name, m, classify(m))

    save_note = ""
    if not hf_user:
        save_note = "\n\n*\u26a0 Sign in with HuggingFace to save your entry to the board. Paste-only results are a snapshot \u2014 not persisted.*"
    elif saved:
        save_note = f"\n\n*Saved to the board as **{_html.escape(name)}** at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}.*"

    hits_html = _greatest_hits_html(name) if hf_user else ""
    profile = profile_md(name,m,rank,len(rows),read) + save_note

    return (profile,
            comp_bar_html(m["composition"]),
            card_html(name,m,rank,len(rows),read),
            hits_html)

# ---------- interactive leaderboard helpers ----------
def resort_board(label):
    """Re-render the board sorted by the chosen column (the 'Rank by' control)."""
    return board_html(sort_key=SORT_LABELS.get(label, "yield"))

def view_operator(name):
    """Render a corpus operator's full profile + share card + learn-from insights."""
    ops = operators()
    if not name or name not in ops:
        return "", "", ""
    m = compute(*ops[name])
    rows = sorted(((n, compute(*v)) for n, v in ops.items()),
                  key=lambda r: r[1]["yield"], reverse=True)
    rank = next(i for i, (n, _) in enumerate(rows, 1) if n == name)
    read = narrate(name, m, classify(m))
    return (profile_md(name, m, rank, len(rows), read),
            card_html(name, m, rank, len(rows), read),
            insights_html(name, m))

def insights_html(name, m):
    """Reader takeaways: what this operator does well + what to avoid."""
    good, avoid = [], []
    lev, snr, vel = m["leverage"], m["snr"], m["velocity"]
    if lev >= 100:   good.append("Exceptional cache reuse — context is re-read, not rebuilt each turn.")
    elif lev >= 10:  good.append("Solid cache leverage — compounding on prior work.")
    else:            avoid.append("Low cache leverage — mostly fresh input each turn (recompute waste).")
    if snr >= 0.5:   good.append("High signal — most tokens are model output, not prompt bloat.")
    else:            avoid.append("Low signal-to-noise — large input vs. output; tighten prompts.")
    if m["non_compounding"]: avoid.append("No cache-create — stateless pipe, no architectural compounding.")
    else:            good.append("Compounding architecture — building reusable context, not one-shotting.")
    if vel >= 1:     good.append("Strong throughput — produces more than it consumes.")
    elif vel < 0.3:  avoid.append("Low velocity — heavy input for little output.")
    g = "".join(f"<li>{x}</li>" for x in good) or "<li>—</li>"
    a = "".join(f"<li>{x}</li>" for x in avoid) or "<li>Nothing major — clean architecture.</li>"
    return (f'<div class="ins-wrap">'
            f'<div class="ins-block ins-good"><div class="ins-h">✓ Doing well</div><ul>{g}</ul></div>'
            f'<div class="ins-block ins-avoid"><div class="ins-h">✕ Watch out</div><ul>{a}</ul></div></div>')

def operator_segments():
    """Live counts: burners (spend, no reuse), builders (compounding), 10×ers (elite reuse)."""
    burn = build = tenx = 0
    for v in operators().values():
        lev = compute(*v)["leverage"]
        if lev < 2:        burn += 1
        elif lev >= 1000:  tenx += 1
        else:              build += 1
    return burn, build, tenx, burn + build + tenx

# ---------- VS / compare ----------
# (label, metrics key, winner = max|min, value formatter)
_CMP_ROWS = [
    ("Υ yield",  "yield",       "max", lambda v: f"{v:,.0f}"),
    ("SNR",      "snr",         "max", lambda v: f"{v:.3f}"),
    ("leverage", "leverage",    "max", lambda v: f"{v:,.0f}×"),
    ("velocity", "velocity",    "max", lambda v: f"{v:.2f}×"),
    ("10x DEV",  "dev10x",      "max", lambda v: f"{v:.2f}"),
    ("$/1M",     "avg_cost_1m", "min", lambda v: f"${_fmt_cost(v)}"),
]

def compare_html(names):
    """Head-to-head table for 2–3 operators; best value per row gets the gold cell."""
    ops = operators()
    names = [n for n in (names or []) if n in ops][:3]
    if len(names) < 2:
        return ('<div class="cmp-empty">Pick <b>2–3 operators</b> above to put them '
                'head-to-head. Winner takes each row.</div>')
    ms = [(n, compute(*ops[n])) for n in names]
    head = "".join(f'<th class="cmp-op">{_html.escape(n)}</th>' for n, _ in ms)
    body = []
    for label, key, mode, fmt in _CMP_ROWS:
        vals = [m.get(key) for _, m in ms]
        nums = [v for v in vals if v is not None]
        best = (max if mode == "max" else min)(nums) if nums else None
        cells = []
        for v in vals:
            win = v is not None and best is not None and v == best and len(nums) > 1
            cells.append(f'<td class="{"cmp-win" if win else ""}">'
                         f'{fmt(v) if v is not None else "—"}</td>')
        body.append(f'<tr><th class="cmp-rowlabel">{label}</th>{"".join(cells)}</tr>')
    return (f'<table class="cmp-table"><thead><tr><th></th>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table>'
            '<div class="cmp-note">Gold = leads that metric · $/1M: lower wins · '
            'Υ is the overall rank metric.</div>')

# ---------- Home / landing ----------
def profile_marquee_html():
    """Auto-scrolling band of operator chips (rank · name · Υ · leverage). Pure CSS loop."""
    ops = operators()
    rows = sorted(((n, compute(*v)) for n, v in ops.items()),
                  key=lambda r: r[1]["yield"], reverse=True)
    def chip(rank, n, m):
        rk = rarity_class(m)[0]
        return (f'<div class="pm-chip species-{rk}">'
                f'<span class="pm-rank">#{rank}</span>'
                f'<span class="pm-name">{_html.escape(n)}</span>'
                f'<span class="pm-stat">Υ {m["yield"]:,.0f}</span>'
                f'<span class="pm-lev">{m["leverage"]:,.0f}× lev</span></div>')
    chips = "".join(chip(i, n, m) for i, (n, m) in enumerate(rows, 1))
    # chips duplicated so the translateX(-50%) loop is seamless
    return f'<div class="pm-wrap"><div class="pm-track">{chips}{chips}</div></div>'

# ---- the metric standard (green feature row) ----
# (symbol, metrics key, equation, value-format, hover description)
_FEATURE_METRICS = [
    ("Υ", "yield", "(Cache·Output) / Input²", "{v:,.0f}",
     "The efficiency score. Reused context (cache) × produced output, measured against "
     "fresh input squared — squaring input is why raw volume can't buy rank."),
    ("SNR", "snr", "Out / (In+Out)", "{v:.2f}",
     "Signal-to-noise. Share of the exchange that's model output vs. prompt/input. "
     "Higher = focused, less bloat."),
    ("10x", "dev10x", "log₁₀(cascade)", "{v:.2f}",
     "The cascade in orders of magnitude (log₁₀ of leverage) — the 10× developer multiplier."),
    ("$/1M", "avg_cost_1m", "blended cost / 1M", "${v}",
     "Blended cost per million tokens across all states. Efficient architecture is also "
     "the cheapest — so cost falls out of good design."),
]

def _corpus_metric_values(key):
    vals = [compute(*v).get(key) for v in operators().values()]
    return sorted(x for x in vals if x is not None)

def _median(vals):
    n = len(vals)
    if not n: return 0
    return vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2

def _status_box_html():
    """Live system status + segment counters — rendered as a metric box."""
    burn, build, tenx, tot = operator_segments()
    return (
        '<div class="mf-box mf-status">'
        '<div class="ms-title"><span class="ms-dot">●</span> ONLINE</div>'
        '<div class="ms-grid">'
        f'<span>BURNERS</span><span class="hs-burn">{burn:03d}</span>'
        f'<span>BUILDERS</span><span class="hs-build">{build:03d}</span>'
        f'<span>10×ERS</span><span class="hs-tenx">{tenx:03d}</span>'
        f'<span>SIGNALS</span><span class="ms-tot">{tot:03d}</span>'
        '</div></div>')

def metric_features_html():
    boxes = []
    for sym, key, form, fmt, desc in _FEATURE_METRICS:
        vals = _corpus_metric_values(key)
        avg = sum(vals) / len(vals) if vals else 0
        big = f"${_fmt_cost(avg)}" if key == "avg_cost_1m" else fmt.format(v=avg)
        boxes.append(
            f'<div class="mf-box" tabindex="0"><div class="mf-sym">{sym}</div>'
            f'<div class="mf-big">{big}</div>'
            f'<div class="mf-form">{form}</div>'
            f'<div class="mf-tip">{desc}</div></div>')
    boxes.insert(2, _status_box_html())   # between SNR and 10x
    return ('<div class="mf-head">Introducing the new standard in '
            '<span>AI metrics &amp; benchmarks</span></div>'
            f'<div class="mf-grid">{"".join(boxes)}</div>'
            '<div class="mf-sub">field average · live counts · hover any metric for what it means</div>')

# ---- real mini renders of each page (live HTML, scaled into a framed thumbnail) ----
def _top_rows(n):
    return sorted(((k, compute(*v)) for k, v in operators().items()),
                  key=lambda r: r[1]["yield"], reverse=True)[:n]

def _mini(cap, inner, accent):
    """Frame real page HTML as a browser-chrome thumbnail; CSS scales it down."""
    return (f'<div class="mini mini-{accent}">'
            f'<div class="mini-chrome"><span></span><span></span><span></span>'
            f'<div class="mini-cap">{cap}</div></div>'
            f'<div class="mini-view"><div class="mini-scale">{inner}</div></div></div>')

def _mini_leaders():
    return _mini("sigrank · leaders", board_html(), "gold")

def _mini_reports():
    k, m = _top_rows(1)[0]
    read = narrate(k, m, classify(m))
    return _mini("sigrank · reports",
                 card_html(k, m, 1, len(operators()), read), "purple")

def _mini_vs():
    return _mini("sigrank · vs", compare_html([k for k, _ in _top_rows(3)]), "blue")

def _mini_create():
    inner = (
        '<div class="cr-mock">'
        '<div class="cr-code">$ ./sigrank --submit</div>'
        '<div class="cr-box">paste ccusage JSON — or four numbers:<br>'
        '<b>1251211 11296121 128196310 2555179769</b></div>'
        '<div class="cr-btn">⬡ Clock My Signal</div>'
        '<div class="cr-res">Υ 18,437 · CASCADE MATRIX</div></div>')
    return _mini("sigrank · create", inner, "green")

_HOME_SECTIONS = [
    ("Leaders", "Prove your signal",
     "The burn-vs-build board — who wins on architecture, not spend.", _mini_leaders, "gold"),
    ("Reports", "Study the field",
     "Pull any operator's full read. R&D — improve yourself.", _mini_reports, "purple"),
    ("VS", "Head-to-head",
     "Who's actually 10×? Who's amplifying signal — and at what cost?", _mini_vs, "blue"),
    ("Create", "Clock your signal",
     "Drop your ledger, get scored, claim your operator card.", _mini_create, "green"),
]

def home_html():
    boxes = "".join(
        f'<div class="hm-box hm-{accent}">{mini()}'
        f'<div class="hm-title">◢ {t}</div>'
        f'<div class="hm-sub">{s}</div><div class="hm-desc">{d}</div>'
        f'<div class="hm-cta">open the {t} tab →</div></div>'
        for t, s, d, mini, accent in _HOME_SECTIONS
    )
    return f'<div class="hm-grid">{boxes}</div>'

def home_footer_html():
    loom = "https://www.loom.com/share/edc345e2e5164e20aed3acb6436a08c3"
    return (
        '<div class="hm-foot">'
        '<div class="hf-col"><div class="hf-h">Watch the demo</div>'
        f'<a class="hf-btn" href="{loom}" target="_blank" rel="noopener">▶ Play demo video</a></div>'
        '<div class="hf-col"><div class="hf-h">Get ranked in 3 steps</div>'
        '<ol class="hf-steps">'
        '<li>Run <code>npx ccusage@latest claude --json</code></li>'
        '<li>Open <b>Create</b>, paste it (or four numbers)</li>'
        '<li>Get your Υ score + operator card</li></ol></div>'
        '<div class="hf-col"><div class="hf-h">More</div>'
        '<a class="hf-link" href="https://mos2es.com" target="_blank" rel="noopener">mos2es.com</a>'
        '<a class="hf-link" href="https://mos2es.com/benchmarks" target="_blank" rel="noopener">benchmarks</a>'
        '<a class="hf-link" href="https://x.com/burnmydays/status/2066666214143758576" target="_blank" rel="noopener">@burnmydays on X</a>'
        '</div></div>'
    )

# ---------- UI ----------
import os as _os
_ON_SPACE = bool(_os.environ.get("SPACE_ID"))

# Ghost/"unminted" card so the right column is never an empty void on first load.
CARD_PLACEHOLDER = (
    '<div class="sig-card species-throughput" id="ghost-card">'
    '<div class="sig-card-watermark">MO\u00a7ES\u2122 SIGRANK</div>'
    '<div class="sig-card-rarity species-throughput">UNMINTED</div>'
    '<div class="sig-card-name">Awaiting Operator\u2026</div>'
    '<div class="sig-card-archetype">Signal Offline</div>'
    '<div class="sig-card-yield">0,000</div>'
    '<div class="sig-card-yield-label">insert token ledger to scan</div>'
    '</div>'
)

def _build_demo():
    _blocks_kw = {"title": "MO\u00a7ES SigRank"}
    _b = gr.Blocks(**_blocks_kw)
    # dynamic hero stats (don't hardcode counts that drift when the corpus changes)
    _ops_now = operators()
    _names = list(_ops_now.keys())
    _ys = sorted((compute(*v)["yield"] for v in _ops_now.values()), reverse=True)
    _lead = (_ys[0] / _ys[1]) if len(_ys) > 1 and _ys[1] > 0 else 0.0
    _burn, _build, _tenx, _tot = operator_segments()
    with _b:
        with gr.Column(elem_id="moses-hero"):
            gr.HTML(
                "<div style='display: flex; align-items: center; justify-content: space-between; gap: 28px; border-bottom: 2px solid #C4923A; padding-bottom: 12px; margin-bottom: 10px;'>"
                "  <div style='text-align: left; flex: none;'>"
                "    <div style='color: #8a7f68; font-size: 11px; letter-spacing: 0.3em; text-transform: uppercase; margin-bottom: 2px;'>Powered by MO\u00a7ES\u2122</div>"
                "    <h1 style='margin: 0 !important; line-height: 0.9; text-shadow: 0 0 24px rgba(196,146,58,0.25);'>SIGRANK</h1>"
                "  </div>"
                "  <div style='text-align: right; color: #E8E0CF; font-size: 14px; font-weight: 600; line-height: 1.5; max-width: 460px;'>"
                "    Ranking AI operators on performance, production, architecture &amp; cost efficiency. "
                "    <span style='color:#C4923A;'>Identifying Burners, Builders, and 10\u00d7ers.</span>"
                "  </div>"
                "</div>"
            )
            # full-width live leaderboard scroller (replaces the old static stat strip)
            gr.HTML(profile_marquee_html())

        # ---- TAB: Home (landing — metric standard + section minis + links) ----
        with gr.Tab("Home"):
            gr.HTML(metric_features_html())
            gr.HTML(home_html())
            gr.HTML(home_footer_html())

        # ---- TAB: Create (clock your signal \u2014 the importer) ----
        with gr.Tab("Create"):
            gr.Markdown("### Primary path \u2014 run the local importer")
            gr.Markdown("Reads your usage on your own machine. **Nothing leaves your computer.** Clone it once, then run:")
            gr.Code(value="git clone https://github.com/Burnmydays/hf-\ncd hf-\n./sigrank",
                    language="shell", show_label=False, elem_id="clone-code")
            with gr.Accordion("More options \u2014 Codex, all providers, or paste instead", open=False):
                gr.Markdown("""`./sigrank --codex` reads Codex usage \u00b7 `./sigrank --all` runs every provider in turn.

**No terminal? Paste instead (the backup).** Run one of these, copy the JSON, drop it in the box below:
```
npx ccusage@latest claude --json
```
```
npx ccusage@latest codex --json
```
\u26a0\ufe0f Run Claude and Codex **separately** \u2014 never bare `ccusage --json` (it merges every agent and distorts the read). No JSON? Type four numbers: `input output cache_create cache_read`.

*Codex input is estimated (\\*): alone \u2192 AA 2:1 baseline; with a Claude profile \u2192 your own Claude input:output ratio.*""")
            gr.HTML("<hr style='border:0;border-top:1px solid var(--moses-line);margin:18px 0;'>")
            with gr.Row():
                with gr.Column(scale=5):
                    gr.Markdown("### Ingest a signal")
                    if _ON_SPACE:
                        gr.LoginButton(elem_id="hf-login-btn")
                    else:
                        gr.Markdown("*HuggingFace login available on the hosted Space \u2014 local mode is transient.*", elem_id="moses-foot")
                    nm = gr.Textbox(label="operator name / handle", placeholder="your handle", max_lines=1)
                    blob = gr.Textbox(label="ccusage JSON \u2014or\u2014 four numbers (I O C R)", lines=5,
                                      placeholder='Paste ccusage JSON here\n\nor four numbers: input output cache_create cache_read\n\nExample: 1251211 11296121 128196310 2555179769')
                    go = gr.Button("Clock My Signal", variant="primary", elem_id="compute-btn")
                    gr.Markdown("### Greatest hits")
                    hits = gr.HTML()
                with gr.Column(scale=6):
                    gr.Markdown("### Minted operator card")
                    card = gr.HTML(CARD_PLACEHOLDER)
                    gr.Markdown("*Right-click \u2192 Save image to share your architectural footprint.*", elem_id="moses-foot")
                    prof_bar = gr.HTML()
                    prof = gr.Markdown(elem_id="moses-profile")
            go.click(run_ingest, [blob, nm], [prof, prof_bar, card, hits])
            gr.Examples(
                examples=[
                    ['{"totals":{"inputTokens":1251211,"outputTokens":11296121,"cacheCreationTokens":128196310,"cacheReadTokens":2555179769}}','MO\u00a7ES'],
                    ['{"data":[{"inputTokens":58920000,"cachedInputTokens":707300000,"outputTokens":3500000,"reasoningOutputTokens":510000}]}','codex-operator'],
                    ['1251211 11296121 128196310 2555179769', 'manual-paste'],
                ],
                inputs=[blob, nm])
            gr.Markdown("### What the metrics mean")
            gr.HTML(metrics_explainer_html())

        # ---- TAB: Leaders (the board) ----
        with gr.Tab("Leaders"):
            gr.Markdown("**The ledger doesn't care what you claim.** Ranked by **\u03a5 = (Cache\u00b7Output)/Input\u00b2** \u2014 raw Read\u00b7Create\u00b7In\u00b7Out stacked under each operator. $/1M is blended cost; efficient architecture is also the cheapest.")
            rank_by = gr.Radio(list(SORT_LABELS.keys()), value="\u03a5 yield",
                               label="Rank by", elem_id="rank-by")
            lb = gr.HTML(board_html())
            rank_by.change(resort_board, rank_by, lb)
            gr.HTML(metrics_key_html())
            gr.Markdown("*Curated corpus \u00b7 pasting scores you live but isn't persisted unless you sign in \u00b7 $/1M is a list-price recompute (~) \u00b7 \\* = structural estimation.*", elem_id="moses-foot")

        # ---- TAB: VS (head-to-head compare) ----
        with gr.Tab("VS"):
            gr.Markdown("### Put operators head-to-head\nSelect 2\u20133 operators. Gold cell wins each metric. **This is where architecture beats budget in plain sight.**")
            cmp_pick = gr.Dropdown(_names, label="Operators (pick 2\u20133)", value=None,
                                   multiselect=True, max_choices=3, elem_id="cmp-pick")
            cmp_out = gr.HTML(compare_html(None))
            cmp_pick.change(compare_html, cmp_pick, cmp_out)

        # ---- TAB: Reports (operator profile inspector) ----
        with gr.Tab("Reports"):
            gr.Markdown("### Full architectural read on any operator\nPick a name to pull their complete profile, a shareable card, and **what to learn from them**.")
            with gr.Row():
                with gr.Column(scale=5):
                    op_pick = gr.Dropdown(_names, label="Operator", value=None, elem_id="op-pick")
                    op_card = gr.HTML(CARD_PLACEHOLDER)
                with gr.Column(scale=6):
                    op_prof = gr.Markdown(elem_id="moses-profile")
                    op_insights = gr.HTML()
            op_pick.change(view_operator, op_pick, [op_prof, op_card, op_insights])

        gr.Markdown(elem_id="moses-foot", value="""Four integers in, full ledger out. Architecture is the only variable that matters.
Wild corpus: tokscale.ai footprints \u00b7 MO\u00a7ES row verified ccusage \u00b7 * = structural estimation.""")
    return _b

demo = _build_demo()

if __name__ == "__main__":
    demo.launch(css=CSS, theme=gr.themes.Base())
