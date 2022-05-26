import sys
from pathlib import Path

import click
import IPython  # type: ignore[import]

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
def main(data_directory: str, interactive: bool) -> None:
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

    click.echo("Parsing messages...")
    messages = list(parse_messages(message_dir))

    click.echo("Parsing activity...")
    activity = list(parse_activity(activity_dir))

    if interactive:
        click.echo(
            f"Use the {click.style('messages', 'green')} and {click.style('activity', 'green')} variables to interact with the parsed data"
        )
        IPython.embed()
    else:
        click.echo(f"Message count: {len(messages)}")
        click.echo(f"Activity count: {len(activity)}")


if __name__ == "__main__":
    main()
