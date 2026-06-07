import typer
from typer.main import get_command

from magick.cast import perform_cast, print_cast_history
from magick.choose import perform_choose

# Subcommands that take a trailing argument after the command name (see _format_lines).
_COMMAND_TAIL_HINTS = {
    "cast": "<string>",
    "choose": "<N>",
}

app = typer.Typer(help="Ritual CLI for intentional action.")


def _format_lines() -> list[str]:
    group = get_command(app)
    if not hasattr(group, "commands"):
        return []
    lines = []
    for name in sorted(group.commands):
        hint = _COMMAND_TAIL_HINTS.get(name)
        suffix = f" {hint}" if hint else ""
        lines.append(f"magick {name}{suffix}")
    return lines


def _emit_command_formats() -> None:
    for line in _format_lines():
        typer.echo(line)


@app.callback(invoke_without_command=True)
def root(ctx: typer.Context) -> None:
    """Ritual CLI for intentional action."""
    if ctx.invoked_subcommand is None:
        _emit_command_formats()


@app.command()
def cast(
    intent: list[str] = typer.Argument(
        ...,
        help="Immediate volitional action to perform right now",
    ),
) -> None:
    """Cast an intent to do something immediately."""
    perform_cast(" ".join(intent))


@app.command()
def history() -> None:
    """Print the log of past casts."""
    print_cast_history()


@app.command()
def choose(
    n: int = typer.Argument(..., help="Number of open Todoist tasks to randomly select."),
) -> None:
    """Pick N random open Todoist tasks to break decision paralysis."""
    perform_choose(n)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
