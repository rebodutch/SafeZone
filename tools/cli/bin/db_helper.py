import json
import csv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from utils.db.schema import cities, regions, covid_cases, populations, metadata

def reset_db_id(db_url):
    """
    Reset the id of the database.

    """
    # init the session
    engine = create_engine(db_url)
    # Create all tables
    metadata.create_all(engine)

    with Session(engine) as session:
        # Reset the id of the tables
        session.execute(text("ALTER SEQUENCE cities_id_seq RESTART WITH 1"))
        session.execute(text("ALTER SEQUENCE regions_id_seq RESTART WITH 1"))
        session.execute(text("ALTER SEQUENCE covid_cases_id_seq RESTART WITH 1"))
        session.execute(text("ALTER SEQUENCE populations_id_seq RESTART WITH 1"))
        session.commit()


def clear_db(db_url):
    """
    Clear the database.

    """
    # init the session
    engine = create_engine(db_url)
    # Create all tables
    metadata.create_all(engine)

    with Session(engine) as session:
        # Delete all data in the tables
        # the delete squences are important, because of the foreign key constraints
        session.execute(populations.delete())
        session.execute(covid_cases.delete())
        session.execute(regions.delete())
        session.execute(cities.delete())
        session.commit()


def init_db(db_url):
    """
    Initialize the database with the taiwan administrative data and population data.

    """
    # init the session
    engine = create_engine(db_url)
    # Create all tables
    metadata.create_all(engine)

    # Load administrative data of Taiwan
    init_administrative_data(engine)

    # Load population data of Taiwan
    init_population_data(engine)


def init_administrative_data(engine):
    # Load administrative data of Taiwan
    admin_file_path = "/app/utils/geo_data/administrative/taiwan_admin.json"
    with open(admin_file_path, encoding="utf-8") as f:
        admin_data = json.load(f)

    # Use Session to interact with the database in SQLAlchemy 2.0 style
    with Session(engine) as session:
        for city in admin_data:
            # Insert city and get its ID
            insert_stmt = cities.insert().values(name=city)
            result = session.execute(insert_stmt)
            cities_id = result.inserted_primary_key[0]

            # Check if the city is created successfully
            city_query = select(cities).where(cities.c.id == cities_id)
            city_result = session.execute(city_query).fetchone()
            if city_result:
                print(f"city '{city}', is created, id {city_result}")
            else:
                print(f"city '{city}', is not created")

            # Insert regions for the city
            for value in admin_data[city]:
                print(f"city = {city}, region = {value}")
                session.execute(regions.insert().values(name=value, city_id=cities_id))

        # Commit the transaction
        session.commit()


def init_population_data(engine):
    # Load population data of Taiwan
    population_file_path = "/app/utils/geo_data/population/region_population.csv"
    with open(population_file_path, encoding="utf-8") as f:
        population_data = csv.DictReader(f)
        # Skip the header
        next(population_data, None)

        for row in population_data:
            # Get city, region, and population by header name in the CSV file
            city = row["COUNTY"]
            region = row["TOWN"]
            population = row["P_CNT"]

            with Session(engine) as session:
                # Get city_id and region_id
                city_id = session.execute(
                    select(cities.c.id).where(cities.c.name == city)
                ).fetchone()[0]
                region_id = session.execute(
                    select(regions.c.id).where(
                        regions.c.city_id == city_id, regions.c.name == region
                    )
                ).fetchone()[0]
                # Insert population data
                session.execute(
                    populations.insert().values(
                        city_id=city_id, region_id=region_id, population=population
                    )
                )
                print(f"city = {city}, region = {region}, population = {population}")
                session.commit()
