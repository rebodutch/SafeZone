# /tools/cli/io.py
"""
integration orschestrator(IO) is an cli tool for SafeZone project.
it is a command line interface tool that helps to manage the SafeZone project, 
and provides a way to interact with the SafeZone project for testing and development. 
"""
import os
import sys
import json
import typer
import requests
from dotenv import load_dotenv

from bin import db_helper

app = typer.Typer(pretty_exceptions_enable=False)

load_dotenv()
# get the environment variables
SIMULATOR_URL = os.getenv("SIMULATOR_URL")
ANALYTICS_API_URL = os.getenv("ANALYTICS_API_URL")
DB_URL = os.getenv("DB_URL")


@app.command()
def simulate(
    date: str = typer.Argument(
        ...,
        help="The date of the simulate data.(it's start_date in interval simulation)",
    ),
    end_date: str = typer.Option(
        None, help="The end date, if simulate interval data is needed."
    ),
):
    """
    simulate the covid data for specific date by calling the simulate api.
    """
    try:
        if end_date is None:
            params = f"?date={date}"
            requests.get(SIMULATOR_URL + "/simulate/daily" + params)
            print(f"Simulated covid data for {date}")
        else:
            params = f"?start_date={date}&end_date={end_date}"
            requests.get(SIMULATOR_URL + "/simulate/interval" + params)
            print(f"Simulated covid data from {date} to {end_date}")
    except Exception as e:
        print(f"Simulate fail: {e}")
        raise e
        sys.exit(1)


@app.command()
def verify(
    date: str = typer.Argument(..., help="The date of the data."),
    interval: str = typer.Option("1", help="The interval of the data."),
    city: str = typer.Option(None, help="The city of the data."),
    region: str = typer.Option(None, help="The region of the data."),
    ratio: bool = typer.Option(False, help="The data is ratio of population or not.")
):
    """
    verify the covid data in the database by api.
    """
    try:
        # call the api to get the data by the given parameters
        params = f"?now={date}&interval={interval}"
        if city and region:
            params += f"&city={city}&region={region}&ratio={ratio}"
            response = requests.get(ANALYTICS_API_URL + "/cases/region" + params)
        elif city:
            params += f"&city={city}&ratio={ratio}"
            response = requests.get(ANALYTICS_API_URL + "/cases/city" + params)
        else:
            response = requests.get(ANALYTICS_API_URL + "/cases/national" + params)
 
        print(response.json())

    except Exception as e:
        print(f"Verify fail: {e}")
        raise e
        sys.exit(1)


@app.command()
def init_db():
    """
    initialize the covid data in the database.
    """
    try:
        db_helper.init_db(DB_URL)

        print(
            "Initialized the database with the taiwan administrative data and population data"
        )
    except Exception as e:
        print(f"Init fail: {e}")
        raise e
        sys.exit(1)


@app.command()
def clear_db():
    """
    clear the covid data in the database.
    """
    confirm = typer.confirm("Are you sure you want to proceed?")
    if not confirm:
        typer.echo("Stop the process!")
        raise typer.Abort()

    try:
        db_helper.clear_db(DB_URL)
        print("Cleared the all data in the database")
    except Exception as e:
        print(f"Clear fail: {e}")
        raise e
        sys.exit(1)


@app.command()
def reset_db_id():
    """
    reset the id of the database.
    """
    confirm = typer.confirm("Are you sure you want to proceed?")
    if not confirm:
        typer.echo("Stop the process!")
        raise typer.Abort()
    try:
        db_helper.reset_db_id(DB_URL)
        print("Reset the id of the database")
    except Exception as e:
        print(f"Reset fail: {e}")
        raise e
        sys.exit(1)


if __name__ == "__main__":
    app()
