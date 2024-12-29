import dash
import dash_bootstrap_components as dbc
from layout.dashboard_layout import dashboard_layout
from callbacks.register import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dashboard_layout

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
