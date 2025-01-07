import dash
import dash_bootstrap_components as dbc
from layout.dashboard_layout import get_dashboard_layout
from callbacks.register import register_callbacks

def create_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
    app.layout = get_dashboard_layout()
    register_callbacks(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run_server(host="0.0.0.0", debug=True)
