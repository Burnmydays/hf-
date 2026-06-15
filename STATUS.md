# STATUS — MO§ES SigRank  (where things stand)

Snapshot for the owner. Deadline: **2026-06-15 23:59 UTC**.
Repo: `github.com/Burnmydays/hf-` (main `9eeaeb4`).  ·  Upload target: `SunrisesIllNeverSee`.

---

## ✅ Built, verified, and pushed
- **Core engine** — `metrics.py`: 4 integers → full ledger. Canonical MO§ES Υ **18,436.98**.
- **Leaderboard** — 11 rows live (MO§ES + 10 tokscale.ai operators), log-scaled Υ, $/1M column.
- **Codex parser (fixed)** — `_codex_input_estimate`: Beta = output × your real Claude ratio;
  Alpha = output × 2.0 (AA baseline). Both flagged `*`. No more hardcoded `/9.0`.
- **Local importer** — `./sigrank` (Claude), `./sigrank --codex` (Codex), `./sigrank --all`.
- **Instructions** — "Clock Your Signal" tab + README: measure each provider separately.
- **Persistence** — Supabase migrated (`submitted_at`, `hf_user`, `sigrank_sessions` + RLS);
  board synced to 11 rows; Greatest Hits read path verified end-to-end.
- **MiniCPM narration** — non-blocking, template fallback, `@GPU` for ZeroGPU.

## ⏳ Left to do
1. **Deploy to the HF Space** (parked on your call)
   - Confirm how code reaches the Space (HF git remote vs GitHub auto-sync vs manual).
   - Set Space secrets from `SECRETS.local.md`: `SUPABASE_URL` + `SUPABASE_ANON_KEY`
     (add `SUPABASE_SERVICE_KEY` only if you want signed-in visitor rows to persist).
2. **Codex handoff** → upload to `SunrisesIllNeverSee` + the remaining Codex-attributed
   commits (`test_metrics.py`, real Codex `$/1M`). See `CODEX.md`.
3. **Submission** — move Space into `build-small-hackathon` org · 60s video · social post ·
   GitHub link in README.

## 🏅 Badges
✅ Off Brand · ✅ Tiny Titan · ✅ Best MiniCPM   |   ⏳ Best Demo (needs video) · ⏳ Codex $10k (needs Codex commits)

## 🔎 Verify anytime
```
cd /Users/dericmchenry/Desktop/moses-sigrank
.venv/bin/python metrics.py        # canonical numbers
./sigrank --all --no-color         # your live Claude + Codex read
```

## 🗂 Where things are documented
- `CODEX.md` — Codex handoff instructions (grab from desktop).
- `TODO.md` — full task board (done at bottom).
- `SCRATCHPAD.md` — live cross-agent state.
- `SUPABASE_MIGRATION.md` — the DB migration (already applied).
- `SECRETS.local.md` — Supabase keys (gitignored, never uploaded).
