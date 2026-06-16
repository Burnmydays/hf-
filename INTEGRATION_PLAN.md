# SigRank Integration Plan
**Last updated:** 2026-06-16  
**Session context:** Deep dive across moses-sigrank (Gradio/Python) + RNS/sigrank-app (Next.js)  
**Author:** Deric McHenry + Devin (Cognition)

---

## What This Document Is

A durable handoff anchor. This plan was written after reading both codebases source-to-source. Any future session (human or AI) can resume from here without replaying prior work.

If something has changed since this was written, check `SIGRANK_BUILD_STATE.md` in `RNS/` for the Next.js side and git log here for the Python side.

---

## The Two Repos — What Each Is

### This repo (`moses-sigrank`) — the Gradio prototype
- **Stack:** Python 3.14, Gradio 6.18, Supabase (optional), HF Spaces ZeroGPU
- **Status:** BUILD GREEN. Runs locally at `localhost:7860` with `.venv/bin/python3 app.py`
- **What it proves:** The cascade math (`transmission × commitment × reuse = leverage`), the Υ yield metric, the ingest pipeline, the SEED corpus, species classification, trading cards
- **What it lacks:** Multi-platform support, billing, claims, the full 9-tier class system, 30-page architecture, word-level sig_army integration

### `RNS/sigrank-app/` — the commercial Next.js product
- **Stack:** Next.js 15, React 19, TypeScript strict, Tailwind, Supabase, Stripe
- **Status:** BUILD GREEN. All 30 pages render on mock data. Awaiting real credentials + 7 decisions to go live.
- **Branch:** `sigrank-app-build` (not pushed to GitHub)
- **What it has:** Full commercial shell, 9-class SIGNA RATE scoring engine, Stripe billing, operator claims, badge system, circles, 3 themes, hand-rolled SVG charts, AuditProvider seam for sig_army
- **What it lacks:** The four-pillar ingest pipeline, the Υ/cascade metrics, real seed data (uses fictional placeholders), trading cards, narration

---

## The Core Insight — These Are the Same Signal

The moses-sigrank and RNS metric systems are **the same signal at the same token-total resolution**, approached from different angles. They converge:

| moses-sigrank metric | RNS CANON ID | Formula (same) |
|---|---|---|
| `snr = o/(i+o)` | **M.01** Compression Ratio (free proxy) | `T.01 / (T.01 + T.02)` |
| `leverage = cr/i` | **M.03** Cross-Thread (free proxy) | `cache_hit_rate × 100` |
| `velocity = o/i` | Embedded in M.01 | numerically equivalent |
| Υ = `(cr·o)/i²` | Not in RNS yet | = M.03-proxy × M.01-proxy (derived) |
| `dev10x` | Not in RNS yet | Cascade amplification exponent |

**The token bridge doc** (`RNS/1_sigrank/1.3_layer-2-mechanics/token_metric_bridge.md`) already specifies this mapping. It was designed in but not yet built.

**SIGNA RATE is the official rank** across all platforms. Υ (Yield) is a Claude/cache-specific diagnostic that runs alongside it. Both measure the same conservation law — SIGNA RATE at lower resolution, Υ at higher fidelity for cache-aware operators.

---

## Decisions Made — Session 2026-06-16

These were open questions. All resolved.

### 1. Multi-platform / cache-less operators
**Resolved:** The ingest pipeline (`ingest.py`) already handles this. ChatGPT/Gemini operators without cache tokens get Υ = `—` in those cells and still rank by SIGNA RATE from whatever pillars they have. The parser routes by payload shape. No separate leaderboard needed. Already built.

### 2. Compression Ratio vs SNR naming
**Resolved:** Keep "Compression Ratio" (M.01) as the canonical RNS name. It aligns with the word-level SigSystem framing (signal_tokens / total_tokens) and the free-tier proxy (`o/(o+i)`) is identical. SNR is the moses-sigrank internal name for the same number. No rename needed — they converge at the formula level.

