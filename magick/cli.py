import typer

from magick.cast import perform_cast

app = typer.Typer(help="Ritual CLI for intentional action.")


@app.callback()
def root() -> None:
    """Ritual CLI for intentional action."""


@app.command()
def cast(
    intent: list[str] = typer.Argument(
        ...,
        help="Immediate volitional action to perform right now",
    ),
) -> None:
    """Cast an intent to do something immediately."""
    perform_cast(" ".join(intent))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
