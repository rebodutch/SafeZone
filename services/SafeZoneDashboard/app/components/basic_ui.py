import dash_bootstrap_components as dbc
from dash import html, dcc

header = html.H3(
    "SafeZone Dashboard",
    className="text-left text-primary",
    style={
        "font-weight": "bold",
        "padding": "10px",
    },
)

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

button_defaults = {"color": "primary", "outline": True}
interval_button = dbc.ButtonGroup(
    [
        dbc.Button("Last 3 days", id="btn-3-days", active=True, **button_defaults),
        dbc.Button("Last 7 days", id="btn-7-days", active=False, **button_defaults),
        dbc.Button("Last 14 days", id="btn-14-days", active=False, **button_defaults),
        dbc.Button("Last 30 days", id="btn-30-days", active=False, **button_defaults),
    ],
    id="interval_button",
    size="md",
)

ratio_button = dbc.ButtonGroup(
    [
        dbc.Button("病例數", id="btn-cases", active=True, **button_defaults),
        dbc.Button("比例", id="btn-ratio", active=False, **button_defaults),
    ],
    size="md",
)

# risk map canvas
risk_map_canvas = dbc.Row(
    [
        html.H4(
            "start_date ~ end_date 疫情風險圖 - 依病例數",
            className="text-white bg-primary p-2",
        ),
        html.Div(
            "台灣全區域案例風險圖：開發中...",
            className="bg-light p-5 border rounded",
            style={"height": "400px"},
        ),
    ]
)


today_new_cases_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H3(
                    html.B("近七日新增案例"),
                    className="card-title",
                ),
                html.H2(
                    "0",
                    style={"textAlign": "right"},
                    className="card-text text-white bg-success",
                ),
                html.H3(
                    html.B("今日新增案例"),
                    className="card-title",
                ),
                html.H2(
                    "0",
                    style={"textAlign": "right"},
                    className="card-text text-white bg-success",
                ),
            ]
        )
    ],
    className="text-white bg-primary mb-3",
)

# the top 10 case growth cities
top_cities_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("最快案例成長城市前十名", className="card-title"),
            html.Ul(
                [html.Li(f"城市 {i+1}: xxx 案例數") for i in range(10)],
                className="list-unstyled",
            ),
        ]
    ),
    className="mb-3",
)