### 3. Species + Class coexisting on profiles
**Resolved:** Both. Class tier = rank credential (TRANSMITTER etc.). Species = behavioral identity / trading card archetype (Cascade · recursive processing loop). They are orthogonal. Show class in the prestige header; show species as the archetype line on the card and in the operator profile sub-header. A TRANSMITTER Cascade is a different story from a TRANSMITTER Cache Architect. Same rank, different playstyle — that's the BlitzStars equivalent of tank class vs. play style. BlitzStars confirmed: their system gates by tier (experience floors) but doesn't collapse identity into tier. Same pattern here.

**BlitzStars experience-floor equivalents already in CANON.md:**
- Dual-gate (Compression AND SIGNA RATE both required for top 4 classes) — anti-gaming
- RS.07 promotion stickiness (3 consecutive cycles) — no one-session rank spike
- B.02 account age + B.03 lifetime messages — the experience floor

### 4. tokscale.ai and ccusage — outreach decision
**Resolved:**
- **tokscale.ai** (@junhoyeo, Seoul, 3.7K stars): Tokscale ranks by volume spent. SigRank ranks by architecture efficiency. Complementary, not competing. Reach out after the leaderboard has real operators. Pitch: "You measure how much. We measure how well." Seed with tokscale users — they're the exact target market.
- **ccusage** (@ryoppippi, UK, 15.3K stars): This is the data source our ingest pipeline reads. The community around it (CCWarriors, viberank, Straude) is already hungry for leaderboards. Reach out after launch with a "we built the reputation layer for ccusage data" pitch. May link from their README.
- **Attribution for SEED corpus:** The 10 wild operators came from tokscale.ai's public leaderboard. Credit tokscale.ai as the source in the leaderboard footnote. Their data is publicly published by operators.
- **Charging yourself:** No. You are the reference operator and proof of concept. MO§ES gets the Founder tier — pre-launch, permanent, zero cost. Your data is what makes the leaderboard real.

### 5. Claim pricing
**Resolved:**
- Lifetime claim: **$19 one-time**
- Launch window (first 100 claimants): **$9** — creates urgency, rewards early movers
- Anchoring: Pro monthly is $19/mo, so a permanent claim at the same price as one month is a clear deal
- Pro yearly: **$190/yr** (~17% discount vs monthly)
- Founder tier: **Yes, at launch** — capped N, permanent, identity badge

### 6. Trading card format
**Resolved:** Both faces, triggered by context:
- **Profile card (stat face):** Codename large, species archetype line, class glyph + tier, SIGNA RATE (128px gold), Υ yield, cascade bars (transmission/commitment/reuse as three horizontal bars — fighter game stats screen style), token composition, badge count
- **Battle card (identity face):** Narration quote, species quadrant position, strongest/weakest metric, "vs" challenge button
- Card is a shareable PNG via `/api/og/operators/{codename}` (server-rendered)
- BlitzStars confirmed: Hall of Fame + replay uploads is the prestige layer. SigRank equivalent = Hall of Signal + snapshot history with verified audit badge

### 7. Product scope — SigRank is BlitzStars for AI operators, not ESPN
**Resolved:** SigRank v1 = BlitzStars model:
- Operator stats tracker with deep profiles
- Circles (clan equivalent)
- Metrics comparison (tank comparison equivalent)
- Hall of Signal with seasonal records (Hall of Fame equivalent)
- Signalgeist Pro (Zeitgeist Pro equivalent — analytics upsell)
- ~one-person build, Patreon/subscription monetized

**The ESPN/Twitch/live arena layer is v2+.** Context: there are already 10+ platforms doing live AI agent battles (CodeClash, DeadNet, BattleBench, Clash of Agents, Moltarena, ForgeAI). **The gap none of them fill: they pit AI models against each other. Nobody is ranking human operators.** SigRank's unique position is that the operator is the athlete. The live events layer for SigRank specifically = scheduled submission windows where results drop simultaneously, class promotions visible in real-time. That's a data event, not a streaming infrastructure problem. BlitzStars does this seasonally. We do it weekly. Ship v1 first.

