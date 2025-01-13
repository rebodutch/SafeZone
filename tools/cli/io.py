# /tools/cli/io.py
"""
integration orschestrator(IO) is an cli tool for SafeZone project.
it is a command line interface tool that helps to manage the SafeZone project, 
and provides a way to interact with the SafeZone project for testing and development. 
"""
import json
import typer
import requests

from bin import db_helper

app = typer.Typer()

simulate_url = "http://192.168.2.250:8000/simulate"
analytics_api_url = "http://192.168.2.250:8010"
db_url = "http://192.168.2.250:6000"


@app.command()
def simulate(start_date: str, end_date: str = None):
    """
    simulate the covid data for specific date by calling the simulate api.
    """
    if end_date is None:
        end_date = start_date
    params = f"?start_date={start_date}&end_date={end_date}"
    requests.get(simulate_url + params)

    print(f"Simulated covid data from {start_date} to {end_date}")


@app.command()
def verify(data: str):
    """
    verify the covid data in the database by api.
    """
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        print("verify fail: invalid expected data format")
        return
    
    response = requests.get(analytics_api_url)

    print(f"Does the result of verify {data == response.json()['data']}")


@app.command()
def clear_db():
    """
    clear the covid data in the database.
    """
    db_helper.clear_db(db_url)

    print("Cleared the all data in the database")


@app.command()
def init_db():
    """
    initialize the covid data in the database.
    """
    db_helper.init_db(db_url)

    print(
        "Initialized the database with the taiwan administrative data and population data"
    )
