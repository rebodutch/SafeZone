import json
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import dcc, html
from datetime import timedelta

from services.update_cases import get_city_data
from config.time_manager import get_now


# risk map canvas
def get_risk_map():
    # get time settings
    end_date = get_now()
    start_date = end_date - timedelta(days=3)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    init_fig = get_tw_risk_map()
    # map banner
    banner = html.H4(
        f"{start_date} ~ {end_date} 疫情風險圖 - 依病例數",
        id="risk-map-title",
        className="text-white bg-primary p-2",
    )
    # store the map current layer and location
    risk_map_state = dcc.Store(
        id="risk-map-state",
        data={"layer": "city", "interval": "3", "ratio": False, "loc": "台灣"},
    )
    # stroe the filters state of map in cache
    map_cache_state = dcc.Store(
        id="store-map-state",
        data={"interval": "3", "ratio": False},
    )
    # the map cache
    map_cache = dcc.Store(
        id="risk-map-store",
        data=init_fig,
    )
    risk_map = dcc.Graph(
        id="risk-map",
        figure=init_fig,
    )

    return dbc.Row(
        [
            banner,
            risk_map_state,
            risk_map,
            map_cache_state,
            map_cache,
        ]
    )


# risk map of whole taiwan
def get_tw_risk_map(risk_level=None):
    # risk map of whole taiwan with city level risk initialized
    with open(f"app/utils/geo_data/boundaries/geo_city.json", "r") as f:
        geojson_data = json.load(f)
    # if risk_level is None, get city data by default filter settings
    if risk_level is None:
        risk_level = get_city_data("3", ratio=False)

    return go.Figure(
        go.Choroplethmapbox(
            geojson=geojson_data,
            locations=list(risk_level.keys()),
            featureidkey="properties.COUNTYNAME",
            z=list(risk_level.values()),
            colorscale="Reds",
            marker_opacity=0.9,
            marker_line_width=1,
            showscale=False,
        ),
        layout={
            "mapbox": {
                "style": "carto-positron",
                "zoom": 6.3,
                "center": {"lat": 23.5525, "lon": 120.5855},
            },
            "margin": {"r": 0, "t": 0, "l": 0, "b": 0},
        },
    )


# risk map of specific city
def get_city_risk_map(geojson_data, region_risk, center, annotation_text=None):
    figure = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson_data,
            locations=list(region_risk.keys()),
            featureidkey="properties.TOWNNAME",
            z=list(region_risk.values()),
            colorscale="Reds",
            marker_opacity=0.9,
            marker_line_width=1,
            showscale=False,
        ),
        layout={
            "mapbox": {
                "style": "carto-positron",
                "zoom": 8,
                "center": center,
            },
            "margin": {"r": 0, "t": 0, "l": 0, "b": 0},
        },
    )
    if annotation_text:
        figure.update_layout(
            annotations=[
                dict(
                    text=annotation_text,
                    x=0.03,
                    y=0.95,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=20, color="red"),
                    align="center",
                    bgcolor="rgba(255, 255, 255, 0.7)",
                    bordercolor="gray",
                    borderwidth=1,
                )
            ]
        )
    return figure