**Live arena competitive landscape (for v2 reference):**
- CodeClash (codeclash.ai) — split-screen AI coding head-to-head, tournament brackets, "ESPN for AI coding"
- DeadNet (deadnet.io) — most polished live spectator UX, debate/games/story formats
- BattleBench (battlebench.ai) — cybersec AI battles, Claude Opus 4.6 is #1 ELO, exact target audience
- ForgeAI (forgeai.gg) — infrastructure for competitive agent gaming, on-chain payouts
- Clash of Agents (clashofagents.org) — MMA-style with agent narrative/drama

---

## Phased Build Plan

### Phase 0 — Repo Consolidation (1 session, ~2 hours)
**Goal:** One repo. Both systems in one place. Clear directory structure.

**Actions:**
- Copy `RNS/sigrank-app/` into this repo as `./app/` (Next.js product)
- Copy `RNS/sigrank-agent/` into this repo as `./agent/` (Python CLI)
- Keep `metrics.py`, `ingest.py`, `db.py`, `sigrank.py`, `app.py`, `theme.py`, `narrate.py` in `./python/` (the proven prototype, reference + HF Spaces target)
- Copy `RNS/1_sigrank/` spec docs into `./specs/` for reference
- Update `.gitignore` to exclude `.venv`, `node_modules`, `__pycache__`
- Single `README.md` at root pointing to each layer

**Result:** One repo, three layers: python prototype / Next.js app / Python CLI agent

---

### Phase 1 — Gradio App: Running & Deployable (1 session, parallel track)
**Goal:** The Gradio app (this repo) is clean, documented, runnable by anyone, deployable to HF Spaces.

**Status now:** `app.py` runs at `localhost:7860` with `.venv/bin/python3 app.py`. Narration falls back to templates (no GPU needed locally).

**What needs to happen:**
- [ ] Verify all 5 tabs work end-to-end locally (Home, Leaders, VS, Reports, Create)
- [ ] Write a clean `run.sh` / startup script so anyone can run it with one command
- [ ] Check HF Spaces deployment config (README header, `app_file:` setting)
- [ ] Confirm Supabase env vars are documented (SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY)
- [ ] Test the `--submit` flag on the CLI (`./sigrank --submit`)
- [ ] Write `DEPLOY.md` with HF Spaces + local instructions

**This is the "operating version available" you want** — the Gradio app stays live as the prototype/demo while the Next.js build happens.

---

### Phase 2 — Ingest Pipeline Port (1–2 sessions)
**Goal:** Port `ingest.py` to TypeScript in the Next.js app. Claude operators can paste ccusage JSON directly into `/submit`.

**Source:** `ingest.py` in this repo (343 lines, thoroughly tested)  
**Target:** `RNS/sigrank-app/lib/ingest/` (new module)

**Specific files to create:**
- `lib/ingest/types.ts` — `IngestMeta`, `TelemetryRaw`, `ParseStrategy` types
- `lib/ingest/ccusage.ts` — `parseCcusage()`, `isCodexShape()`, field alias map
- `lib/ingest/codex.ts` — `parseCodexSubmission()`, Alpha/Beta pathways
- `lib/ingest/four_fields.ts` — `parseFourFields()` fallback
- `lib/ingest/index.ts` — `ingestMeta()` three-strategy router (mirrors `ingest_meta()`)

**Test:** Port `test_metrics.py` Codex parser lock tests to `__tests__/ingest.test.ts`

**Upgrade `/submit` page:** Accept raw ccusage JSON paste (textarea) → ingest → preview computed metrics before submission → confirm → POST to `/api/v1/snapshots`

---

### Phase 3 — Cascade Layer in Scoring Engine (1 session)
**Goal:** Add Υ, cascade, species to `lib/scoring/engine.ts`. Make Υ a sortable leaderboard column.

**Source:** `metrics.py:compute()` in this repo (pure function, no side effects)  
**Target:** New export `computeCascade()` in `lib/scoring/engine.ts`

