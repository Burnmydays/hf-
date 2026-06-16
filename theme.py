"""Custom MO§ES dark/gold CSS — pushes past default Gradio (Off Brand badge)."""

CSS = """
:root {
  --moses-gold: #C4923A;
  --moses-bg: #15130F;
  --moses-card: #1E1B15;
  --moses-line: #3A3324;
  --moses-ink: #E8E0CF;
  --moses-dim: #8a7f68;
  --species-throughput: #6b7280;
  --species-converter: #3b82f6;
  --species-architect: #8b5cf6;
  --species-cascade: #C4923A;
}
.gradio-container, .gradio-container * { font-family: ui-monospace, "SF Mono", Menlo, monospace !important; }
.gradio-container { background: var(--moses-bg) !important; max-width: 1100px !important; margin: 0 auto !important; }
.dark .gradio-container, body { background: var(--moses-bg) !important; }

#moses-hero {
  border-bottom: 1px solid var(--moses-gold);
  padding: 10px 0 4px;
  margin-bottom: 0;
  position: relative;
}
/* kill the dead space: Blocks root column adds a 16px gap between hero and tabs */
.column:has(> #moses-hero) { gap: 4px !important; }
.tab-wrapper { margin: 0 0 2px 0 !important; padding: 0 !important; }
#moses-hero h1 {
  color: var(--moses-gold) !important;
  font-size: 32px !important;
  letter-spacing: 0.16em !important;
  font-weight: 700 !important;
  margin: 0 !important;
}
#moses-hero p { color: var(--moses-dim) !important; font-size: 12px !important; margin: 6px 0 0 !important; }

/* stat strip */
#moses-stat-strip {
  display: flex; gap: 24px; margin-top: 10px;
  font-size: 11px; color: var(--moses-dim); letter-spacing: 0.04em;
}
#moses-stat-strip span { color: var(--moses-ink); font-weight: 700; }

/* Tab padding layout stabilization overrides */
.tabs { background: transparent !important; border: none !important; }
.tabitem {
  background: transparent !important;
  border: none !important;
  padding: 2px 0px !important;
}
.tabitem > div { gap: 10px !important; }
button.selected { color: var(--moses-gold) !important; border-bottom: 2px solid var(--moses-gold) !important; }
/* centered nav links (Gradio 6.x uses .tab-container, not .tab-nav) */
.tab-nav, .tab-container { justify-content: center !important; gap: 6px; }
.tab-nav button, .tab-container > button { color: var(--moses-dim) !important; font-size: 14px !important;
  letter-spacing: 0.08em; text-transform: uppercase; font-weight: 700 !important; padding: 8px 16px !important; }

.dataframe, table { background: var(--moses-card) !important; color: var(--moses-ink) !important;
  border: 1px solid var(--moses-line) !important; font-size: 12px !important; width: 100% !important; }
.dataframe thead th, table thead th { background: var(--moses-bg) !important; color: var(--moses-gold) !important;
  border-bottom: 1px solid var(--moses-gold) !important; font-size: 10px !important;
  letter-spacing: 0.06em !important; text-transform: uppercase; padding: 8px 6px !important; }
.dataframe tbody td, table tbody td { border-bottom: 1px solid var(--moses-line) !important;
  color: var(--moses-dim) !important; padding: 8px 6px !important; }
.dataframe tbody tr:first-child td, table tbody tr:first-child td { color: var(--moses-ink) !important;
  background: rgba(196,146,58,0.08) !important; }

input, textarea, .gr-input, .gr-text-input {
  background: var(--moses-bg) !important; color: var(--moses-ink) !important;
  border: 1px solid var(--moses-line) !important; font-family: ui-monospace, monospace !important; }
input:focus, textarea:focus { border-color: var(--moses-gold) !important; box-shadow: 0 0 0 1px var(--moses-gold) !important; }
label span { color: var(--moses-dim) !important; font-size: 12px !important; letter-spacing: 0.04em; }

button.primary, .gr-button-primary, #compute-btn {
  background: var(--moses-gold) !important; color: var(--moses-bg) !important;
  border: none !important; font-weight: 700 !important; letter-spacing: 0.06em !important; }
button.primary:hover, #compute-btn:hover { background: #d8a449 !important; }

#moses-profile { background: var(--moses-card) !important; border: 1px solid var(--moses-line) !important;
  border-radius: 10px !important; padding: 4px 18px !important; }
#moses-profile h2 { color: var(--moses-gold) !important; letter-spacing: 0.08em; }
#moses-profile blockquote { border-left: 3px solid var(--moses-gold) !important; color: var(--moses-ink) !important;
  background: rgba(196,146,58,0.06); padding: 10px 14px; margin: 10px 0; }
#moses-profile table { font-size: 12px !important; }
#moses-profile th, #moses-profile td { color: var(--moses-ink) !important; }

.prose, .md, #moses-foot { color: var(--moses-dim) !important; font-size: 11px !important; }
#moses-foot { border-top: 1px solid var(--moses-line); padding-top: 10px; margin-top: 16px; line-height: 1.7; }

/* Structural Board Alignment Layout */
.moses-board { font-family: ui-monospace, monospace; margin-top: 6px; width: 100% !important; box-sizing: border-box !important; }
.mb-head, .mb-row { display: grid; grid-template-columns: 32px 1.8fr 0.6fr 0.7fr 0.7fr 0.75fr 0.7fr 1.5fr;
  align-items: center; gap: 12px; padding: 10px 12px; width: 100%; box-sizing: border-box; }
.mb-head { color: #C4923A; font-size: 10px; letter-spacing: 0.06em; text-transform: uppercase;
  border-bottom: 1px solid #C4923A; }
.mb-row { border-bottom: 1px solid #3A3324; color: #8a7f68; font-size: 12px; }
.mb-row.you { background: rgba(196,146,58,0.10); color: #E8E0CF; }
.mb-row.you b { color: #C4923A; }
.mb-row.rank1 {
  border-left: 3px solid var(--moses-gold);
  background: rgba(196,146,58,0.12) !important;
  color: var(--moses-ink) !important;
}
.mb-row.rank1 .mb-yval { color: var(--moses-gold); font-size: 14px; }

/* Species Classification Left Highlights */
.mb-row.species-throughput  { border-left: 3px solid var(--species-throughput); }
.mb-row.species-converter   { border-left: 3px solid var(--species-converter); }
.mb-row.species-architect   { border-left: 3px solid var(--species-architect); }
.mb-row.species-cascade     { border-left: 3px solid var(--species-cascade); }
.mb-rank-1 { color: var(--moses-gold); font-weight: 700; }
.mb-rank-2 { color: #a0a0a0; }
.mb-rank-3 { color: #8a6a3a; }
.mb-row b { color: #E8E0CF; font-family: var(--font-sans, sans-serif); font-size: 13px; }
.mb-raw { color: #7a7060; font-size: 9.5px; }
.mb-num { text-align: right; }
.mb-y { position: relative; display: flex; align-items: center; justify-content: flex-end; gap: 6px; min-height: 20px; }
.mb-bar { position: absolute; left: 0; top: 50%; transform: translateY(-50%); height: 14px;
  background: linear-gradient(90deg, rgba(196,146,58,0.28), rgba(196,146,58,0.72)); border-radius: 2px; }
.mb-row.you .mb-bar { background: linear-gradient(90deg, rgba(196,146,58,0.4), #C4923A); }
.mb-yval { position: relative; z-index: 2; color: #E8E0CF; font-weight: 700; font-size: 12px; padding-right: 4px; }
/* warmer, more inviting rows: subtle gold wash on hover, breathing room for the ledger line */
.mb-row { transition: background 0.12s ease; }
.mb-row:hover { background: rgba(196,146,58,0.07); }
.mb-raw { display: inline-block; margin-top: 3px; letter-spacing: 0.02em; opacity: 0.82; }
/* warm focus ring on the operator pickers */
#op-pick input:focus, #cmp-pick input:focus { box-shadow: 0 0 0 1px var(--moses-gold) !important; }

/* ---------- VS / compare table ---------- */
.cmp-table { width: 100%; border-collapse: collapse; background: var(--moses-card);
  border: 1px solid var(--moses-line); border-radius: 6px; overflow: hidden; margin-top: 6px; }
.cmp-table th, .cmp-table td { padding: 10px 12px; text-align: right; font-size: 13px;
  border-bottom: 1px solid var(--moses-line); }
.cmp-table thead th { color: var(--moses-gold); text-transform: uppercase; font-size: 11px;
  letter-spacing: 0.05em; border-bottom: 1px solid var(--moses-gold); }
.cmp-table th.cmp-op { color: var(--moses-ink); font-weight: 700; }
.cmp-rowlabel { text-align: left !important; color: var(--moses-dim); text-transform: uppercase;
  font-size: 10px; letter-spacing: 0.05em; }
.cmp-win { color: var(--moses-bg) !important; background: var(--moses-gold) !important;
  font-weight: 700; }
.cmp-empty { padding: 26px; text-align: center; color: var(--moses-dim);
  border: 1px dashed var(--moses-line); border-radius: 6px; background: rgba(196,146,58,0.03); }
.cmp-note { color: var(--moses-dim); font-size: 10px; margin-top: 8px; }
@media (max-width: 700px) { .cmp-table th, .cmp-table td { padding: 7px 6px; font-size: 11px; } }

/* ---------- Home / landing ---------- */
.hm-lead { color: var(--moses-dim); font-size: 11px; letter-spacing: 0.04em;
  text-transform: uppercase; margin: 2px 2px 6px; }
.pm-wrap { overflow: hidden; border: 1px solid var(--moses-line); border-radius: 6px;
  background: var(--moses-card); padding: 8px 0; margin-bottom: 14px; }
.pm-track { display: flex; gap: 10px; width: max-content; animation: pm-scroll 70s linear infinite; }
.pm-wrap:hover .pm-track { animation-play-state: paused; }
@keyframes pm-scroll { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.pm-chip { display: flex; align-items: center; gap: 8px; padding: 6px 12px; white-space: nowrap;
  border-left: 3px solid var(--moses-line); background: rgba(196,146,58,0.04); border-radius: 4px; }
.pm-chip.species-throughput { border-left-color: var(--species-throughput); }
.pm-chip.species-converter  { border-left-color: var(--species-converter); }
.pm-chip.species-architect  { border-left-color: var(--species-architect); }
.pm-chip.species-cascade    { border-left-color: var(--species-cascade); }
.pm-rank { color: var(--moses-dim); font-size: 10px; font-weight: 700; }
.pm-name { color: var(--moses-ink); font-size: 12px; font-weight: 700; }
.pm-stat { color: var(--moses-gold); font-size: 11px; font-weight: 700; }
.pm-lev  { color: var(--moses-dim); font-size: 10px; }

.hm-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.hm-box { border: 1px solid var(--moses-line); border-radius: 6px; background: var(--moses-card);
  padding: 16px 18px; transition: border-color 0.12s ease, background 0.12s ease; }
.hm-box:hover { border-color: var(--moses-gold); background: rgba(196,146,58,0.06); }
.hm-title { color: var(--moses-gold); font-size: 15px; font-weight: 800; letter-spacing: 0.04em; }
.hm-sub { color: var(--moses-ink); font-size: 12px; font-weight: 600; margin-top: 3px; }
.hm-desc { color: var(--moses-dim); font-size: 11px; margin-top: 6px; line-height: 1.45; }
.hm-cta { color: var(--moses-gold); font-size: 10px; text-transform: uppercase;
  letter-spacing: 0.06em; margin-top: 12px; }
@media (max-width: 700px) { .hm-grid { grid-template-columns: 1fr; } }

/* metric standard (feature row) */
.mf-head { text-align: center; color: var(--moses-ink); font-size: 26px; font-weight: 800;
  letter-spacing: 0.01em; margin: 0 0 14px; line-height: 1.2; }
.mf-head span { color: var(--moses-gold); text-shadow: 0 0 18px rgba(196,146,58,0.35); }
@media (max-width: 700px) { .mf-head { font-size: 20px; } }
.mf-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 14px; }
.mf-box { border: 1px solid var(--moses-gold); border-radius: 6px; background: rgba(196,146,58,0.06);
  padding: 12px; text-align: center; }
.mf-sym { color: var(--moses-gold); font-size: 22px; font-weight: 800; }
.mf-form { color: var(--moses-ink); font-size: 11px; font-family: ui-monospace, monospace; margin-top: 2px; }
.mf-tag { color: var(--moses-dim); font-size: 10px; text-transform: uppercase; letter-spacing: 0.04em; margin-top: 4px; }
@media (max-width: 700px) { .mf-grid { grid-template-columns: 1fr 1fr; } }

/* mini samples inside section boxes */
.hm-sample { margin: 10px 0; padding: 8px 10px; border: 1px solid var(--moses-line);
  border-radius: 4px; background: var(--moses-bg); font-size: 11px; }
.sm-row { display: flex; gap: 8px; align-items: center; padding: 2px 0; }
.sm-rk { color: var(--moses-dim); font-size: 10px; width: 22px; }
.sm-nm { color: var(--moses-ink); font-weight: 700; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.sm-y { color: var(--moses-gold); font-weight: 700; }
.sm-y2 { color: var(--moses-dim); font-weight: 700; }
.sm-card .sm-nm { font-size: 12px; }
.sm-kv { color: var(--moses-dim); font-size: 10px; margin-top: 3px; }
.sm-vs { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.sm-vsx { color: var(--moses-gold); font-size: 10px; text-transform: uppercase; }
.sm-create { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.sm-create code { color: var(--moses-dim); font-size: 10px; }
.sm-arrow { color: var(--moses-gold); }

/* home footer: demo video + steps + links */
.hm-foot { display: grid; grid-template-columns: 1fr 1.4fr 0.8fr; gap: 16px; margin-top: 14px;
  padding-top: 14px; border-top: 1px solid var(--moses-line); }
.hf-h { color: var(--moses-gold); font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
.hf-btn { display: inline-block; background: var(--moses-gold); color: var(--moses-bg) !important;
  padding: 8px 14px; border-radius: 5px; font-weight: 700; font-size: 12px; text-decoration: none; }
.hf-steps { margin: 0; padding-left: 18px; color: var(--moses-dim); font-size: 11px; line-height: 1.7; }
.hf-steps code { color: var(--moses-ink); font-size: 10px; }
.hf-steps b { color: var(--moses-gold); }
.hf-link { display: block; color: var(--moses-gold) !important; font-size: 12px; margin-bottom: 6px; text-decoration: none; }
.hf-link:hover { text-decoration: underline; }
@media (max-width: 700px) { .hm-foot { grid-template-columns: 1fr; } }

/* ---------- mini page thumbnails (real HTML scaled down) ---------- */
.mini { border-radius: 8px; overflow: hidden; background: var(--moses-card);
  border: 1px solid var(--moses-line); box-shadow: 0 6px 20px rgba(0,0,0,0.5); margin-bottom: 12px; }
.mini-chrome { display: flex; align-items: center; gap: 5px; padding: 6px 9px;
  border-bottom: 1px solid var(--moses-line); background: linear-gradient(90deg,#241f17,#15130f); }
.mini-chrome span { width: 7px; height: 7px; border-radius: 50%; background: #3A3324; flex: none; }
.mini-cap { margin-left: auto; font-size: 8.5px; text-transform: uppercase;
  letter-spacing: 0.08em; color: var(--moses-dim); }
.mini-view { position: relative; height: 190px; overflow: hidden; background: var(--moses-bg); }
.mini-scale { position: absolute; top: 0; left: 0; width: 323%;
  transform: scale(0.31); transform-origin: top left; pointer-events: none; }
/* per-section accent on the chrome dot + frame + glow */
.mini-gold   { border-color: rgba(196,146,58,0.55); }  .mini-gold   .mini-chrome span:first-child { background: #C4923A; }
.mini-purple { border-color: rgba(139,92,246,0.55); }  .mini-purple .mini-chrome span:first-child { background: #8b5cf6; }
.mini-blue   { border-color: rgba(59,130,246,0.55); }  .mini-blue   .mini-chrome span:first-child { background: #3b82f6; }
.mini-green  { border-color: rgba(34,197,94,0.55); }   .mini-green  .mini-chrome span:first-child { background: #22c55e; }

/* colorful section accents */
.hm-gold   { border-top: 3px solid #C4923A; }  .hm-gold   .hm-title { color: #C4923A; }
.hm-purple { border-top: 3px solid #8b5cf6; }  .hm-purple .hm-title { color: #a78bfa; }
.hm-blue   { border-top: 3px solid #3b82f6; }  .hm-blue   .hm-title { color: #60a5fa; }
.hm-green  { border-top: 3px solid #22c55e; }  .hm-green  .hm-title { color: #4ade80; }
.hm-gold:hover   { box-shadow: 0 0 0 1px #C4923A, 0 10px 26px rgba(196,146,58,0.18); border-color: #C4923A; }
.hm-purple:hover { box-shadow: 0 0 0 1px #8b5cf6, 0 10px 26px rgba(139,92,246,0.18); border-color: #8b5cf6; }
.hm-blue:hover   { box-shadow: 0 0 0 1px #3b82f6, 0 10px 26px rgba(59,130,246,0.18); border-color: #3b82f6; }
.hm-green:hover  { box-shadow: 0 0 0 1px #22c55e, 0 10px 26px rgba(34,197,94,0.18); border-color: #22c55e; }

/* create-tab mock (rendered inside its thumbnail) */
.cr-mock { padding: 16px; font-size: 14px; }
.cr-code { color: #4ade80; background: #0f0d0a; padding: 10px 12px; border-radius: 5px;
  font-family: ui-monospace, monospace; }
.cr-box { color: var(--moses-dim); border: 1px dashed var(--moses-line); padding: 12px;
  margin: 10px 0; border-radius: 5px; }
.cr-box b { color: var(--moses-ink); }
.cr-btn { background: var(--moses-gold); color: var(--moses-bg); text-align: center;
  padding: 10px; border-radius: 5px; font-weight: 800; }
.cr-res { color: var(--moses-gold); margin-top: 10px; font-weight: 800; text-align: center; }

/* ---------- middle nav link (Leaders) emphasized ---------- */
.tab-container > button:nth-child(3), .tab-nav > button:nth-child(3) {
  color: var(--moses-gold) !important; font-size: 17px !important; font-weight: 800 !important;
  text-shadow: 0 0 14px rgba(196,146,58,0.4); }

/* ---------- hero status + live counters (top-right) ---------- */
.hero-stat { text-align: right; font-size: 10px; letter-spacing: 0.06em; line-height: 1.65;
  font-weight: 700; color: var(--moses-dim); white-space: nowrap; min-width: 196px; }
.hs-row { display: flex; justify-content: space-between; gap: 16px; }
.hs-div { height: 1px; background: var(--moses-line); margin: 5px 0; }
.hs-burn { color: #ef6b6b; } .hs-build { color: #4ade80; } .hs-tenx { color: var(--moses-gold); }
@media (max-width: 700px) { .hero-stat { display: none; } }

/* ---------- equation boxes: median/avg + hover description ---------- */
.mf-box { position: relative; cursor: help; }
.mf-stat { color: var(--moses-dim); font-size: 9.5px; margin-top: 5px; letter-spacing: 0.02em; }
.mf-tip { position: absolute; left: 50%; bottom: calc(100% + 8px); transform: translateX(-50%);
  width: 220px; max-width: 70vw; background: #0f0d0a; color: var(--moses-ink);
  border: 1px solid var(--moses-gold); border-radius: 6px; padding: 10px 12px; font-size: 11px;
  line-height: 1.45; text-align: left; opacity: 0; visibility: hidden; transition: opacity 0.15s ease;
  z-index: 60; box-shadow: 0 8px 24px rgba(0,0,0,0.6); }
.mf-box:hover .mf-tip, .mf-box:focus .mf-tip { opacity: 1; visibility: visible; }
.mf-sub { text-align: center; color: var(--moses-dim); font-size: 10px; margin: -4px 0 14px; }

/* ---------- reports: learn-from insights ---------- */
.ins-wrap { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 14px; }
.ins-block { border: 1px solid var(--moses-line); border-radius: 6px; padding: 12px 14px; }
.ins-good { border-left: 3px solid #4ade80; background: rgba(34,197,94,0.05); }
.ins-avoid { border-left: 3px solid #ef6b6b; background: rgba(239,107,107,0.05); }
.ins-h { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 800; margin-bottom: 6px; }
.ins-good .ins-h { color: #4ade80; } .ins-avoid .ins-h { color: #ef6b6b; }
.ins-block ul { margin: 0; padding-left: 16px; }
.ins-block li { color: var(--moses-dim); font-size: 11.5px; line-height: 1.5; margin-bottom: 4px; }
@media (max-width: 700px) { .ins-wrap { grid-template-columns: 1fr; } }
.mb-foot { color: #5f573f; font-size: 10.5px; padding: 10px 8px 0; line-height: 1.6; }

/* composition bar */
.comp-bar { display: flex; height: 6px; border-radius: 3px; overflow: hidden; margin: 6px 0 10px; width: 100%; }
.comp-read { background: var(--moses-gold); }
.comp-create { background: #8a6a3a; }
.comp-output { background: #5a7a5a; }
.comp-input { background: #3a4a5a; }

/* trading card */
.sig-card {
  width: 380px; min-height: 500px;
  background: linear-gradient(160deg, #1E1B15 60%, #2a2318);
  border-radius: 12px;
  padding: 28px 24px 20px;
  font-family: ui-monospace, monospace;
  position: relative;
}
.sig-card.species-throughput  { border: 1px solid var(--species-throughput); box-shadow: 0 0 20px rgba(107,114,128,0.12); }
.sig-card.species-converter   { border: 1px solid var(--species-converter);  box-shadow: 0 0 24px rgba(59,130,246,0.15); }
.sig-card.species-architect   { border: 1px solid var(--species-architect);  box-shadow: 0 0 28px rgba(139,92,246,0.18); }
.sig-card.species-cascade     { border: 1px solid var(--species-cascade);    box-shadow: 0 0 40px rgba(196,146,58,0.22), inset 0 1px 0 rgba(196,146,58,0.15); }
.sig-card-watermark {
  position: absolute; top: 14px; right: 16px;
  font-size: 9px; color: var(--moses-dim); letter-spacing: 0.1em;
}
.sig-card-name { color: var(--moses-ink); font-size: 22px; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 4px; }
.sig-card-archetype {
  display: inline-block; font-size: 10px; letter-spacing: 0.08em;
  border: 1px solid var(--moses-gold); color: var(--moses-gold);
  padding: 2px 8px; border-radius: 2px; margin-bottom: 20px; text-transform: uppercase;
}
.sig-card-yield { font-size: 52px; font-weight: 700; color: var(--moses-ink); line-height: 1; }
.sig-card-yield-label { font-size: 10px; color: var(--moses-dim); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 20px; }
.sig-card-rank { font-size: 13px; color: var(--moses-dim); margin-bottom: 16px; }
.sig-card-rank span { color: var(--moses-ink); font-weight: 700; }
.sig-card-cascade {
  display: flex; align-items: center; gap: 6px;
  font-size: 11px; margin-bottom: 16px;
}
.sig-card-cascade-box {
  border: 1px solid #3A3324; padding: 4px 8px; border-radius: 3px;
  color: var(--moses-ink); text-align: center; min-width: 52px;
}
.sig-card-cascade-box small { display: block; color: var(--moses-dim); font-size: 9px; }
.sig-card-cascade-arrow { color: var(--moses-dim); }
.sig-card-quote {
  font-size: 11px; color: var(--moses-dim);
  border-left: 2px solid var(--moses-gold);
  padding: 8px 12px; margin-top: 16px; line-height: 1.5;
  font-style: italic;
}
.sig-card-rarity { display: inline-block; font-size: 9px; letter-spacing: 0.14em; text-transform: uppercase; font-weight: 700; padding: 2px 8px; border-radius: 2px; margin-bottom: 8px; }
.sig-card-rarity.species-throughput  { color: var(--species-throughput); border: 1px solid var(--species-throughput); }
.sig-card-rarity.species-converter   { color: var(--species-converter);  border: 1px solid var(--species-converter); }
.sig-card-rarity.species-architect   { color: var(--species-architect);  border: 1px solid var(--species-architect); }
.sig-card-rarity.species-cascade     { color: var(--species-cascade);    border: 1px solid var(--species-cascade); }
.sig-card-passive { font-size: 9px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--moses-dim); margin: 12px 0 4px; }
.sig-card-effect  { font-size: 10px; color: var(--moses-dim); font-style: italic; border-left: 2px solid #3A3324; padding: 6px 10px; margin-bottom: 14px; line-height: 1.5; }
.sig-card.species-cascade .sig-card-yield { color: var(--species-cascade); }
.sig-card.species-cascade .sig-card-name  { color: var(--species-cascade); }
.sig-card-footer {
  position: absolute; bottom: 16px; left: 24px; right: 24px;
  font-size: 9px; color: #5f573f; letter-spacing: 0.06em;
  border-top: 1px solid #3A3324; padding-top: 8px;
  display: flex; justify-content: space-between;
}

/* parsing mode badge on trading card */
.sig-card-mode {
  font-size: 8px; color: var(--moses-dim); letter-spacing: 0.06em;
  margin-bottom: 10px; padding: 2px 6px;
  border: 1px dashed var(--moses-line); border-radius: 2px;
  display: inline-block;
}

/* estimation asterisk on board rows */
.mb-est { color: var(--moses-gold); font-weight: 700; font-size: 10px; cursor: help; }

/* greatest hits table */
.greatest-hits { margin: 16px 0; }
.greatest-hits h4 { color: var(--moses-gold); font-size: 13px; letter-spacing: 0.08em; margin-bottom: 8px; }
.greatest-hits table { width: 100%; border-collapse: collapse; font-size: 11px; }
.greatest-hits th {
  color: var(--moses-gold); font-size: 9px; letter-spacing: 0.06em;
  text-transform: uppercase; text-align: left; padding: 6px 8px;
  border-bottom: 1px solid var(--moses-gold);
}
.greatest-hits td {
  color: var(--moses-dim); padding: 6px 8px;
  border-bottom: 1px solid var(--moses-line);
}
.greatest-hits tr:first-child td { color: var(--moses-ink); }

/* HF login button styling */
#hf-login-btn { margin-bottom: 8px; }

/* "Rank by" radio -> horizontal pill / segmented control (not a gray form) */
#rank-by { border: none !important; background: transparent !important; padding: 0 !important; }
#rank-by .wrap { display: flex !important; flex-wrap: wrap; gap: 6px; }
#rank-by .wrap label {
  background: var(--moses-card); border: 1px solid var(--moses-line);
  border-radius: 16px; padding: 4px 12px; color: var(--moses-dim);
  font-size: 11px; cursor: pointer; margin: 0 !important; }
#rank-by .wrap label.selected, #rank-by .wrap label:has(input:checked) {
  border-color: var(--moses-gold) !important; color: var(--moses-gold) !important;
  background: rgba(196,146,58,0.12) !important; }
#rank-by input[type="radio"] { display: none !important; }

/* primary-path clone code block — match the dark terminal */
#clone-code, #clone-code * { background: var(--moses-bg) !important; color: var(--moses-ink) !important; }
#clone-code { border: 1px solid var(--moses-line) !important; border-radius: 8px !important; }

/* operator picker dropdown */
#op-pick input { background: var(--moses-bg) !important; color: var(--moses-ink) !important; }

/* ghost / unminted placeholder card */
#ghost-card { opacity: 0.45; border-style: dashed !important; }

footer { display: none !important; }

/* ---------- metrics key (collapsible legend under the board) ---------- */
.metric-key { margin: 10px 2px 0; border: 1px solid #3A3324; border-radius: 6px;
  background: rgba(196,146,58,0.04); }
.metric-key summary { cursor: pointer; padding: 9px 12px; color: #C4923A;
  font-size: 12px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase;
  list-style: none; }
.metric-key summary::-webkit-details-marker { display: none; }
.metric-key summary::before { content: "▸ "; color: #8a7f68; }
.metric-key[open] summary::before { content: "▾ "; }
.metric-key .mk-hint { color: #8a7f68; font-weight: 400; text-transform: none;
  letter-spacing: 0; font-size: 11px; }
.mk-legend { padding: 4px 12px 12px; }
.mk-note { color: #8a7f68; font-size: 11px; margin: 2px 0 10px; }
.mk-note b { color: #C4923A; }
.mk-row { display: grid; grid-template-columns: 96px 150px 130px 1fr; gap: 8px;
  align-items: baseline; padding: 6px 0; border-top: 1px solid #2c2718; }
.mk-name { color: #E8E0CF; font-weight: 700; font-size: 12px; }
.mk-form { color: #C4923A; font-family: ui-monospace, monospace; font-size: 11px; }
.mk-alias { color: #8a7f68; font-size: 11px; font-style: italic; }
.mk-desc { color: #a89e85; font-size: 11px; line-height: 1.45; }
@media (max-width: 700px) {
  /* stack each metric into a card on phones */
  .mk-row { grid-template-columns: 1fr; gap: 2px; }
  .mk-form { font-size: 10px; }
}

@media (max-width: 700px) {
  /* mobile: collapse both boards to rank · operator · Υ. The numeric middle
     columns drop out entirely instead of being crushed into too-few tracks.
     !important beats the slim board's inline grid-template-columns. */
  .mb-head, .mb-row {
    grid-template-columns: 22px 1fr 72px !important;
    gap: 6px !important;
    font-size: 11px;
  }
  .mb-num { display: none !important; }
  .mb-head span:nth-child(3), .mb-head span:nth-child(4),
  .mb-row span:nth-child(3), .mb-row span:nth-child(4) { display: none !important; }
  .mb-op { min-width: 0; overflow-wrap: anywhere; }
  .mb-raw { font-size: 9px; line-height: 1.35; }
  .mb-y, .mb-yval { font-size: 11px !important; }
}
"""
