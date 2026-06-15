"""
db.py — optional Supabase persistence for the SigRank board.

NON-BLOCKING SAFETY NET (non-negotiable, per PERSISTENCE_SPEC):
  If SUPABASE_URL / keys are absent OR any fetch fails, every function falls
  back to metrics.SEED and the app still boots. Persistence is an ENHANCEMENT
  layered on a thing that already works — it can never take the demo down.

Curated mode (A):
  Public Space sets SUPABASE_URL + SUPABASE_ANON_KEY (READ only, RLS-gated).
  Writes require SUPABASE_SERVICE_KEY (admin); leave it UNSET on the public
  Space so visitor pastes stay transient (save_operator becomes a no-op).

`requests` is imported lazily inside the network calls so the module imports
cleanly even where requests isn't installed (it just falls back to SEED).
"""
import os

_URL     = os.environ.get("SUPABASE_URL", "").rstrip("/")
_ANON    = os.environ.get("SUPABASE_ANON_KEY", "")
_SERVICE = os.environ.get("SUPABASE_SERVICE_KEY", "")
_TABLE   = "sigrank_operators"
_TIMEOUT = 6


def enabled():
    """True when the READ path is configured (URL + anon key present)."""
    return bool(_URL and _ANON)


def writes_enabled():
    """True when the WRITE path is configured (URL + service key present).
    Curated public demo leaves the service key unset -> writes are no-ops."""
    return bool(_URL and _SERVICE)


def load_operators():
    """Return {name: (input, output, cache_create, cache_read)} — the exact
    shape of metrics.SEED. Falls back to SEED on any missing-config / network /
    parse failure, so callers never have to handle an error path."""
    from metrics import SEED
    if not enabled():
        return dict(SEED)
    try:
        import requests
        r = requests.get(
            f"{_URL}/rest/v1/{_TABLE}",
            params={"select": "name,input,output,cache_create,cache_read",
                    "order": "id"},
            headers={"apikey": _ANON, "Authorization": f"Bearer {_ANON}"},
            timeout=_TIMEOUT,
        )
        r.raise_for_status()
        ops = {}
        for row in r.json():
            name = row.get("name")
            if not name:
                continue
            ops[name] = (
                int(row.get("input", 0) or 0),
                int(row.get("output", 0) or 0),
                int(row.get("cache_create", 0) or 0),
                int(row.get("cache_read", 0) or 0),
            )
        return ops or dict(SEED)          # empty table -> still show the seed
    except Exception as e:                 # network, auth, JSON, anything
        print(f"[db] load_operators failed, using SEED fallback: {e}")
        return dict(SEED)


def save_operator(name, i, o, cw, cr, cost=None, source="manual",
                  estimated=False, caveat=None):
    """Upsert one operator via the service key (PostgREST merge-duplicates on
    `name`). No-op returning False unless SUPABASE_SERVICE_KEY is set. Never
    raises — failures are swallowed and logged so ingestion can't crash."""
    if not writes_enabled():
        return False
    try:
        import requests
        payload = {
            "name": str(name)[:64],
            "input": int(i), "output": int(o),
            "cache_create": int(cw), "cache_read": int(cr),
            "cost_usd": cost, "source": source,
            "estimated": bool(estimated), "caveat": caveat,
        }
        r = requests.post(
            f"{_URL}/rest/v1/{_TABLE}",
            params={"on_conflict": "name"},
            headers={"apikey": _SERVICE, "Authorization": f"Bearer {_SERVICE}",
                     "Content-Type": "application/json",
                     "Prefer": "resolution=merge-duplicates,return=minimal"},
            json=payload, timeout=_TIMEOUT,
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[db] save_operator failed (non-fatal): {e}")
        return False
