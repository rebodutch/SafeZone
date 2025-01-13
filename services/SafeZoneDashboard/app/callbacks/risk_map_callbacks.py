import json
import dash
import time
import plotly.graph_objects as go

from dash import Output, Input, State

from components.map_chart import get_city_risk_map
from services.update_cases import get_region_data, get_city_data
from config.logger import get_logger

# global variables
city_center = None
city_code = None
# get logger
logger = get_logger()


def get_city_center(city):
    global city_center
    if not city_center:
        with open("app/utils/geo_data/boundaries/accessory/city_center.json", "r") as f:
            city_center = json.load(f)
    return city_center[city]


def get_city_code(city):
    global city_code
    if not city_code:
        with open("app/utils/geo_data/boundaries/accessory/city_code.json", "r") as f:
            city_code = json.load(f)
    return city_code[city]


def risk_map_callbacks(app):
    @app.callback(
        [
            Output("risk-map", "figure"),
            Output("risk-map-state", "data"),
            Output("store-map-state", "data"),
            Output("risk-map-store", "data"),
        ],
        [
            Input("risk-map", "clickData"),
            Input("interval-button-state", "data"),
            Input("ratio-button-state", "data"),
        ],
        [
            # the map state: layer and location
            State("risk-map-state", "data"),
            # the cached map state
            State("store-map-state", "data"),
            # the cached map
            State("risk-map-store", "data"),
        ],
    )
    def update_risk_map(click_map, interval, ratio, map_state, cache_state, map_cache):
        interval = interval["active"]
        ratio = ratio["active"]
        if map_state["ratio"] != ratio or map_state["interval"] != interval:
            print("update map with filters clicked")

            return update_map_with_filters_clicked(
                interval, ratio, map_state, map_cache
            )
        elif click_map:
            return update_map_with_map_clicked(
                click_map,
                interval,
                ratio,
                map_state,
                cache_state,
                map_cache,
            )
        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update]


def update_map_with_map_clicked(
    click_map, interval, ratio, map_state, cache_state, map_cache
):
    # get meanful data
    clicked_city = click_map["points"][0]["location"]

    # return to city level
    if map_state["layer"] == "region":
        map_new_state = {
            "layer": "city",
            "interval": interval,
            "ratio": ratio,
            "loc": "台灣",
        }
        # if the map state is the same as the cache state return the cached map
        if ratio == cache_state["ratio"] and interval == cache_state["interval"]:

            logger.info(
                f"update map with map clicked (cache hit): layer=region->city, "
                f"ratio={ratio}, interval={interval}, loc=台灣"
            )

            return [
                # risk map
                map_cache,
                # map state
                map_new_state,
                # cache state
                dash.no_update,
                # map cache for city level
                dash.no_update,
            ]
        else:
            # get city risk data
            city_risk = get_city_data(interval, ratio)
            # update z values for cached map
            map_cache["data"][0]["location"] = list(city_risk.keys())
            map_cache["data"][0]["z"] = list(city_risk.values())

            logger.info(
                f"update map with map clicked (cache miss): layer=region->city, "
                f"ratio={ratio}, interval={interval}, loc=台灣"
            )

            return [
                # risk map
                map_cache,
                # map state
                map_new_state,
                # cache state: update filter state
                {
                    "interval": interval,
                    "ratio": ratio,
                },
                # map cache for city level
                map_cache,
            ]
    # switch to region level
    else:
        # get region geo data for clicked city
        with open(
            f"app/utils/geo_data/boundaries/regions/{get_city_code(clicked_city)}_region.json",
            "r",
        ) as f:
            geojson_data = json.load(f)
        # get region risk data for clicked city
        region_risk = get_region_data(clicked_city, interval, ratio)

        logger.info(
            f"update map with map clicked: layer=city->region, "
            f"ratio={ratio}, interval={interval}, loc={clicked_city}"
        )

        return [
            # risk map
            get_city_risk_map(
                geojson_data,
                region_risk,
                get_city_center(clicked_city),
                "點擊地圖任區域可返回上一層",
            ),
            # map state
            {
                "layer": "region",
                "interval": interval,
                "ratio": ratio,
                "loc": clicked_city,
            },
            # cache state
            dash.no_update,
            # map cache for city level
            dash.no_update,
        ]


def update_map_with_filters_clicked(interval, ratio, map_state, map_cache):
    # layer is city
    if map_state["layer"] == "city":
        city_risk = get_city_data(interval, ratio)
        # update z values for cached map
        map_cache["data"][0]["location"] = list(city_risk.keys())
        map_cache["data"][0]["z"] = list(city_risk.values())

        logger.info(
            f"update map with filter state changes: layer=city, "
            f"ratio={ratio}, interval={interval}, loc=台灣"
        )

        return [
            # risk map
            map_cache,
            # map state: update filter state
            {
                "layer": "city",
                "interval": interval,
                "ratio": ratio,
                "loc": "台灣",
            },
            # cache state: update filter state
            {
                "interval": interval,
                "ratio": ratio,
            },
            # map cache for city level
            map_cache,
        ]
    # layer is region
    else:
        current_city = map_state["loc"]
        # get region geo data for current city
        with open(
            f"app/utils/geo_data/boundaries/regions/{get_city_code(current_city)}_region.json",
            "r",
        ) as f:
            geojson_data = json.load(f)
        # get region risk data for current city
        region_risk = get_region_data(current_city, interval, ratio)

        logger.info(
            f"update map with filter state changes: layer=region, "
            f"ratio={ratio}, interval={interval}, loc={current_city}"
        )

        return [
            # risk map
            get_city_risk_map(
                geojson_data,
                region_risk,
                get_city_center(current_city),
                "點擊地圖任區域可返回上一層",
            ),
            # map state
            {
                "layer": "region",
                "interval": interval,
                "ratio": ratio,
                "loc": map_state["loc"],
            },
            # cache state
            dash.no_update,
            # map cache for city level
            dash.no_update,
        ]
