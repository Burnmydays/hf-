---
title: MO§ES SigRank
emoji: 📡
colorFrom: yellow
colorTo: gray
sdk: gradio
sdk_version: "4.44.0"
app_file: app.py
pinned: false
license: mit
models:
  - openbmb/MiniCPM4-0.5B
tags:
  - thousand-token-wood
  - off-brand
  - tiny-titan
  - best-demo
  - minicpm
---

# MO§ES™ SigRank — the diagnostic x-ray of the token economy

A leaderboard that judges AI coding operators by **architecture, not budget**.
Paste your token usage; get an operator profile with a tiny-model narration and
your rank. The sort metric **Υ = (Cache·Output)/Input²** penalizes raw-input
padding quadratically — volume can't buy rank.

## What it does
Paste `npx ccusage@latest --json` (Claude Code), `ccusage codex --json` (Codex),
or four numbers →
- **operator profile** — a 0.5B MiniCPM model narrates your architecture, plus
  raw ledger, composition, full metrics, cascade breakdown
- **leaderboard placement** vs real operators, ranked by Υ, with blended **$/1M cost**

## The model (Tiny Titan / MiniCPM)
`openbmb/MiniCPM4-0.5B` (0.5B params, well under the 4B cap) runs on ZeroGPU and
narrates the operator read. It is **non-blocking**: if unavailable, a deterministic
template is used and the app still works. Everything quantitative is pure computation.

## How the numbers work
Four raw integers — `input`, `output`, `cache_create`, `cache_read` — drive all:

| metric | formula | meaning |
|---|---|---|
| SNR | O/(I+O) | output share |
| 10x DEV | log₁₀(cascade) | amplification exponent |
| Operating Ratio | C:I:O, input=1 | footprint vs Artificial Analysis 7:2:1 |
| Velocity | O/I | output per input token |
| Leverage | C/I | cache reads per human token |
| Efficiency | (C+O)/I ÷ 4.0 | vs AA baseline |
| Avg $/1M | blended cost ÷ total | efficient architecture is also cheapest |
| **Υ (Yield)** | (C·O)/I² | **un-gameable ranking metric** |

Cascade (10x DEV) = transmission (O/I) × commitment (Create/O) × compounding
(Read/Create); its log-sum is the exponent. By telescoping, 10^X = Leverage = C/I.

## Codex support
Codex reports a *combined* input figure (fresh + cached) and never itemizes cache
writes. SigRank splits it with the measured field anchor **input:output ≈ 2:1**
(estimated fresh input = 2×output; remainder → cache_create, clamped ≥0). Every
Codex-derived row is flagged with its directional caveat (↑ input-heavy /
↓ output-rich). The anchor is provisional and being refined (see CODEX.md).

## Cost
For Claude Code, ccusage supplies real cost → exact $/1M. For manual/wild rows
without cost data, $/1M is a list-price estimate (shown with ~). Either way the
finding holds: the cache-dominant operator at the top of the board is also the
cheapest per token, by an order of magnitude.

## Demo video
<!-- TODO: paste YouTube/HF link before submission (60-sec script in TODO.md) -->

## Social post
<!-- TODO: paste link to your X/LinkedIn post before submission (draft in TODO.md) -->

## Notes
- **Persistence boundary.** Your pasted row is scored live against the field but
  is *not* added to the persisted board — the leaderboard corpus is curated
  (owner-seeded). The board is backed by Supabase with a hardcoded-seed fallback,
  so it renders identically even if the database is unreachable.
- **Cost provenance.** The board's `$/1M` is a list-price recompute for every
  corpus row (shown with `~`); only the **live ccusage paste** path surfaces real
  blended cost. MO§ES's verified ccusage cost is **$0.527**, which the list-price
  recompute reproduces exactly. The six wild operators have no real cost data.
- Wild-corpus operator values are provisional (public tokscale footprints);
  MO§ES row is verified ccusage data.
- Υ is an engineered macro-efficiency index motivated by thermodynamics
  (Landauer, Ohmic dissipation); log Υ = X + log(Velocity). An analogy, not a
  microscopic-entropy derivation.

Built for the HF/Gradio Build Small Hackathon · Thousand Token Wood 🍄 · MO§ES™
