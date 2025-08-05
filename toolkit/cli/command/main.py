#!/usr/bin/env python3
import sys
import uuid
import logging

import typer  # type: ignore
import rich  # type: ignore

from bin.client import DataflowClient, DBClient, HealthClient, TimeClient

app = typer.Typer(
    help="SafeZone CLI tool to control Dataflow, DB, and System operations.",
    pretty_exceptions_enable=False,
)
logger = logging.getLogger(__name__)
trace_id = str(uuid.uuid4())


# ---- Callback Functions ----
@app.callback()
def main(
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug mode for more verbose output.",
    ),
    logfile: str = typer.Option(
        None,
        "--logfile",
        "-l",
        help="Specify a log file to write logs to.",
    ),
):
    handlers = []
    if debug or logfile is not None:
        # Set up logging handlers
        handlers.append(logging.StreamHandler(sys.stderr))
        if logfile:
            file_handler = logging.handlers.RotatingFileHandler(
                logfile,
                mode="a+",
                maxBytes=1 * 1024 * 1024,
                backupCount=3,
                encoding="utf-8",
            )
            handlers.append(file_handler)

        if not logging.getLogger().hasHandlers():
            logging.basicConfig(
                level=logging.DEBUG,
                handlers=handlers,
            )

        class TraceIdFilter(logging.Filter):
            def filter(self, record):
                record.trace_id = trace_id
                return True

        logging.getLogger().addFilter(TraceIdFilter())

        class SafeTraceFormatter(logging.Formatter):
            def format(self, record):
                if not hasattr(record, "trace_id"):
                    record.trace_id = trace_id
                return super().format(record)

        # Use SafeTraceFormatter to include trace_id in log messages
        formatter = SafeTraceFormatter(
            "[%(trace_id)s] %(asctime)s %(levelname)s %(name)s %(message)s"
        )
        for handler in handlers:
            handler.setFormatter(formatter)

        rich.print("[bold yellow]Debug mode enabled.[/bold yellow]")


# ---- Database Commands ----
db_app = typer.Typer(help="Database control commands (init, clear, reset_id).")


@db_app.command()
def init(
    force: bool = typer.Option(
        False, "--force", help="Force re-initialize the database."
    )
):
    """Initialize the covid data in the database."""
    try:

        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )
        resp = DBClient(trace_id).init(force=force)
        rich.print(resp)
    except Exception as e:
        rich.print(f"[DB Init fail] {e}")
        raise typer.Exit(1)


@db_app.command()
def clear():
    """Clear the covid data in the database."""
    if not typer.confirm("Are you sure you want to clear the database?"):
        rich.print("Aborted.")
        raise typer.Abort()
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )
        resp = DBClient(trace_id).clear()
        rich.print(resp)
    except Exception as e:
        rich.print(f"[DB Clear fail] {e}")
        raise typer.Exit(1)


@db_app.command()
def reset():
    """Reset the database to its initial state."""
    if not typer.confirm("Are you sure you want to reset the database?"):
        rich.print("Aborted.")
        raise typer.Abort()
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )
        resp = DBClient(trace_id).reset()
        rich.print("clear all data in db including administrative data and covid data")
        rich.print("re-initialize the database with administrative data")
        rich.print(resp)
    except Exception as e:
        rich.print(f"[DB Reset fail] {e}")
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
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )
        rich.print(TimeClient(trace_id).now())
    except Exception as e:
        rich.print(f"[Time now fail] {e}")
        raise typer.Exit(1)


@time_app.command("set")
def set(
    reset: bool = typer.Option(
        False, "--reset", help="Reset the system time to real time."
    ),
    mock_date: str = typer.Option(None, "--mockdate", help="Mock date (YYYY-MM-DD)"),
    acceleration: int = typer.Option(
        None, "--acceleration", help="Time acceleration rate"
    ),
):
    """Set the system mock_date or acceleration."""
    mock = False if reset else True

    # Check if both mock_date and acceleration are None
    if mock and not mock_date and not acceleration:
        rich.print(
            "[bold red]Error:[/bold red] You must specify either --mockdate or --acceleration."
        )
        raise typer.Exit(1)

    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )
        rich.print(
            TimeClient(trace_id).set(
                mock=mock, mock_date=mock_date, acceleration=acceleration
            )
        )
    except Exception as e:
        rich.print(f"[Time set fail] {e}")
        raise typer.Exit(1)


@time_app.command("status")
def status():
    """Get current time management status."""
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(TimeClient(trace_id).get_status())
    except Exception as e:
        rich.print(f"[Time status fail] {e}")
        raise typer.Exit(1)


system_app.add_typer(time_app, name="time")

# -- Time Commands --
health_app = typer.Typer(help="Health check commands.")


@health_app.command("all")
def all():
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(HealthClient(trace_id).check(all=True))
    except Exception as e:
        rich.print(f"[Health check fail] {e}")
        raise typer.Exit(1)


@health_app.command("cli-relay")
def cli_relay():
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(HealthClient(trace_id).check(target="cli-relay"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}")
        raise typer.Exit(1)


@health_app.command("db")
def db():
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(HealthClient(trace_id).check(target="db"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}")
        raise typer.Exit(1)


@health_app.command("redis")
def redis():
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(HealthClient(trace_id).check(target="redis"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}")
        raise typer.Exit(1)


@health_app.command("data-simulator")
def data_simulator():
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(HealthClient(trace_id).check(target="data-simulator"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}")
        raise typer.Exit(1)


@health_app.command("data-ingestor")
def data_ingestor():
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(HealthClient(trace_id).check(target="data-ingestor"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}")
        raise typer.Exit(1)


@health_app.command("analytics-api")
def analytics_api():
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(HealthClient(trace_id).check(target="analytics-api"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}")
        raise typer.Exit(1)


@health_app.command("dashboard")
def dashboard():
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(HealthClient(trace_id).check(target="dashboard"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}")
        raise typer.Exit(1)


@health_app.command("mkdoc")
def mkdoc():
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(HealthClient(trace_id).check(target="mkdoc"))
    except Exception as e:
        rich.print(f"[Health check fail] {e}")
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
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(
            DataflowClient(trace_id).simulate(
                date=date, end_date=enddate, dry_run=dry_run
            )
        )
    except Exception as e:
        rich.print(f"[Simulate fail] {e}")
        raise typer.Exit(1)


@dataflow_app.command()
def verify(
    date: str = typer.Argument(..., help="Date to verify (YYYY-MM-DD)"),
    interval: int = typer.Option(
        1, "--interval", help="Interval in days for verification"
    ),
    city: str = typer.Option(None, "--city", help="City"),
    region: str = typer.Option(None, "--region", help="Region"),
    ratio: bool = typer.Option(False, "--ratio", help="Show as ratio (per 10,000)"),
):
    """Verify covid data in the database."""
    try:
        rich.print(
            f"the task's trace_id is: {trace_id}，you can use it to trace the task in the log."
        )

        rich.print(
            DataflowClient(trace_id).verify(
                date=date, interval=interval, city=city, region=region, ratio=ratio
            )
        )
    except Exception as e:
        rich.print(f"[Verify fail] {e}")
        raise typer.Exit(1)


app.add_typer(dataflow_app, name="dataflow")

if __name__ == "__main__":
    app()
