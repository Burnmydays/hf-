# PERSISTENCE SPEC — make board rows SAVE (Supabase)

Goal: pasted operators PERSIST on the board across reloads/sessions.
Honors standing rule: NEW TABLE ONLY in AppFeeder. Nothing existing altered.

Project: AppFeeder  (betcyfbzsgusaghriptz)  ·  org MO§ES (iwiixslkceolawfcbbhg)

DECISION YOU MUST MAKE FIRST (affects RLS):
  A) Curated  — only YOU seed/write. Public demo READS only. (recommended for hackathon)
  B) Public   — anyone who pastes lands permanently. Needs anti-spam later.
This spec writes RLS for (A). For (B), see the note at bottom.

------------------------------------------------------------------
## STEP 1 — create the table (run in Supabase SQL editor)
------------------------------------------------------------------
```sql
create table if not exists public.sigrank_operators (
  id            bigint generated always as identity primary key,
  name          text not null unique,
  input         bigint not null default 0,
  output        bigint not null default 0,
  cache_create  bigint not null default 0,
  cache_read    bigint not null default 0,
  cost_usd      double precision,            -- null = no real cost (estimate in UI)
  source        text not null default 'manual',  -- ccusage | codex | manual | seed
  estimated     boolean not null default false,  -- true for codex 2:1-anchor rows
  caveat        text,                            -- directional flag for estimated
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

alter table public.sigrank_operators enable row level security;

-- (A) curated: anyone can READ, nobody writes via anon key
create policy "public_read_sigrank"
  on public.sigrank_operators for select
  to anon, authenticated
  using (true);
-- (no insert/update policy for anon => writes blocked unless service role)
```

------------------------------------------------------------------
## STEP 2 — seed the verified corpus (run once, SQL editor)
------------------------------------------------------------------
```sql
insert into public.sigrank_operators
  (name, input, output, cache_create, cache_read, cost_usd, source, estimated)
values
  ('MO§ES (ccusage)', 1251211, 11296121, 128196310, 2555179769, NULL, 'seed', false),
  ('vincentkoc',      6600000000, 342700000, 223700000, 195000000000, NULL, 'seed', false),
  ('MapleEve',        34800000000, 2800000000, 550100000, 794600000000, NULL, 'seed', false),
  ('kzquandary',      118400000000, 5900000000, 0, 1066000000000, NULL, 'seed', false),
  ('iamtheavoc1',     989500000000, 1272000000000, 0, 4524000000000, NULL, 'seed', false),
  ('Nepomuk5665',     4037000000000, 1259000000000, 96300000000, 1658000000000, NULL, 'seed', false),
  ('cexll',           67700000000, 64000000000, 217800000, 36900000000, NULL, 'seed', false)
on conflict (name) do nothing;
```
NOTE: MO§ES cost_usd left NULL here so the engine recomputes $0.527 from list
price; if you want the REAL ccusage cost frozen, set it explicitly instead.

------------------------------------------------------------------
## STEP 3 — get your keys (Supabase dashboard → Project Settings → API)
------------------------------------------------------------------
- Project URL:        https://betcyfbzsgusaghriptz.supabase.co
- anon public key:    (for READ in the app)
- service_role key:   (for WRITES — server-side ONLY, never in client/Space env that's public)

For the HF Space, set as SECRETS (Space settings → Variables and secrets):
  SUPABASE_URL          = https://betcyfbzsgusaghriptz.supabase.co
  SUPABASE_ANON_KEY     = <anon key>
  SUPABASE_SERVICE_KEY  = <service_role key>   # only if you allow writes from app

------------------------------------------------------------------
## STEP 4 — code changes (I will write these as a separate diff .md on your go)
------------------------------------------------------------------
New file  db.py:
  - load_operators()  -> reads sigrank_operators via REST (anon key), returns
    same shape as SEED dict. Falls back to hardcoded SEED if env/keys missing
    (so the app NEVER breaks if Supabase is down — this is the safety net).
  - save_operator(name, i,o,cw,cr, cost, source, estimated, caveat)
    -> upsert via service key. Only called if SUPABASE_SERVICE_KEY present.

metrics.py:
  - keep SEED as the FALLBACK constant (do not delete — it's the safety net).

app.py:
  - board reads from db.load_operators() instead of SEED directly.
  - run_ingest(): after compute, if save enabled, call db.save_operator(...)
    then re-read the board so the new row is persisted AND shown.
  - decision A: gate save behind service key (so public demo is read-only,
    your own seeding/admin writes work).

requirements.txt:
  - add:  requests   (REST calls; no heavy supabase sdk needed)

------------------------------------------------------------------
## SAFETY NET (non-negotiable)
------------------------------------------------------------------
If SUPABASE_URL / keys are absent OR the fetch fails, the app falls back to the
hardcoded SEED dict and still boots. Persistence is an ENHANCEMENT layered on
top of a thing that already works — it can never take the demo down.

------------------------------------------------------------------
## IF YOU CHOSE (B) PUBLIC WRITE instead
------------------------------------------------------------------
Add this policy (anyone can insert), and accept the spam/gaming risk for now:
```sql
create policy "public_insert_sigrank"
  on public.sigrank_operators for insert
  to anon
  with check (true);
```
Harden later with: name length limits, a per-row honeypot/captcha, or move
writes server-side behind the service key + your own validation. NOT advised
to ship public-write three hours from a deadline.
