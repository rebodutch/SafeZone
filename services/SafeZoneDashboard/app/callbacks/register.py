from callbacks.button_callbacks import interval_button_callbacks, ratio_button_callbacks
from callbacks.risk_map_callbacks import risk_map_callbacks

def register_callbacks(app):
    interval_button_callbacks(app)
    ratio_button_callbacks(app)
    risk_map_callbacks(app)
