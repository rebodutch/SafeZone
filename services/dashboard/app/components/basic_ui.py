import logging

from dash import html, dcc  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore

from components.button import get_filter_buttons
from components.map_chart import get_init_map

logger = logging.getLogger(__name__)

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

    logger.debug("Creating header and navbar for the dashboard.")

    return dbc.Row(
        [
            header,
            navbar,
        ],
        className="mb-4",
    )


def get_timer():

    logger.debug("Creating global timer and system date store.")

    return dbc.Col(
        [
            dcc.Interval(id="global-timer", interval=5 * 60 * 1000, n_intervals=0),
            dcc.Store(id="system-date-store", data={"system_date": "1970-01-01"}),  # default date 
        ]
    )


def get_cards():

    logger.debug("Creating cards for the dashboard.")

    return dbc.Col(
        [
            dbc.Card(None, className="text-white bg-primary mb-3", id="cases-card"),
            dbc.Card(None, className="mb-3", id="top-cities-card"),
        ],
        width=4,
    )


def get_risk_map_section():

    logger.debug("Creating risk map section with filter buttons and initial map.")

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
                    get_init_map(),
                ],
            )
        ],
        width=8,
    )
