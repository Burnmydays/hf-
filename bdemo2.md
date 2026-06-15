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
        # Header Area — Monochrome / Gold Core Terminal Style
        with gr.Column(elem_id="moses-hero"):
            gr.HTML("<h1>MO\u00a7ES\u2122 SigRank</h1>"
                    "<p>The Diagnostic X-Ray of the Token Economy // Ranked by \u03a5 (Net Volumetric Yield) // Volume Can't Buy Rank</p>")
            gr.HTML('<div id="moses-stat-strip">'
                    f'<div>OPERATORS RANKED <span>{len(_ops_now)}</span></div>'
                    f'<div>MO\u00a7ES LEADS BY <span>{_lead:,.0f}\u00d7</span></div>'
                    '<div>ARCHITECTURE BEATS BUDGET</div>'
                    '</div>')

        # TAB 1: LEADERBOARD DETAILED VIEW
        with gr.Tab("Leaderboard"):
            gr.Markdown("Ranked by **\u03a5 = (Cache\u00b7Output)/Input\u00b2**. Raw Read\u00b7Create\u00b7In\u00b7Out stacked under each operator. $/1M is blended cost \u2014 efficient architecture is also the cheapest.")
            
            with gr.Row():
                # Left Column: The actual ranking table
                with gr.Column(scale=7):
                    rank_by = gr.Radio(list(SORT_LABELS.keys()), value="\u03a5 yield",
                                       label="Rank by Column Target")
                    lb = gr.HTML(board_html())
                    rank_by.change(resort_board, rank_by, lb)
                    gr.Markdown("*Corpus is curated \u2014 pasting your usage scores you live against the field but doesn't add you to the persisted board unless you're signed in via HuggingFace.*", elem_id="moses-foot")

                # Right Column: Instant Operator Profile & Card View (Sticky inspection)
                with gr.Column(scale=5):
                    gr.Markdown("### Operator Profile Inspector")
                    op_pick = gr.Dropdown(_names, label="Select Operator to Inspect Card", value=None)
                    
                    # Trading Card visual frame taking visual priority
                    op_card = gr.HTML()
                    op_prof = gr.Markdown(elem_id="moses-profile")
                    
                    op_pick.change(view_operator, op_pick, [op_prof, op_card])

        # TAB 2: INTERACTIVE SIGNAL EVALUATION
        with gr.Tab("Clock Your Signal"):
            
            # Primary execution path: Local terminal importer visible immediately
            gr.Markdown("### Primary Path: Run local importer")
            gr.Markdown("Execute directly on your machine to analyze your trace logs with zero network exposure. Nothing leaves your computer.")
            
            # Clean bash block with plain URL for reliable copy-pasting
            gr.Code(
                value="git clone https://github.com/Burnmydays/hf-\ncd hf-\n./sigrank",
                language="bash",
                show_label=False
            )
            
            with gr.Accordion("Alternative: Advanced arguments & Codex setup overrides", open=False):
                gr.Markdown("""
                Run `./sigrank --codex` to handle non-itemized cache layers, or `./sigrank --all` to process every provider sequence simultaneously.
                """)

            gr.HTML("<hr style='border-color: #3a3324; margin: 20px 0;'>")

            with gr.Row():
                # Left Column: Input and Local Persistence Controls
                with gr.Column(scale=5):
                    gr.Markdown("### Secondary Path: Manual ingestion block")
                    if _ON_SPACE:
                        gr.LoginButton(elem_id="hf-login-btn")
                    else:
                        gr.Markdown("*HuggingFace login available on the hosted Space \u2014 local mode is transient.*", elem_id="moses-foot")
                    
                    nm = gr.Textbox(label="Operator Name / Handle", placeholder="Enter handle...", max_lines=1)
                    blob = gr.Textbox(label="ccusage JSON Sequence —or— Four Raw Numbers (I O C R)", lines=5,
                                      placeholder='Paste JSON telemetry here...\n\nAlternatively, enter plain integers: input output cache_create cache_read')
                    
                    go = gr.Button("Clock My Signal", variant="primary", elem_id="compute-btn")
                    
                    # Live Placement Board loads beneath interaction panel
                    gr.Markdown("### Live Board Placement Analysis")
                    ob = gr.HTML(board_html())
                    
                    gr.Markdown("### Operator Greatest Hits")
                    hits = gr.HTML()

                # Right Column: The Minting Floor — Shows the generated trading card immediately
                with gr.Column(scale=6):
                    gr.Markdown("### Minted Operator Share Card")
                    card = gr.HTML() # The HTML card component takes visual priority layout position
                    
                    gr.Markdown("*Right-click → Save image to capture architectural footprint.*", elem_id="moses-foot")
                    
                    prof_bar = gr.HTML() # Raw composition tracks directly underneath card
                    prof = gr.Markdown(elem_id="moses-profile")

            # Connect state changes and click triggers
            go.click(run_ingest, [blob, nm], [prof, prof_bar, card, hits, ob])

            # Inline Examples block underneath the workspace
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