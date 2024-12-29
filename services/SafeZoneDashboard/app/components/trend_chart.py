from dash import dcc, html

def create_trend_chart():
    return html.Div(
        children=[
            html.H3("病例趨勢圖", style={"textAlign": "center"}),
            dcc.Graph(
                id="trend-chart",
                style={"height": "400px"}
            )
        ],
        style={"margin": "20px"}
    )
