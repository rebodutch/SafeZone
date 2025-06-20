# app/services/data_validator.py
from pipeline.query_service import query_population, query_cases

def handle_query_request(params):
    query_result = query_cases(**params)
    return query_result