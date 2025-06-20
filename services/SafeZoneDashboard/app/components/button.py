from dash import dcc
import dash_bootstrap_components as dbc


# the filter buttons
def get_filter_buttons():
    # the default style of all filter buttons
    button_defaults = {"color": "primary", "outline": True}

    interval_button = dbc.ButtonGroup(
        [
            dbc.Button("Last 3 days", id="btn-3-days", active=True, **button_defaults),
            dbc.Button("Last 7 days", id="btn-7-days", active=False, **button_defaults),
            dbc.Button(
                "Last 14 days", id="btn-14-days", active=False, **button_defaults
            ),
            dbc.Button(
                "Last 30 days", id="btn-30-days", active=False, **button_defaults
            ),
        ],
        id="interval_buttons",
        size="md",
    )

    ratio_button = dbc.ButtonGroup(
        [
            dbc.Button("病例數", id="btn-cases", active=True, **button_defaults),
            dbc.Button("比例", id="btn-ratio", active=False, **button_defaults),
        ],
        id="ratio_buttons",
        size="md",
    )

    interval_state_stroe = dcc.Store(
        id="interval-button-state",
        data={"active": "3"},
    )

    ratio_state_stroe = dcc.Store(
        id="ratio-button-state",
        data={"active": False},
    )
    return dbc.Row(
        [
            dbc.Col(
                [
                    interval_state_stroe,
                    interval_button,
                ],
                width=8,
            ),
            dbc.Col(
                [
                    ratio_state_stroe,
                    ratio_button,
                ],
                width=4,
            ),
        ],
        className="mb-4",
    )
