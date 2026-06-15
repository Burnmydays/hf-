# What to paste into "Measure yourself"

The parser accepts three input shapes. Use whichever matches your tool.

## 1. Claude Code  (recommended — gives real cost)
Run in your terminal:
```
npx ccusage@latest --json
```
Paste the ENTIRE output. The parser reads any recent ccusage shape:
- `totals` object, OR `daily` array, OR a flat list of session records
- field names in camelCase (`inputTokens`) or snake_case (`input_tokens`)
- `costUSD` / `totalCost` if present -> real blended $/1M (no estimate marker)

Fields consumed:
```
inputTokens / input_tokens
outputTokens / output_tokens
cacheCreationTokens / cache_creation_input_tokens
cacheReadTokens / cache_read_input_tokens
costUSD / totalCost            (optional -> real $/1M)
```

## 2. Codex
Run in your terminal:
```
ccusage codex --json
```
Paste the ENTIRE output. Codex reports a COMBINED input figure and never
itemizes cache writes, so the row is ESTIMATED and flagged:
- `input_tokens`      (combined: fresh + cached)
- `cached_input_tokens`   -> cache_read (measured)
- `output_tokens` + `reasoning_output_tokens` -> output
- cache_create is estimated by the 2:1 field anchor and clamped >= 0
- every Codex row carries a directional caveat (up=input-heavy / down=output-rich)

## 3. Four numbers (no ccusage available)
Paste four integers in any delimiter, in this order:
```
input output cache_create cache_read
```
Example (the MO§ES verified row):
```
1251211 11296121 128196310 2555179769
```
Cost shows as a list-price estimate (~) since no cost data is supplied.

## Notes
- Only Claude Code ccusage output carries real cost. Codex and four-number
  inputs show ~ list-price estimates for $/1M.
- The board ranks by Y = (Cache*Output)/Input^2. Nothing you paste can change
  another operator's rank — your row is scored by the same fixed formula.
