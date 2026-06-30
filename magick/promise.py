import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import typer

PROMISE_FILE = Path.home() / ".magick" / "promises"
CONFIG_FILE = Path.home() / ".magick" / "config"

_TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def _utc_stamp(dt: datetime) -> str:
    """Second-precision UTC, matching the shared invariant (see cast.py)."""
    return dt.astimezone(timezone.utc).strftime(_TS_FORMAT)


def _load_config() -> dict:
    """Read ~/.magick/config (simple key=value lines); env vars take precedence."""
    config: dict[str, str] = {}
    if CONFIG_FILE.is_file():
        for line in CONFIG_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            config[key.strip()] = value.strip()
    return config


def _parse_when(when: str) -> datetime:
    """Parse a local datetime string into an aware UTC datetime."""
    raw = when.strip().replace("Z", "")
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        raise typer.BadParameter(
            f'could not read the time "{when}". '
            "use ISO form, e.g. 2026-07-01T15:00."
        )
    # Naive input is taken as local time; aware input is honored as given.
    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    return parsed.astimezone(timezone.utc)


def _send_to_bell(commitment: str, due_ts: str) -> None:
    """Relay the promise to the Worker so the phone can be rung. Best-effort."""
    config = _load_config()
    url = os.environ.get("MAGICK_WORKER_URL") or config.get("MAGICK_WORKER_URL")
    token = os.environ.get("MAGICK_PROMISE_TOKEN") or config.get("MAGICK_PROMISE_TOKEN")
    if not url:
        typer.echo("(the bell is unset; this vow rests here only — see README.)")
        return

    body = json.dumps(
        {"commitment": commitment, "dueAt": due_ts, "source": "cli"}
    ).encode("utf-8")
    # Cloudflare blocks the default Python-urllib user-agent (error 1010), so set one.
    headers = {"Content-Type": "application/json", "User-Agent": "magick-cli"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        f"{url.rstrip('/')}/promise", data=body, headers=headers, method="POST"
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except (urllib.error.URLError, OSError) as e:
        reason = getattr(e, "reason", e)
        typer.echo(f"(the vow was recorded but could not reach the bell: {reason})")


def perform_promise(commitment: str, when: str) -> None:
    commitment = commitment.strip()
    if not commitment:
        raise typer.BadParameter("A promise needs a commitment.")

    due = _parse_when(when)
    now = datetime.now(timezone.utc)
    if due <= now:
        raise typer.BadParameter("A promise can only be made for a time yet to come.")

    due_ts = _utc_stamp(due)
    created_ts = _utc_stamp(now)

    local_when = due.astimezone().strftime("%Y-%m-%d %H:%M")
    typer.echo(
        f'the vow is sealed: "{commitment}" — to be kept at {local_when}. Godspeed.'
    )

    PROMISE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PROMISE_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{created_ts} | {due_ts} | {commitment}\n")

    _send_to_bell(commitment, due_ts)


def print_promise_history() -> None:
    if not PROMISE_FILE.is_file():
        typer.echo("(No promises made yet.)")
        return
    text = PROMISE_FILE.read_text(encoding="utf-8")
    if not text.strip():
        typer.echo("(No promises made yet.)")
        return
    typer.echo(text.rstrip("\n"))
