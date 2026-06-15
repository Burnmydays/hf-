# TODO — MO§ES SigRank submission

Deadline: **June 15 2026, 23:59 UTC**. Track: Thousand Token Wood 🍄

## ⚡ REMAINING ACTION ITEMS — DO NOT FORGET (updated 2026-06-15)

### A. Turn persistence ON (HF Space → Settings → Variables and secrets)
- **Keys live in `SECRETS.local.md`** (gitignored, NOT uploaded). Copy `SUPABASE_URL` + `SUPABASE_ANON_KEY` from there into the Space secrets.
- Curated mode = set ONLY those two on the public Space (leave `service_role` OFF so visitor pastes stay transient).
- Table already built + seeded: `public.sigrank_operators` in AppFeeder (betcyfbzsgusaghriptz), curated RLS, 7 rows.

### B. Blocked on owner (data / quality)
- [ ] FIX 3 — re-pull clean tokscale numbers, add "MCH (tokscale read)" as a LABELED instrument-comparison row (don't freeze the screenshot figure).
- [ ] FIX 5 — (optional, pre-record) install MiniCPM deps into venv for REAL narration on camera: `.venv/bin/python -m pip install torch transformers accelerate sentencepiece`

### C. Reserved for Codex (earns the $10k attribution — do AFTER repo is in the org)
- [ ] Refine 2:1 anchor → turn-delta method (keep 2:1 fallback)
- [ ] `test_metrics.py` — lock Υ 18,437 / lev 2042 / X 3.31 / telescoping
- [ ] Real Codex `$/1M` via OpenAI prices in `parse_codex` meta
- [ ] Board visual marker on estimated (Codex) rows

### D. NEXT BUILD — automatic ingestion (paste = backup only)
- [ ] Make usage upload automatic (MCP tool / Claude Code hook / CLI uploader) — design in progress, see SCRATCHPAD.md "AUTO-INGEST" section.

### E. Submission (non-negotiable)
- [ ] Move Space into `build-small-hackathon` org
- [ ] Record 60s demo video + paste link in README
- [ ] Social post (X/LinkedIn) + paste link in README

## CODE — done this session
- [x] metrics.py — engine, 4 ints in, full ledger (incl Avg $/1M)
- [x] ingest.py — ccusage parser (any shape) + Codex parser (2:1 anchor, clamped, flagged) + four-number fallback
- [x] narrate.py — MiniCPM4-0.5B, non-blocking, template fallback
- [x] theme.py — gold/dark CSS, log-scaled Υ bars, 8-col board grid
- [x] app.py — board_html hero (with $/1M column) used on BOTH tabs; profile; measure-yourself
- [x] requirements.txt, README.md
- [x] stress test passes (compile + 5 logic cases)

## CODE — optional hardening (hand to Codex, see CODEX.md)
- [ ] Refine 2:1 anchor → turn-delta method (keep 2:1 as fallback)
- [ ] test_metrics.py — lock canonical numbers (Υ 18437, lev 2042, X 3.31, telescoping)
- [ ] Real Codex $/1M via OpenAI prices in parse_codex meta
- [ ] Board: visual marker on estimated (Codex) rows

## SUBMISSION REQUIREMENTS (non-negotiable, from field guide)
- [ ] **Space lives in the `build-small-hackathon` org** (not just your personal namespace)
- [ ] **Demo video** recorded + link pasted into README (placeholder is there)
- [ ] **Social post** (X / LinkedIn) + link pasted into README (placeholder is there)
- [ ] Confirm model ≤32B (MiniCPM4-0.5B ✓ — also unlocks Tiny Titan ≤4B + Best MiniCPM)

## BADGES IN REACH (free, already engineered — just confirm in README/tags)
- [ ] Off Brand ($1,500) — custom non-default UI ✓ (theme.py)
- [ ] Tiny Titan ($1,500) — ≤4B model ✓ (0.5B)
- [ ] Best Demo ($1,000) — needs the video to land
- [ ] Best MiniCPM sponsor ($2,500) — built on MiniCPM ✓
- [ ] Codex sponsor ($10k) — needs Codex-attributed commits (see CODEX.md)

## DEMO VIDEO — 60-sec script (open cold on the board)
1. (0-10s) Open ON the leaderboard. Don't explain. Let the eye hit the 4-orders Υ gap.
   "This is every operator's token usage, ranked by one number."
2. (10-25s) Point at $/1M column. "The operator at the top is also the cheapest.
   Efficiency isn't a tradeoff against cost — it IS the cost."
3. (25-45s) Go to Measure Yourself. Paste a live `ccusage --json`. Hit compute.
   New operator drops onto the board in real time with a narrated profile.
4. (45-60s) "Υ = cache × output over input squared. You can't buy rank with volume —
   padding input is penalized quadratically. That's the whole game." End on board.

## SOCIAL POST — draft
"Built MO§ES SigRank for the @Gradio Build Small hackathon: a diagnostic x-ray of
the token economy. Paste your ccusage output, get ranked by Net Volumetric Yield —
the metric where volume can't buy rank. A 0.5B MiniCPM narrates your architecture.
🍄 Thousand Token Wood. [link]"

## VERIFY BLOCK (run before every upload / after every Codex edit)
```
cd ~/moses-sigrank
python3 -c "import py_compile,glob; [py_compile.compile(f,doraise=True) for f in glob.glob('*.py')]"
python3 metrics.py          # canonical numbers print
# optional full launch:
pip install -r requirements.txt && python3 app.py
```
