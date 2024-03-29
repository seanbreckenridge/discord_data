import sys
from pathlib import Path

import click

from .parse import parse_activity, parse_messages


@click.command()
@click.argument(
    "DATA_DIRECTORY",
    type=click.Path(exists=True),
)
@click.option(
    "--interactive/--non-interactive",
    is_flag=True,
    help="Drop into the REPL",
    default=True,
    show_default=True,
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["json", "repl", "count"]),
    default="repl",
    show_default=True,
)
def main(data_directory: str, interactive: bool, output: str) -> None:
    """
    Utility command to test parsing a data directory
    """
    dd = Path(data_directory)
    message_dir = dd / "messages"
    activity_dir = dd / "activity"
    if not message_dir.exists():
        click.echo(f"Expected message dir to exist at {message_dir}", err=True)
        sys.exit(2)
    if not activity_dir.exists():
        click.echo(f"Expected activity dir to exist at {activity_dir}", err=True)
        sys.exit(2)

    click.echo("Parsing messages...", err=True)
    messages = list(parse_messages(message_dir))

    click.echo("Parsing activity...", err=True)
    activity = list(parse_activity(activity_dir))

    if output == "repl":
        if interactive:
            click.echo(
                f"Use the {click.style('messages', 'green')} and {click.style('activity', 'green')} variables to interact with the parsed data"
            )
            try:
                import IPython  # type: ignore[import]
            except ImportError:
                import code

                click.secho(
                    "IPython not installed, falling back to standard REPL", fg="yellow"
                )

                code.interact(local=locals())
            else:
                IPython.embed()  # type: ignore[no-untyped-call]
        else:
            # backwards compatibility, keep here
            click.echo(f"Message count: {len(messages)}")
            click.echo(f"Activity count: {len(activity)}")
    elif output == "json":
        from .model import serialize

        click.echo(serialize({"messages": messages, "activity": activity}))
    elif output == "count":
        click.echo(f"Message count: {len(messages)}")
        click.echo(f"Activity count: {len(activity)}")


if __name__ == "__main__":
    main()
