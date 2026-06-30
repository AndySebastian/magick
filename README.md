This is a magick system for manifesting intent into the world.

See also: [magick-pwa](https://github.com/AndySebastian/magick-pwa) — the same ritual as an installable web app for your phone.

For the concept behind magick and how the two repos relate, see [`docs/overview.md`](docs/overview.md).

**Log files:** `~/.magick/logofcasts` (casts; one line per cast with UTC timestamp) and `~/.magick/promises` (promises; one line `{created} | {due} | {commitment}`, both timestamps UTC). Both append-only.

**Commands:**

- `magick cast <string>`: this is essentially "I will do this specific action right now". It could be "do laundry" or "take a shower" or whatever. We cast the intention that it will happen, and it happens.
  - **Chaining multiple intents:** separate them with `;` (quote the whole string so your shell doesn't split it as commands):
    ```
    magick cast "do laundry; order food; meditate for 5 minutes"
    ```
    Today this is logged as a single line; splitting them into separate log entries is a planned enhancement, but the convention is forward-compatible.
- `magick history`
- `magick choose <N>`: pick `N` open Todoist tasks at random — a coin flip to break decision paralysis. If you have fewer than `N` open tasks you get all of them. Requires `TODOIST_API_TOKEN` in your environment (Todoist → Settings → Integrations → Developer).
- `magick promise <string> --at <when>`: vow to do something at a future time, e.g. `magick promise "call mom" --at 2026-07-01T15:00`. The time is local; ISO form (`YYYY-MM-DDTHH:MM`). The vow is logged to `~/.magick/promises` and, if a bell is configured (see below), relayed so the magick-pwa on your phone pushes a notification at that time.
- `magick promises`: print the log of promises made.

**Promise bell (optional, for phone push):** set `MAGICK_WORKER_URL` and `MAGICK_PROMISE_TOKEN` — either in your environment or in `~/.magick/config` (`KEY=value` lines, one per line; env wins). These point at the Cloudflare Worker (see `~/magick-worker/`) that relays promises to the phone. Without them, promises are still recorded locally; they just don't ring the phone.

Running `magick` with no arguments prints the lines above (derived from registered subcommands; trailing-argument hints come from `_COMMAND_TAIL_HINTS` in [`magick/cli.py`](magick/cli.py)).

**Technical (for contributors / agents):**

- Python package layout: `pyproject.toml` at repo root; package name `magick` in [`magick/`](magick/) (`cli.py` = Typer app and commands, `cast.py` = message + logging, `choose.py` = Todoist fetch + random sample, `promise.py` = future-dated vow: parse + log + relay to the Worker).
- Console entry point: `magick` → `magick.cli:main` (see `[project.scripts]` in `pyproject.toml`).
- Dependency: Typer (`typer>=0.12`). Requires Python **3.9+**.
- Local dev: `python3 -m venv .venv && source .venv/bin/activate && pip install -e .`
- Multi-word intents: all tokens after `cast` are joined (quotes optional).
- The CLI name `magick` may collide with [ImageMagick](https://imagemagick.org/)’s `magick` on some systems; use `which magick` if behavior looks wrong.
