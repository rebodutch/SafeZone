from dash import html
import dash_bootstrap_components as dbc
from datetime import timedelta

from services.update_cases import get_national_cases
from components.trend_chart import get_trend_bar
from config.time_manager import get_now

def get_case_card():
    return dbc.Card(
    [
        dbc.CardBody(
            [
                html.H3(
                    html.B("近七日新增案例"),
                    className="card-title",
                ),
                html.H2(
                    get_national_cases(interval="7"),
                    style={"textAlign": "right"},
                    className="card-text text-white bg-success",
                ),
                html.H3(
                    html.B("今日新增案例"),
                    className="card-title",
                ),
                html.H2(
                    get_national_cases(interval="1"),
                    style={"textAlign": "right"},
                    className="card-text text-white bg-success",
                ),
            ]
        )
    ],
    className="text-white bg-primary mb-3",
)

def get_top_cities_card():
    end_date = get_now()
    start_date = end_date - timedelta(days=7)
    # format the date
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    return dbc.Card(
    dbc.CardBody(
        [
            html.H4("最快案例成長城市前十名", className="card-title text-primary"),
            html.P(
                f"統計日期為{start_date} ~ {end_date}",
                className="card-subtitle text-primary",
            ),
            get_trend_bar(),
        ]
    ),
    className="mb-3",
)
