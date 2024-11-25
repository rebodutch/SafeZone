# app/schemas/case.py
import json
from datetime import datetime
from common.custom_exceptions.exceptions import InvalidTaiwanCityException
from common.custom_exceptions.exceptions import InvalidTaiwanRegionException
from common.custom_exceptions.exceptions import InvalidCasesNumberException
from common.custom_exceptions.exceptions import InvalidDateFormatException
from common.custom_exceptions.exceptions import MissingDataException
from common.custom_exceptions.exceptions import ExtraFieldException


class CovidCase:
    def __init__(self, date=None, city=None, region=None, cases=None, **kwargs):
        self.check_extra_fields(kwargs)
        self.check_missing_fields(date, city, region, cases)
        CovidCase.validate_data(date, city, region, cases)
        
        self.date = date
        self.city = city
        self.region = region
        self.cases = cases
        

    def check_extra_fields(self, kwargs):
        if kwargs:
            raise ExtraFieldException

    def check_missing_fields(self, date, city, region, cases):
        if date is None or cases is None or city is None or region is None:
            raise MissingDataException

    @staticmethod
    def validate_data(date, city, region, cases):
        """
        Validate the data to ensure it is in the correct format.

        This method validates the date, city, region, and cases fields of the CovidCase instance.
        """
        # Check the values in every field in the data
        CovidCase.validate_date(date)

        CovidCase.validate_geo(city, region)

        CovidCase.validate_cases(cases)
    
    
    @staticmethod
    def validate_date(date):
        if not isinstance(date, str):
            raise InvalidDateFormatException
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise InvalidDateFormatException

    @staticmethod
    def validate_geo(city, region):
        if not isinstance(city, str):
            raise InvalidTaiwanCityException
        if not isinstance(region, str):
            raise InvalidTaiwanRegionException

        # Load geo data once
        with open("/app/common/geo_data/taiwan_geo_data.json", encoding="utf-8") as f:
            geo_data = json.load(f)

        if city not in geo_data:
            raise InvalidTaiwanCityException
        if region not in geo_data[city]:
            raise InvalidTaiwanRegionException

    @staticmethod
    def validate_cases(cases):
        if not isinstance(cases, int):
            raise InvalidCasesNumberException
        if cases <= 0:
            raise InvalidCasesNumberException

    def to_json(self):
        # Convert the object to JSON format for sending
        return json.dumps(
            {
                "date": self.date,
                "city": self.city,
                "region": self.region,
                "cases": self.cases,
            }
        )
