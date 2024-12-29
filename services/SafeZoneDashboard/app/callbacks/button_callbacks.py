from components.basic_ui import interval_button, ratio_button
from dash import Input, Output, State


def interval_button_callbacks(app):
    @app.callback(
        [
            Output("btn-3-days", "active"),
            Output("btn-7-days", "active"),
            Output("btn-14-days", "active"),
            Output("btn-30-days", "active"),
            Output("interval-button-state", "data"),
        ],
        [
            Input("btn-3-days", "n_clicks_timestamp"),
            Input("btn-7-days", "n_clicks_timestamp"),
            Input("btn-14-days", "n_clicks_timestamp"),
            Input("btn-30-days", "n_clicks_timestamp"),
        ],
        [State("ratio-button-state", "data")],
    )
    def update_active_button(ts1, ts2, ts3, ts4, data):
        timestamps = {
            "btn-3-days": ts1,
            "btn-7-days": ts2,
            "btn-14-days": ts3,
            "btn-30-days": ts4,
        }

        # find the newest clicked button
        active_button = max(timestamps, key=lambda x: timestamps[x] or 0)
        # update the risk map based on the active button
        print(active_button, data["active"])
        # update_risk_map(active_button)

        # return the active state of each button
        return [
            active_button == "btn-3-days",
            active_button == "btn-7-days",
            active_button == "btn-14-days",
            active_button == "btn-30-days",
            {"active": active_button},
        ]


def ratio_button_callbacks(app):
    @app.callback(
        [
            Output("btn-cases", "active"),
            Output("btn-ratio", "active"),
            Output("ratio-button-state", "data"),
        ],
        [
            Input("btn-cases", "n_clicks_timestamp"),
            Input("btn-ratio", "n_clicks_timestamp"),
        ],
        [State("interval-button-state", "data")],
    )
    def update_active_button(ts1, ts2, data):
        timestamps = {
            "btn-cases": ts1,
            "btn-ratio": ts2,
        }

        # find the newest clicked button
        active_button = max(timestamps, key=lambda x: timestamps[x] or 0)
        # update the risk map based on the active button
        print(active_button, data["active"])
        # update_risk_map(active_button)

        # return the active state of each button
        return [
            active_button == "btn-cases",
            active_button == "btn-ratio",
            {"active": active_button},
        ]
