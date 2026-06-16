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
[HOOK] 2026-06-16 14:23 UTC · ceccb77 · Burnmydays · feat: _merge/ workspace — README, LOG, post-commit hook
<!-- Format: `[HOOK] {timestamp} {hash} {subject}` -->

