from callbacks.button_callbacks import interval_button_callbacks, ratio_button_callbacks
def register_callbacks(app):
    interval_button_callbacks(app)
    ratio_button_callbacks(app)