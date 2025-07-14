# app/services/data_validator.py
from pipeline.query_service import query_cases


def handle_query_request(request, params):
    # Extract the database session and caches from the request app state
    db_session = request.app.state.Session
    geo_cache = request.app.state.city_region_cache
    populations_cache = request.app.state.populations_cache
    
    # query the cases based on the parameters from db
    query_result = query_cases(db_session, geo_cache, populations_cache, params=params)
    
    return query_result
