import json
import logging
import hashlib
import functools

import redis.asyncio as aioredis  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from sqlalchemy import select  # type: ignore

from utils.db.orm import City, Region
from utils.db.schema import populations
from config.settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD


logger = logging.getLogger(__name__)


async def get_redis_client():
    try:
        redis_client = aioredis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True,
        )
        await redis_client.ping()  # Test the connection
        logger.info("Connected to Redis successfully.")
        return redis_client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return None


def generate_cache_key(endpoint: str, params_model):
    # sort by keys to ensure consistent hashing
    raw = json.dumps(params_model.model_dump(), sort_keys=True, default=str)
    hashed = hashlib.sha256(raw.encode()).hexdigest()
    return f"{endpoint}:{hashed}"


def redis_cache(endpoint, ttl=86400):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # check cache availability
            request = kwargs.get("request", None)
            # get the redis client from the request app state
            redis_client = request.app.state.redis_client if request else None
            if not redis_client:
                # if redis_client is None, just call the function without caching
                logger.warning("Redis client is not available, skipping cache.")
                return await func(*args, **kwargs)

            # get the parameters from the request parameters
            params = kwargs.get("params", None)
            if not params:
                # if no parameters are provided, just call the function
                return await func(*args, **kwargs)

            cache_key = generate_cache_key(endpoint, params)
            cached = await redis_client.get(cache_key)
            if cached:
                logger.debug(f"Cache hit: {cache_key}")
                return JSONResponse(content=json.loads(cached))

            # if cache miss, call the function and store the result in cache
            logger.debug(f"Cache miss: {cache_key}")
            resp = await func(*args, **kwargs)
            # resp is an instance of AnalyticsAPIResponse, it can be serialized to JSON
            # and can be return as a JSONResponse content
            await redis_client.setex(cache_key, ttl, resp.body)
            return resp

        return wrapper

    return decorator


# --- lookup caches in memory ---#
# geo_cache stores city-region mapping in the format:
# city -> (city_id, {region_name -> region_id})
def get_city_region_cache(Session) -> dict[str, tuple[int, dict[str, int]]]:
    geo_cache = {}
    with Session() as session:
        results = (
            session.query(City, Region)
            .outerjoin(Region, Region.city_id == City.id)
            .all()
        )
        for city, region in results:
            if city.name not in geo_cache:
                geo_cache[city.name] = (city.id, {})
            if region:
                geo_cache[city.name][1][region.name] = region.id
    logger.debug("City-region cache loaded successfully.")
    return geo_cache


# populations_cache stores population data in the format:
# city_id -> {region_id -> population}
def get_populations_cache(Session) -> dict[int, dict[int, int]]:
    populations_cache = {}
    with Session() as session:
        populations_cache.clear()
        select_stmt = select(
            populations.c.city_id, populations.c.region_id, populations.c.population
        )
        for city_id, region_id, population in session.execute(select_stmt):
            # print(f"city_id: {city_id}, region_id: {region_id}, population: {population}")
            if city_id not in populations_cache:
                populations_cache[city_id] = {}
            populations_cache[city_id][region_id] = population
    logger.debug("population cache loaded successfully.")
    return populations_cache
