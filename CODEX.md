# Codex handoff — MO§ES SigRank

Read this first. It's the instruction set for driving **OpenAI Codex** against this
repo and the thing that earns the **Codex $10k sponsor prize**.

Local path (desktop storage): `/Users/dericmchenry/Desktop/moses-sigrank`
GitHub (current): `github.com/Burnmydays/hf-`  →  upload target: `github.com/SunrisesIllNeverSee`

## How the prize works (important)
The sponsor track rewards repos where **Codex did real work**, shown through
**Codex-attributed commits**. It does NOT require that 100% of the repo is Codex's.
Two rules:
1. **Genuine work only.** Let Codex actually write the code and commit it with its own
   attribution. Do not hand-copy output or fake attribution — that risks disqualification.
2. **Verify the official rule** on the hackathon page before relying on this.

## Current state (as of this handoff)
Done and pushed to Burnmydays/hf- (main):
- Codex parser fixed — `_codex_input_estimate` in `ingest.py` (Beta = output × real Claude
  io_ratio; Alpha = output × 2.0 AA baseline). Two pathways, both flagged `*` estimated.
- `./sigrank --all` (run every provider in turn).
- Instructions sharpened (app.py "Clock Your Signal" tab + README).
- Wild corpus = 10 tokscale.ai operators; board = 11 rows; Supabase migrated + synced.

## Tasks for Codex (each = one attributed commit)
1. **Turn-delta Codex parser** — the headline Codex-token-parsing work. The current
   estimate (`_codex_input_estimate` in `ingest.py`) is a single ratio applied to total
   output. Make it more accurate: when the Codex JSON has **daily/session granularity**,
   estimate `cache_create` from **per-day context growth** (each day's input above the
   prior day's floor ≈ new cache writes) instead of one flat ratio. Keep the ratio path
   (Alpha 2:1 / Beta Claude-ratio) as the fallback when only totals are present, and keep
   the `*` estimated flag + caveat naming the method used. This is real parsing work on
   Codex's own token data — the natural Codex-attributed commit.
2. **`test_metrics.py`** — pytest that locks the canonical numbers and identities:
   - MO§ES Υ = 18,436.98, leverage = 2042.2, 10x DEV = 3.31.
   - Telescoping identity `(o/i)·(cw/o)·(cr/cw) == cr/i` for every SEED operator with cache.
   - Both Codex pathways: Alpha `output×2`, Beta `output×io_ratio`.
3. **Real Codex `$/1M`** — wire OpenAI per-1M prices into `parse_codex_submission` meta so
   Codex rows can show real (not list-estimate) cost. Keep the `*` estimated flag on input.
4. **Upload the repo to `github.com/SunrisesIllNeverSee`** (the prize-submission location).

## Verify BEFORE every Codex commit
```
cd /Users/dericmchenry/Desktop/moses-sigrank
.venv/bin/python -c "import py_compile,glob; [py_compile.compile(f,doraise=True) for f in glob.glob('*.py')]"
.venv/bin/python metrics.py    # MO§ES must print Y 18436.98, lev 2042.2, 10xDEV 3.31, $/1M 0.527
```
(use `python3` if there's no `.venv`.)

## DO NOT let Codex touch
- The MO§ES (ccusage) SEED row in `metrics.py` (canonical, Υ 18436.98).
- The Υ formula `(C·O)/I²` or the telescoping identity — these are the thesis.
- The Codex estimation must stay **flagged (`*`)** — never a silent strict assumption.

## Already done — NOT available as Codex commits
- 2:1 → real-ratio anchor refinement (Alpha/Beta unified). Done by Claude this session.
- Board `~`/`*` estimated-row marker. Done by Claude this session.

See `SCRATCHPAD.md` for live cross-agent state and `TODO.md` for the full task board.
