# Magick — project overview

_Cross-repo context doc covering both the `magick` CLI and the `magick-pwa` companion._
_Lives in the CLI repo (`magick/docs/overview.md`); referenced from the PWA's README._

## What it is (practical utility)

Magick is a **personalized productivity tool dressed as a ritual**. It borrows the
language of magick — *casting*, *spells*, *intent* — to do one psychological job:
convert the wish to act into the act itself. You state an intention out loud (well,
in writing), the tool ceremonially confirms it, and that small act of declaration
nudges you across the gap from "I should" to "I'm doing it now."

The framing is the feature. Plenty of to-do apps let you record tasks; magick is
deliberately not a backlog. A **cast** means *"I will do this specific action right
now"* — laundry, a shower, five minutes of meditation. The mystical wrapper turns a
mundane intention into a deliberate, almost performative commitment, which is exactly
the friction-reducer that decision-paralysis and procrastination respond to. The
confirmation line — `the spell is cast for "X". Godspeed.` — is intentionally a tiny
hit of ceremony and encouragement.

One supporting trick reinforces the same theme: **`choose`** pulls a few of your open
Todoist tasks at random — a literal coin flip to break "what should I even do?"
paralysis. The point isn't optimization; it's removing the cost of deciding.

So: a mood/ritual layer over intentional action. Less "task manager," more "a small
spell you cast on yourself to start moving."

## The two repos

Same ritual, two surfaces. They are **independent** — separate repos, separate data
stores, no runtime dependency and no sync between them.

| | `magick` (CLI) | `magick-pwa` (PWA) |
|---|---|---|
| Repo | github.com/AndySebastian/magick | github.com/AndySebastian/magick-pwa |
| Surface | Terminal (Python, Typer) | Installable phone web app (vanilla HTML/CSS/JS) |
| Storage | `~/.magick/logofcasts` (append-only text log) | IndexedDB on device |
| Hosted | local install (`pip install -e .`) | GitHub Pages: andysebastian.github.io/magick-pwa |
| Python | 3.9+ | n/a (`python3 -m http.server` only for local dev) |

**CLI commands:** `cast <intent>`, `history`, `choose <N>`, `promise <commitment> --at <when>`, `promises`.
**PWA views:** *cast*, *history*, *choose*, and *promise* (disclosure panels).

Both support **chaining** intents with `;` (e.g. `do laundry; order food; meditate`),
today recorded as a single entry — splitting into separate entries is a planned
enhancement, and the `;` convention is forward-compatible.

## The shared invariant (why they line up without being coupled)

The PWA mirrors the CLI's record shape *on purpose*, so a future
"export the phone's casts into `~/.magick/logofcasts`" feature needs no translation
layer. Neither imports the other; they're parallel implementations of one shape:

- **Timestamp:** `YYYY-MM-DDTHH:MM:SSZ` — second-precision UTC, ISO 8601.
  (CLI: `datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")`.)
- **Log line / record:** CLI writes `"{timestamp} | {intent}\n"`; PWA stores
  `{ timestamp, intent }`, which maps to the same line.
- **Confirmation string:** verbatim `the spell is cast for "X". Godspeed.` in both.

Change any of these in one place and you either update the other or accept that a
later export feature needs a translator. (Notably: don't switch the PWA to raw
millisecond `new Date().toISOString()` without changing the CLI.)

## Promises — the deliberate exception

Everything above says "no sync." **Promises are the one feature that needs a relay.**
A promise is a commitment plus a future time; at that time the phone should buzz. iOS
PWAs can't wake themselves while closed, so a tiny always-on sender is unavoidable —
a third component, the **Cloudflare Worker** (`~/magick-worker/`), holds the VAPID key,
stores the phone's push subscription, and sends a Web Push at the due moment. Both the
CLI (`magick promise`) and the PWA POST `{ commitment, dueAt }` to it; the PWA also
registers its push subscription. The promise's `dueAt` keeps the same UTC
`YYYY-MM-DDTHH:MM:SSZ` shape as the cast timestamp. The CLI additionally logs every
promise to `~/.magick/promises` (`{created} | {due} | {commitment}`). When the push
arrives and you open the app, a temporary **keep** button (available for one hour after
the due time) lets you mark `promise kept.`

## If you're asked to "look at magick"

It's ambiguous — clarify whether it means the **CLI** (`~/magick/`) or the
**PWA** (`~/magick-pwa/`). They share the ritual and the record shape; they share
nothing else.

## Code map (for deeper questions)

- CLI: `magick/cli.py` (Typer app + commands), `magick/cast.py` (message + logging),
  `magick/choose.py` (Todoist fetch + random sample), `magick/promise.py` (parse a
  future time, log to `~/.magick/promises`, relay to the Worker). Entry point `magick` →
  `magick.cli:main`. `choose` needs `TODOIST_API_TOKEN`; `promise` needs
  `MAGICK_WORKER_URL` / `MAGICK_PROMISE_TOKEN` (env or `~/.magick/config`) to ring the phone.
- Worker: `~/magick-worker/` (separate repo) — Cloudflare Worker + KV + 1-min Cron
  Trigger; stores the push subscription and pending promises, sends Web Push at the due time.
- PWA: `index.html` (two views + tab bar), `app.js` (IndexedDB wrapper + view logic),
  `style.css` (dark, minimal, serif-leaning), `manifest.webmanifest`, `sw.js`
  (cache-first service worker — bump `CACHE_VERSION` when assets change).
