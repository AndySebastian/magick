This is a magick system for manifesting intent into the world.

**Log file:** `~/.magick/logofcasts` (append-only; one line per cast with UTC timestamp)

**Command:**

- `magick cast <string>`

**Technical (for contributors / agents):**

- Python package layout: `pyproject.toml` at repo root; package name `magick` in [`magick/`](magick/) (`cli.py` = Typer app and commands, `cast.py` = message + logging).
- Console entry point: `magick` → `magick.cli:main` (see `[project.scripts]` in `pyproject.toml`).
- Dependency: Typer (`typer>=0.12`). Requires Python **3.9+**.
- Local dev: `python3 -m venv .venv && source .venv/bin/activate && pip install -e .`
- Multi-word intents: all tokens after `cast` are joined (quotes optional).
- The CLI name `magick` may collide with [ImageMagick](https://imagemagick.org/)’s `magick` on some systems; use `which magick` if behavior looks wrong.
