import logging
import dash_bootstrap_components as dbc # type: ignore

from components.basic_ui import get_header_with_navbar, get_risk_map_section, get_cards, get_timer

logger = logging.getLogger(__name__)
def get_dashboard_layout():
    logger.debug("Creating dashboard layout.")
    return dbc.Container(
        [
            # timer
            get_timer(),
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
