import dash
import dash_bootstrap_components as dbc
from flask import jsonify

from layout.dashboard_layout import get_dashboard_layout
from callbacks.register import register_callbacks
from config.settings import SERVER_IP, SERVER_PORT, SERVICE_NAME, SERVICE_VERSION
from config.logger import get_logger

def create_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
    app.layout = get_dashboard_layout()
    register_callbacks(app)

    @app.server.route("/health")
    def health_check():
        return jsonify({"status": "healthy"}), 200
    return app

if __name__ == "__main__":
    logger = get_logger()
    app = create_app()
    logger.info(f"Starting {SERVICE_NAME} version {SERVICE_VERSION}.")
    app.run_server(host=SERVER_IP, port=SERVER_PORT, debug=True)
