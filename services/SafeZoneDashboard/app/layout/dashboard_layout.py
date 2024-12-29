import dash_bootstrap_components as dbc
from dash import dcc
from components.basic_ui import header, navbar
from components.basic_ui import interval_button, ratio_button
from components.basic_ui import risk_map_canvas
from components.basic_ui import today_new_cases_card, top_cities_card

dashboard_layout = dbc.Container(
    [
        # header and navbar
        dbc.Row(
            [
                header,
                navbar,
            ],
            className="mb-4",
        ),
        # cotent
        dbc.Row(
            [
                # left side risk map and filters
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Store(
                                            id="interval-button-state",
                                            data={"active": "btn-3-days"},
                                        ),
                                        interval_button,
                                    ],
                                    width=8,
                                ),
                                dbc.Col(
                                    [
                                        dcc.Store(
                                            id="ratio-button-state",
                                            data={"active": "btn-cases"},
                                        ),
                                        ratio_button,
                                    ],
                                    width=4,
                                ),
                            ],
                            className="mb-4",
                        ),
                        risk_map_canvas,
                    ],
                    width=8,
                ),
                # right side cards
                dbc.Col(
                    [
                        today_new_cases_card,
                        top_cities_card,
                    ],
                    width=4,
                ),
            ]
        ),
    ],
    fluid=True,
)
