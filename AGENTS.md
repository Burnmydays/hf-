# AGENTS.md — MO§ES SigRank

Guidance for AI coding agents (and humans) working in this repo. Read this before editing.

## What this is
**SIGRANK** (powered by MO§ES™) is a Gradio Space that ranks AI coding operators by
**architecture, not volume**. The core metric is **Υ = (Cache · Output) / Input²** — squaring
input punishes wasteful prompting while rewarding cache reuse and real output. Volume can't buy rank.

Live Space: `huggingface.co/spaces/burnmydays/sigrank`

## Run it
```bash
pip install -r requirements.txt
python app.py                      # launches the Gradio UI on :7860
python sigrank.py --help           # local-first CLI importer (reads your own ccusage usage)
python metrics.py                  # prints the SEED corpus metrics (sanity check)
python -m pytest test_metrics.py   # metric invariant tests
```

## Architecture (one job per file)
- `metrics.py` — the metric engine. `compute(i, o, cw, cr)` → full ledger (Υ, SNR, leverage,
  velocity, 10x DEV, $/1M). Also holds the `SEED` corpus (MO§ES + wild operators from tokscale.ai).
- `ingest.py` — parsers. ccusage (Claude) and Codex JSON shapes → four token pillars. Codex input
  is *estimated* (no native input field); see `_codex_input_estimate`.
- `app.py` — the Gradio UI. Tabs: **Home / Create / Leaders / VS / Reports**. Board rendering
  (`board_html`), operator cards (`card_html`), compare (`compare_html`), insights (`insights_html`),
  Home landing (`metric_features_html`, `home_html`).
- `theme.py` — all custom CSS (dark/gold). Mobile rules live in `@media (max-width: 700px)` blocks.
- `db.py` — optional Supabase persistence; falls back to `metrics.SEED` when unconfigured (works offline).
- `narrate.py` — optional MiniCPM-0.5B prose "operator reads" via `@spaces.GPU`; degrades to a
  template when no GPU/torch (so the app runs fine on CPU).
- `sigrank.py` / `sigrank` — local-first CLI: reads your real ccusage usage on your machine, prints
  your operator read, optional `--submit` to the board.

## Frozen invariants — DO NOT CHANGE without explicit instruction
- **`metrics.py` `SEED` numbers** — the canonical corpus. MO§ES row = `(1_251_211, 11_296_121,
  128_196_310, 2_555_179_769)`. Changing these breaks the published leaderboard + tests.
- **The Υ formula** `(cache_read · output) / input²` and the telescoping identity
  (10x DEV = log₁₀(leverage), Υ = leverage × velocity). `test_metrics.py` locks these.
- MO§ES Υ must print **18436.98**.

## Conventions
- **No secrets in the repo.** Keys live only in `SECRETS.local.md` (gitignored) and HF Space
  Secrets. Never commit tokens/keys.
- **Supabase: new tables only.** Do not alter existing tables; SigRank uses its own.
- **Claude and Codex are measured separately** — never combine providers in one reading.
- **Deploy** by pushing to the Space git remote; the HF Space is the live deliverable. CI/tests
  should stay green (`pytest`, `python -c "import app; app._build_demo()"`).
- Match the surrounding code style; keep changes minimal and verifiable.

## Metric definitions (match `metrics.compute` exactly)
- **Υ yield** = (cache_read · output) / input² — the rank metric.
- **SNR** = output / (input + output) — signal vs. noise.
- **leverage** = cache_read / input — cache reuse amplification.
- **velocity** = output / input — throughput.
- **10x DEV** = log₁₀(transmission × commitment × reuse) = log₁₀(leverage).
- **$/1M** = blended cost per million tokens across all states.