**What to add:**
```typescript
// lib/scoring/engine.ts additions
export interface CascadeMetrics {
  yield_: number          // Υ = (cr/i) × (o/i)
  leverage: number        // cr/i
  velocity: number        // o/i
  snr: number             // o/(i+o)  — same as M.01 proxy
  dev10x: number | null   // log10(T×C×R) — null if non-compounding
  cascade_str: string     // "9.0×11.3×20.0" display
  transmission: number | null
  commitment: number | null
  reuse: number | null
  avg_cost_1m: number
  composition: { input: number; output: number; create: number; read: number }
  species: 'CASCADE' | 'CACHE_ARCHITECT' | 'CONVERTER' | 'THROUGHPUT' | 'NON_COMPOUNDING'
  non_compounding: boolean
}

export function computeCascade(telemetry: {
  fresh_input: number; output: number; cache_create: number; cache_read: number;
  cost_usd?: number
}): CascadeMetrics
```

**DB migration:** Add columns to `metric_snapshots`:
- `yield_score NUMERIC(12,2)` — nullable (null for non-Claude platforms)
- `leverage NUMERIC(10,2)` — nullable
- `velocity NUMERIC(8,4)` — nullable
- `dev10x NUMERIC(6,3)` — nullable
- `avg_cost_1m NUMERIC(8,6)` — nullable
- `species TEXT` — nullable
- `token_composition_json JSONB` — nullable

**Leaderboard:** Add Υ as an alternate sort column. Null values sort to bottom. Show `—` in cells for operators without cache telemetry.

---

### Phase 4 — Real SEED Data (1 session)
**Goal:** Replace fictional mock.ts placeholders with real SEED corpus.

**Source:** `metrics.SEED` in this repo (11 verified operators)  
**Target:** `RNS/sigrank-app/supabase/migrations/0004_seed_real.sql`

**For each SEED operator, compute:**
- `compression_ratio = o / (o + i)` (M.01 free-tier proxy)
- `cross_thread = cr / (cr + cw + i) * 100` (M.03 free-tier proxy)  
- `session_depth_raw` = use known values for MO§ES (348.9), default 5 for others
- `token_throughput = i + o + cw + cr` (total tokens, T.05)
- `prompt_complexity = 50` (placeholder, low confidence)
- Then run `scoreSnapshot()` to get SIGNA RATE and class tier
- Then run `computeCascade()` to get Υ, leverage, species

**MO§ES canonical values from CANON.md:**
- R.09 compression: `0.9694`
- R.10 cross-thread: `96.88%`
- R.11 session_depth_raw: `348.9`
- R.07 total_tokens: `1,123,252,011`

**mock.ts stays as the no-creds fallback** — it just uses real SEED data now instead of fictional placeholders.

---

### Phase 5 — Trading Cards & Battles (1–2 sessions)
**Goal:** Shareable operator card + `/compare` enhanced to a battle view.

