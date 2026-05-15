from datetime import datetime, timezone
from pathlib import Path

import typer

LOG_FILE = Path.home() / ".magick" / "logofcasts"


def perform_cast(intent: str) -> None:
    intent = intent.strip()
    if not intent:
        raise typer.BadParameter("Intent cannot be empty.")

    typer.echo(f'the spell is cast for "{intent}". Godspeed.')

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {intent}\n")


def print_cast_history() -> None:
    if not LOG_FILE.is_file():
        typer.echo("(No casts logged yet.)")
        return
    text = LOG_FILE.read_text(encoding="utf-8")
    if not text.strip():
        typer.echo("(Log file is empty.)")
        return
    typer.echo(text.rstrip("\n"))
