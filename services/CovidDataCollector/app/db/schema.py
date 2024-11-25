from sqlalchemy import MetaData
from sqlalchemy import Date
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

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