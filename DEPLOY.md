# SigRank Deployment Guide

## Run Locally (Gradio)

```bash
cd /path/to/moses-sigrank
.venv/bin/python3 app.py
# → http://localhost:7860
```

- No GPU needed. Narration falls back to deterministic templates.
- No Supabase needed. Falls back to SEED corpus (11 verified operators).

**Run tests:**
```bash
.venv/bin/python3 -m pytest test_metrics.py -v
```

**Run CLI:**
```bash
.venv/bin/python3 sigrank.py           # reads ccusage claude
.venv/bin/python3 sigrank.py --codex   # reads ccusage codex
.venv/bin/python3 sigrank.py --all     # both
.venv/bin/python3 sigrank.py --file my_usage.json
```

---

## Deploy to HF Spaces

The README header already has the HF Spaces config. Push this repo to a HF Space:

```bash
# One-time setup
git remote add space https://huggingface.co/spaces/YOUR_HF_USERNAME/sigrank
git push space main
```

**HF Spaces config (already in README.md):**
- `sdk: gradio`
- `sdk_version: 6.17.3`
- `app_file: app.py`
- `hf_oauth: true`
- `models: openbmb/MiniCPM4-0.5B`

**Environment Variables to set in HF Spaces settings:**

| Variable | Required | Purpose |
|---|---|---|
| `SUPABASE_URL` | Optional | Enables live board persistence |
| `SUPABASE_ANON_KEY` | Optional | Read access to operator table |
| `SUPABASE_SERVICE_KEY` | Optional | Write access (authenticated users only) |

Without Supabase env vars: app runs in curated mode (SEED corpus, read-only, no new submissions persist between sessions).

**GPU (ZeroGPU):** Required only for MiniCPM4-0.5B narration. App works without it — falls back to deterministic template narration.

---

## Supabase Schema (if enabling persistence)

Create these tables in your Supabase project:

```sql
-- Operator current best scores
CREATE TABLE sigrank_operators (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  input BIGINT DEFAULT 0,
  output BIGINT DEFAULT 0,
  cache_create BIGINT DEFAULT 0,
  cache_read BIGINT DEFAULT 0,
  cost_usd FLOAT,
  source TEXT DEFAULT 'manual',
  estimated BOOLEAN DEFAULT false,
  caveat TEXT,
  hf_user TEXT,
  submitted_at TIMESTAMPTZ DEFAULT now()
);

-- Session history (append-only)
CREATE TABLE sigrank_sessions (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  input BIGINT DEFAULT 0,
  output BIGINT DEFAULT 0,
  cache_create BIGINT DEFAULT 0,
  cache_read BIGINT DEFAULT 0,
  cost_usd FLOAT,
  source TEXT DEFAULT 'manual',
  estimated BOOLEAN DEFAULT false,
  caveat TEXT,
  hf_user TEXT,
  submitted_at TIMESTAMPTZ DEFAULT now()
);

-- RLS: allow anon reads, require service key for writes
ALTER TABLE sigrank_operators ENABLE ROW LEVEL SECURITY;
ALTER TABLE sigrank_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "anon_read" ON sigrank_operators FOR SELECT USING (true);
CREATE POLICY "anon_read" ON sigrank_sessions FOR SELECT USING (true);
```

---

## What Each File Does

| File | Purpose |
|---|---|
| `app.py` | Gradio UI — 5 tabs (Home/Create/Leaders/VS/Reports) |
| `metrics.py` | Core math engine — Υ, cascade, SNR, SEED corpus |
| `ingest.py` | Parser — ccusage JSON, Codex, named fields, four numbers |
| `db.py` | Supabase persistence — non-blocking, SEED fallback |
| `sigrank.py` | Local CLI — reads ccusage directly from your machine |
| `narrate.py` | MiniCPM4-0.5B narration — optional, template fallback |
| `theme.py` | Dark gold CSS theme for Gradio |
| `test_metrics.py` | Unit tests — canonical metric locks, cascade identity |
