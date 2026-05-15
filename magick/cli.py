import typer
from typer.main import get_command

from magick.cast import perform_cast, print_cast_history

# Subcommands that take a free-text tail after the command name (see _format_lines).
_COMMANDS_WITH_TEXT_TAIL = frozenset({"cast"})

app = typer.Typer(help="Ritual CLI for intentional action.")


def _format_lines() -> list[str]:
    group = get_command(app)
    if not hasattr(group, "commands"):
        return []
    lines = []
    for name in sorted(group.commands):
        suffix = " <string>" if name in _COMMANDS_WITH_TEXT_TAIL else ""
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


def main() -> None:
    app()


if __name__ == "__main__":
    main()
