# /tools/cli/app.py
import sys

import typer

from commander.auth import auth_login
from commander.client import DataflowClient, DBClient

# typer app predefined
app = typer.Typer(
    help="SafeZone CLI tool to control Dataflow and DB operations.",
    pretty_exceptions_enable=False,
)

dataflow_app = typer.Typer(help="Dataflow control commands (simulate, verify).")
db_app = typer.Typer(help="Database control commands (init, clear, reset-id).")

app.add_typer(db_app, name="db")
app.add_typer(dataflow_app, name="dataflow")


@app.command()
def login(
    url: str = typer.Option(None, help="The relay server url."),
):
    """
    login to the relay server.
    """
    try:
        auth_login(url)
    except Exception as e:
        print(f"Login fail: {e}")
        sys.exit(1)


@dataflow_app.command()
def simulate(
    date: str = typer.Argument(
        ...,
        help="The date of the simulate data.(it's start_date in interval simulation)",
    ),
    end_date: str = typer.Option(
        None, help="The end date, if simulate interval data is needed."
    ),
    dry_run: bool = typer.Option(False, help="Dry run the simulation or not."),
):
    """
    simulate the covid data for specific date by calling the simulate api.
    """
    try:
        resp = DataflowClient().simulate(date=date, end_date=end_date, dry_run=dry_run)
        print(resp)
    except Exception as e:
        print(f"Simulate fail: {e}")
        sys.exit(1)


@dataflow_app.command()
def verify(
    date: str = typer.Argument(..., help="The date of the data."),
    interval: str = typer.Option("1", help="The interval of the data."),
    city: str = typer.Option(None, help="The city of the data."),
    region: str = typer.Option(None, help="The region of the data."),
    ratio: bool = typer.Option(False, help="The data is ratio of population or not."),
):
    """
    verify the covid data in the database by api.
    """
    try:
        resp = DataflowClient().verify(
            date=date, interval=interval, city=city, region=region, ratio=ratio
        )
        print(resp)
    except Exception as e:
        print(f"Verify fail: {e}")
        sys.exit(1)


@db_app.command()
def init():
    """
    initialize the covid data in the database.
    """
    try:
        resp = DBClient().init()
        print(resp)
    except Exception as e:
        print(f"Init fail: {e}")
        sys.exit(1)


@db_app.command()
def clear():
    """
    clear the covid data in the database.
    """
    confirm = typer.confirm("Are you sure you want to proceed?")
    if not confirm:
        typer.echo("Stop the process!")
        raise typer.Abort()
    try:
        resp = DBClient().clear()
        print(resp)
    except Exception as e:
        print(f"Clear fail: {e}")
        sys.exit(1)


@db_app.command()
def reset():
    """
    reset the id of the database.
    """
    confirm = typer.confirm("Are you sure you want to proceed?")
    if not confirm:
        typer.echo("Stop the process!")
        raise typer.Abort()
    try:
        resp = DBClient().reset()
        print(resp)
    except Exception as e:
        print(f"Reset fail: {e}")
        sys.exit(1)


if __name__ == "__main__":
    app()
