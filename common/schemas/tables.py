from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Date, Integer, String

metadata = MetaData()

covid_cases = Table(
    "covid_cases",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", Date, nullable=False),
    Column("city", String, nullable=False),
    Column("region", String, nullable=False),
    Column("cases", Integer, nullable=False),
)