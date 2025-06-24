import logging

import dash # type: ignore
from dash import Output, Input, State# type: ignore

from services.time_manager import get_now

logger = logging.getLogger(__name__)

# Timer callbacks to update the system date in the store
def timer_callbacks(app):
    @app.callback(
        Output("system-date-store", "data"),
        Input("global-timer", "n_intervals"),
        State("system-date-store", "data"),
        prevent_initial_call=False,
    )
    def update_system_date(n_intervals, date_data):
        # if get now return the same date, do not update
        logger.debug(f"Global timer triggered: {n_intervals} intervals.")
        system_date = get_now()
        if date_data["system_date"] == system_date:
            return dash.no_update
        # update the system date store
        logger.debug(f"System date updated to {system_date}.")
        return {"system_date": system_date}