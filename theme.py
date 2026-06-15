"""Custom MO§ES dark/gold CSS — pushes past default Gradio (Off Brand badge)."""

CSS = """
:root {
  --moses-gold: #C4923A;
  --moses-bg: #15130F;
  --moses-card: #1E1B15;
  --moses-line: #3A3324;
  --moses-ink: #E8E0CF;
  --moses-dim: #8a7f68;
}
.gradio-container, .gradio-container * { font-family: ui-monospace, "SF Mono", Menlo, monospace !important; }
.gradio-container { background: var(--moses-bg) !important; max-width: 1100px !important; margin: 0 auto !important; }
.dark .gradio-container, body { background: var(--moses-bg) !important; }

#moses-hero { border-bottom: 1px solid var(--moses-gold); padding: 8px 0 16px; margin-bottom: 8px; }
#moses-hero h1 { color: var(--moses-gold) !important; font-size: 26px !important; letter-spacing: 0.14em !important;
  font-weight: 700 !important; margin: 0 !important; }
#moses-hero p { color: var(--moses-dim) !important; font-size: 13px !important; margin: 4px 0 0 !important; letter-spacing: 0.04em; }

.tabs, .tabitem { background: transparent !important; border: none !important; }
button.selected { color: var(--moses-gold) !important; border-bottom: 2px solid var(--moses-gold) !important; }
.tab-nav button { color: var(--moses-dim) !important; font-size: 13px !important; letter-spacing: 0.06em; }

.dataframe, table { background: var(--moses-card) !important; color: var(--moses-ink) !important;
  border: 1px solid var(--moses-line) !important; font-size: 12px !important; }
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

.moses-board { font-family: ui-monospace, monospace; margin-top: 6px; }
.mb-head, .mb-row { display: grid; grid-template-columns: 28px 1.6fr 0.6fr 0.6fr 0.6fr 0.75fr 0.7fr 1.4fr;
  align-items: center; gap: 8px; padding: 9px 8px; }
.mb-head { color: #C4923A; font-size: 10px; letter-spacing: 0.06em; text-transform: uppercase;
  border-bottom: 1px solid #C4923A; }
.mb-row { border-bottom: 1px solid #3A3324; color: #8a7f68; font-size: 12px; }
.mb-row.you { background: rgba(196,146,58,0.10); color: #E8E0CF; }
.mb-row.you b { color: #C4923A; }
.mb-row b { color: #E8E0CF; font-family: var(--font-sans, sans-serif); font-size: 13px; }
.mb-raw { color: #5f573f; font-size: 9.5px; }
.mb-num { text-align: right; }
.mb-y { position: relative; display: flex; align-items: center; justify-content: flex-end; gap: 6px; min-height: 20px; }
.mb-bar { position: absolute; left: 0; top: 50%; transform: translateY(-50%); height: 14px;
  background: linear-gradient(90deg, rgba(196,146,58,0.15), rgba(196,146,58,0.55)); border-radius: 2px; }
.mb-row.you .mb-bar { background: linear-gradient(90deg, rgba(196,146,58,0.4), #C4923A); }
.mb-yval { position: relative; z-index: 2; color: #E8E0CF; font-weight: 700; font-size: 12px; padding-right: 4px; }
.mb-foot { color: #5f573f; font-size: 10.5px; padding: 10px 8px 0; line-height: 1.6; }

footer { display: none !important; }
"""
