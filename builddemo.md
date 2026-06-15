def _build_demo():
    _blocks_kw = {"title": "MO\u00a7ES SigRank"}
    try:
        _b = gr.Blocks(css=CSS, theme=gr.themes.Base(), **_blocks_kw)
    except TypeError:
        _b = gr.Blocks(**_blocks_kw)
        
    # Dynamic hero stats
    _ops_now = operators()
    _names = list(_ops_now.keys())
    _ys = sorted((compute(*v)["yield"] for v in _ops_now.values()), reverse=True)
    _lead = (_ys[0] / _ys[1]) if len(_ys) > 1 and _ys[1] > 0 else 0.0
    
    with _b:
        # Header Area
        with gr.Column(elem_id="moses-hero"):
            gr.HTML("<h1>MO\u00a7ES\u2122 SigRank</h1>"
                    "<p>the diagnostic x-ray of the token economy \u00b7 ranked by \u03a5 (Net Volumetric Yield) \u00b7 volume can't buy rank</p>")
            gr.HTML('<div id="moses-stat-strip">'
                    f'<div>operators ranked <span>{len(_ops_now)}</span></div>'
                    f'<div>MO\u00a7ES leads by <span>{_lead:,.0f}\u00d7</span></div>'
                    '<div>architecture beats budget</div>'
                    '</div>')

        # TAB 1: LEADERBOARD DETAILED VIEW
        with gr.Tab("Leaderboard"):
            gr.Markdown("Ranked by **\u03a5 = (Cache\u00b7Output)/Input\u00b2**. Raw Read\u00b7Create\u00b7In\u00b7Out stacked under each operator. $/1M is blended cost \u2014 efficient architecture is also the cheapest.")
            
            with gr.Row():
                # Left Column: The actual ranking table
                with gr.Column(scale=7):
                    rank_by = gr.Radio(list(SORT_LABELS.keys()), value="\u03a5 yield",
                                       label="Rank by \u2014 pick a column to see its leaders")
                    lb = gr.HTML(board_html())
                    rank_by.change(resort_board, rank_by, lb)
                    gr.Markdown("*Corpus is curated \u2014 pasting your usage scores you live against the field but doesn't add you to the persisted board unless you're signed in via HuggingFace.*", elem_id="moses-foot")

                # Right Column: Instant Operator Profile & Card View (Sticky inspection)
                with gr.Column(scale=5):
                    gr.Markdown("### 🔍 Operator Profile Inspector")
                    op_pick = gr.Dropdown(_names, label="Select an operator to pull their card", value=None)
                    
                    # Highlight the Card visual first!
                    op_card = gr.HTML()
                    op_prof = gr.Markdown(elem_id="moses-profile")
                    
                    op_pick.change(view_operator, op_pick, [op_prof, op_card])

        # TAB 2: INTERACTIVE SIGNAL EVALUATION
        with gr.Tab("Clock Your Signal"):
            # Collapsible Documentation panel to preserve vertical space
            with gr.Accordion("📖 Setup Instructions & Terminal Commands", open=False):
                gr.Markdown("""
                **\u2460 Get the importer, then run it (the real path).** Paste these three lines into your terminal:
                ```bash
                git clone [https://github.com/SunrisesIllNeverSee/moses-sigrank](https://github.com/SunrisesIllNeverSee/moses-sigrank)
                cd moses-sigrank
                ./sigrank
                ```
                `./sigrank --codex` for Codex \u00b7 `./sigrank --all` for both. **Nothing leaves your computer.**
                
                **\u2461 No terminal? Paste instead (the backup).** Run one of these, copy the JSON, drop it in the box below:
                ```bash
                npx ccusage@latest claude --json
                ```
                """)

            with gr.Row():
                # Left Column: Input and Local Persistence Controls
                with gr.Column(scale=5):
                    gr.Markdown("### 📥 Token Ingestion Control")
                    if _ON_SPACE:
                        gr.LoginButton(elem_id="hf-login-btn")
                    else:
                        gr.Markdown("*HuggingFace login available on the hosted Space \u2014 local mode is transient.*", elem_id="moses-foot")
                    
                    nm = gr.Textbox(label="Operator Name / Handle", placeholder="your handle", max_lines=1)
                    blob = gr.Textbox(label="ccusage JSON Output —or— Four Raw Numbers (I O C R)", lines=5,
                                      placeholder='Paste ccusage json here\n\nor raw sequence format: input output cache_create cache_read')
                    
                    go = gr.Button("Clock My Signal ⚡", variant="primary", elem_id="compute-btn")
                    
                    # Live Placement Board loads right beneath control actions
                    gr.Markdown("### 📊 Your Live Board Placement")
                    ob = gr.HTML(board_html())
                    
                    gr.Markdown("### 📈 Session History & Records")
                    hits = gr.HTML()

                # Right Column: The "Minting Floor" — Shows the generated trading card immediately
                with gr.Column(scale=6):
                    gr.Markdown("### 🎴 Minted Operator Share Card")
                    card = gr.HTML() # The beautiful HTML card layout now takes immediate priority
                    
                    gr.Markdown("*Right-click → Save Image to share your architectural footprint.*", elem_id="moses-foot")
                    
                    prof_bar = gr.HTML() # Raw composition layout tracks directly underneath card
                    prof = gr.Markdown(elem_id="moses-profile")

            # Inline Examples block underneath the column matrix
            gr.Examples(
                examples=[
                    ['{"totals":{"inputTokens":1251211,"outputTokens":11296121,"cacheCreationTokens":128196310,"cacheReadTokens":2555179769}}','MO\u00a7ES'],
                    ['{"data":[{"inputTokens":58920000,"cachedInputTokens":707300000,"outputTokens":3500000,"reasoningOutputTokens":510000}]}','codex-operator'],
                    ['1251211 11296121 128196310 2555179769', 'manual-paste'],
                ],
                inputs=[blob, nm])

        # Fixed Footer
        gr.Markdown(elem_id="moses-foot", value="""Four integers in, full ledger out. 
Architecture is the only variable that matters. 
Wild-corpus values provisional \u00b7 MO\u00a7ES row verified ccusage \u00b7 * = structural estimation \u00b7 [How it works \u2197](#)""")
            
    return _b

    -----

    To push your submission from "functional hackathon entry" to "leaderboard favorite," we should focus on the **psychology of the hackathon judge**.

