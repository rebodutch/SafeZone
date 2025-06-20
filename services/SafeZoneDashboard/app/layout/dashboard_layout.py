import dash_bootstrap_components as dbc
from dash import dcc

from components.basic_ui import get_header_with_navbar, get_risk_map_section, get_cards

def get_dashboard_layout():
    return dbc.Container(
        [
            # header and navbar
            get_header_with_navbar(),
            # cotent
            dbc.Row(
                [
                    # # left side risk map
                    get_risk_map_section(),
                    # right side cards
                    get_cards(),
                ]
            ),
        ],
        fluid=True,
    )
