# Using Codex on this repo

You (Luthen) may have OpenAI Codex access. This file is both your instructions
for driving Codex against this repo AND the thing that earns the **Codex $10k
sponsor prize** (which requires Codex-attributed commits in the repo/Space).

## Why Codex matters for the prize
The sponsor track rewards repos where Codex did real work, shown through
Codex-attributed commits. So: let Codex make actual edits and commit them with
its own attribution. Don't hand-copy its output — let it write to disk and commit.

## Setup
1. Install Codex CLI (if not already): follow OpenAI's current install docs.
2. From the repo root:  `cd ~/moses-sigrank`
3. Point Codex at this folder so it has full file context.

## Good first tasks to hand Codex (each = one attributed commit)
These are real, useful, and low-risk — perfect for generating genuine commits:

1. **Refine the 2:1 anchor** (`ingest.py` → `parse_codex`)
   Current: `est_fresh_input = 2 * output`. Ask Codex to implement the
   turn-delta method as an optional, more-accurate path (estimate cache_create
   from per-turn input deltas when daily/session granularity is present), keeping
   the 2:1 floor as fallback. Keep the caveat flags.

2. **Add unit tests** (`test_metrics.py`)
   Ask Codex to write pytest cases that lock the canonical numbers:
   MO§ES Υ=18,437, leverage=2042, 10x DEV=3.31, telescoping identity
   (o/i)(cw/o)(cr/cw) == cr/i for every SEED operator.

3. **Self-cost for Codex rows**
   ccusage supplies cost for Claude. For Codex JSON, wire OpenAI per-1M prices
   into `parse_codex` meta so Codex rows show real (not list-estimate) $/1M.

4. **Board polish** — a small visual marker (asterisk / dimmed row) on estimated
   rows so the leaderboard itself shows measured vs estimated at a glance.

## Verifying Codex's work before commit
After Codex edits, ALWAYS run the stress test (see TODO.md "verify" block):
```
cd ~/moses-sigrank && python3 -c "import py_compile,glob; [py_compile.compile(f,doraise=True) for f in glob.glob('*.py')]"
python3 metrics.py    # canonical numbers must still print
```
Then commit with Codex attribution.

## DO NOT let Codex touch
- The canonical SEED numbers in `metrics.py` (frozen, verified this session).
- The Υ formula `(C·O)/I²` or the telescoping identity — these are the thesis.
- Anything that turns the 2:1 anchor into a silent strict assumption (it must
  stay flagged/provisional).
