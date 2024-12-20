class InvalidTaiwanCityException(Exception):
    def __init__(self, city):
        message=f"The city '{city}' is not a valid Taiwan city."
        super().__init__(message)


class InvalidTaiwanRegionException(Exception):
    def __init__(self, city, region):
        message=f"The region '{region}' does not belong to the city '{city}'."
        super().__init__(message)