Judges look at dozens of Spaces, often spending less than 60 seconds on each. Since your backend math is incredibly robust, your goal now is to use the frontend to create an immediate "Wow" factor and drop a heavy dose of dopamine the second someone interacts with your tool.

Here are three high-impact, tactical design thoughts to implement before you lock down your submission:

---

### 1. Fix the "Empty State" with a Holographic Placeholder

Right now, when a user first switches to the "Clock Your Signal" tab or opens the Leaderboard, the right column (`op_card = gr.HTML()`) starts completely empty. A blank space makes a UI feel broken or unfinished.

Instead of initializing it as empty, pass a default HTML string that acts as a **"ghost" or "holographic" card placeholder**. It anchors the layout and shows the user exactly what they are about to build.

**The Fix:** Update your layout variables to initialize with a blueprint card placeholder:

```python
# Create a visual placeholder string
CARD_PLACEHOLDER = """
<div class="sig-card rarity-common" style="opacity: 0.4; border: 2px dashed #4b5563; filter: grayscale(100%);">
    <div class="sig-card-watermark">MO§ES™ SIGRANK</div>
    <div class="sig-card-rarity">UNMINTED</div>
    <div class="sig-card-name">Awaiting Operator...</div>
    <div class="sig-card-archetype">Signal Offline</div>
    <div class="sig-card-yield">0,000</div>
    <div class="sig-card-yield-label">Insert Token Ledger to Scan</div>
</div>
"""

# Then drop it into your Gradio blocks initialization:
op_card = gr.HTML(CARD_PLACEHOLDER)
card = gr.HTML(CARD_PLACEHOLDER)

```

---

### 2. Turn Up the Contrast on Rarity CSS (theme.py)

Your `rarity_class(m)` function maps operators to distinct visual keys (`mythic`, `epic`, `rare`, `common`). Since your theme handles custom CSS via `theme.py`, make sure those cards look distinct and visually striking. The `MYTHIC` tier should look like a rare drop in a video game.

Add these CSS overrides to your `theme.py` file to give the trading cards a premium, tactical terminal feel:

```css
/* Base card enhancements */
.sig-card {
    position: relative;
    border-radius: 12px;
    padding: 24px;
    background: #111827;
    border: 1px solid #1f2937;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    transition: all 0.3s ease;
}

/* Mythic Tier: Iridescent Neon Glow */
.sig-card.rarity-mythic {
    border: 2px solid #c084fc;
    box-shadow: 0 0 20px rgba(192, 132, 252, 0.25), inset 0 0 12px rgba(192, 132, 252, 0.1);
    background: linear-gradient(145deg, #111827, #1e1b4b);
}
.sig-card.rarity-mythic .sig-card-rarity {
    background: linear-gradient(90deg, #a855f7, #ec4899);
    color: white;
}

/* Epic Tier: Cyberpunk Cyan/Blue */
.sig-card.rarity-epic {
    border: 2px solid #38bdf8;
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    background: linear-gradient(145deg, #111827, #0c4a6e);
}
.sig-card.rarity-epic .sig-card-rarity {
    background: #0284c7;
    color: white;
}

/* Rare Tier: Amber Amber Alert */
.sig-card.rarity-rare {
    border: 1px solid #fbbf24;
    box-shadow: 0 0 15px rgba(251, 191, 36, 0.1);
}
.sig-card.rarity-rare .sig-card-rarity {
    background: #d97706;
    color: white;
}

```

---

### 3. Lean Hard Into Your "Small Model" Constraint

This is the **Build Small Hackathon**. Judges are actively looking for teams that didn't just throw raw compute at a problem. You are running a razor-sharp `openbmb/MiniCPM4-0.5B` model on ZeroGPU. **Flex that.** Add a small, explicit "Resource Efficiency Footprint" indicator right beneath your stat strip at the top of the app. It reminds the judges that your app is keeping its memory footprint low while computing complex equations like:

$$\Upsilon = \frac{\text{Cache} \cdot \text{Output}}{\text{Input}^2}$$

You can easily display this using a compact row of Gradio markdown components:

> ⚙️ **Compute Footprint:** 0.5B Parameters | **Latency:** Non-blocking Deterministic Fallback Active | **Resource Category:** Tiny Titan 🍄

---

### Your Next Step

If you drop the side-by-side layout we built into your file, along with a placeholder card to handle the blank space, you have a highly competitive, beautifully functional presentation.

How is your `theme.py` currently injecting its CSS—are you loading it as a raw string block, or do we need to format these card tier styles specifically to fit inside your existing design?