import dash_bootstrap_components as dbc
from dash import html, dcc

from components.button import get_filter_buttons
from components.map_chart import get_risk_map
from components.card import get_case_card, get_top_cities_card


def get_header_with_navbar():
    # the header of the dashboard
    header = html.H3(
        "SafeZone Dashboard",
        className="text-left text-primary",
        style={
            "font-weight": "bold",
            "padding": "10px",
        },
    )
    # the navigation bar
    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                dbc.NavLink("空氣品質", href="#"), className="me-3"
                            ),
                            dbc.DropdownMenu(
                                label="傳染病",
                                children=[
                                    dbc.DropdownMenuItem("COVID-19", href="#"),
                                    dbc.DropdownMenuItem("H1N1", href="#"),
                                ],
                                nav=True,
                                className="me-3",
                            ),
                        ],
                        style={"font-weight": "bold", "font-size": "1.3rem"},
                        navbar=True,
                    ),
                    is_open=False,
                    navbar=True,
                ),
            ],
            fluid=True,
        ),
        color="dark",
        dark=True,
    )

    return dbc.Row(
        [
            header,
            navbar,
        ],
        className="mb-4",
    )


def get_cards():
    return dbc.Col(
        [
            get_case_card(),
            get_top_cities_card(),
        ],
        width=4,
    )


def get_risk_map_section():
    return dbc.Col(
        [
            # add loading spinner to avoid the map loading delay and race condition
            dcc.Loading(
                id="loading-risk-map",
                type="circle",
                children=[
                    dbc.Row(
                        [
                            get_filter_buttons(),
                        ],
                        className="mb-4",
                    ),
                    get_risk_map(),
                ],
            )
        ],
        width=8,
    )
