# _merge/ — SigRank Integration Workspace

**What this folder is:** A shared coordination space for the merger of `moses-sigrank` (Gradio/Python proof-of-concept) into the RNS `sigrank-app` (Next.js commercial product). Every agent, human, or session working on this integration reads and writes here.

**Rule:** Read `LOG.md` before you do anything. Sign in at the bottom of the sign-in sheet below when you arrive. Append to `LOG.md` when you complete work.

---

## The Mission in One Paragraph

SigRank is a BlitzStars-style leaderboard for AI operators — the humans steering Claude, ChatGPT, Codex, and other AI tools. It ranks them not by how much they spend but by how efficiently they build: cache reuse, output density, session depth, prompt architecture. The conservation law at the core (same signal measurable at word level via sig_army and at token level via this product) means the ranking is defensible, not arbitrary.

**The ultimate goal:** unify people and locate Transmitters. Find the operators whose architecture is genuinely compounding — not the ones spending the most, but the ones building the most. That's the product.

**v1 = BlitzStars for AI operators.** Deep profiles, class tiers, circles, compare, Hall of Signal, Signalgeist Pro. One-person-built, Patreon/subscription monetized. The live event layer (weekly drop windows, real-time class promotions) bolts on without streaming infrastructure — it's a data event. v2+ = the arena.

---

## Sign-In Sheet

When you start work on this repo, add a row here. Format:

```
| Date (UTC) | Identity | Arrived from | Status on arrival | What you plan to do |
```

| Date (UTC) | Identity | Arrived from | Status on arrival | What you plan to do |
|---|---|---|---|---|
| 2026-06-16 | Devin (Cognition) | New session | INTEGRATION_PLAN.md written, 7 decisions resolved, Gradio app verified green | Created _merge/ workspace, post-commit hook, LOG.md |
| | | | | |

---

## Repo Map (what's where)

```
moses-sigrank/          ← THIS REPO (Gradio prototype + merger workspace)
├── app.py              ← Gradio UI (5 tabs, HF Spaces deployable)
├── metrics.py          ← Core math: Υ, cascade, SNR, SEED corpus
├── ingest.py           ← Parser: ccusage JSON, Codex, named fields, 4 numbers
├── db.py               ← Supabase persistence (non-blocking, SEED fallback)
├── sigrank.py          ← Local CLI: reads ccusage directly from your machine
├── narrate.py          ← MiniCPM4-0.5B narration (optional, template fallback)
├── theme.py            ← Dark/gold CSS
├── test_metrics.py     ← Unit tests (canonical locks)
├── INTEGRATION_PLAN.md ← The full merger plan (READ THIS)
├── DEPLOY.md           ← How to run + HF Spaces deployment
├── SCRATCHPAD.md       ← Per-session coordination (existing)
├── _merge/             ← THIS FOLDER
│   ├── README.md       ← You are here
│   └── LOG.md          ← Running append-only work log
│
RNS/sigrank-app/        ← Next.js commercial product (separate repo)
RNS/1_sigrank/          ← Spec docs (CANON.md, site_architecture.md, etc.)
RNS/sigrank-agent/      ← Python CLI agent
```

---

## Canonical Verify (run after EVERY change)

```bash
cd /Users/dericmchenry/Desktop/moses-sigrank
.venv/bin/python3 -m py_compile metrics.py ingest.py db.py app.py sigrank.py narrate.py theme.py
.venv/bin/python3 -c "from metrics import compute, SEED; m=compute(*SEED['MO§ES (ccusage)']); assert abs(m['yield']-18436.98)<0.1 and abs(m['leverage']-2042.2)<1 and abs(m['dev10x']-3.31)<0.01 and abs(m['avg_cost_1m']-0.527)<0.001; print('CANONICAL OK: Υ',round(m[\"yield\"],2),'lev',round(m['leverage'],1),'10xDEV',round(m['dev10x'],2),'$/1M',round(m['avg_cost_1m'],3))"
```

Expected output: `CANONICAL OK: Υ 18436.98 lev 2042.2 10xDEV 3.31 $/1M 0.527`

**Do NOT change these numbers.** They are the canonical anchor. If verify fails, do not commit.

---

## DO NOT TOUCH (frozen thesis)

- `metrics.py` MO§ES SEED row — canonical (Υ 18436.98)
- The Υ formula `(C·O)/I²` and the telescoping identity `(o/i)(cw/o)(cr/cw)==cr/i`
- Codex estimation must stay flagged/estimated — never a silent assumption
- The 9-class SIGNA RATE scoring engine in `RNS/sigrank-app/lib/scoring/engine.ts`

---

## Active Phase

**Current: Phase 0 (documentation) complete. Phase 1 (ingest port to TypeScript) is next.**

See `INTEGRATION_PLAN.md` for the full phase breakdown.
