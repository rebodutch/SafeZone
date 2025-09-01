from callbacks.button_callbacks import interval_button_callbacks, ratio_button_callbacks
from callbacks.risk_map_callbacks import risk_map_callbacks, risk_title_callbacks
from callbacks.card_callbacks import card_callbacks
from callbacks.timer_callbacks import timer_callbacks

def register_callbacks(app):
    timer_callbacks(app)
    card_callbacks(app)
    interval_button_callbacks(app)
    ratio_button_callbacks(app)
    risk_map_callbacks(app)
    risk_title_callbacks(app)
