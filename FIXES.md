# FIXES — open items for the SigRank build

Status legend:  [ ] not done · [~] partial/optional · [x] done this session
Each fix lists FILE, WHERE, WHAT, WHY. Run through VS Code against the git repo.

---

## CONFIRMED WORKING (no action — listed so you know the baseline)
- [x] ccusage import → fills ALL board columns for the operator's row.
      FILE ingest.py parse_ccusage() → metrics.py compute(). Verified: MO§ES
      paste returns Υ 18,437, real $0.527. SNR/10xDEV/velocity/leverage/eff/Υ all derived.
- [x] Codex import → 2:1 anchor split, clamped ≥0, caveat-flagged, full cascade.
- [x] Four-number fallback. Garbage input handled gracefully.
- [x] Avg $/1M is a real board column (8-col grid).
- [x] Board (board_html) used on BOTH tabs — hero version is consistent.
- [x] App boots under gradio 6.x (version-safe launch).

---

## FIX 1 — Persistence boundary is undocumented (HONESTY FIX, do first)
- [ ] FILE: README.md  +  app.py (Leaderboard tab markdown)
- WHERE: add a one-line note near the board.
- WHAT: state that pasting ccusage computes your row against the SEED corpus
  but does NOT permanently add you to the board (no backend yet).
- WHY: right now a viewer could assume their paste joins the leaderboard. It
  doesn't — the 7 SEED operators are hardcoded; your row is transient. Saying so
  is the honest framing and pre-empts a judge's "where did my row go?" moment.
- SUGGESTED LINE: "Your pasted row is scored live against the field but not
  persisted — the leaderboard corpus is fixed for this demo."

## FIX 2 — Wild-corpus rows have no real cost (LABEL FIX)
- [ ] FILE: metrics.py SEED  +  README.md
- WHERE: SEED dict comment / README notes.
- WHAT: make explicit that the 6 wild operators show ~list-price $/1M estimates,
  only MO§ES carries real ccusage cost.
- WHY: the ~ marker is in the UI but the data provenance isn't stated in the
  repo. One sentence closes it.

## FIX 3 — tokscale MCH row (DATA, BLOCKED on your re-pull)
- [ ] FILE: metrics.py SEED
- WHERE: add one operator entry once you re-pull.
- WHAT: add "MCH (tokscale read)" as a LABELED instrument-comparison row, NOT a
  second person. Frame: same operator via the noisy instrument (input inflated
  to ~8.36M vs ccusage 1.25M — the +568% streaming-sum artifact).
- WHY: demonstrates instrument divergence honestly. Held open until you re-pull
  clean numbers (don't freeze the screenshot figure).

## FIX 4 — Species/quadrant framing instead of rarity ladder (NARRATIVE)
- [~] FILE: new file species_cards.md (or into the deck, not the app)
- WHAT: replace linear Common→Mythic ladder with a 2×2 Scale × Amplification
  quadrant. Four species by which term dominates the math:
    Throughput (volume) · Converter (I→O) · Cache Architect (reuse) · Cascade (stacks)
  MO§ES = the empty quadrant (high amplification, low scale), not "top rank."
- WHY: a linear ladder with MO§ES alone at "Mythic" reads as self-coronation on
  a board you built + scored. "Different species" is the defensible finding and
  is literally the 4-orders-of-magnitude geometry.
- FLAVOR TEXT FIX: "built to compound, not just spend" (architecture claim) —
  NOT "teaches tokens to work" (mechanism claim the metric can't prove).
- ADD ONE HONEST LINE: high reuse is the SIGNATURE of a compounding loop but
  doesn't by itself prove compounding over agentic re-reading; the independent
  Instrument-2 kernels (time/task, $/LOC) are what corroborate it.

## FIX 5 — MiniCPM not in venv (DEMO QUALITY, optional pre-record)
- [~] FILE: requirements.txt already lists torch/transformers; venv only has gradio.
- WHAT: if you want the REAL MiniCPM narration on camera (not the template
  fallback), install deps into the venv before recording:
    .venv/bin/python -m pip install torch transformers accelerate sentencepiece
- WHY: non-blocking by design, but the demo currently shows template prose.
  MiniCPM narration is what earns Best MiniCPM / Tiny Titan framing on video.
- NOTE: heavy download. Numbers/board/cost/cascade are identical either way —
  only the prose paragraph changes.

## FIX 6 — CSS render check under gradio 6.x (VISUAL, verify only)
- [ ] FILE: theme.py (no change unless broken)
- WHAT: eyeball that the gold/dark CSS + 8-col board grid actually render under
  gradio 6.x (the !important overrides + grid-template-columns). Off Brand badge
  depends on the custom look surviving.
- WHY: 6.x moved css/theme to launch(); the app handles it, but confirm visually
  the $/1M column doesn't crowd the grid at your window width.

---

## SUBMISSION (yours, not code — from TODO.md)
- [ ] Move Space into build-small-hackathon ORG
- [ ] Record demo video (script in TODO.md) + paste link in README
- [ ] Social post + paste link in README
- [ ] If chasing Codex $10k: do Codex commits AFTER repo is in the org (so
      attribution lands in the submitted location) — see CODEX.md

## VERIFY (run after every fix)
```
cd /Users/dericmchenry/Desktop/moses-sigrank
.venv/bin/python -c "import py_compile,glob; [py_compile.compile(f,doraise=True) for f in glob.glob('*.py')]"
.venv/bin/python metrics.py     # canonical numbers must still print
```