**New components:**
- `components/profile/OperatorCard.tsx` — 380×500 card: codename, species, class, SIGNA RATE, Υ, cascade bars, composition, narration quote
- `app/api/og/operators/[codename]/route.tsx` — server-side PNG via `@vercel/og` / satori
- Cascade composition bars (port from `theme.py`'s `.comp-bar` styling)
- Deterministic narration (port `narrate.py`'s `_template()` as pure TS function)
- Battle modal on `/compare`: two cards side-by-side, metric deltas, winner highlights

**Card battle spec (from your vision):**
- Operator A card vs Operator B card
- Per-metric "winner" cell highlighted (like the existing VS tab in Gradio)
- Share button → copies `/compare?a=X&b=Y` URL
- "Challenge" button on operator profile → prefills compare with that operator

---

### Phase 6 — Go Live (operator-gated, <1 session once decisions are made)
**Actions (all in `GO_LIVE.md`):**
1. Provide `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
2. Run migrations: `0001_initial_schema.sql` → `0002_seed.sql` → `0003_audit_patch.sql` → `0004_seed_real.sql`
3. Provide Stripe test keys + create price IDs for 4 tiers + claim price
4. Resolve 7 open decisions (see below)
5. Deploy to Vercel: `vercel --prod` from `app/`
6. Set env vars in Vercel dashboard
7. Configure Stripe webhook endpoint to `/api/v1/billing/stripe-webhook`

---

### Phase 7+ — sig_army Bridge (ongoing, Pro tier)
**Goal:** Connect the AuditProvider seam to real sig_army Python for exact Compression + PC.

**The seam already exists:** `lib/audit/provider.ts` defines `AuditProvider.getProMetric()` returning `{ value, finalized, confidence }`.

**What to build:**
- `lib/audit/sigarmyProvider.ts` — calls sig_army Python script via subprocess or API
- sig_army outputs exact compression (signal/total tokens) and PC sub-scores
- Results update `metric_snapshots` with `pc_confidence: 'exact'`
- Conservation invariant check: if exact compression diverges >15% from proxy, flag for review

**This is the academic paper validation story** — empirical proof that token-level proxies converge with word-level exact measurements. That's the IP hardening.

---

## The 7 Open Decisions — Resolved

| # | Decision | Resolution | Rationale |
|---|---|---|---|
| 1 | B.03 lifetime count | Append-only (T.11 per snapshot) | Never lose data |
| 2 | T.08 active minutes | Wall-clock session duration sum | Verifiable from session files |
| 3 | C.03 Drift Ratio | `finalized:false` stub at launch | Pro-only, sig_army in Phase 7 |
| 4 | PC sub-extractor | Free: `min(100, log10(unique_prompts+1)×20)` per CANON M.02; Pro: sig_army | Already in CANON spec |
| 5 | Old master lists | Skip — not blocking | Conservation already proven |
| 6 | Pro yearly pricing | **$190/yr** | Your number. ~17% discount. |
| 7 | Founder tier | **Yes at launch** | First-mover identity, launch urgency |

---

## Current Gradio App — How to Run

```bash
# From this repo root:
cd /Users/dericmchenry/Desktop/moses-sigrank
.venv/bin/python3 app.py
# → opens at http://localhost:7860
```

Narration falls back to deterministic templates locally (no GPU/torch needed).  
Supabase is optional — falls back to SEED corpus if unconfigured.

**To run the CLI:**
```bash
.venv/bin/python3 sigrank.py           # auto-reads ccusage claude
.venv/bin/python3 sigrank.py --codex   # auto-reads ccusage codex
.venv/bin/python3 sigrank.py --all     # both providers
```

**To run tests:**
```bash
.venv/bin/python3 -m pytest test_metrics.py -v
```

---

## Next.js App — How to Run

```bash
cd /Users/dericmchenry/RNS/sigrank-app
npm run dev    # dev server at localhost:3000
npm run build  # verify build green (30 routes)
```

No env vars needed — falls back to mock data.

---

## Files to Read for Context

**To understand the math:** `metrics.py`, `token_metric_bridge.md`, `CANON.md`  
**To understand the product vision:** `CONSERVATION_LAW.md`, `species_cards.md`, `MODERATOR_NOTE.md`  
**To understand the Next.js build state:** `SIGRANK_BUILD_STATE.md`, `AUDIT.md`, `GO_LIVE.md`  
**To understand what's been decided:** `RNS/5_comms/decisions/layer-*-decisions.md`

---

## What This Product Is (In One Paragraph)

SigRank is an ESPN-style leaderboard for AI operators — the people using Claude, ChatGPT, Gemini to build and create. It ranks them not by how much they spend, but by how efficiently they use context: cache reuse, output density, session depth, prompt architecture. The conservation law at its core — the same signal measurable at word level (SigSystem/sig_army) and at token level (this product) — means the ranking is real and defensible, not arbitrary. The token layer is the launchable version because platform APIs expose token counts. The word layer is the precision tier and the long-term IP moat. The trading cards, battles, and event system make it a spectator sport.

---

*Document version: 1.0 — written 2026-06-16*  
*Resume session: read this file + `SIGRANK_BUILD_STATE.md` in RNS + git log in both repos*
