import typer
import rich

from bin.auth import auth_login
from bin.client import DataflowClient, DBClient, HealthClient, TimeClient

app = typer.Typer(
    help="SafeZone CLI tool to control Dataflow, DB, and System operations.",
    pretty_exceptions_enable=False,
)

# ---- Database Commands ----
db_app = typer.Typer(help="Database control commands (init, clear, reset_id).")


@db_app.command()
def init():
    """Initialize the covid data in the database."""
    try:
        resp = DBClient().init()
        rich.print(resp)
    except Exception as e:
        rich.print(f"[DB Init fail] {e}", err=True)
        raise typer.Exit(1)


@db_app.command()
def clear(
    resetid: bool = typer.Option(
        False, "--resetid", help="Reset primary key auto-increment."
    )
):
    """Clear the covid data in the database."""
    if not typer.confirm("Are you sure you want to clear the database?"):
        rich.print("Aborted.")
        raise typer.Abort()
    try:
        resp = DBClient().clear()
        rich.print(resp)
        if resetid:
            rich.print(DBClient().reset())
    except Exception as e:
        rich.print(f"[DB Clear fail] {e}", err=True)
        raise typer.Exit(1)


app.add_typer(db_app, name="db")

# ---- System Commands ----
system_app = typer.Typer(help="System control commands (time control, health check).")

# -- Time Commands --
time_app = typer.Typer(help="Time control commands.")


@time_app.command("now")
def now():
    """Get the current system time."""
    try:
        rich.print(TimeClient().now())
    except Exception as e:
        rich.print(f"[Time now fail] {e}", err=True)
        raise typer.Exit(1)


@time_app.command("set")
def set(
    mock_time: str = typer.Option(None, "--mocktime", help="Mock time (YYYY-MM-DD)"),
    accelerate: int = typer.Option(None, "--accelerate", help="Time acceleration rate"),
):
    """Set the system mock time or acceleration."""
    try:
        if mock_time is None and accelerate is None:
            raise ValueError("Either --mocktime or --accelerate must be provided.")
        
        rich.print(
            TimeClient().set(mock_time=mock_time, acceleration=accelerate)
        )
    except Exception as e:
        rich.print(f"[Time set fail] {e}", err=True)
        raise typer.Exit(1)


@time_app.command("status")
def status():
    """Get current time management status."""
    try:
        rich.print(TimeClient().status())
    except Exception as e:
        rich.print(f"[Time status fail] {e}", err=True)
        raise typer.Exit(1)


system_app.add_typer(time_app, name="time")

# -- Time Commands --
health_app = typer.Typer(help="Health check commands.")


@health_app.command("all")
def all():
    try:
        rich.print(HealthClient().check(all=True))
    except Exception as e:
        rich.print(f"[Health check fail] {e}", err=True)
        raise typer.Exit(1)


@health_app.command("cli-relay")
def cli_relay():
    try:
        rich.print(HealthClient().check(target="cli-relay"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}", err=True)
        raise typer.Exit(1)


@health_app.command("db")
def db():
    try:
        rich.print(HealthClient().check(target="db"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}", err=True)
        raise typer.Exit(1)


@health_app.command("redis")
def redis():
    try:
        rich.print(HealthClient().check(target="redis"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}", err=True)
        raise typer.Exit(1)


@health_app.command("data-simulator")
def data_simulator():
    try:
        rich.print(HealthClient().check(target="data-simulator"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}", err=True)
        raise typer.Exit(1)


@health_app.command("data-ingestor")
def data_ingestor():
    try:
        rich.print(HealthClient().check(target="data-ingestor"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}", err=True)
        raise typer.Exit(1)


@health_app.command("analytics-api")
def analytics_api():
    try:
        rich.print(HealthClient().check(target="analytics-api"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}", err=True)
        raise typer.Exit(1)


@health_app.command("dashboard")
def dashboard():
    try:
        rich.print(HealthClient().check(target="dashboard"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}", err=True)
        raise typer.Exit(1)


@health_app.command("mkdoc")
def mkdoc():
    try:
        rich.print(HealthClient().check(target="mkdoc"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}", err=True)
        raise typer.Exit(1)


system_app.add_typer(health_app, name="health")

app.add_typer(system_app, name="system")

# ---- Dataflow Commands ----
dataflow_app = typer.Typer(help="Dataflow control commands (simulate, verify).")


@dataflow_app.command()
def simulate(
    date: str = typer.Argument(..., help="Start date for simulation (YYYY-MM-DD)"),
    enddate: str = typer.Option(
        None, "--enddate", help="End date for interval simulation (YYYY-MM-DD)"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Dry run mode"),
):
    """Simulate covid data for a specific date or interval."""
    try:
        rich.print(
            DataflowClient().simulate(date=date, end_date=enddate, dry_run=dry_run)
        )
    except Exception as e:
        rich.print(f"[Simulate fail] {e}", err=True)
        raise typer.Exit(1)


@dataflow_app.command()
def verify(
    date: str = typer.Argument(..., help="Date to verify (YYYY-MM-DD)"),
    city: str = typer.Option(None, "--city", help="City"),
    region: str = typer.Option(None, "--region", help="Region"),
    ratio: bool = typer.Option(False, "--ratio", help="Show as ratio (per 10,000)"),
):
    """Verify covid data in the database."""
    try:
        rich.print(
            DataflowClient().verify(date=date, city=city, region=region, ratio=ratio)
        )
    except Exception as e:
        rich.print(f"[Verify fail] {e}", err=True)
        raise typer.Exit(1)


app.add_typer(dataflow_app, name="dataflow")


# ---- Auth Command ----
@app.command()
def login(
    relay_url: str = typer.Option(None, "--relay-url", help="Relay server URL"),
    token_file: str = typer.Option(None, "--token-file", help="Token file path"),
    client_secret_file: str = typer.Option(
        None, "--client-secret-file", help="Client secret file path"
    ),
    verbose: bool = typer.Option(True, "--verbose", help="Enable verbose output"),
):
    """Login to the relay server."""
    try:
        auth_login(
            relay_url=relay_url,
            token_file=token_file,
            client_secret_file=client_secret_file,
            verbose=verbose,
        )
        rich.print("Login success!")
    except Exception as e:
        rich.print(f"[Login fail] {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
