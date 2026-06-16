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
- [ ] The "locate Transmitters" vision — does this mean: (a) public discovery page where anyone can find the highest-class operators in their domain, (b) a notification/alert system ("a new TRANSMITTER emerged"), or (c) something else?

---

<!-- POST-COMMIT HOOK APPENDS BELOW THIS LINE -->
<!-- Format: `[HOOK] {timestamp} {hash} {subject}` -->

