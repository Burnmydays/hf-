# _merge/LOG.md — Running Work Log

**Format:** Newest entry at top. Append, never edit old entries. Each entry gets: date/time UTC, identity, what was done, canonical verify result, what's next.

---

## 2026-06-16 — Devin (Cognition)

**Session summary:** Deep read of both repos (moses-sigrank Gradio + RNS sigrank-app Next.js). Wrote INTEGRATION_PLAN.md. Resolved 7 open decisions. Researched competitive landscape (BlitzStars, tokscale.ai, ccusage, 10 AI arena platforms). Created `_merge/` workspace.

**What was done:**
- Read full source: `metrics.py`, `ingest.py`, `db.py`, `sigrank.py`, `narrate.py`, `app.py`, `theme.py`
- Read full spec: `CANON.md`, `token_metric_bridge.md`, `CONSERVATION_LAW.md`, `engine.ts`, `ruleset.ts`, `mock.ts`, `site_architecture.md`
- Read secondary: `species_cards.md`, `SigTune` buildouts, `SiGlobe` CLAUDE/AUDIT, `signal-Areana` App.tsx
- Created `INTEGRATION_PLAN.md` — full phased merger plan
- Created `DEPLOY.md` — local + HF Spaces run instructions
- Resolved all 7 open decisions (see INTEGRATION_PLAN.md §Decisions Made)
- Created `_merge/README.md` + `_merge/LOG.md` (this file)
- Installed post-commit hook → auto-appends to this log on every commit

**Canonical verify:** PASS — Υ 18436.98, lev 2042.2, 10xDEV 3.31, $/1M 0.527

**Commits this session:**
- `65a3082` — docs: integration plan + deploy guide
- `069f425` — docs: resolve all 7 open questions + add competitive landscape
- (pending) — feat: _merge/ workspace + post-commit hook

**Current phase:** Phase 0 (documentation) → COMPLETE  
**Next phase:** Phase 1 — port `ingest.py` to TypeScript in `RNS/sigrank-app/lib/ingest/`

**Open items / questions for owner:**
- [ ] HF Spaces secrets still need to be set (SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY) — see SCRATCHPAD.md BLOCKED ON OWNER section
- [ ] Confirm Founder tier cap (how many slots before closing?)
- [ ] When to reach out to tokscale.ai / ccusage — after first live operators, or at launch?
- [x] The "locate Transmitters" vision — ANSWERED: goal is to unify people and locate Transmitters. See architecture decision below.

---

## Architecture Decision — "Locate Transmitters" (2026-06-16)

**Owner confirmed:** The ultimate goal of SigRank is to unify people and locate Transmitters. This is the thesis, not a feature.

**What this requires (resolved):**

1. **`/transmitters` discovery page** — K.01-only filtered leaderboard view. Filterable by platform, domain, circle. CTA = "Challenge" → `/compare?a={codename}&b=you`. This is BlitzStars `/topplayers` but gated to TRANSMITTER class.

2. **Domain tags on operator profiles** — free text + preset tags (code / legal / creative / research / multi). One DB column (`operator_domains TEXT[]`) that unlocks the entire discovery dimension. Without domain tags, a TRANSMITTER is a number. With them, they're findable.

3. **Class-promotion events** — when RS.07 stickiness fires and a promotion to TRANSMITTER completes, it's a DB state change. That change powers: homepage feed ("A new TRANSMITTER emerged"), circle notifications, webhook. No streaming required — Supabase realtime on `class_tier` column → Next.js `useChannel()` → homepage live feed.

4. **Weekly Drop Window** (the live event that bolts on):
   - Mon 00:00–Fri 23:59 UTC: submission window open
   - Sat 00:00 UTC: window closes
   - Sat 12:00 UTC: scoring cron runs (`app/api/cron/weekly-drop/route.ts` on Vercel)
   - Sat 13:00 UTC: leaderboard updates atomically, class changes fire as events
   - This is the "live event" — a data event, not streaming infrastructure

**Build position:** Phase 3.5 (between real seed data and trading cards). Requires:
- `operator_domains` column in DB schema
- `/transmitters` page (~1 page component)
- `app/api/cron/weekly-drop/route.ts` (Vercel cron)
- Supabase realtime subscription on `class_tier` in the homepage component

**This is what makes SigRank a social product, not just a stats tracker.**

---

<!-- POST-COMMIT HOOK APPENDS BELOW THIS LINE -->
[HOOK] 2026-06-16 23:37 UTC · 5142b32 · Burnmydays · ui(hero): logo inline + absolutely page-centered on the title row (above the divider)
[HOOK] 2026-06-16 23:25 UTC · 040c71a · Burnmydays · ui(hero): move § logo above the divider line, centered + larger (82px)
[HOOK] 2026-06-16 22:31 UTC · a037512 · Burnmydays · ui: hero recompose (centered logo+Identifying, bigger Ranking) + filter centered + board ratio column
[HOOK] 2026-06-16 20:43 UTC · c47b6d8 · Burnmydays · ui(board): narrow Υ column + min-width:0 so the ledger no longer pushes off-screen
[HOOK] 2026-06-16 20:17 UTC · be61774 · Burnmydays · ui(board): ledger uses 1 decimal (2.6B, not 3B)
[HOOK] 2026-06-16 20:13 UTC · 8baf743 · Burnmydays · ui(board): contain Υ bar; ledger rounds to whole K/M/B/T + Σ total
[HOOK] 2026-06-16 19:54 UTC · 261167e · Burnmydays · ui(hero): ground logo + subhead to the divider; stack Identifying above Ranking
[HOOK] 2026-06-16 19:19 UTC · 6bc1e58 · Burnmydays · fix(hero): CSS-drawn logo (Gradio strips both <svg> and data: <img>)
[HOOK] 2026-06-16 19:10 UTC · 2ec4d0a · Burnmydays · fix(hero): render logo as base64 data-URI <img> (Gradio strips inline <svg>)
[HOOK] 2026-06-16 19:03 UTC · 6d179af · Burnmydays · ui(hero): replace placeholder §§ with SVG rebuild of the MO§ES logo
[HOOK] 2026-06-16 18:59 UTC · 685a4f1 · Burnmydays · ui: clickable Home minis + board column re-tune + hero §§ mark (placeholder)
[HOOK] 2026-06-16 18:35 UTC · 512646e · Burnmydays · ui: hero subhead clears HF pill; board raw data moved to last 'ledger' column
[HOOK] 2026-06-16 15:11 UTC · 288ba6a · Burnmydays · redesign(hero): SIGRANK left / subhead right; move counters into a status metric box
[HOOK] 2026-06-16 14:54 UTC · 1eb5a6f · Burnmydays · fix(ui): center hero brand + condense/sharpen board columns
[HOOK] 2026-06-16 14:44 UTC · 1b200e0 · Burnmydays · feat(ui): full metrics explainer + README Υ disambiguation
[HOOK] 2026-06-16 14:37 UTC · f2a7d8a · Burnmydays · docs: add AGENTS.md — agent/dev guide (architecture, frozen invariants, conventions)
[HOOK] 2026-06-16 14:35 UTC · b60e583 · Burnmydays · docs(_merge): log Transmitter locator architecture decision
[HOOK] 2026-06-16 14:23 UTC · ceccb77 · Burnmydays · feat: _merge/ workspace — README, LOG, post-commit hook
<!-- Format: `[HOOK] {timestamp} {hash} {subject}` -->

