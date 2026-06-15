# TODO — MO§ES SigRank submission

Deadline: **June 15 2026, 23:59 UTC**. Track: Thousand Token Wood 🍄
Completed items are at the BOTTOM. Everything still TO DO is up top.

═══════════════════════════════════════════════════════════════════
# ⚡ TO DO — DO NOT FORGET
═══════════════════════════════════════════════════════════════════

### A. Deploy to the HF Space  (parked until you confirm the Space path)
- [ ] Confirm how code reaches the Space (HF git remote vs GitHub auto-sync vs manual).
- [ ] Set Space secrets (Settings → Variables and secrets) from `SECRETS.local.md`:
      `SUPABASE_URL` + `SUPABASE_ANON_KEY` (read). Add `SUPABASE_SERVICE_KEY` ONLY if
      you want HF-authed visitor rows to persist (curated demo can leave it off).
- DB is live and ready: board reads **11 rows** (MO§ES + 10 tokscale) via anon; anon
  write blocked; `sigrank_sessions` table + Greatest Hits read path verified.

### B. Hand off to Codex → upload to github.com/SunrisesIllNeverSee
- [ ] Codex uploads the repo to your SunrisesIllNeverSee GitHub.
- [ ] **Codex-attributed commits for the $10k prize** (must be genuinely Codex's work):
  - [ ] `test_metrics.py` — lock Υ 18,437 / lev 2042 / X 3.31 + telescoping for every SEED row.
  - [ ] Real Codex `$/1M` via OpenAI per-1M prices in `parse_codex_submission` meta.
  - NOTE: the 2:1→real-ratio anchor refinement and the estimated-row `~` marker were
        already done this session (Claude), so they're no longer available as Codex commits.

### C. Submission (non-negotiable)
- [ ] Move Space into `build-small-hackathon` org.
- [ ] Record 60s demo video (script below) + paste link in README.
- [ ] Social post (X/LinkedIn, draft below) + paste link in README.
- [ ] Add a link back to your GitHub (SunrisesIllNeverSee) in the README.

### D. Optional / blocked
- [ ] FIX 3 — add "MCH (tokscale read)" as a LABELED instrument-comparison row (your re-pull).
- [ ] FIX 5 — (pre-record only) install MiniCPM deps for REAL narration:
      `.venv/bin/python -m pip install torch transformers accelerate sentencepiece`

═══════════════════════════════════════════════════════════════════
# 📋 REFERENCE
═══════════════════════════════════════════════════════════════════

## DEMO VIDEO — 60-sec script (open cold on the board)
1. (0-10s) Open ON the leaderboard. Don't explain. Let the eye hit the ~4-orders Υ gap.
   "This is every operator's token usage, ranked by one number."
2. (10-25s) Point at $/1M column. "The operator at the top is also the cheapest.
   Efficiency isn't a tradeoff against cost — it IS the cost."
3. (25-45s) Go to Clock Your Signal. Run `./sigrank` (or paste `ccusage claude --json`).
   New operator drops onto the board in real time with a narrated profile.
4. (45-60s) "Υ = cache × output over input squared. You can't buy rank with volume —
   padding input is penalized quadratically. That's the whole game." End on board.

## SOCIAL POST — draft
"Built MO§ES SigRank for the @Gradio Build Small hackathon: a diagnostic x-ray of
the token economy. Paste your ccusage output, get ranked by Net Volumetric Yield —
the metric where volume can't buy rank. A 0.5B MiniCPM narrates your architecture.
🍄 Thousand Token Wood. [link]"

## BADGES WE'RE APPLYING FOR  (confirm this list)
README tags: `thousand-token-wood` `off-brand` `tiny-titan` `best-demo` `minicpm`
- [x] **Off Brand** ($1,500) — custom non-default UI ✓ (theme.py gold/dark)
- [x] **Tiny Titan** ($1,500) — ≤4B model ✓ (MiniCPM4-0.5B)
- [x] **Best MiniCPM** sponsor ($2,500) — built on MiniCPM ✓
- [ ] **Best Demo** ($1,000) — needs the video to land
- [ ] **Codex sponsor** ($10k) — needs genuine Codex-attributed commits (see B + CODEX.md)
- [x] Model ≤32B confirmed (MiniCPM4-0.5B)

═══════════════════════════════════════════════════════════════════
# ✅ DONE
═══════════════════════════════════════════════════════════════════

## THIS SESSION (reconcile + importer overhaul + fixes)
- [x] Reconciled local with Devin's PRs #5/#6 (merged); dropped duplicate claudetodolist.md.
- [x] **Codex parser fixed** — unified Alpha/Beta into one `_codex_input_estimate` helper
      (removed both hardcoded `/9.0` copies). Beta = operator's REAL Claude input/output
      ratio; Alpha = AA 2:1 baseline. Verified both pathways + guard fallback.
- [x] **`./sigrank --all`** — runs each provider in turn; Codex reuses Claude's ratio; one
      failing provider doesn't stop the others.
- [x] **Instructions sharpened** (app.py Clock Your Signal tab + README How-to-measure):
      measure each provider separately, never bare `ccusage --json`; what/where/where-to-input.
- [x] **Wild corpus → 10 tokscale.ai operators** (replaces old 6), cited in metrics.py +
      README. All columns populate. MO§ES canonical Υ 18436.98 untouched.
- [x] **Supabase migration** (via MCP): `submitted_at` + `hf_user` on operators,
      `sigrank_sessions` table + indexes + RLS (anon read / service insert). Verified.
- [x] **Supabase board synced** to 11 rows (MO§ES + 10 tokscale, real cost stored).
- [x] Pushed all of the above to github.com/Burnmydays/hf- (main = 39fba4e).

## EARLIER
- [x] Engine: metrics.py (4 ints → full ledger incl Avg $/1M); telescoping identity.
- [x] narrate.py — MiniCPM4-0.5B, non-blocking, template fallback, @GPU for ZeroGPU.
- [x] theme.py — gold/dark CSS, log-scaled Υ bars, rarity tiers, board grid.
- [x] app.py — board hero on both tabs, profile, share card, Greatest Hits, HF login,
      XSS-safe name escaping, `~` estimated marker.
- [x] db.py — Supabase REST read + service-key upsert + session history, SEED fallback.
- [x] FIX 1 persistence-boundary honesty · FIX 2 cost provenance · FIX 4 species/quadrant
      reframe · FIX 6 grid check.
- [x] her-style local importer sigrank.py (auto-reads ccusage, paste = backup).
